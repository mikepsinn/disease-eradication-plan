import fs from 'node:fs';
import path from 'node:path';

import { Client } from '@notionhq/client';
import dotenv from 'dotenv';

const projectRoot = process.cwd();

dotenv.config({ path: path.resolve(projectRoot, '..', '.env') });
dotenv.config({ path: path.resolve(projectRoot, '..', '.env.local') });
dotenv.config({ path: path.resolve(projectRoot, '.env') });
dotenv.config({ path: path.resolve(projectRoot, '.env.local') });

const notionToken = process.env.NOTION_TOKEN;
const parametersDatabaseId =
  process.env.NOTION_PARAMETERS_DATABASE_ID ?? 'd8ead1b2f9924a928a19cc619f5c3528';
const manualPagesDatabaseId =
  process.env.NOTION_MANUAL_PAGES_DATABASE_ID ?? 'a7166366a9c842f9860781e18a1b666b';
const parametersJsonPath = path.resolve(projectRoot, 'assets', 'json', 'parameters.json');

if (!notionToken) {
  throw new Error('NOTION_TOKEN is required. Put it in ../.env, .env, or the shell environment.');
}

type CitationAuthor = {
  family?: string;
  given?: string;
  literal?: string;
};

type Citation = {
  title?: string;
  source?: string;
  publisher?: string;
  author?: CitationAuthor[];
  year?: string | number;
  issued?: { 'date-parts'?: Array<Array<number>> };
};

type ParameterExport = {
  value: number;
  formatted?: string | null;
  unit?: string | null;
  description?: string | null;
  displayName?: string | null;
  sourceType?: string | null;
  sourceRef?: string | null;
  sourceUrl?: string | null;
  confidence?: string | null;
  formula?: string | null;
  calculationUrl?: string | null;
  confidenceInterval?: [number, number];
  distribution?: string | null;
  inputs?: string[];
  computeExpr?: string | null;
  latex?: string | null;
  chapterUrl?: string | null;
};

type ParametersPayload = {
  parameters: Record<string, ParameterExport>;
  citations: Record<string, Citation>;
};

type ExistingPage = {
  id: string;
  title: string;
};

const notion = new Client({ auth: notionToken });

function richText(content: string | null | undefined) {
  const clean = (content ?? '').trim();
  return clean ? [{ text: { content: clean.slice(0, 2000) } }] : [];
}

function selectValue(name: string | null | undefined) {
  const clean = (name ?? '').trim();
  return clean ? { name: clean } : null;
}

function urlValue(url: string | null | undefined): string | null {
  const clean = (url ?? '').trim();
  if (!clean.startsWith('http://') && !clean.startsWith('https://')) {
    return null;
  }
  return clean;
}

function normalizeUrl(url: string | null | undefined): string {
  return (url ?? '').trim().replace(/\/$/, '').toLowerCase();
}

function titleFromPage(page: any, propertyName: string): string {
  const title = page.properties?.[propertyName]?.title ?? [];
  return title.map((part: any) => part.plain_text ?? '').join('');
}

function urlFromPage(page: any, propertyName: string): string | null {
  return page.properties?.[propertyName]?.url ?? null;
}

function citationYear(citation: Citation): string {
  if (citation.year) {
    return String(citation.year);
  }
  const issuedYear = citation.issued?.['date-parts']?.[0]?.[0];
  return issuedYear ? String(issuedYear) : '';
}

function citationAuthor(citation: Citation): string {
  const firstAuthor = citation.author?.[0];
  if (!firstAuthor) {
    return '';
  }
  if (firstAuthor.literal) {
    return firstAuthor.literal;
  }
  return [firstAuthor.given, firstAuthor.family].filter(Boolean).join(' ');
}

function citationLabel(sourceRef: string | null | undefined, citations: Record<string, Citation>): string {
  if (!sourceRef) {
    return '';
  }
  const citation = citations[sourceRef];
  if (!citation) {
    return sourceRef;
  }
  const source = citation.source || citation.publisher || citationAuthor(citation) || sourceRef;
  const year = citationYear(citation);
  const prefix = year ? `${source} (${year})` : source;
  return citation.title ? `${prefix} - ${citation.title}` : prefix;
}

function confidenceIntervalText(parameter: ParameterExport): string {
  const interval = parameter.confidenceInterval;
  return interval ? `${interval[0]} to ${interval[1]}` : '';
}

function relationForChapter(
  parameter: ParameterExport,
  manualPageByPublicUrl: Map<string, string>,
) {
  const chapterPageId = manualPageByPublicUrl.get(normalizeUrl(parameter.chapterUrl));
  return chapterPageId ? [{ id: chapterPageId }] : [];
}

function propertiesForParameter(
  name: string,
  parameter: ParameterExport,
  citations: Record<string, Citation>,
  manualPageByPublicUrl: Map<string, string>,
  syncedAt: string,
) {
  return {
    Parameter: { title: [{ text: { content: name } }] },
    'Display Name': { rich_text: richText(parameter.displayName) },
    'Formatted Value': { rich_text: richText(parameter.formatted) },
    'Raw Value': { number: Number.isFinite(parameter.value) ? parameter.value : null },
    Unit: { rich_text: richText(parameter.unit) },
    'Source Type': { select: selectValue(parameter.sourceType) },
    Confidence: { select: selectValue(parameter.confidence) },
    Description: { rich_text: richText(parameter.description) },
    Formula: { rich_text: richText(parameter.formula) },
    Inputs: { rich_text: richText((parameter.inputs ?? []).join(', ')) },
    'Compute Expr': { rich_text: richText(parameter.computeExpr) },
    LaTeX: { rich_text: richText(parameter.latex) },
    'Calculation URL': { url: urlValue(parameter.calculationUrl) },
    'Source Ref': { rich_text: richText(parameter.sourceRef) },
    'Source URL': { url: urlValue(parameter.sourceUrl) },
    Citation: { rich_text: richText(citationLabel(parameter.sourceRef, citations)) },
    Distribution: { select: selectValue(parameter.distribution) },
    'Confidence Interval': { rich_text: richText(confidenceIntervalText(parameter)) },
    'Used In': { relation: relationForChapter(parameter, manualPageByPublicUrl) },
    'Chapter URL': { url: urlValue(parameter.chapterUrl) },
    'Last Synced': { date: { start: syncedAt } },
  };
}

async function queryAllDatabasePages(databaseId: string): Promise<any[]> {
  const pages: any[] = [];
  let startCursor: string | undefined;

  do {
    const response = await notion.databases.query({
      database_id: databaseId,
      page_size: 100,
      start_cursor: startCursor,
    });
    pages.push(...response.results);
    startCursor = response.has_more ? response.next_cursor ?? undefined : undefined;
  } while (startCursor);

  return pages;
}

async function loadExistingParameterPages(): Promise<Map<string, ExistingPage>> {
  const pages = await queryAllDatabasePages(parametersDatabaseId);
  const byTitle = new Map<string, ExistingPage>();
  for (const page of pages) {
    const title = titleFromPage(page, 'Parameter');
    if (title) {
      byTitle.set(title, { id: page.id, title });
    }
  }
  return byTitle;
}

async function loadManualPageRelations(): Promise<Map<string, string>> {
  const pages = await queryAllDatabasePages(manualPagesDatabaseId);
  const byPublicUrl = new Map<string, string>();
  for (const page of pages) {
    const publicUrl = urlFromPage(page, 'Public URL');
    if (publicUrl) {
      byPublicUrl.set(normalizeUrl(publicUrl), page.id);
    }
  }
  return byPublicUrl;
}

function loadParametersPayload(): ParametersPayload {
  return JSON.parse(fs.readFileSync(parametersJsonPath, 'utf8')) as ParametersPayload;
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function syncParameters(dryRun: boolean): Promise<void> {
  const payload = loadParametersPayload();
  const existingPages = await loadExistingParameterPages();
  const manualPageByPublicUrl = await loadManualPageRelations();
  const syncedAt = new Date().toISOString();
  const entries = Object.entries(payload.parameters).sort(([a], [b]) => a.localeCompare(b));

  let created = 0;
  let updated = 0;
  let missingManualPage = 0;

  for (const [name, parameter] of entries) {
    const existingPage = existingPages.get(name);
    const properties = propertiesForParameter(
      name,
      parameter,
      payload.citations,
      manualPageByPublicUrl,
      syncedAt,
    );

    if (parameter.chapterUrl && relationForChapter(parameter, manualPageByPublicUrl).length === 0) {
      missingManualPage += 1;
    }

    if (dryRun) {
      if (existingPage) {
        updated += 1;
      } else {
        created += 1;
      }
      continue;
    }

    if (existingPage) {
      await notion.pages.update({
        page_id: existingPage.id,
        properties: properties as any,
      });
      updated += 1;
    } else {
      await notion.pages.create({
        parent: { database_id: parametersDatabaseId },
        properties: properties as any,
      });
      created += 1;
    }

    await sleep(350);
  }

  console.log(
    `Generated parameter sync ${dryRun ? 'dry run' : 'complete'}. ` +
      `rows=${entries.length} create=${created} update=${updated} ` +
      `manual_relation_misses=${missingManualPage}`,
  );
}

const dryRun = process.argv.includes('--dry-run');
await syncParameters(dryRun);
