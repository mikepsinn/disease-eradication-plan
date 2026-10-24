#!/usr/bin/env tsx
/**
 * WISHONIA CLI
 * Command-line interface for the WISHONIA agent system
 */

import "dotenv/config";
import { WISHONIAVoltAgent } from "./wishonia-voltagent";

async function main() {
  const args = process.argv.slice(2);

  const options = {
    full: args.includes("--full"),
    file: args.find((arg) => arg.startsWith("--file="))?.split("=")[1],
    exportTodo: args.includes("--export-todo"),
    status: args.includes("--status"),
    help: args.includes("--help") || args.includes("-h"),
  };

  if (options.help) {
    printHelp();
    process.exit(0);
  }

  console.log("\n🧠 WISHONIA - WISdom and Health Optimization Network Intelligence Agent\n");

  const wishonia = new WISHONIAVoltAgent();
  await wishonia.init();

  try {
    if (options.exportTodo) {
      console.log("📝 Exporting todo list...\n");
      await wishonia.exportTodoList();
    } else if (options.status) {
      await wishonia.printStatus();
    } else if (options.file) {
      console.log(`📄 Processing file: ${options.file}\n`);
      await wishonia.processFile(options.file);
    } else if (options.full) {
      console.log("🔍 Processing all files...\n");
      await wishonia.processAllFiles();
    } else {
      console.log("🔍 Processing stale files (changed since last review)...\n");
      await wishonia.processStaleFiles();
    }

    console.log("\n✅ WISHONIA completed successfully!\n");
  } catch (error: any) {
    console.error("\n❌ WISHONIA encountered an error:");
    console.error(error.message);
    process.exit(1);
  }
}

function printHelp() {
  console.log(`
🧠 WISHONIA - WISdom and Health Optimization Network Intelligence Agent

Usage:
  npm run wishonia                 Process stale files (changed since last review)
  npm run wishonia:full            Process all .qmd files
  npm run wishonia:file -- --file=knowledge/problem/intro.qmd
                                   Process a specific file
  npm run wishonia:todo            Export todo list to JSON/YAML/Markdown
  npm run wishonia:status          Show current status and statistics

Options:
  --full                Process all files (not just stale ones)
  --file=<path>         Process a specific file
  --export-todo         Export todo list
  --status              Show status
  --help, -h            Show this help message

Examples:
  npm run wishonia
  npm run wishonia:full
  npm run wishonia:file -- --file=knowledge/problem/cost-of-war.qmd
  npm run wishonia:status

For more information, see tools/agents/README.md
  `);
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
