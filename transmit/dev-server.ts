#!/usr/bin/env npx tsx
/**
 * Local dev server for transmit.
 *
 * Serves static files from public/ and routes /api/* to the Vercel edge
 * function handlers. Loads .env from the repo root.
 *
 * Run:  npx tsx transmit/dev-server.ts
 */

import { createServer } from "http";
import { readFileSync, existsSync, statSync } from "fs";
import { resolve, join, extname } from "path";
import { config } from "dotenv";

// Load .env from repo root
config({ path: resolve(__dirname, "..", ".env") });

const PORT = Number(process.env.PORT) || 3333;
const PUBLIC_DIR = resolve(__dirname, "public");

const MIME: Record<string, string> = {
  ".html": "text/html",
  ".css": "text/css",
  ".js": "application/javascript",
  ".json": "application/json",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".svg": "image/svg+xml",
  ".ico": "image/x-icon",
  ".woff2": "font/woff2",
};

// Lazy-import API handlers
async function loadHandler(name: string) {
  const mod = await import(`./api/${name}`);
  return mod.default;
}

const server = createServer(async (req, res) => {
  const url = new URL(req.url || "/", `http://localhost:${PORT}`);

  // Proxy JSON assets to manual.warondisease.org (mirrors Vercel rewrites)
  if (url.pathname === "/assets/image-index.json" || url.pathname.startsWith("/assets/json/")) {
    try {
      const upstream = await fetch("https://manual.warondisease.org" + url.pathname);
      res.writeHead(upstream.status, { "Content-Type": "application/json" });
      const body = await upstream.arrayBuffer();
      res.end(Buffer.from(body));
    } catch {
      res.writeHead(502);
      res.end("Proxy error");
    }
    return;
  }

  // API routes: convert Node req to Web Request, call handler, pipe back
  if (url.pathname.startsWith("/api/")) {
    const route = url.pathname.replace("/api/", "").replace(/\/$/, "");
    try {
      const handler = await loadHandler(route);

      // Build a Web Request from the Node request
      const headers = new Headers();
      for (const [k, v] of Object.entries(req.headers)) {
        if (v) headers.set(k, Array.isArray(v) ? v.join(", ") : v);
      }

      let body: string | undefined;
      if (req.method !== "GET" && req.method !== "HEAD") {
        body = await new Promise<string>((resolve) => {
          let data = "";
          req.on("data", (chunk: Buffer) => (data += chunk.toString()));
          req.on("end", () => resolve(data));
        });
      }

      const webReq = new Request(url.toString(), {
        method: req.method,
        headers,
        body: body || undefined,
      });

      const webRes: Response = await handler(webReq);

      // Write status + headers
      const resHeaders: Record<string, string> = {};
      webRes.headers.forEach((v, k) => (resHeaders[k] = v));
      res.writeHead(webRes.status, resHeaders);

      // Stream the body
      if (webRes.body) {
        const reader = webRes.body.getReader();
        const pump = async () => {
          while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            res.write(value);
          }
          res.end();
        };
        pump();
      } else {
        res.end(await webRes.text());
      }
    } catch (err: any) {
      res.writeHead(500, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: err.message }));
    }
    return;
  }

  // Static files from public/
  let filePath = join(PUBLIC_DIR, url.pathname);
  if (existsSync(filePath) && statSync(filePath).isDirectory()) {
    filePath = join(filePath, "index.html");
  }
  if (!existsSync(filePath)) {
    // SPA fallback
    filePath = join(PUBLIC_DIR, "index.html");
  }

  try {
    const data = readFileSync(filePath);
    const ext = extname(filePath);
    res.writeHead(200, { "Content-Type": MIME[ext] || "application/octet-stream" });
    res.end(data);
  } catch {
    res.writeHead(404);
    res.end("Not found");
  }
});

server.listen(PORT, () => {
  console.log(`\n  transmit dev server running at http://localhost:${PORT}\n`);
  console.log(`  API key loaded: ${process.env.GOOGLE_GENERATIVE_AI_API_KEY ? "yes" : "NO - check .env"}`);
  console.log(`  Static files:   ${PUBLIC_DIR}\n`);
});
