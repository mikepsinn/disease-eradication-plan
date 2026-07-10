import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

import { Client } from '@notionhq/client';
import dotenv from 'dotenv';
import matter from 'gray-matter';
import { load as loadYaml } from 'js-yaml';

const projectRoot = process.cwd();

dotenv.config({ path: path.resolve(projectRoot, '..', '.env') });
dotenv.config({ path: path.resolve(projectRoot, '..', '.env.local') });
dotenv.config({ path: path.resolve(projectRoot, '.env') });
dotenv.config({ path: path.resolve(projectRoot, '.env.local') });

const notionToken = process.env.NOTION_TOKEN;
const manualPagesDatabaseId =
  process.env.NOTION_MANUAL_PAGES_DATABASE_ID ?? 'a7166366a9c842f9860781e18a1b666b';

if (!notionToken) {
  throw new Error('NOTION_TOKEN is required. Put it in ../.env, .env, or the shell environment.');
}

type QuartoEntry = {
  part: string;
  text: string;
  href: string;
};

type ManualPageRow = {
  order: number;
  part: string;
  page: string;
  path: string;
  publicUrl: string;
  description: string;
  tags: string;
  published: boolean;
  lastGitModified: string | null;
};

const notion = new Client({ auth: notionToken });

function qmdToPublicUrl(siteUrl: string, href: string): string {
  const cleanSite = siteUrl.replace(/\/$/, '');
  if (href === 'index.qmd') {
    return cleanSite;
  }
  return `${cleanSite}/${href.replace(/\\/g, '/').replace(/\.qmd$/, '.html')}`;
}

function titleFromPath(filePath: string): string {
  const base = path.basename(filePath, '.qmd');
  if (base === 'index') {
    return 'Start Here';
  }
  return base
    .split(/[-_]/)
    .filter(Boolean)
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}

function toTextList(value: unknown): string {
  if (Array.isArray(value)) {
    return value.map(String).join(', ');
  }
  if (value == null) {
    return '';
  }
  return String(value);
}

function getGitModifiedDate(filePath: string): string | null {
  const result = spawnSync('git', ['log', '-1', '--format=%cI', '--', filePath], {
    cwd: projectRoot,
    encoding: 'utf8',
  });
  if (result.status !== 0) {
    return null;
  }
  const stdout = result.stdout.trim();
  return stdout || null;
}

function walkQuartoEntries(value: unknown, part: string, rows: QuartoEntry[]): void {
  if (Array.isArray(value)) {
    for (const item of value) {
      if (typeof item === 'string' && item.endsWith('.qmd')) {
        rows.push({ part, text: '', href: item });
      } else {
        walkQuartoEntries(item, part, rows);
      }
    }
    return;
  }

  if (!value || typeof value !== 'object') {
    return;
  }

  const item = value as Record<string, unknown>;
  const nextPart = typeof item.part === 'string' ? item.part : part;
  const sectionPart = typeof item.section === 'string' ? item.section : nextPart;

  if (typeof item.href === 'string' && item.href.endsWith('.qmd')) {
    rows.push({
      part,
      text: typeof item.text === 'string' ? item.text : '',
      href: item.href,
    });
  }

  for (const key of ['chapters', 'contents']) {
    if (key in item) {
      walkQuartoEntries(item[key], sectionPart, rows);
    }
  }
}

function collectManualRows(): ManualPageRow[] {
  const configPath = path.resolve(projectRoot, '_quarto-manual.yml');
  const config = loadYaml(fs.readFileSync(configPath, 'utf8')) as Record<string, any>;
  const siteUrl =
    config?.book?.['site-url'] ??
    config?.website?.['site-url'] ??
    'https://manual.warondisease.org';

  const entries: QuartoEntry[] = [];
  walkQuartoEntries(config?.book?.sidebar?.contents ?? [], 'Key Resources', entries);
  walkQuartoEntries(config?.book?.chapters ?? [], '', entries);

  const seen = new Set<string>();
  const rows: ManualPageRow[] = [];

  for (const entry of entries) {
    if (seen.has(entry.href)) {
      continue;
    }
    seen.add(entry.href);

    const fullPath = path.resolve(projectRoot, entry.href);
    const exists = fs.existsSync(fullPath);
    const parsed = exists ? matter(fs.readFileSync(fullPath, 'utf8')) : { data: {} };
    const data = parsed.data as Record<string, unknown>;
    const page =
      entry.text ||
      (typeof data.title === 'string' ? data.title : '') ||
      titleFromPath(entry.href);

    rows.push({
      order: rows.length + 1,
      part: entry.part,
      page,
      path: entry.href.replace(/\\/g, '/'),
      publicUrl: qmdToPublicUrl(siteUrl, entry.href),
      description: typeof data.description === 'string' ? data.description : '',
      tags: toTextList(data.tags ?? data.categories),
      published: data.published !== false,
      lastGitModified: exists ? getGitModifiedDate(entry.href) : null,
    });
  }

  return rows;
}

function richText(content: string) {
  return content ? [{ text: { content: content.slice(0, 2000) } }] : [];
}

function propertiesForRow(row: ManualPageRow) {
  return {
    Page: { title: [{ text: { content: row.page.slice(0, 2000) } }] },
    Part: { rich_text: richText(row.part) },
    Order: { number: row.order },
    'Public URL': { url: row.publicUrl },
    'QMD Path': { rich_text: richText(row.path) },
    Description: { rich_text: richText(row.description) },
    Tags: { rich_text: richText(row.tags) },
    Published: { checkbox: row.published },
    'Last Git Modified': row.lastGitModified
      ? { date: { start: row.lastGitModified } }
      : { date: null },
  };
}

async function findExistingPage(pathValue: string): Promise<string | null> {
  const response = await notion.databases.query({
    database_id: manualPagesDatabaseId,
    filter: {
      property: 'QMD Path',
      rich_text: {
        equals: pathValue,
      },
    },
    page_size: 1,
  });

  return response.results[0]?.id ?? null;
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function upsertRows(rows: ManualPageRow[], dryRun: boolean): Promise<void> {
  let created = 0;
  let updated = 0;

  for (const row of rows) {
    const existingPageId = await findExistingPage(row.path);

    if (dryRun) {
      console.log(`${existingPageId ? 'UPDATE' : 'CREATE'} ${row.order}: ${row.path}`);
      continue;
    }

    if (existingPageId) {
      await notion.pages.update({
        page_id: existingPageId,
        properties: propertiesForRow(row),
      });
      updated += 1;
    } else {
      await notion.pages.create({
        parent: { database_id: manualPagesDatabaseId },
        properties: propertiesForRow(row),
      });
      created += 1;
    }

    await sleep(350);
  }

  console.log(`Manual page index synced. rows=${rows.length} created=${created} updated=${updated}`);
}

async function main(): Promise<void> {
  const dryRun = process.argv.includes('--dry-run');
  const rows = collectManualRows();
  console.log(`Found ${rows.length} rendered manual pages in _quarto-manual.yml.`);
  await upsertRows(rows, dryRun);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
