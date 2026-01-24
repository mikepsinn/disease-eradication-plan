/**
 * CLI Utilities - Common command-line argument parsing
 *
 * Consolidates argument parsing patterns used across scripts.
 */

/**
 * Common CLI options used across image scripts
 */
export interface CommonCliOptions {
  /** Dry run mode - show what would happen without making changes */
  dryRun: boolean
  /** Limit processing to N items */
  limit?: number
  /** Target path/directory */
  path?: string
  /** Process all items (not just unprocessed ones) */
  all: boolean
  /** Force overwrite existing data */
  force: boolean
  /** Show help message */
  help: boolean
}

/**
 * Parse common CLI arguments
 *
 * Recognizes these common flags:
 * - `--dry-run` or `-n`: Don't make changes
 * - `--limit N`: Process only N items
 * - `--path <dir>`: Target directory
 * - `--all` or `-a`: Process all items
 * - `--force` or `-f`: Force overwrite
 * - `--help` or `-h`: Show help
 *
 * @param args - Command line arguments (typically process.argv.slice(2))
 * @returns Parsed common options
 *
 * @example
 * ```ts
 * const { dryRun, limit, path, all } = parseCommonArgs(process.argv.slice(2))
 * if (dryRun) console.log('Dry run mode')
 * ```
 */
export function parseCommonArgs(args: string[]): CommonCliOptions {
  const result: CommonCliOptions = {
    dryRun: false,
    limit: undefined,
    path: undefined,
    all: false,
    force: false,
    help: false,
  }

  for (let i = 0; i < args.length; i++) {
    const arg = args[i]

    switch (arg) {
      case '--dry-run':
      case '-n':
        result.dryRun = true
        break

      case '--all':
      case '-a':
        result.all = true
        break

      case '--force':
      case '-f':
        result.force = true
        break

      case '--help':
      case '-h':
        result.help = true
        break

      case '--limit':
        if (args[i + 1] && !args[i + 1].startsWith('-')) {
          const num = parseInt(args[i + 1], 10)
          if (!isNaN(num) && num > 0) {
            result.limit = num
          }
          i++ // Skip the value
        }
        break

      case '--path':
        if (args[i + 1] && !args[i + 1].startsWith('-')) {
          result.path = args[i + 1]
          i++ // Skip the value
        }
        break
    }
  }

  return result
}

/**
 * Get a named argument value from args array
 *
 * @param args - Command line arguments
 * @param name - Argument name (without --)
 * @param aliases - Alternative names for the argument
 * @returns The value or undefined
 *
 * @example
 * ```ts
 * const search = getArgValue(args, 'search', ['s'])
 * // Matches: --search "text" or -s "text"
 * ```
 */
export function getArgValue(
  args: string[],
  name: string,
  aliases: string[] = []
): string | undefined {
  const flags = [`--${name}`, ...aliases.map(a => (a.length === 1 ? `-${a}` : `--${a}`))]

  for (let i = 0; i < args.length; i++) {
    if (flags.includes(args[i]) && args[i + 1] && !args[i + 1].startsWith('-')) {
      return args[i + 1]
    }
  }

  return undefined
}

/**
 * Check if a flag is present in args
 *
 * @param args - Command line arguments
 * @param name - Flag name (without --)
 * @param aliases - Alternative names for the flag
 * @returns true if flag is present
 *
 * @example
 * ```ts
 * const verbose = hasFlag(args, 'verbose', ['v'])
 * // Matches: --verbose or -v
 * ```
 */
export function hasFlag(args: string[], name: string, aliases: string[] = []): boolean {
  const flags = [`--${name}`, ...aliases.map(a => (a.length === 1 ? `-${a}` : `--${a}`))]
  return args.some(arg => flags.includes(arg))
}

/**
 * Get positional arguments (non-flag arguments)
 *
 * @param args - Command line arguments
 * @returns Array of positional arguments
 *
 * @example
 * ```ts
 * const [inputFile, outputFile] = getPositionalArgs(args)
 * ```
 */
export function getPositionalArgs(args: string[]): string[] {
  const positional: string[] = []
  let skipNext = false

  for (let i = 0; i < args.length; i++) {
    if (skipNext) {
      skipNext = false
      continue
    }

    const arg = args[i]

    if (arg.startsWith('-')) {
      // Check if this flag takes a value
      const nextArg = args[i + 1]
      if (nextArg && !nextArg.startsWith('-')) {
        // Flags that take values
        const valuedFlags = ['--limit', '--path', '--output', '--search', '--replace', '--quality']
        if (valuedFlags.some(f => arg === f || arg.startsWith(f + '='))) {
          skipNext = true
        }
      }
    } else {
      positional.push(arg)
    }
  }

  return positional
}

/**
 * Print a formatted header for CLI output
 */
export function printHeader(title: string, width: number = 60): void {
  console.log(title)
  console.log('='.repeat(width))
}

/**
 * Print a formatted summary section
 */
export function printSummary(stats: Record<string, string | number | boolean>): void {
  console.log('\n' + '='.repeat(60))
  console.log('SUMMARY')
  console.log('='.repeat(60))
  for (const [key, value] of Object.entries(stats)) {
    console.log(`${key}: ${value}`)
  }
}

/**
 * Format options object for display at script start
 */
export function formatOptions(options: Record<string, unknown>): string {
  return Object.entries(options)
    .map(([key, value]) => {
      const displayValue =
        value === undefined ? '(not set)' : value === true ? 'yes' : value === false ? 'no' : value
      return `  ${key}: ${displayValue}`
    })
    .join('\n')
}
