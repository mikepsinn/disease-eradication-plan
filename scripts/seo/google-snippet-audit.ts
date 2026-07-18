/**
 * Google snippet audit.
 *
 * For every page in the live sitemap, fetch the page's <title> and meta
 * description, ask Google (via Serper.dev) what it actually displays for a
 * title query, and flag pages where Google overrides the meta description
 * with extracted body text. For overridden pages, locates the body sentence
 * Google chose so it can be rewritten.
 *
 * Usage:
 *   npx tsx scripts/seo/google-snippet-audit.ts [--filter=knowledge/strategy] [--limit=20] [--out=snippet-audit-report.md]
 *
 * Requires SERPER_API_KEY in .env or the environment.
 * Free key (2,500 searches): https://serper.dev
 */
import { existsSync, readFileSync, writeFileSync } from 'node:fs'

if (existsSync('.env')) {
  for (const line of readFileSync('.env', 'utf8').split(/\r?\n/)) {
    const m = line.match(/^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)\s*$/)
    if (m && !(m[1] in process.env)) process.env[m[1]] = m[2].replace(/^["']|["']$/g, '')
  }
}

const SITE = 'manual.warondisease.org'
const SITEMAP_URL = `https://${SITE}/sitemap.xml`
const API_KEY = process.env.SERPER_API_KEY

const args: Record<string, string> = Object.fromEntries(
  process.argv
    .slice(2)
    .filter((a) => a.startsWith('--'))
    .map((a) => {
      const [k, ...v] = a.replace(/^--/, '').split('=')
      return [k, v.join('=') || 'true']
    })
)

if (!API_KEY) {
  console.error('SERPER_API_KEY is not set.')
  console.error('1. Create a free account at https://serper.dev (2,500 free searches).')
  console.error('2. Add SERPER_API_KEY=... to .env and rerun.')
  process.exit(1)
}

const decode = (s: string) =>
  s
    .replace(/&amp;/g, '&')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&nbsp;/g, ' ')

const stripHtml = (html: string) =>
  decode(
    html
      .replace(/<script[\s\S]*?<\/script>/gi, ' ')
      .replace(/<style[\s\S]*?<\/style>/gi, ' ')
      .replace(/<[^>]+>/g, ' ')
  )

const norm = (s: string) => s.toLowerCase().replace(/[“”"']/g, '').replace(/\s+/g, ' ').trim()

const canonPath = (url: string) =>
  new URL(url)
    .pathname.toLowerCase()
    .replace(/\/index\.html$/, '')
    .replace(/\.html$/, '')
    .replace(/\/$/, '') || '/'

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms))

interface PageResult {
  url: string
  path: string
  verdict: string
  query?: string
  pageTitle?: string
  metaDesc?: string
  googleTitle?: string
  googleSnippet?: string
  snippetSource?: string[]
  note?: string
}

const sitemapRes = await fetch(SITEMAP_URL)
if (!sitemapRes.ok) {
  console.error(`Sitemap fetch failed: HTTP ${sitemapRes.status}`)
  process.exit(1)
}
const xml = await sitemapRes.text()
let urls = [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1].trim())
if (args.filter) urls = urls.filter((u) => u.toLowerCase().includes(args.filter.toLowerCase()))
if (args.limit) urls = urls.slice(0, Number(args.limit))
console.log(`Auditing ${urls.length} pages from ${SITEMAP_URL}\n`)

const results: PageResult[] = []

for (const [i, url] of urls.entries()) {
  const path = canonPath(url)
  const pageRes = await fetch(url)
  if (!pageRes.ok) {
    results.push({ url, path, verdict: 'FETCH_FAILED', note: `HTTP ${pageRes.status}` })
    console.log(`[${i + 1}/${urls.length}] FETCH_FAILED       ${path}`)
    continue
  }
  const html = await pageRes.text()
  const pageTitle = decode((html.match(/<title[^>]*>([\s\S]*?)<\/title>/i)?.[1] ?? '').trim())
  const metaDesc = decode(
    html.match(/<meta\s+name="description"\s+content="([^"]*)"/i)?.[1] ??
      html.match(/<meta\s+content="([^"]*)"\s+name="description"/i)?.[1] ??
      ''
  )
  const titleCore = pageTitle.split(/\s+[–—|]\s+/)[0].trim()
  const query = `site:${SITE} ${titleCore}`

  const serperRes = await fetch('https://google.serper.dev/search', {
    method: 'POST',
    headers: { 'X-API-KEY': API_KEY, 'Content-Type': 'application/json' },
    body: JSON.stringify({ q: query, num: 10, gl: 'us', hl: 'en' }),
  })
  if (!serperRes.ok) {
    console.error(`Serper error ${serperRes.status}: ${await serperRes.text()}`)
    process.exit(1)
  }
  const data = await serperRes.json()
  const organic: Array<{ title: string; link: string; snippet?: string }> = data.organic ?? []
  const hit = organic.find((o) => canonPath(o.link) === path)

  let verdict: string
  let snippetSource: string[] | undefined
  if (!hit) {
    verdict = 'NOT_IN_RESULTS'
  } else if (!metaDesc) {
    verdict = 'NO_META_DESCRIPTION'
  } else if (!hit.snippet) {
    verdict = 'NO_SNIPPET'
  } else {
    const d = norm(metaDesc)
    const s = norm(hit.snippet.replace(/^[.…\s]+|[.…\s]+$/g, ''))
    const usesMeta = d.includes(s.slice(0, 80)) || s.includes(d.slice(0, 80))
    verdict = usesMeta ? 'USES_META' : 'OVERRIDDEN'
    if (verdict === 'OVERRIDDEN') {
      const body = norm(stripHtml(html))
      snippetSource = hit.snippet
        .split(/\.{3}|…/)
        .map((f) => norm(f))
        .filter((f) => f.length >= 15)
        .map((f) => {
          const idx = body.indexOf(f.slice(0, 60))
          return idx >= 0 ? `...${body.slice(Math.max(0, idx - 60), idx + 180)}...` : `(not located in body: "${f.slice(0, 60)}")`
        })
    }
  }

  results.push({
    url,
    path,
    verdict,
    query,
    pageTitle,
    metaDesc,
    googleTitle: hit?.title,
    googleSnippet: hit?.snippet,
    snippetSource,
  })
  console.log(`[${i + 1}/${urls.length}] ${verdict.padEnd(18)} ${path}`)
  await sleep(350)
}

const by = (v: string) => results.filter((r) => r.verdict === v)
const overridden = by('OVERRIDDEN')
const noMeta = by('NO_META_DESCRIPTION')
const notInResults = by('NOT_IN_RESULTS')
const usesMeta = by('USES_META')
const other = results.filter((r) => !['OVERRIDDEN', 'NO_META_DESCRIPTION', 'NOT_IN_RESULTS', 'USES_META'].includes(r.verdict))

const lines: string[] = []
lines.push(`# Google Snippet Audit`)
lines.push(``)
lines.push(`Generated: ${new Date().toISOString()} | Pages: ${results.length}`)
lines.push(``)
lines.push(
  `| Verdict | Count | Meaning |\n|---|---:|---|\n| OVERRIDDEN | ${overridden.length} | Google ignored your meta description and extracted body text |\n| NO_META_DESCRIPTION | ${noMeta.length} | Page ships no meta description at all |\n| NOT_IN_RESULTS | ${notInResults.length} | Page did not appear for a site: title query (indexing problem or weak title) |\n| USES_META | ${usesMeta.length} | Google shows your meta description (good) |\n| other | ${other.length} | fetch failures / empty snippets |`
)

if (overridden.length) {
  lines.push(``, `## Overridden (fix these: rewrite the extracted body sentence or the description)`)
  for (const r of overridden) {
    lines.push(``, `### ${r.path}`)
    lines.push(`- Query: \`${r.query}\``)
    lines.push(`- Google shows: "${r.googleSnippet}"`)
    lines.push(`- Your meta description: "${r.metaDesc}"`)
    if (r.snippetSource?.length) {
      lines.push(`- Extracted from body near:`)
      for (const s of r.snippetSource) lines.push(`  - ${s}`)
    }
  }
}
if (noMeta.length) {
  lines.push(``, `## No meta description`)
  for (const r of noMeta) lines.push(`- ${r.path} (Google shows: "${r.googleSnippet ?? ''}")`)
}
if (notInResults.length) {
  lines.push(``, `## Not in results for title query`)
  for (const r of notInResults) lines.push(`- ${r.path} (query: \`${r.query}\`)`)
}
if (other.length) {
  lines.push(``, `## Other`)
  for (const r of other) lines.push(`- ${r.path}: ${r.verdict} ${r.note ?? ''}`)
}
lines.push(``, `## Using meta description (no action needed)`)
for (const r of usesMeta) lines.push(`- ${r.path}`)
lines.push(``)

const outPath = args.out ?? 'snippet-audit-report.md'
writeFileSync(outPath, lines.join('\n'), 'utf8')
console.log(`\nDone. ${overridden.length} overridden, ${noMeta.length} missing descriptions, ${notInResults.length} not found.`)
console.log(`Report: ${outPath}`)
