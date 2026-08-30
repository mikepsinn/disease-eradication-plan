#!/usr/bin/env npx tsx

import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

interface ExternalSite {
  name: string;
  url: string;
  keyword: string;
}

interface MonitorConfig {
  externalSites: ExternalSite[];
  excludedRedirectHosts: string[];
  keywordOverrides: Record<string, string>;
}

interface DesiredMonitor {
  friendlyName: string;
  url: string;
  keyword: string;
}

interface UptimeRobotMonitor {
  id: number;
  friendlyName: string;
  url: string;
}

interface AlertContact {
  id: number;
  value: string | null;
}

interface Pagination<T> {
  data: T[];
  nextLink: string | null;
}

const API_BASE_URL = "https://api.uptimerobot.com/v3";
const API_REQUEST_INTERVAL_MS = 6_500;
const REPOSITORY_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

function normalizeUrl(url: string): string {
  return url.replace(/\/+$/, "");
}

function keywordFromTarget(target: string): string {
  const targetUrl = new URL(target);
  const lastPathSegment = targetUrl.pathname.split("/").filter(Boolean).at(-1);
  return lastPathSegment?.replace(/\.html$/, "") || targetUrl.hostname.split(".")[0];
}

export async function loadDesiredMonitors(repositoryRoot = REPOSITORY_ROOT): Promise<DesiredMonitor[]> {
  const redirectMapPath = path.join(repositoryRoot, "cloudflare", "redirect-worker", "redirect-map.json");
  const monitorConfigPath = path.join(repositoryRoot, "monitoring", "uptimerobot-sites.json");

  const [redirectMapJson, monitorConfigJson] = await Promise.all([
    readFile(redirectMapPath, "utf8"),
    readFile(monitorConfigPath, "utf8"),
  ]);

  const redirectMap = JSON.parse(redirectMapJson) as Record<string, string>;
  const monitorConfig = JSON.parse(monitorConfigJson) as MonitorConfig;
  const excludedRedirectHosts = new Set(monitorConfig.excludedRedirectHosts);

  for (const hostname of excludedRedirectHosts) {
    if (!(hostname in redirectMap)) {
      throw new Error(`Excluded redirect host is not present in the redirect map: ${hostname}`);
    }
  }

  const redirectMonitors = Object.entries(redirectMap)
    .filter(([hostname]) => !excludedRedirectHosts.has(hostname))
    .map(([hostname, target]) => ({
      friendlyName: `EOS redirect | ${hostname}`,
      url: `https://${hostname}/`,
      keyword: monitorConfig.keywordOverrides[hostname] || keywordFromTarget(target),
    }));

  const externalMonitors = monitorConfig.externalSites.map((site) => ({
    friendlyName: `EOS site | ${site.name}`,
    url: site.url,
    keyword: site.keyword,
  }));

  const monitors = [...redirectMonitors, ...externalMonitors].sort((a, b) =>
    a.friendlyName.localeCompare(b.friendlyName),
  );
  const names = new Set(monitors.map((monitor) => monitor.friendlyName));
  const urls = new Set(monitors.map((monitor) => normalizeUrl(monitor.url)));

  if (names.size !== monitors.length) {
    throw new Error("UptimeRobot monitor names must be unique");
  }
  if (urls.size !== monitors.length) {
    throw new Error("UptimeRobot monitor URLs must be unique");
  }
  if (monitors.length > 50) {
    throw new Error(`The UptimeRobot Free plan supports 50 monitors, but ${monitors.length} were generated`);
  }
  for (const monitor of monitors) {
    if (!monitor.keyword.trim()) {
      throw new Error(`Monitor ${monitor.friendlyName} has an empty keyword`);
    }
  }

  return monitors;
}

function monitorPayload(monitor: DesiredMonitor, alertContactId: number, update = false) {
  return {
    friendlyName: monitor.friendlyName,
    interval: 300,
    assignedAlertContacts: [
      {
        alertContactId,
        threshold: 0,
        recurrence: 0,
      },
    ],
    httpMethodType: "GET",
    followRedirections: true,
    type: "KEYWORD",
    url: monitor.url,
    timeout: 30,
    keywordType: "ALERT_NOT_EXISTS",
    keywordCaseType: update ? 1 : "CaseInsensitive",
    keywordValue: monitor.keyword,
  };
}

let lastApiRequestAt = 0;

async function waitForApiRateLimit(): Promise<void> {
  const elapsed = Date.now() - lastApiRequestAt;
  const remaining = API_REQUEST_INTERVAL_MS - elapsed;
  if (remaining > 0) {
    await new Promise((resolve) => setTimeout(resolve, remaining));
  }
}

async function apiRequest<T>(apiKey: string, endpoint: string, init: RequestInit = {}): Promise<T> {
  const requestUrl = endpoint.startsWith("http") ? endpoint : `${API_BASE_URL}${endpoint}`;

  for (;;) {
    await waitForApiRateLimit();
    const response = await fetch(requestUrl, {
      ...init,
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json",
        ...init.headers,
      },
      signal: AbortSignal.timeout(30_000),
    });
    lastApiRequestAt = Date.now();

    if (response.status === 429) {
      const retryAfterSeconds = Number(response.headers.get("retry-after") || "60");
      await new Promise((resolve) => setTimeout(resolve, (retryAfterSeconds + 1) * 1_000));
      continue;
    }

    const responseText = await response.text();
    const responseBody = responseText ? JSON.parse(responseText) : null;
    if (!response.ok) {
      throw new Error(`UptimeRobot API ${response.status}: ${JSON.stringify(responseBody)}`);
    }
    return responseBody as T;
  }
}

async function listPaginated<T>(apiKey: string, endpoint: string): Promise<T[]> {
  const items: T[] = [];
  let nextEndpoint: string | null = endpoint;

  while (nextEndpoint) {
    const page: Pagination<T> = await apiRequest<Pagination<T>>(apiKey, nextEndpoint);
    items.push(...page.data);
    nextEndpoint = page.nextLink;
  }

  return items;
}

async function getAlertContactId(apiKey: string): Promise<number> {
  const configuredId = process.env.UPTIMEROBOT_ALERT_CONTACT_ID;
  if (configuredId) {
    return Number(configuredId);
  }

  const contacts = await listPaginated<AlertContact>(apiKey, "/alert-contacts");
  const emailContacts = contacts.filter((contact) => contact.value?.includes("@"));
  if (emailContacts.length !== 1) {
    throw new Error(
      `Expected exactly one UptimeRobot email alert contact, found ${emailContacts.length}. Set UPTIMEROBOT_ALERT_CONTACT_ID.`,
    );
  }
  return emailContacts[0].id;
}

async function syncMonitors(monitors: DesiredMonitor[]): Promise<void> {
  const apiKey = process.env.UPTIMEROBOT_API_KEY;
  if (!apiKey) {
    throw new Error("UPTIMEROBOT_API_KEY is required to synchronize monitors");
  }

  const alertContactId = await getAlertContactId(apiKey);
  const existingMonitors = await listPaginated<UptimeRobotMonitor>(apiKey, "/monitors?limit=200");
  const desiredUrls = new Set(monitors.map((monitor) => normalizeUrl(monitor.url)));

  for (const existing of existingMonitors) {
    const isManagedRedirect = existing.friendlyName.startsWith("EOS redirect | ");
    if (isManagedRedirect && !desiredUrls.has(normalizeUrl(existing.url))) {
      await apiRequest(apiKey, `/monitors/${existing.id}`, {
        method: "DELETE",
      });
      console.log(`[deleted] ${existing.friendlyName}`);
    }
  }

  for (const monitor of monitors) {
    const existing = existingMonitors.find(
      (candidate) =>
        candidate.friendlyName === monitor.friendlyName || normalizeUrl(candidate.url) === normalizeUrl(monitor.url),
    );
    const payload = monitorPayload(monitor, alertContactId, Boolean(existing));

    if (existing) {
      await apiRequest(apiKey, `/monitors/${existing.id}`, {
        method: "PATCH",
        body: JSON.stringify(payload),
      });
      console.log(`[updated] ${monitor.friendlyName}`);
    } else {
      await apiRequest(apiKey, "/monitors", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      console.log(`[created] ${monitor.friendlyName}`);
    }
  }

  console.log(`Synchronized ${monitors.length} UptimeRobot monitors`);
}

async function validateLiveSites(monitors: DesiredMonitor[]): Promise<void> {
  const checks = await Promise.allSettled(
    monitors.map(async (monitor) => {
      const response = await fetch(monitor.url, {
        redirect: "follow",
        headers: { "User-Agent": "EOS-UptimeRobot-Config-Check/1.0" },
        signal: AbortSignal.timeout(30_000),
      });
      const body = await response.text();
      return {
        monitor,
        status: response.status,
        finalUrl: response.url,
        keywordFound: body.toLowerCase().includes(monitor.keyword.toLowerCase()),
      };
    }),
  );

  let failures = 0;
  for (let index = 0; index < checks.length; index += 1) {
    const check = checks[index];
    const monitor = monitors[index];
    if (check.status === "rejected") {
      failures += 1;
      console.error(`[error] ${monitor.friendlyName}: ${String(check.reason)}`);
      continue;
    }

    const healthy = check.value.status >= 200 && check.value.status < 300 && check.value.keywordFound;
    if (!healthy) {
      failures += 1;
    }
    console.log(
      `${healthy ? "[ok]" : "[failed]"} ${monitor.friendlyName}: HTTP ${check.value.status}, keyword=${check.value.keywordFound}, final=${check.value.finalUrl}`,
    );
  }

  if (failures > 0) {
    throw new Error(`${failures} of ${monitors.length} monitor checks failed`);
  }
}

async function main(): Promise<void> {
  const monitors = await loadDesiredMonitors();
  const command = process.argv[2] || "--list";

  if (command === "--list") {
    console.log(JSON.stringify(monitors, null, 2));
    return;
  }
  if (command === "--check") {
    await validateLiveSites(monitors);
    return;
  }
  if (command === "--sync") {
    await syncMonitors(monitors);
    return;
  }

  throw new Error(`Unknown command: ${command}`);
}

main();
