import 'dotenv/config'; // Load environment variables
import { Client as PgClient, ClientConfig } from 'pg';
import { Client as SshClient, ConnectConfig } from 'ssh2';
import * as fs from 'fs';
import * as path from 'path';
import * as net from 'net';
import { spawnSync } from 'child_process';

// Define a type for the environment variables
interface EnvVars {
  RESTORE_DB_HOST: string;
  RESTORE_DB_PORT: string;
  RESTORE_DB_NAME: string;
  RESTORE_DB_USER: string;
  RESTORE_DB_PASSWORD: string;
  RESTORE_SSH_HOST?: string;
  RESTORE_SSH_USER?: string;
  RESTORE_SSH_PRIVATE_KEY_PATH?: string;
  RESTORE_SSH_PORT?: string;
  USE_SSH_TUNNEL?: string; // Assuming this env var exists based on logic
}

// Cast process.env to the defined type for easier access and type checking
const env = process.env as EnvVars;

// Determine if SSH tunnel should be used based on presence of SSH env vars or explicit flag
const useSshTunnel = env.USE_SSH_TUNNEL === 'true' || (
    !!env.RESTORE_SSH_HOST &&
    !!env.RESTORE_SSH_USER &&
    !!env.RESTORE_SSH_PRIVATE_KEY_PATH
);

if (useSshTunnel) {
  console.log('SSH tunnel variables detected. Restoring via an SSH tunnel.');
} else {
  console.log('No SSH tunnel variables detected. Restoring directly.');
}

// Validate required environment variables based on whether SSH tunnel is used
const requiredEnvVars: (keyof EnvVars)[] = [
  'RESTORE_DB_HOST',
  'RESTORE_DB_PORT',
  'RESTORE_DB_NAME',
  'RESTORE_DB_USER',
  'RESTORE_DB_PASSWORD',
];

if (useSshTunnel) {
    requiredEnvVars.push('RESTORE_SSH_HOST', 'RESTORE_SSH_USER', 'RESTORE_SSH_PRIVATE_KEY_PATH');
}

const missingEnvVars = requiredEnvVars.filter(varName => !env[varName]);
if (missingEnvVars.length > 0) {
  console.error('Error: Missing required environment variables:');
  missingEnvVars.forEach(varName => console.error(`- ${varName}`));
  console.error('\nPlease make sure these variables are set in your .env file');
  process.exit(1);
}

const {
  RESTORE_DB_HOST,
  RESTORE_DB_PORT,
  RESTORE_DB_NAME,
  RESTORE_DB_USER,
  RESTORE_DB_PASSWORD
} = env;

const RESTORE_SSH_HOST = env.RESTORE_SSH_HOST;
const RESTORE_SSH_USER = env.RESTORE_SSH_USER;
const RESTORE_SSH_PRIVATE_KEY_PATH = env.RESTORE_SSH_PRIVATE_KEY_PATH;
const RESTORE_SSH_PORT = env.RESTORE_SSH_PORT || '22';

// Validate SSH private key exists if tunnel is used
if (useSshTunnel && RESTORE_SSH_PRIVATE_KEY_PATH && !fs.existsSync(RESTORE_SSH_PRIVATE_KEY_PATH)) {
  console.error(`Error: SSH private key file not found at: ${RESTORE_SSH_PRIVATE_KEY_PATH}`);
  process.exit(1);
}

// Determine backup file path.
// If a file is provided as a command-line argument, use it.
// Otherwise, search ../backups for the most recent .sql file.
let backupFilePath: string;
const commandLineFile = process.argv[2];

if (commandLineFile) {
  backupFilePath = path.resolve(commandLineFile);
  if (!fs.existsSync(backupFilePath)) {
    console.error(`Backup file not found: ${backupFilePath}`);
    process.exit(1);
  }
} else {
  const backupDir = path.join(__dirname, '../backups');
  if (!fs.existsSync(backupDir)) {
    console.error(`Backup directory not found: ${backupDir}`);
    process.exit(1);
  }
  
  let files: string[];
  try {
     files = fs.readdirSync(backupDir)
        .filter(file => file.endsWith('.sql'))
        .map(file => path.join(backupDir, file));
  } catch (readDirError) {
      console.error(`Error reading backup directory ${backupDir}:`, readDirError);
      process.exit(1);
  }

  if (files.length === 0) {
    console.error(`No backup files found in directory: ${backupDir}`);
    process.exit(1);
  }
  // Sort files by modification time in descending order (newest first)
  files.sort((a, b) => fs.statSync(b).mtime.getTime() - fs.statSync(a).mtime.getTime());
  backupFilePath = files[0];
  console.log(`No backup file provided. Using the most recent file: ${backupFilePath}`);
}

interface SSHTunnelInfo {
  ssh: SshClient;
  localPort: number;
  server: net.Server;
}

/**
 * Creates an SSH tunnel to the target restore database.
 * Returns a promise resolving to an object containing the SSH client, localPort, and the tunnel server.
 */
async function createSSHTunnel(): Promise<SSHTunnelInfo> {
  const ssh = new SshClient();
  return new Promise((resolve, reject) => {
    ssh.on('ready', () => {
      console.log('SSH connection established successfully');
      console.log(`Forwarding local port to remote restore DB at ${RESTORE_DB_HOST}:${RESTORE_DB_PORT}`);
      const server = net.createServer((socket) => {
        ssh.forwardOut(
          socket.remoteAddress || '127.0.0.1', // Provide default if remoteAddress is undefined
          socket.remotePort || 0, // Provide default if remotePort is undefined
          RESTORE_DB_HOST as string, // Ensure host is string
          parseInt(RESTORE_DB_PORT as string, 10), // Ensure port is string
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
      server.listen(0, '127.0.0.1', () => {
        const localPort = (server.address() as net.AddressInfo).port;
        console.log(`SSH tunnel established: 127.0.0.1:${localPort} -> ${RESTORE_DB_HOST}:${RESTORE_DB_PORT}`);
        resolve({ ssh, localPort, server });
      });
    });
    ssh.on('error', (err: Error) => {
      console.error('SSH connection error:', err);
      reject(err);
    });

    if (!RESTORE_SSH_HOST || !RESTORE_SSH_USER || !RESTORE_SSH_PRIVATE_KEY_PATH) {
        return reject(new Error("SSH environment variables not fully set for tunnel creation."));
    }

    console.log(`Connecting to SSH server ${RESTORE_SSH_HOST}:${RESTORE_SSH_PORT} as ${RESTORE_SSH_USER}`);
    console.log('Using private key from:', RESTORE_SSH_PRIVATE_KEY_PATH);
    let privateKey: string;
    try {
      privateKey = fs.readFileSync(RESTORE_SSH_PRIVATE_KEY_PATH, 'utf8');
    } catch (err: any) {
      console.error('Error reading private key:', err);
      return reject(err);
    }

    const connectConfig: ConnectConfig = {
        host: RESTORE_SSH_HOST,
        port: parseInt(RESTORE_SSH_PORT, 10),
        username: RESTORE_SSH_USER,
        privateKey: privateKey
    };

    ssh.connect(connectConfig);
  });
}

/**
 * Main function to restore backup via psql CLI
 */
async function main(): Promise<void> {
  let sshClient: SshClient | undefined;
  let tunnelServer: net.Server | undefined;
  let connectionHost: string = RESTORE_DB_HOST as string; // Initialize with direct connection details
  let connectionPort: string = RESTORE_DB_PORT as string;

  try {
    console.log('Starting restore process...');

    if (useSshTunnel) {
      console.log('Setting up SSH tunnel...');
      const { ssh, localPort, server } = await createSSHTunnel();
      sshClient = ssh;
      tunnelServer = server;
      connectionHost = '127.0.0.1';
      connectionPort = localPort.toString();
      console.log('SSH tunnel established.');
    }

    console.log('\nDatabase restore connection details:');
    console.log(`- Host: ${connectionHost}`);
    console.log(`- Port: ${connectionPort}`);
    console.log(`- Target restore DB: ${RESTORE_DB_NAME}`);
    console.log(`- DB user: ${RESTORE_DB_USER}`);
    console.log(`- Backup file: ${backupFilePath}`);

    // Set up environment for psql command
    const envVars = {
      ...process.env,
      PGPASSWORD: RESTORE_DB_PASSWORD,
      PGSSLMODE: 'prefer'  // Changed from 'require' to handle servers without SSL
    };

    // Cleanup commands
    // Removed DROP/CREATE SCHEMA to avoid potential data loss on incorrect backups
    const cleanupCommands = [
      `GRANT ALL ON SCHEMA public TO ${RESTORE_DB_USER};`,
      'GRANT ALL ON SCHEMA public TO public;'
    ].join(' ');

    // Run database cleanup - using psql -c command
    console.log('Running post-restore cleanup commands...');
    const cleanupArgs = [
      '-U', RESTORE_DB_USER,
      '-h', connectionHost,
      '-p', connectionPort,
      '-d', RESTORE_DB_NAME,
      '-c', cleanupCommands
    ];

    const cleanupResult = spawnSync('psql', cleanupArgs, { 
      stdio: 'pipe',  // Capture output
      env: envVars, // Pass the environment with PGPASSWORD
      encoding: 'utf-8' // Specify encoding for stdout/stderr
    });

    if (cleanupResult.status !== 0) {
      console.error('\nCleanup failed with error:');
      console.error('STDOUT:', cleanupResult.stdout);
      console.error('STDERR:', cleanupResult.stderr);
      throw new Error(`Database cleanup failed with exit code ${cleanupResult.status}`);
    }
    console.log('Cleanup commands executed successfully.');

    // Execute the backup file using psql -f command
    console.log('Starting restoration...');
    const restoreArgs = [
      '-U', RESTORE_DB_USER,
      '-h', connectionHost,
      '-p', connectionPort,
      '-d', RESTORE_DB_NAME,
      '-f', backupFilePath
    ];

    // Use stdio: 'inherit' to show restore progress/errors directly
    const restoreResult = spawnSync('psql', restoreArgs, { stdio: 'inherit', env: envVars });
    if (restoreResult.status !== 0) {
      throw new Error(`Restore process failed with exit code ${restoreResult.status}`);
    }

    console.log('Database restore completed successfully.');

  } catch (error: any) {
    console.error('\nError during restore process:');
    console.error(error);
    process.exit(1); // Exit with a non-zero code to indicate failure
  } finally {
    // Ensure resources are cleaned up
    if (tunnelServer) {
      tunnelServer.close();
      console.log('SSH tunnel server closed.');
    }
    if (sshClient) {
      sshClient.end();
      console.log('SSH connection closed.');
    }
  }
}

// Execute the main function
main(); 