import 'dotenv/config'; // Load environment variables
import { Client as PgClient, ClientConfig } from 'pg';
import { Client as SshClient, ConnectConfig, SFTPWrapper } from 'ssh2';
import * as fs from 'fs';
import * as path from 'path';
import * as net from 'net';
import { glob } from 'glob';

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

interface SSHTunnelInfo {
  ssh: SshClient;
  localPort: number;
  server: net.Server;
}

// Function to create SSH tunnel
async function createSSHTunnel(): Promise<SSHTunnelInfo> {
  const ssh = new SshClient();

  return new Promise((resolve, reject) => {
    ssh.on('ready', () => {
      console.log('SSH connection established successfully');

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

    try {
      const privateKey = fs.readFileSync(SSH_PRIVATE_KEY_PATH, 'utf8');
      const connectConfig: ConnectConfig = {
        host: SSH_HOST,
        port: parseInt(SSH_PORT),
        username: SSH_USER,
        privateKey: privateKey
      };
      ssh.connect(connectConfig);
    } catch (err) {
      console.error('Error reading private key:', err);
      reject(err);
    }
  });
}

// Function to find all markdown files in the repository
async function findMarkdownFiles(): Promise<string[]> {
  const options = {
    ignore: ['node_modules/**', '.git/**'],
    absolute: false
  };

  try {
    const files = await glob('**/*.md', options);
    return files.map(f => f.replace(/\\/g, '/')); // Normalize path separators
  } catch (err) {
    console.error('Error finding markdown files:', err);
    throw err;
  }
}

interface DbPage {
  id: string;
  path: string;
  title: string;
}

async function findOrphanedPages(localPort: number, shouldDelete = false): Promise<void> {
  const connectionConfig: ClientConfig = {
    host: '127.0.0.1',
    port: localPort,
    database: DB_NAME,
    user: DB_USER,
    password: DB_PASSWORD,
    ssl: false // Assuming SSL is not needed over the SSH tunnel
  };

  const client = new PgClient(connectionConfig);

  try {
    await client.connect();
    console.log('Connected to database');

    // Get all pages from database
    const result = await client.query<DbPage>('SELECT id, path, title FROM pages ORDER BY path');
    const dbPages: DbPage[] = result.rows;

    // Get all markdown files from repository
    const markdownFiles = await findMarkdownFiles();

    // Find pages that don't have corresponding files
    const orphanedPages = dbPages.filter(page => {
      const pagePath = page.path.startsWith('/') ? page.path.slice(1) : page.path;
      return !markdownFiles.some(file => {
        // Try both with and without .md extension and case-insensitivity
        const normalizedFile = file.toLowerCase();
        const normalizedPagePath = pagePath.toLowerCase();
        return normalizedFile === normalizedPagePath || normalizedFile === `${normalizedPagePath}.md`;
      });
    });

    if (orphanedPages.length === 0) {
      console.log('No orphaned pages found!');
    } else {
      console.log('\nOrphaned pages found:');
      console.log('=====================');
      orphanedPages.forEach(page => {
        console.log(`ID: ${page.id}`);
        console.log(`Path: ${page.path}`);
        console.log(`Title: ${page.title}`);
        console.log('---------------------');
      });
      console.log(`\nTotal orphaned pages: ${orphanedPages.length}`);

      if (shouldDelete) {
        console.log('\nDeleting orphaned pages...');
        for (const page of orphanedPages) {
          console.log(`Deleting page: ${page.path}`);
          // Using parameterized query to prevent SQL injection
          await client.query('DELETE FROM pages WHERE id = $1', [page.id]);
        }
        console.log(`\nSuccessfully deleted ${orphanedPages.length} orphaned pages.`);
      } else {
        console.log('\nTo delete these pages, run the script with --delete flag');
      }
    }

  } catch (error) {
    console.error('Error:', error);
    throw error;
  } finally {
    // Ensure client connection is ended
    if (client) {
        await client.end();
    }
  }
}

async function main(): Promise<void> {
  let sshClient: SshClient | undefined;
  let server: net.Server | undefined;

  try {
    const args = process.argv.slice(2);
    const shouldDelete = args.includes('--delete');
    if (shouldDelete) {
      console.log('WARNING: Delete mode enabled. Orphaned pages will be removed from the database.');
      console.log('Press Ctrl+C within 5 seconds to abort...');
      // Wait for 5 seconds, but allow interruption
      await new Promise((resolve, reject) => {
          const timeoutId = setTimeout(resolve, 5000);
          process.on('SIGINT', () => {
              clearTimeout(timeoutId);
              reject(new Error('Deletion aborted by user.'));
          });
      });
    }

    const { ssh, localPort, server: sshServer } = await createSSHTunnel();
    sshClient = ssh;
    server = sshServer;

    await findOrphanedPages(localPort, shouldDelete);

  } catch (error) {
    console.error('Error:', error);
    // Exit with a non-zero code to indicate failure
    process.exit(1);
  } finally {
    // Clean up resources
    if (server) {
      server.close();
      console.log('Local server closed.');
    }
    if (sshClient) {
      sshClient.end();
      console.log('SSH client disconnected.');
    }
  }
}

// Execute the main function
main(); 