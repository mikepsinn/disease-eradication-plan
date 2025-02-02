require('dotenv').config();
const { Client: PgClient } = require('pg');
const { Client: SshClient } = require('ssh2');
const fs = require('fs');
const path = require('path');
const net = require('net');

// Validate required environment variables
const requiredEnvVars = [
  'DB_HOST',
  'DB_PORT',
  'DB_NAME',
  'DB_USER',
  'DB_PASSWORD',
  'SSH_HOST',
  'SSH_USER',
  'SSH_PRIVATE_KEY_PATH'
];

const missingEnvVars = requiredEnvVars.filter(varName => !process.env[varName]);
if (missingEnvVars.length > 0) {
  console.error('Error: Missing required environment variables:');
  missingEnvVars.forEach(varName => console.error(`- ${varName}`));
  console.error('\nPlease make sure these variables are set in your .env file');
  process.exit(1);
}

// Environment variables
const {
  DB_HOST,
  DB_PORT,
  DB_NAME,
  DB_USER,
  DB_PASSWORD,
  SSH_HOST,
  SSH_USER,
  SSH_PORT = '22',
  SSH_PRIVATE_KEY_PATH,
} = process.env;

// Validate SSH private key exists
if (!fs.existsSync(SSH_PRIVATE_KEY_PATH)) {
  console.error(`Error: SSH private key file not found at: ${SSH_PRIVATE_KEY_PATH}`);
  process.exit(1);
}

// Create backups directory if it doesn't exist
const backupDir = path.join(__dirname, '../backups');
if (!fs.existsSync(backupDir)) {
  fs.mkdirSync(backupDir);
}

const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
const backupFileName = `backup-${DB_NAME}-${timestamp}.sql`;
const backupPath = path.join(backupDir, backupFileName);

// Function to create SSH tunnel
async function createSSHTunnel() {
  const ssh = new SshClient();
  
  return new Promise((resolve, reject) => {
    ssh.on('ready', () => {
      console.log('SSH connection established successfully');
      console.log(`Will forward local port to remote database at ${DB_HOST}:${DB_PORT}`);

      const server = net.createServer((socket) => {
        ssh.forwardOut(
          socket.remoteAddress,
          socket.remotePort,
          DB_HOST,
          parseInt(DB_PORT),
          (err, stream) => {
            if (err) {
              console.error('Port forwarding error:', err);
              socket.end();
              return;
            }
            socket.pipe(stream).pipe(socket);
          }
        );
      });
      
      // Listen on a random port assigned by the OS
      server.listen(0, '127.0.0.1', () => {
        const localPort = server.address().port;
        console.log(`SSH tunnel established: 127.0.0.1:${localPort} -> ${DB_HOST}:${DB_PORT}`);
        resolve({ ssh, localPort, server });
      });
    });
    
    ssh.on('error', (err) => {
      console.error('SSH connection error:', err);
      reject(err);
    });
    
    console.log(`Connecting to SSH server ${SSH_HOST}:${SSH_PORT} as ${SSH_USER}`);
    console.log('Using private key from:', SSH_PRIVATE_KEY_PATH);
    
    try {
      const privateKey = fs.readFileSync(SSH_PRIVATE_KEY_PATH, 'utf8');
      ssh.connect({
        host: SSH_HOST,
        port: parseInt(SSH_PORT),
        username: SSH_USER,
        privateKey: privateKey,
        debug: true,
      });
    } catch (err) {
      console.error('Error reading private key:', err);
      reject(err);
    }
  });
}

async function getTableNames(client) {
  const query = `
    SELECT tablename 
    FROM pg_tables 
    WHERE schemaname = 'public'
  `;
  const result = await client.query(query);
  return result.rows.map(row => row.tablename);
}

async function getTableSchema(client, tableName) {
  // Get column definitions
  const columnsQuery = `
    SELECT column_name, data_type, character_maximum_length, column_default, is_nullable
    FROM information_schema.columns
    WHERE table_name = $1
    ORDER BY ordinal_position;
  `;
  const columns = await client.query(columnsQuery, [tableName]);

  // Get primary key constraints
  const pkQuery = `
    SELECT c.column_name
    FROM information_schema.table_constraints tc
    JOIN information_schema.constraint_column_usage AS ccu USING (constraint_schema, constraint_name)
    JOIN information_schema.columns AS c ON c.table_schema = tc.constraint_schema
      AND tc.table_name = c.table_name AND ccu.column_name = c.column_name
    WHERE constraint_type = 'PRIMARY KEY' AND tc.table_name = $1;
  `;
  const pks = await client.query(pkQuery, [tableName]);

  // Get foreign key constraints
  const fkQuery = `
    SELECT
      kcu.column_name,
      ccu.table_name AS foreign_table_name,
      ccu.column_name AS foreign_column_name
    FROM information_schema.table_constraints AS tc
    JOIN information_schema.key_column_usage AS kcu
      ON tc.constraint_name = kcu.constraint_name
      AND tc.table_schema = kcu.table_schema
    JOIN information_schema.constraint_column_usage AS ccu
      ON ccu.constraint_name = tc.constraint_name
      AND ccu.table_schema = tc.table_schema
    WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name = $1;
  `;
  const fks = await client.query(fkQuery, [tableName]);

  // Get indexes
  const indexQuery = `
    SELECT indexname, indexdef
    FROM pg_indexes
    WHERE tablename = $1;
  `;
  const indexes = await client.query(indexQuery, [tableName]);

  return {
    columns: columns.rows,
    primaryKeys: pks.rows,
    foreignKeys: fks.rows,
    indexes: indexes.rows
  };
}

async function generateCreateTableStatement(client, tableName, schema) {
  let sql = `CREATE TABLE IF NOT EXISTS "${tableName}" (\n`;

  // Add columns
  const columnDefs = schema.columns.map(col => {
    let def = `  "${col.column_name}" ${col.data_type}`;
    if (col.character_maximum_length) {
      def += `(${col.character_maximum_length})`;
    }
    if (col.column_default) {
      def += ` DEFAULT ${col.column_default}`;
    }
    if (col.is_nullable === 'NO') {
      def += ' NOT NULL';
    }
    return def;
  });

  // Add primary key constraint
  if (schema.primaryKeys.length > 0) {
    const pkColumns = schema.primaryKeys.map(pk => `"${pk.column_name}"`).join(', ');
    columnDefs.push(`  PRIMARY KEY (${pkColumns})`);
  }

  // Add foreign key constraints
  schema.foreignKeys.forEach(fk => {
    columnDefs.push(
      `  FOREIGN KEY ("${fk.column_name}") REFERENCES "${fk.foreign_table_name}" ("${fk.foreign_column_name}")`
    );
  });

  sql += columnDefs.join(',\n');
  sql += '\n);\n\n';

  // Add indexes
  schema.indexes.forEach(index => {
    if (!index.indexdef.includes('PRIMARY KEY')) {
      sql += `${index.indexdef};\n`;
    }
  });

  return sql;
}

async function backupDatabase(localPort) {
  // When using an SSH tunnel, we always connect to the tunnel's local endpoint
  const connectionConfig = {
    host: '127.0.0.1',  // Use 127.0.0.1 explicitly instead of localhost
    port: localPort,
    database: DB_NAME,
    user: DB_USER,
    password: DB_PASSWORD,
    ssl: false,
    keepAlive: true,
    connectionTimeoutMillis: 5000
  };

  console.log('\nDatabase connection details:');
  console.log('- Connecting through SSH tunnel at:', `${connectionConfig.host}:${connectionConfig.port}`);
  console.log('- Target database:', DB_NAME);
  console.log('- Database user:', DB_USER);
  console.log('- Password length:', DB_PASSWORD.length, 'characters');
  console.log('- SSL:', connectionConfig.ssl);
  console.log('- Timeout:', connectionConfig.connectionTimeoutMillis, 'ms');

  const client = new PgClient(connectionConfig);

  // Add error handler for client
  client.on('error', (err) => {
    console.error('PostgreSQL client error:', err);
  });

  try {
    console.log('\nEstablishing database connection...');
    await client.connect();
    console.log('Successfully connected to database');
    const writeStream = fs.createWriteStream(backupPath);

    // Write initial comments and settings
    writeStream.write('-- Database backup generated by Node.js backup script\n');
    writeStream.write(`-- Timestamp: ${new Date().toISOString()}\n\n`);
    writeStream.write('SET statement_timeout = 0;\n');
    writeStream.write('SET lock_timeout = 0;\n');
    writeStream.write('SET client_encoding = \'UTF8\';\n');
    writeStream.write('SET standard_conforming_strings = on;\n\n');

    // Get all tables
    const tables = await getTableNames(client);
    
    // Process each table
    for (const tableName of tables) {
      console.log(`Processing table: ${tableName}`);
      
      // Get table schema and generate CREATE TABLE statement
      const schema = await getTableSchema(client, tableName);
      const createTableSql = await generateCreateTableStatement(client, tableName, schema);
      writeStream.write(`-- Table: ${tableName}\n`);
      writeStream.write(`DROP TABLE IF EXISTS "${tableName}" CASCADE;\n`);
      writeStream.write(createTableSql);

      // Get table data
      const result = await client.query(`SELECT * FROM "${tableName}"`);
      if (result.rows.length > 0) {
        writeStream.write(`-- Data for table: ${tableName}\n`);
        for (const row of result.rows) {
          const columns = Object.keys(row).map(key => `"${key}"`).join(', ');
          const values = Object.values(row).map(value => 
            value === null ? 'NULL' : 
            typeof value === 'string' ? `'${value.replace(/'/g, "''")}'` :
            value instanceof Date ? `'${value.toISOString()}'` :
            value
          ).join(', ');
          
          writeStream.write(`INSERT INTO "${tableName}" (${columns}) VALUES (${values});\n`);
        }
        writeStream.write('\n');
      }
    }

    writeStream.end();
    await new Promise((resolve) => writeStream.on('finish', resolve));
    return backupPath;
  } catch (error) {
    console.error('Database connection/backup error:');
    console.error('- Error name:', error.name);
    console.error('- Error message:', error.message);
    console.error('- Error code:', error.code);
    console.error('- Error severity:', error.severity);
    console.error('- Error file:', error.file);
    console.error('- Error line:', error.line);
    console.error('- Error routine:', error.routine);
    if (error.hint) console.error('- Error hint:', error.hint);
    throw error;
  } finally {
    console.log('Closing database connection...');
    await client.end();
  }
}

// Main function
async function main() {
  let sshClient;
  let tunnelStream;
  
  try {
    console.log('Environment check:');
    console.log('- DB_HOST:', DB_HOST);
    console.log('- DB_PORT:', DB_PORT);
    console.log('- DB_NAME:', DB_NAME);
    console.log('- DB_USER:', DB_USER);
    console.log('- SSH_HOST:', SSH_HOST);
    console.log('- SSH_USER:', SSH_USER);
    console.log('- SSH_PORT:', SSH_PORT);
    console.log('- SSH_PRIVATE_KEY_PATH exists:', fs.existsSync(SSH_PRIVATE_KEY_PATH));
    
    console.log('\nCreating SSH tunnel...');
    const { ssh, localPort, server } = await createSSHTunnel();
    sshClient = ssh;
    tunnelStream = server;
    
    console.log('\nStarting database backup...');
    await backupDatabase(localPort);
    console.log(`\nBackup completed successfully! File saved to: ${backupPath}`);
    
  } catch (error) {
    console.error('\nError during backup process:');
    console.error(error);
    process.exit(1);
  } finally {
    if (tunnelStream) {
      tunnelStream.end();
    }
    if (sshClient) {
      console.log('Closing SSH connection...');
      sshClient.end();
    }
  }
}

main(); 