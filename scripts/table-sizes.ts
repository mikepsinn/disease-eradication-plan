import 'dotenv/config'; // Load environment variables
import { Client as PgClient, ClientConfig } from 'pg';
import { Client as SshClient, ConnectConfig } from 'ssh2';
import * as fs from 'fs';
import * as net from 'net';
import * as path from 'path'; // Import path for fs.existsSync

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

interface SSHTunnelInfo {
  ssh: SshClient;
  localPort: number;
  server: net.Server;
}

/**
 * Function to create an SSH tunnel
 */
function createSSHTunnel(): Promise<SSHTunnelInfo> {
  const ssh = new SshClient();

  return new Promise((resolve, reject) => {
    ssh.on('ready', () => {
      console.log('SSH connection established successfully');
      console.log(`Forwarding local connections to ${DB_HOST}:${DB_PORT}`);

      // Create a TCP server that forwards data through the SSH tunnel
      const server = net.createServer((socket) => {
        ssh.forwardOut(
          socket.remoteAddress || '127.0.0.1', // Provide default if remoteAddress is undefined
          socket.remotePort || 0, // Provide default if remotePort is undefined
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
        const localPort = (server.address() as net.AddressInfo).port; // Cast to get port
        console.log(`SSH tunnel established at 127.0.0.1:${localPort}`);
        resolve({ ssh, localPort, server });
      });
    });

    ssh.on('error', (err: Error) => {
      console.error('SSH connection error:', err);
      reject(err);
    });

    try {
      console.log(`Connecting to SSH server ${SSH_HOST}:${SSH_PORT} as ${SSH_USER}`);
      console.log('Using private key from:', SSH_PRIVATE_KEY_PATH);
      const privateKey = fs.readFileSync(SSH_PRIVATE_KEY_PATH, 'utf8');
      const connectConfig: ConnectConfig = {
        host: SSH_HOST,
        port: parseInt(SSH_PORT),
        username: SSH_USER,
        privateKey: privateKey,
        debug: false,
      };
      ssh.connect(connectConfig);
    } catch (err: any) {
      console.error('Error reading SSH private key or connecting:', err);
      reject(err);
    }
  });
}

// Define interface for the query result rows
interface TableSize {
    Table: string;
    "Total Size": string; // Column name includes a space
}

/**
 * Function to query the size of all public tables in the database
 */
async function queryTableSizes(client: PgClient): Promise<TableSize[]> {
  const query = `
    SELECT relname AS "Table",
           pg_size_pretty(pg_total_relation_size(relid)) AS "Total Size"
    FROM pg_catalog.pg_statio_user_tables
    ORDER BY pg_total_relation_size(relid) DESC;
  `;
  const result = await client.query<TableSize>(query);
  return result.rows;
}

/**
 * Main function to set up the SSH tunnel, connect to the database, and output table sizes
 */
async function main(): Promise<void> {
  let sshClient: SshClient | undefined;
  let tunnelServer: net.Server | undefined;
  let pgClient: PgClient | undefined; // Keep track of the PG client

  try {
    console.log('Creating SSH tunnel...');
    const { ssh, localPort, server } = await createSSHTunnel();
    sshClient = ssh;
    tunnelServer = server;

    // Database connection configuration via the tunnel
    const connectionConfig: ClientConfig = {
      host: '127.0.0.1',  // Connect to the tunnel endpoint
      port: localPort,
      database: DB_NAME,
      user: DB_USER,
      password: DB_PASSWORD,
      ssl: false, // Assuming SSL is not needed over the SSH tunnel
      connectionTimeoutMillis: 5000,
      keepAlive: true
    };

    console.log(`Connecting to database "${DB_NAME}" using 127.0.0.1:${localPort}...`);
    const client = new PgClient(connectionConfig);
    pgClient = client; // Assign client to the variable for cleanup

    client.on('error', (err: Error) => console.error('PostgreSQL client error:', err));
    await client.connect();
    console.log('Connected to database successfully.');

    // Query table sizes
    const sizes = await queryTableSizes(client);
    console.log('\nTable Sizes:');

    // Use console.table for formatted output (common in Node.js scripts)
    console.table(sizes);

  } catch (error: any) {
    console.error('Error during process:');
    console.error(error);
    process.exit(1);
  } finally {
    // Ensure resources are cleaned up
    if (pgClient) {
        await pgClient.end();
        console.log('PostgreSQL client disconnected.');
    }
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