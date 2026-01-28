#!/usr/bin/env npx tsx
/**
 * Domain Status Checker
 *
 * Extracts all site-url values from Quarto config files and checks their status.
 * Reports any domains that are unreachable or returning errors.
 *
 * Usage:
 *   npx tsx scripts/check-domain-status.ts
 *   npx tsx scripts/check-domain-status.ts --json  # Output as JSON for CI
 */

import fs from "fs/promises";
import path from "path";
import { glob } from "glob";

interface DomainResult {
  configFile: string;
  siteUrl: string;
  status: "ok" | "error" | "redirect" | "timeout" | "dns-error";
  statusCode?: number;
  redirectUrl?: string;
  error?: string;
  responseTime?: number;
}

interface CheckSummary {
  timestamp: string;
  totalDomains: number;
  healthy: number;
  unhealthy: number;
  results: DomainResult[];
}

const TIMEOUT_MS = 10000;

// Domains to skip (test environments, etc.)
const SKIP_DOMAINS = [
  "test.warondisease.org",
];

async function extractSiteUrls(): Promise<
  Array<{ configFile: string; siteUrl: string }>
> {
  const results: Array<{ configFile: string; siteUrl: string }> = [];

  // Find all _quarto*.yml files in the root directory (not in _build_temp)
  const configFiles = await glob("_quarto*.yml", {
    cwd: process.cwd(),
    absolute: true,
  });

  for (const configFile of configFiles) {
    try {
      const content = await fs.readFile(configFile, "utf-8");

      // Extract site-url values using regex (simpler than YAML parsing for this case)
      const siteUrlMatches = content.matchAll(/^\s*site-url:\s*(.+)$/gm);

      for (const match of siteUrlMatches) {
        let url = match[1].trim();
        // Remove quotes if present
        url = url.replace(/^["']|["']$/g, "");
        if (url && url.startsWith("http")) {
          results.push({
            configFile: path.basename(configFile),
            siteUrl: url,
          });
        }
      }
    } catch (error) {
      console.error(`Error reading ${configFile}:`, error);
    }
  }

  // Deduplicate by URL while keeping track of which configs use each URL
  const urlMap = new Map<string, string[]>();
  for (const { configFile, siteUrl } of results) {
    if (!urlMap.has(siteUrl)) {
      urlMap.set(siteUrl, []);
    }
    urlMap.get(siteUrl)!.push(configFile);
  }

  return Array.from(urlMap.entries())
    .filter(([siteUrl]) => {
      try {
        const hostname = new URL(siteUrl).hostname;
        return !SKIP_DOMAINS.includes(hostname);
      } catch {
        return true;
      }
    })
    .map(([siteUrl, configs]) => ({
      configFile: configs.join(", "),
      siteUrl,
    }));
}

async function checkDomain(
  configFile: string,
  siteUrl: string
): Promise<DomainResult> {
  const startTime = Date.now();

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), TIMEOUT_MS);

    const response = await fetch(siteUrl, {
      method: "HEAD",
      redirect: "manual",
      signal: controller.signal,
      headers: {
        "User-Agent": "DomainStatusChecker/1.0 (Health Check)",
      },
    });

    clearTimeout(timeoutId);
    const responseTime = Date.now() - startTime;

    // Handle redirects
    if (response.status >= 300 && response.status < 400) {
      const redirectUrl = response.headers.get("location") || undefined;
      return {
        configFile,
        siteUrl,
        status: "redirect",
        statusCode: response.status,
        redirectUrl,
        responseTime,
      };
    }

    // Success
    if (response.status >= 200 && response.status < 300) {
      return {
        configFile,
        siteUrl,
        status: "ok",
        statusCode: response.status,
        responseTime,
      };
    }

    // Error status codes
    return {
      configFile,
      siteUrl,
      status: "error",
      statusCode: response.status,
      responseTime,
    };
  } catch (error: unknown) {
    const responseTime = Date.now() - startTime;

    if (error instanceof Error) {
      if (error.name === "AbortError") {
        return {
          configFile,
          siteUrl,
          status: "timeout",
          error: `Request timed out after ${TIMEOUT_MS}ms`,
          responseTime,
        };
      }

      // DNS or network errors
      if (
        error.message.includes("ENOTFOUND") ||
        error.message.includes("getaddrinfo")
      ) {
        return {
          configFile,
          siteUrl,
          status: "dns-error",
          error: "DNS resolution failed",
          responseTime,
        };
      }

      return {
        configFile,
        siteUrl,
        status: "error",
        error: error.message,
        responseTime,
      };
    }

    return {
      configFile,
      siteUrl,
      status: "error",
      error: "Unknown error",
      responseTime,
    };
  }
}

function formatResult(result: DomainResult): string {
  const statusEmoji = {
    ok: "[OK]",
    error: "[ERROR]",
    redirect: "[REDIRECT]",
    timeout: "[TIMEOUT]",
    "dns-error": "[DNS ERROR]",
  };

  const emoji = statusEmoji[result.status];
  const time = result.responseTime ? ` (${result.responseTime}ms)` : "";

  let line = `${emoji} ${result.siteUrl}${time}`;

  if (result.statusCode) {
    line += ` - HTTP ${result.statusCode}`;
  }

  if (result.redirectUrl) {
    line += ` -> ${result.redirectUrl}`;
  }

  if (result.error && result.status !== "ok") {
    line += ` - ${result.error}`;
  }

  line += `\n    Config: ${result.configFile}`;

  return line;
}

async function main() {
  const args = process.argv.slice(2);
  const jsonOutput = args.includes("--json");

  console.log("Domain Status Checker");
  console.log("=====================\n");

  console.log("Extracting site URLs from Quarto configs...");
  const sites = await extractSiteUrls();

  if (sites.length === 0) {
    console.log("No site URLs found in Quarto config files.");
    process.exit(0);
  }

  console.log(`Found ${sites.length} unique domains to check.\n`);

  const results: DomainResult[] = [];

  for (const { configFile, siteUrl } of sites) {
    if (!jsonOutput) {
      process.stdout.write(`Checking ${siteUrl}... `);
    }
    const result = await checkDomain(configFile, siteUrl);
    results.push(result);
    if (!jsonOutput) {
      console.log(result.status === "ok" ? "[OK]" : `[${result.status.toUpperCase()}]`);
    }
  }

  const summary: CheckSummary = {
    timestamp: new Date().toISOString(),
    totalDomains: results.length,
    healthy: results.filter((r) => r.status === "ok" || r.status === "redirect")
      .length,
    unhealthy: results.filter(
      (r) => r.status !== "ok" && r.status !== "redirect"
    ).length,
    results,
  };

  if (jsonOutput) {
    console.log(JSON.stringify(summary, null, 2));
  } else {
    console.log("\n" + "=".repeat(60));
    console.log("RESULTS");
    console.log("=".repeat(60) + "\n");

    // Group by status
    const healthy = results.filter(
      (r) => r.status === "ok" || r.status === "redirect"
    );
    const unhealthy = results.filter(
      (r) => r.status !== "ok" && r.status !== "redirect"
    );

    if (unhealthy.length > 0) {
      console.log("UNHEALTHY DOMAINS:");
      console.log("-".repeat(40));
      for (const result of unhealthy) {
        console.log(formatResult(result));
        console.log();
      }
    }

    if (healthy.length > 0) {
      console.log("\nHEALTHY DOMAINS:");
      console.log("-".repeat(40));
      for (const result of healthy) {
        console.log(formatResult(result));
        console.log();
      }
    }

    console.log("=".repeat(60));
    console.log(`SUMMARY: ${summary.healthy}/${summary.totalDomains} healthy`);
    if (summary.unhealthy > 0) {
      console.log(`WARNING: ${summary.unhealthy} domain(s) have issues!`);
    }
    console.log("=".repeat(60));
  }

  // Exit with error code if any domains are unhealthy
  if (summary.unhealthy > 0) {
    process.exit(1);
  }
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
