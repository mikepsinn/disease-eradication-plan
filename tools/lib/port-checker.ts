import { createServer } from "net";

/**
 * Check if a port is available
 */
export async function isPortAvailable(port: number): Promise<boolean> {
  return new Promise((resolve) => {
    const server = createServer();

    server.once("error", (err: any) => {
      if (err.code === "EADDRINUSE") {
        resolve(false);
      } else {
        resolve(false);
      }
    });

    server.once("listening", () => {
      server.close();
      resolve(true);
    });

    server.listen(port, "0.0.0.0");
  });
}

/**
 * Ensure port is available or throw
 */
export async function ensurePortAvailable(port: number): Promise<void> {
  const available = await isPortAvailable(port);

  if (!available) {
    throw new Error(
      `Port ${port} is already in use! ` +
        `Please stop the existing VoltAgent server or choose a different port.\n\n` +
        `To find and kill the process:\n` +
        `  Windows: netstat -ano | findstr ":${port}" then taskkill //F //PID <PID>\n` +
        `  Linux/Mac: lsof -ti:${port} | xargs kill -9\n\n` +
        `Or change VOLTAGENT_PORT in your .env file.`
    );
  }
}

/**
 * Find an available port starting from the given port
 */
export async function findAvailablePort(
  startPort: number,
  maxAttempts: number = 10
): Promise<number> {
  for (let port = startPort; port < startPort + maxAttempts; port++) {
    if (await isPortAvailable(port)) {
      return port;
    }
  }

  throw new Error(
    `Could not find an available port between ${startPort} and ${startPort + maxAttempts}`
  );
}
