#!/usr/bin/env tsx
/**
 * replace-links-with-citations.ts
 *
 * Replaces inline [text](https://...) hyperlinks in QMD files with [@citation-key]
 * references from references.bib. For URLs not yet in the bib, generates new entries.
 *
 * Usage:
 *   npx tsx scripts/replace-links-with-citations.ts                  # Dry run
 *   npx tsx scripts/replace-links-with-citations.ts --apply          # Apply all changes
 *   npx tsx scripts/replace-links-with-citations.ts --existing-only  # Only replace links with existing bib entries
 */
import fs from 'fs';
import path from 'path';

const ROOT = path.resolve(import.meta.dirname!, '..');
const BIB_PATH = path.join(ROOT, 'references.bib');

const SKIP_DOMAINS = ['warondisease.org', 'dih.earth', 'wishocracy.org'];

const args = process.argv.slice(2);
const APPLY = args.includes('--apply');
const EXISTING_ONLY = args.includes('--existing-only');

// ── URL helpers ──

function normalizeUrl(url: string): string {
  try {
    const u = new URL(url);
    let norm = `${u.protocol}//${u.hostname.toLowerCase()}${u.pathname.replace(/\/+$/, '')}`;
    if (u.search) norm += u.search;
    return norm;
  } catch {
    return url.toLowerCase().replace(/\/+$/, '');
  }
}

function isInternal(url: string): boolean {
  try {
    const h = new URL(url).hostname.toLowerCase();
    return SKIP_DOMAINS.some(d => h === d || h.endsWith(`.${d}`));
  } catch {
    return false;
  }
}

// ── Bib parsing ──

function loadBibUrlMap(): Map<string, string> {
  const content = fs.readFileSync(BIB_PATH, 'utf-8');
  const map = new Map<string, string>();
  let currentKey = '';
  for (const line of content.split('\n')) {
    const km = line.match(/^@\w+\{(.+?),\s*$/);
    if (km) currentKey = km[1].trim();
    const um = line.match(/^\s*url\s*=\s*\{(.+?)\}\s*,?\s*$/);
    if (um && currentKey) map.set(normalizeUrl(um[1]), currentKey);
  }
  return map;
}

function loadBibKeys(): Set<string> {
  const content = fs.readFileSync(BIB_PATH, 'utf-8');
  const keys = new Set<string>();
  for (const m of content.matchAll(/^@\w+\{(.+?),\s*$/gm)) {
    keys.add(m[1].trim());
  }
  return keys;
}

// ── File discovery ──

function findQmdFiles(dir: string): string[] {
  const skip = new Set(['node_modules', '_site', '_book', '_freeze', '.git', '.quarto', '.venv', '_build_temp']);
  const results: string[] = [];
  for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
    if (ent.name.startsWith('.') && ent.name !== '.') continue;
    if (skip.has(ent.name)) continue;
    const full = path.join(dir, ent.name);
    if (ent.isDirectory()) results.push(...findQmdFiles(full));
    else if (ent.name.endsWith('.qmd')) results.push(full);
  }
  return results;
}

// ── Link scanning ──

interface LinkHit {
  file: string;
  line: number;
  match: string;       // [text](url)
  text: string;        // display text
  url: string;
  wrappedInParens: boolean;  // ([text](url))
}

function scanFile(filePath: string): LinkHit[] {
  const content = fs.readFileSync(filePath, 'utf-8');
  const lines = content.split('\n');
  const hits: LinkHit[] = [];
  let inCode = false;

  for (let i = 0; i < lines.length; i++) {
    const ln = lines[i];
    if (ln.trim().startsWith('```')) { inCode = !inCode; continue; }
    if (inCode) continue;

    const re = /\[([^\]]+)\]\((https:\/\/[^)]+)\)/g;
    let m;
    while ((m = re.exec(ln)) !== null) {
      // Skip if inside backtick inline code
      const before = ln.substring(0, m.index);
      if ((before.match(/`/g) || []).length % 2 === 1) continue;

      if (isInternal(m[2])) continue;

      const wrappedInParens = m.index > 0 && ln[m.index - 1] === '(' &&
        m.index + m[0].length < ln.length && ln[m.index + m[0].length] === ')';

      hits.push({
        file: filePath,
        line: i + 1,
        match: m[0],
        text: m[1],
        url: m[2],
        wrappedInParens,
      });
    }
  }
  return hits;
}

// ── Citation key generation ──

/** Display text that is too generic/numeric to derive a good key from */
function isWeakText(text: string): boolean {
  const t = text.trim();
  // Pure numbers, dollar amounts, percentages, dates, measurements
  if (/^[\$\d,.\-%~x+≈<>\s]+$/.test(t)) return true;
  // Numeric with units: "$1.62 billion", "50-500MB", "7.2 years", "~$257 Million / year", "$48-225 million"
  if (/^[~≈<>\\]*\$?\d/.test(t)) return true;
  // Very short or generic words
  if (t.length < 4) return true;
  const generic = ['source', 'here', 'link', 'reacted', 'this', 'study', 'data', 'report'];
  if (generic.includes(t.toLowerCase())) return true;
  return false;
}

/** Slug-ify a string for use as a bib key fragment */
function slugify(s: string): string {
  return s.toLowerCase()
    .replace(/[./]/g, '-')          // dots and slashes to hyphens
    .replace(/[^a-z0-9\s-]/g, '')   // strip other special chars
    .trim()
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .slice(0, 60)
    .replace(/-+$/, '');
}

/** Extract a meaningful key base from the URL structure */
function keyFromUrl(url: string): string {
  const u = new URL(url);
  const host = u.hostname.replace(/^www\./, '').toLowerCase();
  const pathParts = decodeURIComponent(u.pathname).split('/').filter(p => p && p.length > 1);

  // Wikipedia: use article name
  if (host.includes('wikipedia.org')) {
    const article = pathParts[pathParts.length - 1]?.replace(/_/g, '-').toLowerCase() || 'article';
    return `wikipedia-${article}`;
  }

  // PubMed direct
  if (host === 'pubmed.ncbi.nlm.nih.gov') {
    return `pubmed-${pathParts[0] || 'article'}`;
  }

  // PMC articles
  if (host.includes('ncbi.nlm.nih.gov') && u.pathname.includes('/pmc/')) {
    const id = pathParts.find(p => p.startsWith('PMC'));
    return id ? id.toLowerCase() : `ncbi-pmc-${pathParts[pathParts.length - 1] || 'article'}`;
  }

  // NCBI books
  if (host.includes('ncbi.nlm.nih.gov') && u.pathname.includes('/books/')) {
    return `ncbi-${pathParts[pathParts.length - 1] || 'book'}`;
  }

  // NCBI pubmed (old-style /pubmed/ID)
  if (host.includes('ncbi.nlm.nih.gov') && u.pathname.includes('/pubmed/')) {
    const id = pathParts.find(p => /^\d+$/.test(p));
    return id ? `pubmed-${id}` : `ncbi-pubmed`;
  }

  // arXiv
  if (host === 'arxiv.org') {
    return `arxiv-${pathParts[pathParts.length - 1] || 'paper'}`;
  }

  // Nature
  if (host.includes('nature.com')) {
    const slug = pathParts[pathParts.length - 1] || 'article';
    return `nature-${slug}`;
  }

  // NEJM
  if (host.includes('nejm.org')) {
    const slug = pathParts[pathParts.length - 1] || 'article';
    return `nejm-${slug}`;
  }

  // JAMA
  if (host.includes('jamanetwork.com')) {
    const slug = pathParts[pathParts.length - 1] || 'article';
    return `jama-${slug}`;
  }

  // ScienceDirect
  if (host.includes('sciencedirect.com')) {
    const id = pathParts[pathParts.length - 1] || 'article';
    return `sciencedirect-${id}`;
  }

  // FDA
  if (host.includes('fda.gov')) {
    const lastSeg = pathParts[pathParts.length - 1]?.replace(/\.[^.]+$/, '') || 'page';
    return `fda-${slugify(lastSeg)}`;
  }

  // Congress.gov
  if (host === 'congress.gov') {
    return 'congress-gov';
  }

  // GitHub
  if (host === 'github.com') {
    return `github-${pathParts.join('-') || 'repo'}`;
  }

  // LSHTM (London School of Hygiene & Tropical Medicine)
  if (host.includes('lshtm.ac.uk')) {
    const slug = pathParts[pathParts.length - 1] || 'article';
    return `lshtm-${slug}`;
  }

  // Generic: short domain + last meaningful path segment
  const domainParts = host.split('.');
  const domainSlug = domainParts.length > 2
    ? domainParts.slice(-2, -1)[0]  // e.g., "anjusoftware" from "www.anjusoftware.com"
    : domainParts[0];               // e.g., "bio" from "bio.org"
  const lastSeg = pathParts[pathParts.length - 1]
    ?.replace(/\.[^.]+$/, '')
    ?.replace(/[^a-z0-9-]/gi, '-')
    ?.toLowerCase()
    ?.replace(/-+/g, '-')
    ?.slice(0, 40);
  return lastSeg ? `${domainSlug}-${lastSeg}` : domainSlug;
}

/** Get a better title when display text is weak */
function titleFromUrl(url: string): string {
  const u = new URL(url);
  const host = u.hostname.replace(/^www\./, '');
  const pathParts = u.pathname.split('/').filter(p => p && p.length > 1);

  if (host.includes('wikipedia.org')) {
    const article = pathParts[pathParts.length - 1]?.replace(/_/g, ' ');
    return article ? `Wikipedia: ${article}` : host;
  }
  if (host === 'pubmed.ncbi.nlm.nih.gov' || (host.includes('ncbi') && u.pathname.includes('/pubmed/'))) {
    const id = pathParts.find(p => /^\d+$/.test(p));
    return id ? `PubMed ${id}` : 'PubMed article';
  }
  if (host.includes('ncbi.nlm.nih.gov') && u.pathname.includes('/pmc/')) {
    const id = pathParts.find(p => p.startsWith('PMC'));
    return id || 'PMC article';
  }
  if (host === 'arxiv.org') {
    return `arXiv ${pathParts[pathParts.length - 1] || 'paper'}`;
  }

  // Generic: last path segment humanized, URL-decoded
  const lastSeg = decodeURIComponent(pathParts[pathParts.length - 1] || '')
    .replace(/\.[^.]+$/, '')
    .replace(/[-_]/g, ' ');
  if (lastSeg && lastSeg.length > 3) {
    return `${host}: ${lastSeg}`;
  }
  return host;
}

function makeKey(text: string, url: string, existing: Set<string>): string {
  let base: string;

  if (isWeakText(text)) {
    // Display text is a number/generic word; derive key from URL
    base = keyFromUrl(url);
  } else {
    base = slugify(text);
    // If slugify produced something too short, fall back to URL
    if (base.length < 4) {
      base = keyFromUrl(url);
    }
  }

  // Final cleanup
  base = base.replace(/-+/g, '-').replace(/^-|-$/g, '').slice(0, 60);
  if (!base) base = 'source';

  let key = base;
  let n = 2;
  while (existing.has(key)) { key = `${base}-${n++}`; }
  existing.add(key);
  return key;
}

// ── Bib entry builder ──

function buildBibEntry(key: string, url: string, displayText: string): string {
  const today = new Date().toISOString().split('T')[0];
  const title = (isWeakText(displayText) ? titleFromUrl(url) : displayText).replace(/[{}]/g, '');
  const u = new URL(url);
  const host = u.hostname.replace(/^www\./, '').toLowerCase();

  // Determine bib type
  const isArticle = ['pubmed', 'ncbi', 'arxiv', 'nejm', 'nature.com', 'jamanetwork',
    'sciencedirect', 'cochranelibrary', 'lancet'].some(d => host.includes(d));
  const bibType = isArticle ? 'article' : 'misc';

  // Determine author from domain
  let author = '';
  const authorMap: Record<string, string> = {
    'fda.gov': 'U.S. Food and Drug Administration',
    'epa.gov': 'U.S. Environmental Protection Agency',
    'nih.gov': 'National Institutes of Health',
    'ncats.nih.gov': 'National Center for Advancing Translational Sciences',
    'who.int': 'World Health Organization',
    'worldbank.org': 'World Bank',
    'sipri.org': 'SIPRI',
    'unesco.org': 'UNESCO',
    'bls.gov': 'U.S. Bureau of Labor Statistics',
    'cbo.gov': 'Congressional Budget Office',
    'cancer.gov': 'National Cancer Institute',
    'ukri.org': 'UK Research and Innovation',
    'acleddata.com': 'Armed Conflict Location \\& Event Data Project',
    'start.umd.edu': 'National Consortium for the Study of Terrorism',
    'ucdp.uu.se': 'Uppsala Conflict Data Program',
    'recoverytrial.net': 'RECOVERY Collaborative Group',
  };
  for (const [domain, auth] of Object.entries(authorMap)) {
    if (host.includes(domain)) { author = auth; break; }
  }

  const lines = [`@${bibType}{${key},`, `  title = {${title}},`];
  if (author) lines.push(`  author = {${author}},`);
  lines.push(
    `  year = {${new Date().getFullYear()}},`,
    `  url = {${url}},`,
    `  urldate = {${today}}`,
    `}`,
    '',
  );
  return lines.join('\n');
}

// ── Replacement logic ──

interface Action {
  file: string;
  line: number;
  search: string;    // literal string to find in file
  replace: string;   // replacement text
  key: string;
  isNew: boolean;
}

function buildActions(
  hits: LinkHit[],
  bibUrlMap: Map<string, string>,
  allKeys: Set<string>,
): { actions: Action[]; newBibEntries: Map<string, string> } {
  const actions: Action[] = [];
  const newBibEntries = new Map<string, string>();
  const urlToNewKey = new Map<string, string>();

  for (const hit of hits) {
    const norm = normalizeUrl(hit.url);
    let key = bibUrlMap.get(norm);
    let isNew = false;

    if (!key) {
      if (EXISTING_ONLY) continue;

      // Check if we already generated a key for this URL
      key = urlToNewKey.get(norm);
      if (!key) {
        key = makeKey(hit.text, hit.url, allKeys);
        urlToNewKey.set(norm, key);
        newBibEntries.set(key, buildBibEntry(key, hit.url, hit.text));
      }
      isNew = true;
    }

    const replace = hit.wrappedInParens
      ? `[@${key}]`
      : `${hit.text} [@${key}]`;
    const search = hit.wrappedInParens ? `(${hit.match})` : hit.match;

    actions.push({ file: hit.file, line: hit.line, search, replace, key, isNew });
  }

  return { actions, newBibEntries };
}

// ── Apply changes ──

function applyActions(actions: Action[], newBibEntries: Map<string, string>) {
  // Group by file
  const byFile = new Map<string, Action[]>();
  for (const a of actions) {
    if (!byFile.has(a.file)) byFile.set(a.file, []);
    byFile.get(a.file)!.push(a);
  }

  for (const [file, fileActions] of byFile) {
    let content = fs.readFileSync(file, 'utf-8');
    // Sort by search length descending to avoid substring collisions
    fileActions.sort((a, b) => b.search.length - a.search.length);
    for (const a of fileActions) {
      content = content.replace(a.search, a.replace);
    }
    fs.writeFileSync(file, content, 'utf-8');
    console.log(`  Updated: ${path.relative(ROOT, file).replace(/\\/g, '/')}`);
  }

  if (newBibEntries.size > 0) {
    const append = '\n' + [...newBibEntries.values()].join('\n');
    fs.appendFileSync(BIB_PATH, append, 'utf-8');
    console.log(`  Added ${newBibEntries.size} new entries to references.bib`);
  }
}

// ── Main ──

function main() {
  console.log(APPLY ? '=== APPLY MODE ===\n' : '=== DRY RUN (use --apply to apply) ===\n');

  const bibUrlMap = loadBibUrlMap();
  const allKeys = loadBibKeys();
  console.log(`references.bib: ${allKeys.size} entries, ${bibUrlMap.size} with URLs`);

  const qmdFiles = findQmdFiles(ROOT);
  const allHits: LinkHit[] = [];
  for (const f of qmdFiles) allHits.push(...scanFile(f));
  console.log(`QMD files: ${qmdFiles.length} scanned, ${allHits.length} external https links found\n`);

  const { actions, newBibEntries } = buildActions(allHits, bibUrlMap, allKeys);

  const existingActions = actions.filter(a => !a.isNew);
  const newActions = actions.filter(a => a.isNew);

  console.log(`  ${existingActions.length} links match existing bib entries`);
  console.log(`  ${newActions.length} links need new bib entries (${newBibEntries.size} unique URLs)\n`);

  // Report: existing matches
  if (existingActions.length) {
    console.log('--- EXISTING BIB MATCHES ---\n');
    for (const a of existingActions) {
      const rel = path.relative(ROOT, a.file).replace(/\\/g, '/');
      console.log(`  ${rel}:${a.line}  [@${a.key}]`);
      console.log(`    - ${a.search.slice(0, 140)}`);
      console.log(`    + ${a.replace}`);
      console.log();
    }
  }

  // Report: new entries
  if (newActions.length) {
    console.log('--- NEW BIB ENTRIES NEEDED ---\n');
    for (const a of newActions) {
      const rel = path.relative(ROOT, a.file).replace(/\\/g, '/');
      console.log(`  ${rel}:${a.line}  [@${a.key}]`);
      console.log(`    - ${a.search.slice(0, 140)}`);
      console.log(`    + ${a.replace}`);
      console.log();
    }

    console.log('--- GENERATED BIB ENTRIES ---\n');
    for (const [, text] of newBibEntries) {
      console.log(text);
    }
  }

  // Summary
  console.log(`--- SUMMARY ---`);
  console.log(`  Total replacements: ${actions.length}`);
  console.log(`  Existing bib matches: ${existingActions.length}`);
  console.log(`  New bib entries: ${newBibEntries.size}`);

  if (APPLY && actions.length) {
    console.log('\nApplying changes...\n');
    applyActions(actions, newBibEntries);
    console.log(`\nDone! Review with: git diff`);
    if (newBibEntries.size > 0) {
      console.log(`NOTE: ${newBibEntries.size} new bib entries have minimal metadata (title from link text).`);
      console.log(`      Review and improve them in references.bib, then run: npm run sort-references`);
    }
  } else if (!APPLY) {
    console.log(`\nRun with --apply to execute. Or --existing-only --apply for safe mode (existing bib only).`);
  }
}

main();
