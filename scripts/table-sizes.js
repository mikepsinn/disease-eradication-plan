require('dotenv').config();
const { Client: PgClient } = require('pg');
const { Client: SshClient } = require('ssh2');
const fs = require('fs');
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

/**
 * Function to create an SSH tunnel
 */
function createSSHTunnel() {
  const ssh = new SshClient();
  
  return new Promise((resolve, reject) => {
    ssh.on('ready', () => {
      console.log('SSH connection established successfully');
      console.log(`Forwarding local connections to ${DB_HOST}:${DB_PORT}`);

      // Create a TCP server that forwards data through the SSH tunnel
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
      
      // Listen on a random available port
      server.listen(0, '127.0.0.1', () => {
        const localPort = server.address().port;
        console.log(`SSH tunnel established at 127.0.0.1:${localPort}`);
        resolve({ ssh, localPort, server });
      });
    });
    
    ssh.on('error', (err) => {
      console.error('SSH connection error:', err);
      reject(err);
    });
    
    try {
      console.log(`Connecting to SSH server ${SSH_HOST}:${SSH_PORT} as ${SSH_USER}`);
      console.log('Using private key from:', SSH_PRIVATE_KEY_PATH);
      const privateKey = fs.readFileSync(SSH_PRIVATE_KEY_PATH, 'utf8');
      ssh.connect({
        host: SSH_HOST,
        port: parseInt(SSH_PORT),
        username: SSH_USER,
        privateKey: privateKey,
        debug: false,
      });
    } catch (err) {
      console.error('Error reading SSH private key:', err);
      reject(err);
    }
  });
}

/**
 * Function to query the size of all public tables in the database
 */
async function queryTableSizes(client) {
  const query = `
    SELECT relname AS "Table", 
           pg_size_pretty(pg_total_relation_size(relid)) AS "Total Size"
    FROM pg_catalog.pg_statio_user_tables
    ORDER BY pg_total_relation_size(relid) DESC;
  `;
  const result = await client.query(query);
  return result.rows;
}

/**
 * Main function to set up the SSH tunnel, connect to the database, and output table sizes
 */
async function main() {
  let sshClient;
  let tunnelServer;
  
  try {
    console.log('Creating SSH tunnel...');
    const { ssh, localPort, server } = await createSSHTunnel();
    sshClient = ssh;
    tunnelServer = server;
    
    // Database connection configuration via the tunnel
    const connectionConfig = {
      host: '127.0.0.1',  // Connect to the tunnel endpoint
      port: localPort,
      database: DB_NAME,
      user: DB_USER,
      password: DB_PASSWORD,
      ssl: false,
      connectionTimeoutMillis: 5000,
      keepAlive: true
    };
    
    console.log(`Connecting to database "${DB_NAME}" using 127.0.0.1:${localPort}...`);
    const client = new PgClient(connectionConfig);
    client.on('error', (err) => console.error('PostgreSQL client error:', err));
    await client.connect();
    console.log('Connected to database successfully.');
    
    // Query table sizes
    const sizes = await queryTableSizes(client);
    console.log('\nTable Sizes:');
    console.table(sizes);
    
    await client.end();
  } catch (error) {
    console.error('Error during process:');
    console.error(error);
    process.exit(1);
  } finally {
    if (tunnelServer) {
      tunnelServer.close();
    }
    if (sshClient) {
      console.log('Closing SSH connection...');
      sshClient.end();
    }
  }
}

main(); 