/**
 * Script to restore a PostgreSQL database backup to a target server using the node-postgres package.
 *
 * Usage:
 *   node scripts/db-restore.js [path/to/backup-file.sql]
 *
 * If no backup file is provided, the script will use the most recent .sql file
 * in the ../backups directory.
 *
 * If the environment variables RESTORE_SSH_HOST, RESTORE_SSH_USER, and 
 * RESTORE_SSH_PRIVATE_KEY_PATH are present, an SSH tunnel will be created.
 * Otherwise, the restore process connects directly.
 *
 * Required environment variables for database connection:
 *   RESTORE_DB_HOST
 *   RESTORE_DB_PORT
 *   RESTORE_DB_NAME
 *   RESTORE_DB_USER
 *   RESTORE_DB_PASSWORD
 *
 * Optional SSH tunneling environment variables:
 *   RESTORE_SSH_HOST
 *   RESTORE_SSH_USER
 *   RESTORE_SSH_PRIVATE_KEY_PATH
 *   RESTORE_SSH_PORT (defaults to 22)
 *
 * This script uses the "pg" Node package (declared in package.json) instead of spawning the "psql" command.
 */

require('dotenv').config();
const { Client: SshClient } = require('ssh2');
const fs = require('fs');
const net = require('net');
const path = require('path');
const { spawnSync } = require('child_process');

// Check required environment variables for the database connection
const requiredDbEnvVars = [
  'RESTORE_DB_HOST',
  'RESTORE_DB_PORT',
  'RESTORE_DB_NAME',
  'RESTORE_DB_USER',
  'RESTORE_DB_PASSWORD'
];
const missingDbEnvVars = requiredDbEnvVars.filter(v => !process.env[v]);
if (missingDbEnvVars.length > 0) {
  console.error('Error: Missing required database environment variables:');
  missingDbEnvVars.forEach(v => console.error(`- ${v}`));
  process.exit(1);
}

// Determine if SSH tunnel should be used (if SSH env vars are set)
const useSshTunnel = 
  process.env.RESTORE_SSH_HOST && 
  process.env.RESTORE_SSH_USER && 
  process.env.RESTORE_SSH_PRIVATE_KEY_PATH;

if (useSshTunnel) {
  console.log('SSH tunnel variables detected. Restoring via an SSH tunnel.');
} else {
  console.log('No SSH tunnel variables detected. Restoring directly.');
}

const {
  RESTORE_DB_HOST,
  RESTORE_DB_PORT,
  RESTORE_DB_NAME,
  RESTORE_DB_USER,
  RESTORE_DB_PASSWORD
} = process.env;

const RESTORE_SSH_HOST = process.env.RESTORE_SSH_HOST;
const RESTORE_SSH_USER = process.env.RESTORE_SSH_USER;
const RESTORE_SSH_PRIVATE_KEY_PATH = process.env.RESTORE_SSH_PRIVATE_KEY_PATH;
const RESTORE_SSH_PORT = process.env.RESTORE_SSH_PORT || '22';

// Determine backup file path.
// If a file is provided as a command-line argument, use it.
// Otherwise, search ../backups for the most recent .sql file.
let backupFilePath;
if (process.argv[2]) {
  backupFilePath = path.resolve(process.argv[2]);
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
  const files = fs.readdirSync(backupDir)
    .filter(file => file.endsWith('.sql'))
    .map(file => path.join(backupDir, file));

  if (files.length === 0) {
    console.error(`No backup files found in directory: ${backupDir}`);
    process.exit(1);
  }
  // Sort files by modification time in descending order (newest first)
  files.sort((a, b) => fs.statSync(b).mtime - fs.statSync(a).mtime);
  backupFilePath = files[0];
  console.log(`No backup file provided. Using the most recent file: ${backupFilePath}`);
}

/**
 * Creates an SSH tunnel to the target restore database.
 * Returns a promise resolving to an object containing the SSH client, localPort, and the tunnel server.
 */
async function createSSHTunnel() {
  const ssh = new SshClient();
  return new Promise((resolve, reject) => {
    ssh.on('ready', () => {
      console.log('SSH connection established successfully');
      console.log(`Forwarding local port to remote restore DB at ${RESTORE_DB_HOST}:${RESTORE_DB_PORT}`);
      const server = net.createServer((socket) => {
        ssh.forwardOut(
          socket.remoteAddress,
          socket.remotePort,
          RESTORE_DB_HOST,
          parseInt(RESTORE_DB_PORT, 10),
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
        const localPort = server.address().port;
        console.log(`SSH tunnel established: 127.0.0.1:${localPort} -> ${RESTORE_DB_HOST}:${RESTORE_DB_PORT}`);
        resolve({ ssh, localPort, server });
      });
    });
    ssh.on('error', (err) => {
      console.error('SSH connection error:', err);
      reject(err);
    });
    console.log(`Connecting to SSH server ${RESTORE_SSH_HOST}:${RESTORE_SSH_PORT} as ${RESTORE_SSH_USER}`);
    console.log('Using private key from:', RESTORE_SSH_PRIVATE_KEY_PATH);
    let privateKey;
    try {
      privateKey = fs.readFileSync(RESTORE_SSH_PRIVATE_KEY_PATH, 'utf8');
    } catch (err) {
      console.error('Error reading private key:', err);
      return reject(err);
    }
    ssh.connect({
      host: RESTORE_SSH_HOST,
      port: parseInt(RESTORE_SSH_PORT, 10),
      username: RESTORE_SSH_USER,
      privateKey: privateKey
    });
  });
}

/**
 * Main function to restore backup via psql CLI
 */
async function main() {
  let sshClient, tunnelServer;
  let connectionHost = RESTORE_DB_HOST;
  let connectionPort = RESTORE_DB_PORT;

  try {
    console.log('Starting restore process...');
    
    if (useSshTunnel) {
      const { ssh, localPort, server } = await createSSHTunnel();
      sshClient = ssh;
      tunnelServer = server;
      connectionHost = '127.0.0.1';
      connectionPort = localPort.toString();
    }

    console.log('\nDatabase restore connection details:');
    console.log(`- Host: ${connectionHost}`);
    console.log(`- Port: ${connectionPort}`);
    console.log(`- Target restore DB: ${RESTORE_DB_NAME}`);
    console.log(`- DB user: ${RESTORE_DB_USER}`);
    console.log(`- Backup file: ${backupFilePath}`);

    // Set up environment for psql command
    const env = {
      ...process.env,
      PGPASSWORD: RESTORE_DB_PASSWORD,
      PGSSLMODE: 'require' // Equivalent to rejectUnauthorized: false
    };

    // Cleanup commands
    const cleanupCommands = [
      'DROP SCHEMA IF EXISTS public CASCADE;',
      'CREATE SCHEMA public;',
      `GRANT ALL ON SCHEMA public TO ${RESTORE_DB_USER};`,
      'GRANT ALL ON SCHEMA public TO public;'
    ].join(' ');

    // Run database cleanup
    console.log('Cleaning existing database objects...');
    const cleanupArgs = [
      '-U', RESTORE_DB_USER,
      '-h', connectionHost,
      '-p', connectionPort,
      '-d', RESTORE_DB_NAME,
      '-c', cleanupCommands
    ];

    const cleanupResult = spawnSync('psql', cleanupArgs, { stdio: 'inherit', env });
    if (cleanupResult.status !== 0) {
      throw new Error('Database cleanup failed');
    }

    // Execute the backup file
    console.log('Starting restoration...');
    const restoreArgs = [
      '-U', RESTORE_DB_USER,
      '-h', connectionHost,
      '-p', connectionPort,
      '-d', RESTORE_DB_NAME,
      '-f', backupFilePath
    ];

    const restoreResult = spawnSync('psql', restoreArgs, { stdio: 'inherit', env });
    if (restoreResult.status !== 0) {
      throw new Error('Restore process failed');
    }

    console.log('Database restore completed successfully.');

  } catch (error) {
    console.error('\nError during restore process:');
    console.error(error);
    process.exit(1);
  } finally {
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

main(); 