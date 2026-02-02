#!/usr/bin/env npx tsx
/**
 * Rename Long Images
 * ==================
 *
 * Finds image files with long names, shortens them while preserving style suffixes,
 * and updates all references in QMD/MD files.
 *
 * Usage:
 *   npx tsx scripts/rename-long-images.ts [--dry-run] [--max-length 80] [--interactive]
 *
 * Options:
 *   --dry-run       Show what would be changed without making changes
 *   --max-length N  Maximum filename length before shortening (default: 80)
 *   --interactive   Prompt for each rename (otherwise auto-shortens)
 *   --dir PATH      Specific directory to scan (default: assets/images)
 */

import { readdirSync, renameSync, readFileSync, writeFileSync, statSync, existsSync } from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'
import { createInterface } from 'readline'
import ignore, { Ignore } from 'ignore'
import { VisualStyles } from './lib/image-prompts.js'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

// Style suffixes to preserve (from image-prompts.ts)
const STYLE_SUFFIXES = Object.values(VisualStyles).map(s => s.suffix)

/**
 * Load and parse .gitignore file
 */
function loadGitignore(projectRoot: string): Ignore {
  const ig = ignore()
  const gitignorePath = path.join(projectRoot, '.gitignore')

  if (existsSync(gitignorePath)) {
    const content = readFileSync(gitignorePath, 'utf-8')
    ig.add(content)
  }

  // Always ignore these
  ig.add(['node_modules', '.git', '_book'])

  return ig
}

// Image extensions to process
const IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']

interface RenameEntry {
  oldPath: string
  newPath: string
  oldName: string
  newName: string
  relOldPath: string
  relNewPath: string
}

function findProjectRoot(): string {
  let current = __dirname
  while (current !== path.dirname(current)) {
    if (existsSync(path.join(current, 'package.json')) || existsSync(path.join(current, '_quarto-manual.yml'))) {
      return current
    }
    current = path.dirname(current)
  }
  return process.cwd()
}

/**
 * Extract style suffix from filename
 */
function extractStyleSuffix(filename: string): { base: string; suffix: string; ext: string } | null {
  const ext = path.extname(filename)
  const nameWithoutExt = filename.slice(0, -ext.length)

  for (const suffix of STYLE_SUFFIXES) {
    if (nameWithoutExt.endsWith(suffix)) {
      return {
        base: nameWithoutExt.slice(0, -suffix.length),
        suffix,
        ext,
      }
    }
  }

  // No style suffix found
  return {
    base: nameWithoutExt,
    suffix: '',
    ext,
  }
}

/**
 * Shorten a filename while preserving style suffix
 */
function shortenFilename(filename: string, maxLength: number): string {
  if (filename.length <= maxLength) return filename

  const parsed = extractStyleSuffix(filename)
  if (!parsed) return filename

  const { base, suffix, ext } = parsed
  const reservedLength = suffix.length + ext.length
  const maxBaseLength = maxLength - reservedLength

  if (maxBaseLength < 10) {
    console.warn(`Cannot shorten "${filename}" - suffix and extension too long`)
    return filename
  }

  // Smart shortening: try to keep meaningful parts
  let shortened = base

  // Remove common redundant patterns
  shortened = shortened
    .replace(/-section-/g, '-')  // Remove redundant "section"
    .replace(/--+/g, '-')        // Remove double dashes
    .replace(/-var-[a-z_]+/g, '') // Remove variable references in names

  // If still too long, truncate
  if (shortened.length > maxBaseLength) {
    // Try to truncate at a word boundary
    const truncated = shortened.slice(0, maxBaseLength)
    const lastDash = truncated.lastIndexOf('-')
    if (lastDash > maxBaseLength * 0.6) {
      shortened = truncated.slice(0, lastDash)
    } else {
      shortened = truncated
    }
  }

  // Clean up trailing dashes
  shortened = shortened.replace(/-+$/, '')

  return shortened + suffix + ext
}

/**
 * Find all images with long filenames
 */
function findLongImages(baseDir: string, maxLength: number): { path: string; name: string }[] {
  const results: { path: string; name: string }[] = []

  function walk(dir: string) {
    let entries
    try {
      entries = readdirSync(dir, { withFileTypes: true })
    } catch {
      return
    }

    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name)

      if (entry.isDirectory()) {
        if (!entry.name.startsWith('.') && !entry.name.startsWith('_')) {
          walk(fullPath)
        }
      } else if (entry.isFile()) {
        const ext = path.extname(entry.name).toLowerCase()
        if (IMAGE_EXTENSIONS.includes(ext) && entry.name.length > maxLength) {
          results.push({ path: fullPath, name: entry.name })
        }
      }
    }
  }

  walk(baseDir)
  return results.sort((a, b) => b.name.length - a.name.length) // Longest first
}

/**
 * Find all QMD/MD/JSON files in the project (respects .gitignore)
 */
function findContentFiles(projectRoot: string, ig: Ignore): string[] {
  const results: string[] = []
  const CONTENT_EXTENSIONS = ['.qmd', '.md', '.json', '.yml', '.yaml']

  function walk(dir: string) {
    let entries
    try {
      entries = readdirSync(dir, { withFileTypes: true })
    } catch {
      return
    }

    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name)
      const relPath = path.relative(projectRoot, fullPath).replace(/\\/g, '/')

      // Skip if ignored by .gitignore
      if (ig.ignores(relPath)) {
        continue
      }

      if (entry.isDirectory()) {
        if (!entry.name.startsWith('.')) {
          walk(fullPath)
        }
      } else if (entry.isFile()) {
        const ext = path.extname(entry.name).toLowerCase()
        if (CONTENT_EXTENSIONS.includes(ext)) {
          results.push(fullPath)
        }
      }
    }
  }

  walk(projectRoot)
  return results
}

/**
 * Update references in content files (respects .gitignore)
 */
function updateReferences(
  projectRoot: string,
  renames: RenameEntry[],
  dryRun: boolean,
  ig: Ignore
): number {
  const mdFiles = findContentFiles(projectRoot, ig)
  let filesModified = 0

  for (const mdFile of mdFiles) {
    let content: string
    try {
      content = readFileSync(mdFile, 'utf-8')
    } catch {
      continue
    }

    let modified = content

    for (const rename of renames) {
      // Replace both old filename and old relative path
      const oldFilename = rename.oldName
      const newFilename = rename.newName

      // Simple filename replacement (handles most cases)
      if (modified.includes(oldFilename)) {
        modified = modified.split(oldFilename).join(newFilename)
      }
    }

    if (modified !== content) {
      const relPath = path.relative(projectRoot, mdFile)
      console.log(`  [UPDATE] ${relPath}`)

      if (!dryRun) {
        writeFileSync(mdFile, modified, 'utf-8')
      }
      filesModified++
    }
  }

  return filesModified
}

/**
 * Interactive prompt for user confirmation
 */
async function promptUser(question: string): Promise<string> {
  const rl = createInterface({
    input: process.stdin,
    output: process.stdout,
  })

  return new Promise(resolve => {
    rl.question(question, answer => {
      rl.close()
      resolve(answer.trim().toLowerCase())
    })
  })
}

async function main() {
  const args = process.argv.slice(2)
  const dryRun = args.includes('--dry-run') || args.includes('-n')
  const interactive = args.includes('--interactive') || args.includes('-i')

  // Parse max-length (Windows NTFS max filename is 255, max path is 260)
  let maxLength = 100
  const maxLengthIdx = args.findIndex(a => a === '--max-length' || a === '-m')
  if (maxLengthIdx !== -1 && args[maxLengthIdx + 1]) {
    maxLength = parseInt(args[maxLengthIdx + 1], 10) || 80
  }

  // Parse directory
  let scanDir = 'assets/images'
  const dirIdx = args.findIndex(a => a === '--dir' || a === '-d')
  if (dirIdx !== -1 && args[dirIdx + 1]) {
    scanDir = args[dirIdx + 1]
  }

  const projectRoot = findProjectRoot()
  const imagesDir = path.join(projectRoot, scanDir)
  const ig = loadGitignore(projectRoot)

  console.log('Rename Long Images')
  console.log('==================')
  console.log(`Project root: ${projectRoot}`)
  console.log(`Scanning: ${scanDir}`)
  console.log(`Max length: ${maxLength} characters`)
  console.log(`Mode: ${dryRun ? 'DRY RUN' : 'LIVE'}`)
  console.log(`Respecting .gitignore: yes`)
  console.log()

  // Find long images
  const longImages = findLongImages(imagesDir, maxLength)

  if (longImages.length === 0) {
    console.log('No images with names longer than', maxLength, 'characters found.')
    return 0
  }

  console.log(`Found ${longImages.length} images with names > ${maxLength} characters:\n`)

  // Build rename list
  const renames: RenameEntry[] = []

  for (const img of longImages) {
    const newName = shortenFilename(img.name, maxLength)

    if (newName === img.name) {
      console.log(`  SKIP: ${img.name} (cannot shorten further)`)
      continue
    }

    const newPath = path.join(path.dirname(img.path), newName)
    const relOldPath = path.relative(projectRoot, img.path).replace(/\\/g, '/')
    const relNewPath = path.relative(projectRoot, newPath).replace(/\\/g, '/')

    console.log(`  ${img.name.length} chars: ${img.name}`)
    console.log(`       -> ${newName.length} chars: ${newName}`)
    console.log()

    if (interactive) {
      const answer = await promptUser('  Rename? [y/N/custom name]: ')
      if (answer === 'y' || answer === 'yes') {
        renames.push({
          oldPath: img.path,
          newPath,
          oldName: img.name,
          newName,
          relOldPath,
          relNewPath,
        })
      } else if (answer && answer !== 'n' && answer !== 'no') {
        // Custom name provided
        const customPath = path.join(path.dirname(img.path), answer)
        renames.push({
          oldPath: img.path,
          newPath: customPath,
          oldName: img.name,
          newName: answer,
          relOldPath,
          relNewPath: path.relative(projectRoot, customPath).replace(/\\/g, '/'),
        })
      }
    } else {
      renames.push({
        oldPath: img.path,
        newPath,
        oldName: img.name,
        newName,
        relOldPath,
        relNewPath,
      })
    }
  }

  if (renames.length === 0) {
    console.log('\nNo renames to perform.')
    return 0
  }

  // Perform renames
  console.log('\n' + '='.repeat(60))
  console.log('RENAMING FILES')
  console.log('='.repeat(60))

  for (const rename of renames) {
    console.log(`  ${rename.oldName}`)
    console.log(`  -> ${rename.newName}`)

    if (!dryRun) {
      renameSync(rename.oldPath, rename.newPath)
    }
  }

  console.log(`\nRenamed ${renames.length} files`)

  // Update references
  console.log('\n' + '='.repeat(60))
  console.log('UPDATING REFERENCES IN QMD/MD/JSON/YAML FILES')
  console.log('='.repeat(60))

  const filesModified = updateReferences(projectRoot, renames, dryRun, ig)

  console.log(`\nModified ${filesModified} content files`)

  // Summary
  console.log('\n' + '='.repeat(60))
  if (dryRun) {
    console.log(`DRY RUN: Would rename ${renames.length} files and modify ${filesModified} content files`)
    console.log('\nRun without --dry-run to apply changes.')
  } else {
    console.log(`DONE: Renamed ${renames.length} files and modified ${filesModified} content files`)
  }

  return 0
}

main().catch(err => {
  console.error('Error:', err)
  process.exit(1)
})
