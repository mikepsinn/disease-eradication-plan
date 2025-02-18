require('dotenv').config();
const { Client: PgClient } = require('pg');
const { Client: SshClient } = require('ssh2');
const fs = require('fs');
const path = require('path');
const net = require('net');
const { glob } = require('glob');

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

// Function to create SSH tunnel
async function createSSHTunnel() {
  const ssh = new SshClient();
  
  return new Promise((resolve, reject) => {
    ssh.on('ready', () => {
      console.log('SSH connection established successfully');

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
    
    try {
      const privateKey = fs.readFileSync(SSH_PRIVATE_KEY_PATH, 'utf8');
      ssh.connect({
        host: SSH_HOST,
        port: parseInt(SSH_PORT),
        username: SSH_USER,
        privateKey: privateKey
      });
    } catch (err) {
      console.error('Error reading private key:', err);
      reject(err);
    }
  });
}

// Function to find all markdown files in the repository
async function findMarkdownFiles() {
  const options = {
    ignore: ['node_modules/**', '.git/**'],
    absolute: false
  };
  
  try {
    const files = await glob('**/*.md', options);
    return files.map(f => f.replace(/\\/g, '/'));
  } catch (err) {
    console.error('Error finding markdown files:', err);
    throw err;
  }
}

async function findOrphanedPages(localPort, shouldDelete = false) {
  const connectionConfig = {
    host: '127.0.0.1',
    port: localPort,
    database: DB_NAME,
    user: DB_USER,
    password: DB_PASSWORD,
    ssl: false
  };

  const client = new PgClient(connectionConfig);
  
  try {
    await client.connect();
    console.log('Connected to database');

    // Get all pages from database
    const result = await client.query('SELECT id, path, title FROM pages ORDER BY path');
    const dbPages = result.rows;
    
    // Get all markdown files from repository
    const markdownFiles = await findMarkdownFiles();
    
    // Find pages that don't have corresponding files
    const orphanedPages = dbPages.filter(page => {
      const pagePath = page.path.startsWith('/') ? page.path.slice(1) : page.path;
      return !markdownFiles.some(file => {
        // Try both with and without .md extension
        return file === pagePath || file === `${pagePath}.md`;
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
    await client.end();
  }
}

async function main() {
  let sshClient;
  let server;
  
  try {
    const shouldDelete = process.argv.includes('--delete');
    if (shouldDelete) {
      console.log('WARNING: Delete mode enabled. Orphaned pages will be removed from the database.');
      console.log('Press Ctrl+C within 5 seconds to abort...');
      await new Promise(resolve => setTimeout(resolve, 5000));
    }

    const { ssh, localPort, server: sshServer } = await createSSHTunnel();
    sshClient = ssh;
    server = sshServer;
    
    await findOrphanedPages(localPort, shouldDelete);
    
  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  } finally {
    if (server) {
      server.close();
    }
    if (sshClient) {
      sshClient.end();
    }
  }
}

main(); 