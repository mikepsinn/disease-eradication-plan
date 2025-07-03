import 'dotenv/config'; // Load environment variables
import { Client as PgClient, ClientConfig, QueryResult } from 'pg';
import { Client as SshClient, ConnectConfig, Channel, SFTPWrapper } from 'ssh2';
import * as fs from 'fs';
import * as fspromises from 'fs/promises';
import * as path from 'path';
import * as net from 'net';
import { spawnSync } from 'child_process';

// Define a type for the environment variables
interface EnvVars {
  DB_HOST: string;
  DB_PORT: string;
  DB_NAME: string;
  DB_USER: string;
  DB_PASSWORD: string;
  SSH_HOST: string;
  SSH_USER: string;
  SSH_PORT?: string;
  SSH_PRIVATE_KEY_PATH: string;
}

// Cast process.env to the defined type for easier access and type checking
const env = process.env as EnvVars;

// Validate required environment variables
const requiredEnvVars: (keyof EnvVars)[] = [
  'DB_HOST',
  'DB_PORT',
  'DB_NAME',
  'DB_USER',
  'DB_PASSWORD',
  'SSH_HOST',
  'SSH_USER',
  'SSH_PRIVATE_KEY_PATH'
];

const missingEnvVars = requiredEnvVars.filter(varName => !env[varName]);
if (missingEnvVars.length > 0) {
  console.error('Error: Missing required environment variables:');
  missingEnvVars.forEach(varName => console.error(`- ${varName}`));
  console.error('\nPlease make sure these variables are set in your .env file');
  process.exit(1);
}

// Environment variables (now accessed via the typed env object)
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
} = env;

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

interface SSHTunnelInfo {
  ssh: SshClient;
  localPort: number;
  server: net.Server;
}

/**
 * Function to create SSH tunnel
 */
async function createSSHTunnel(): Promise<SSHTunnelInfo> {
  const ssh = new SshClient();

  return new Promise((resolve, reject) => {
    ssh.on('ready', () => {
      console.log('SSH connection established successfully');
      console.log(`Will forward local port to remote database at ${DB_HOST}:${DB_PORT}`);

      const server = net.createServer((socket) => {
        ssh.forwardOut(
          socket.remoteAddress || '127.0.0.1', // Provide default if remoteAddress is undefined
          socket.remotePort || 0, // Provide default if remotePort is undefined
          DB_HOST,
          parseInt(DB_PORT, 10),
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
        const localPort = (server.address() as net.AddressInfo).port; // Cast to get port
        console.log(`SSH tunnel established: 127.0.0.1:${localPort} -> ${DB_HOST}:${DB_PORT}`);
        resolve({ ssh, localPort, server });
      });
    });

    ssh.on('error', (err: Error) => {
      console.error('SSH connection error:', err);
      reject(err);
    });

    console.log(`Connecting to SSH server ${SSH_HOST}:${SSH_PORT} as ${SSH_USER}`);
    console.log('Using private key from:', SSH_PRIVATE_KEY_PATH);

    try {
      const privateKey = fs.readFileSync(SSH_PRIVATE_KEY_PATH, 'utf8');
      const connectConfig: ConnectConfig = {
        host: SSH_HOST,
        port: parseInt(SSH_PORT, 10),
        username: SSH_USER,
        privateKey: privateKey,
        debug: false, // Set to true for detailed SSH logging
      };
      ssh.connect(connectConfig);
    } catch (err: any) {
      console.error('Error reading private key:', err);
      reject(err);
    }
  });
}

async function getTableNames(client: PgClient): Promise<string[]> {
  const query = `
    SELECT tablename
    FROM pg_tables
    WHERE schemaname = 'public'
  `;
  const result: QueryResult<{ tablename: string }> = await client.query(query);
  return result.rows.map(row => row.tablename);
}

interface ColumnInfo {
  column_name: string;
  data_type: string;
  character_maximum_length: number | null;
  column_default: string | null;
  is_nullable: 'YES' | 'NO';
}

interface PrimaryKeyInfo {
  column_name: string;
}

interface ForeignKeyInfo {
  column_name: string;
  foreign_table_name: string;
  foreign_column_name: string;
}

interface IndexInfo {
  indexname: string;
  indexdef: string;
}

interface TableSchema {
  columns: ColumnInfo[];
  primaryKeys: PrimaryKeyInfo[];
  foreignKeys: ForeignKeyInfo[];
  indexes: IndexInfo[];
}

async function getTableSchema(client: PgClient, tableName: string): Promise<TableSchema> {
  // Get column definitions
  const columnsQuery = `
    SELECT column_name, data_type, character_maximum_length, column_default, is_nullable
    FROM information_schema.columns
    WHERE table_name = $1
    ORDER BY ordinal_position;
  `;
  const columns: QueryResult<ColumnInfo> = await client.query(columnsQuery, [tableName]);

  // Get primary key constraints
  const pkQuery = `
    SELECT c.column_name
    FROM information_schema.table_constraints tc
    JOIN information_schema.constraint_column_usage AS ccu USING (constraint_schema, constraint_name)
    JOIN information_schema.columns AS c ON c.table_schema = tc.constraint_schema
      AND tc.table_name = c.table_name AND ccu.column_name = c.column_name
    WHERE constraint_type = 'PRIMARY KEY' AND tc.table_name = $1;
  `;
  const pks: QueryResult<PrimaryKeyInfo> = await client.query(pkQuery, [tableName]);

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
      AND ccu.constraint_schema = tc.constraint_schema -- Added missing schema join
    WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name = $1;
  `;
  const fks: QueryResult<ForeignKeyInfo> = await client.query(fkQuery, [tableName]);

  // Get indexes
  const indexQuery = `
    SELECT indexname, indexdef
    FROM pg_indexes
    WHERE tablename = $1;
  `;
  const indexes: QueryResult<IndexInfo> = await client.query(indexQuery, [tableName]);

  return {
    columns: columns.rows,
    primaryKeys: pks.rows,
    foreignKeys: fks.rows,
    indexes: indexes.rows
  };
}

async function generateCreateTableStatement(client: PgClient, tableName: string, schema: TableSchema): Promise<string> {
  let sql = `CREATE TABLE IF NOT EXISTS "${tableName}" (\n`;

  // Add columns
  const columnDefs = schema.columns.map(col => {
    let def = `  "${col.column_name}" ${col.data_type}`;
    if (col.character_maximum_length) {
      def += `(${col.character_maximum_length})`;
    }
    if (col.column_default) {
      // Handle defaults that are functions or keywords correctly
      const defaultValue = col.column_default.toLowerCase().startsWith('nextval(') || col.column_default.toLowerCase() === 'now()' || col.column_default.toLowerCase() === 'gen_random_uuid()'
        ? col.column_default
        : `'${col.column_default.replace(/'/g, "''")}'`; // Quote string defaults
      def += ` DEFAULT ${defaultValue}`;
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
    // Only include non-primary key indexes
    if (!index.indexdef.includes('PRIMARY KEY')) {
      sql += `${index.indexdef};\n`;
    }
  });

  return sql;
}

async function backupDatabase(localPort: number): Promise<string> {
  // When using an SSH tunnel, we always connect to the tunnel's local endpoint
  const connectionConfig: ClientConfig = {
    host: '127.0.0.1',  // Use 127.0.0.1 explicitly instead of localhost
    port: localPort,
    database: DB_NAME,
    user: DB_USER,
    password: DB_PASSWORD,
    ssl: false, // Assuming SSL is not needed over the SSH tunnel
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
  client.on('error', (err: Error) => {
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
      const result = await client.query<any>(`SELECT * FROM "${tableName}"`); // Use any as row structure is dynamic
      if (result.rows.length > 0) {
        writeStream.write(`-- Data for table: ${tableName}\n`);
        for (const row of result.rows) {
          const columns = Object.keys(row).map(key => `"${key}"`).join(', ');
          const values = Object.values(row).map(value =>
            value === null ? 'NULL' :
            typeof value === 'string' ? `'${value.replace(/'/g, "''")}'` :
            value instanceof Date ? `'${value.toISOString()}'` :
            // Handle other types like numbers, booleans, arrays, JSON objects etc.
            // For simplicity, treating non-string/non-Date objects as JSON string
            typeof value === 'object' && value !== null ? `'${JSON.stringify(value).replace(/'/g, "''")}'` :
            String(value) // Fallback for other primitive types
          ).join(', ');

          writeStream.write(`INSERT INTO "${tableName}" (${columns}) VALUES (${values});\n`);
        }
        writeStream.write('\n');
      }
    }

    writeStream.end();
    // Wait for the write stream to finish
    await new Promise<void>((resolve, reject) => {
        writeStream.on('finish', resolve);
        writeStream.on('error', reject); // Reject promise on write error
    });

    return backupPath; // Return the path on success
  } catch (error: any) {
    console.error('Database connection/backup error:', error);
    // Log specific PG error details if available
    if (error.code) console.error('- Error code:', error.code);
    if (error.detail) console.error('- Error detail:', error.detail);
    if (error.hint) console.error('- Error hint:', error.hint);
    throw error; // Re-throw the error to be caught by main
  } finally {
    console.log('Closing database connection...');
    // Ensure client is ended even if an error occurs after connecting
    if (client) {
      await client.end();
    }
  }
}

// Main function
async function main(): Promise<void> {
  let sshClient: SshClient | undefined;
  let tunnelServer: net.Server | undefined; // Correctly type tunnelServer

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
    // Pass the required environment variables to createSSHTunnel if needed, 
    // but they are already accessed via `env` object globally in this script
    const { ssh, localPort, server } = await createSSHTunnel();
    sshClient = ssh;
    tunnelServer = server; // Assign server to tunnelServer

    console.log('\nStarting database backup...');
    const finalBackupPath = await backupDatabase(localPort);
    console.log(`\nBackup completed successfully! File saved to: ${finalBackupPath}`);

  } catch (error: any) {
    console.error('\nError during backup process:');
    console.error(error);
    process.exit(1); // Exit with a non-zero code to indicate failure
  } finally {
    // Ensure resources are cleaned up
    if (tunnelServer) {
      tunnelServer.close();
      console.log('Local tunnel server closed.');
    }
    if (sshClient) {
      console.log('Closing SSH connection...');
      sshClient.end();
    }
  }
}

main(); 