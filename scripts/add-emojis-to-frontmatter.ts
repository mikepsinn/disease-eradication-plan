#!/usr/bin/env node
/**
 * Add emojis to chapter frontmatter titles based on _quarto.yml structure
 */

import fs from 'fs';
import path from 'path';
import yaml from 'js-yaml';

interface Chapter {
  file: string;
  partTitle: string;
  partEmoji: string;
}

interface Change {
  file: string;
  oldTitle: string;
  newTitle: string;
}

// Extract emoji from start of string
function extractEmoji(text: string): string | null {
  const emojiMatch = text.match(/^([\u{1F300}-\u{1F9FF}]|[\u{2600}-\u{26FF}]|[\u{2700}-\u{27BF}])/u);
  return emojiMatch ? emojiMatch[1] : null;
}

// Check if string starts with an emoji
function hasEmoji(text: string): boolean {
  return extractEmoji(text) !== null;
}

// Personalized emoji mapping for each chapter file
const chapterEmojiMap: Record<string, string> = {
  // Index
  'index.qmd': '🚀',

  // Problem Section
  'brain/book/problem.qmd': '🚨',
  'brain/book/problem/the-daily-massacre.qmd': '💀',
  'brain/book/problem/nih-spent-1-trillion-eradicating-0-diseases.qmd': '🔥',
  'brain/book/problem/fda-is-unsafe-and-ineffective.qmd': '💊',
  'brain/book/problem/cost-of-war.qmd': '⚔️',
  'brain/book/problem/cost-of-disease.qmd': '🏥',
  'brain/book/problem/the-119-trillion-death-toilet.qmd': '🚽',
  'brain/book/problem/unrepresentative-democracy.qmd': '🎭',
  'brain/book/problem/regulatory-capture.qmd': '🎣',
  'brain/book/problem/genetic-slavery.qmd': '🧬',

  // Theory Section
  'brain/book/theory.qmd': '🧠',
  'brain/book/theory/public-choice.qmd': '🗳️',
  'brain/book/theory/central-planning-kills.qmd': '☠️',
  'brain/book/theory/the-two-wars.qmd': '⚔️',

  // Solution Section
  'brain/book/solution.qmd': '💡',
  'brain/book/solution/1-percent-treaty.qmd': '🤝',
  'brain/book/solution/dih.qmd': '🏥',
  'brain/book/solution/wishocracy.qmd': '🌟',
  'brain/book/solution/dfda.qmd': '🔬',
  'brain/book/solution/war-on-disease.qmd': '⚕️',
  'brain/book/solution/global-draft.qmd': '🌍',
  'brain/book/solution/aligning-incentives.qmd': '🎯',

  // Proof/Case Section
  'brain/book/proof.qmd': '✅',
  'brain/book/proof/historical-precedents.qmd': '📜',
  'brain/book/proof/body-as-repairable-machine.qmd': '🔧',

  // Economics
  'brain/book/economics.qmd': '💰',
  'brain/book/economics/victory-bonds.qmd': '🎖️',
  'brain/book/economics/coalition-that-wins.qmd': '🤝',
  'brain/book/economics/economic-impact-summary.qmd': '📊',
  'brain/book/economics/best-idea-in-the-world.qmd': '💎',
  'brain/book/economics/financial-plan.qmd': '📋',
  'brain/book/economics/campaign-budget.qmd': '💵',
  'brain/book/economics/central-banks.qmd': '🏦',
  'brain/book/economics/health-savings-sharing-model.qmd': '💰',

  // Futures
  'brain/book/futures.qmd': '🔮',
  'brain/book/futures/dystopia-skynet-wins.qmd': '🤖',
  'brain/book/futures/utopia-health-and-happiness.qmd': '🌈',

  // Call to Action
  'brain/book/call-to-action/your-personal-benefits.qmd': '🎁',
  'brain/book/call-to-action/every-objection-demolished.qmd': '💥',
  'brain/book/call-to-action/three-actions.qmd': '✊',

  // Legal
  'brain/book/legal.qmd': '⚖️',
  'brain/book/legal/legal-framework.qmd': '🏛️',
  'brain/book/legal/securities-law.qmd': '📜',
  'brain/book/legal/election-law.qmd': '🗳️',
  'brain/book/legal/treaty-framework.qmd': '📝',

  // Strategy
  'brain/book/strategy.qmd': '🎯',
  'brain/book/strategy/global-referendum.qmd': '🌍',
  'brain/book/strategy/five-step-execution.qmd': '🪜',
  'brain/book/strategy/bribe-sequence.qmd': '💸',
  'brain/book/strategy/viral-marketing.qmd': '📱',
  'brain/book/strategy/grassroots-mobilization.qmd': '🌱',
  'brain/book/strategy/diplomatic-approach.qmd': '🤝',
  'brain/book/strategy/co-opting-defense-contractors.qmd': '🛡️',
  'brain/book/strategy/legislation-package.qmd': '📜',

  // Appendix - Essential References
  'brain/book/appendix/faq.qmd': '❓',
  'brain/book/references.qmd': '📚',
  'brain/book/appendix/recovery-trial.qmd': '🏆',
  'brain/book/appendix/historical-evidence-supporting-decentralized-efficacy-trials.qmd': '📊',

  // Appendix - Implementation Strategy
  'brain/book/appendix/1-percent-treaty.qmd': '📄',
  'brain/book/appendix/highest-leverage-advocacy.qmd': '🎯',
  'brain/book/appendix/co-opt-dont-compete.qmd': '🤝',

  // Appendix - Policy & Regulatory
  'brain/book/appendix/right-to-trial-fda-upgrade-act.qmd': '⚖️',
  'brain/book/appendix/hhs-dFDA-policy-recommendations.qmd': '📋',
  'brain/book/appendix/dfda-implementation-via-executive-action.qmd': '✍️',
  'brain/book/appendix/impact-securities-reform.qmd': '💼',

  // Appendix - Economic Analysis
  'brain/book/appendix/total-economic-impact.qmd': '💰',
  'brain/book/appendix/economic-summary.qmd': '📊',
  'brain/book/appendix/humanity-budget-overview.qmd': '🌍',
  'brain/book/appendix/global-government-medical-research-spending.qmd': '💵',

  // Appendix - Detailed Calculations
  'brain/book/appendix/peace-dividend-analysis.qmd': '☮️',
  'brain/book/appendix/1-percent-treaty-peace-dividend-analysis.qmd': '📈',
  'brain/book/appendix/dfda-cost-benefit-analysis.qmd': '⚖️',
  'brain/book/appendix/dfda-roi-breakdown.qmd': '📊',
  'brain/book/appendix/economic-value-of-accelerated-treatments.qmd': '💎',
  'brain/book/appendix/icer-full-calculation.qmd': '🧮',
  'brain/book/appendix/intervention-comparison-table.qmd': '📋',

  // Appendix - Financial Planning
  'brain/book/appendix/dih-market-returns.qmd': '📈',
  'brain/book/appendix/investor-risk-analysis.qmd': '⚠️',
  'brain/book/appendix/fundraising-strategy.qmd': '💰',

  // Appendix - Governance & Organization
  'brain/book/appendix/vision.qmd': '🔭',
  'brain/book/appendix/governance.qmd': '🏛️',
  'brain/book/appendix/organizational-structure.qmd': '🏢',
  'brain/book/appendix/dih-integration-model.qmd': '🔗',
  'brain/book/appendix/open-ecosystem-and-bounty-model.qmd': '🌐',
  'brain/book/appendix/command-and-control-systems.qmd': '🎮',

  // Appendix - Operations & Legal
  'brain/book/appendix/operations-roadmap.qmd': '🗺️',
  'brain/book/appendix/nonprofit-roadmap.qmd': '🛣️',
  'brain/book/appendix/legal-compliance-framework.qmd': '⚖️',
  'brain/book/appendix/dih-seed-grant-proposal-template.qmd': '🌱',
  'brain/book/appendix/recruitment-and-propaganda-plan.qmd': '📢',
  'brain/book/appendix/free-rider-solution.qmd': '🚴',
};

// Get emoji for chapter file
function getEmojiForChapter(filePath: string, partEmoji: string): string {
  // Check if we have a specific emoji for this chapter
  if (chapterEmojiMap[filePath]) {
    return chapterEmojiMap[filePath];
  }

  // Default to part emoji if no specific mapping
  return partEmoji;
}

// Parse _quarto.yml and extract chapters with their parent parts
function parseQuartoYml(quartoPath: string): Chapter[] {
  const content = fs.readFileSync(quartoPath, 'utf-8');
  const config = yaml.load(content) as any;

  const chapters: Chapter[] = [];
  let currentPartTitle = '';
  let currentPartEmoji = '';

  // Process main chapters
  if (config.book?.chapters) {
    for (const item of config.book.chapters) {
      if (item.part) {
        currentPartTitle = item.part;
        currentPartEmoji = extractEmoji(item.part) || '📄';
      } else if (typeof item === 'string' && item.endsWith('.qmd')) {
        chapters.push({
          file: item,
          partTitle: currentPartTitle,
          partEmoji: currentPartEmoji
        });
      } else if (item.href && item.href.endsWith('.qmd')) {
        chapters.push({
          file: item.href,
          partTitle: currentPartTitle,
          partEmoji: currentPartEmoji
        });
      }

      // Process chapters within parts
      if (item.chapters) {
        for (const chapter of item.chapters) {
          if (typeof chapter === 'string' && chapter.endsWith('.qmd')) {
            chapters.push({
              file: chapter,
              partTitle: currentPartTitle,
              partEmoji: currentPartEmoji
            });
          }
        }
      }
    }
  }

  // Process appendices
  if (config.book?.appendices) {
    for (const item of config.book.appendices) {
      if (item.part) {
        currentPartTitle = item.part;
        currentPartEmoji = extractEmoji(item.part) || '📋';
      } else if (typeof item === 'string' && item.endsWith('.qmd')) {
        chapters.push({
          file: item,
          partTitle: currentPartTitle,
          partEmoji: currentPartEmoji
        });
      }

      // Process chapters within parts
      if (item.chapters) {
        for (const chapter of item.chapters) {
          if (typeof chapter === 'string' && chapter.endsWith('.qmd')) {
            chapters.push({
              file: chapter,
              partTitle: currentPartTitle,
              partEmoji: currentPartEmoji
            });
          }
        }
      }
    }
  }

  return chapters;
}

// Extract frontmatter from a .qmd file
function extractFrontmatter(content: string): { frontmatter: any; rest: string } | null {
  // Normalize line endings to \n
  const normalizedContent = content.replace(/\r\n/g, '\n').replace(/\r/g, '\n');

  // Try to match frontmatter with various patterns
  const match = normalizedContent.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!match) {
    // Try without trailing content requirement
    const simpleMatch = normalizedContent.match(/^---\n([\s\S]*?)\n---/);
    if (!simpleMatch) return null;

    try {
      const frontmatter = yaml.load(simpleMatch[1]);
      const rest = normalizedContent.substring(simpleMatch[0].length);
      return { frontmatter, rest };
    } catch (e) {
      return null;
    }
  }

  try {
    const frontmatter = yaml.load(match[1]);
    return { frontmatter, rest: match[2] };
  } catch (e) {
    return null;
  }
}

// Update frontmatter in file content
function updateFrontmatter(content: string, newFrontmatter: any): string {
  // Normalize line endings
  const normalizedContent = content.replace(/\r\n/g, '\n').replace(/\r/g, '\n');

  const match = normalizedContent.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!match) {
    // Try simpler match
    const simpleMatch = normalizedContent.match(/^---\n[\s\S]*?\n---/);
    if (!simpleMatch) return content;

    const rest = normalizedContent.substring(simpleMatch[0].length);
    const newYaml = yaml.dump(newFrontmatter, { lineWidth: -1 });
    return `---\n${newYaml}---${rest}`;
  }

  const newYaml = yaml.dump(newFrontmatter, { lineWidth: -1 });
  return `---\n${newYaml}---\n${match[2]}`;
}

// Main function
async function main() {
  const rootDir = process.cwd();
  const quartoPath = path.join(rootDir, '_quarto.yml');

  console.log('📖 Parsing _quarto.yml...\n');
  const chapters = parseQuartoYml(quartoPath);

  console.log(`Found ${chapters.length} chapters\n`);

  const changes: Change[] = [];
  const skipped: string[] = [];
  const errors: string[] = [];

  // Analyze all files
  for (const chapter of chapters) {
    const filePath = path.join(rootDir, chapter.file);

    if (!fs.existsSync(filePath)) {
      errors.push(`File not found: ${chapter.file}`);
      continue;
    }

    const content = fs.readFileSync(filePath, 'utf-8');
    const parsed = extractFrontmatter(content);

    if (!parsed) {
      errors.push(`Could not parse frontmatter: ${chapter.file}`);
      continue;
    }

    const { frontmatter } = parsed;

    if (!frontmatter.title) {
      errors.push(`No title in frontmatter: ${chapter.file}`);
      continue;
    }

    const currentTitle = frontmatter.title;

    // Skip if already has emoji
    if (hasEmoji(currentTitle)) {
      skipped.push(chapter.file);
      continue;
    }

    // Determine emoji to add
    const emoji = getEmojiForChapter(chapter.file, chapter.partEmoji);
    const newTitle = `${emoji} ${currentTitle}`;

    changes.push({
      file: chapter.file,
      oldTitle: currentTitle,
      newTitle: newTitle
    });
  }

  // Display preview
  console.log('📝 Preview of changes:\n');
  console.log('='.repeat(80));

  for (const change of changes) {
    console.log(`\n${change.file}`);
    console.log(`  - ${change.oldTitle}`);
    console.log(`  + ${change.newTitle}`);
  }

  if (skipped.length > 0) {
    console.log('\n\n✅ Already have emojis (skipped):');
    for (const file of skipped) {
      console.log(`  • ${file}`);
    }
  }

  if (errors.length > 0) {
    console.log('\n\n⚠️  Errors:');
    for (const error of errors) {
      console.log(`  • ${error}`);
    }
  }

  console.log('\n' + '='.repeat(80));
  console.log(`\n📊 Summary:`);
  console.log(`  • ${changes.length} files to update`);
  console.log(`  • ${skipped.length} files already have emojis`);
  console.log(`  • ${errors.length} errors\n`);

  // Ask for confirmation
  const answer = await new Promise<string>((resolve) => {
    process.stdout.write('Apply these changes? (y/n): ');
    process.stdin.once('data', (data) => {
      resolve(data.toString().trim());
    });
  });

  if (answer.toLowerCase() === 'y' || answer.toLowerCase() === 'yes') {
    // Apply changes
    for (const change of changes) {
      const filePath = path.join(rootDir, change.file);
      const content = fs.readFileSync(filePath, 'utf-8');
      const parsed = extractFrontmatter(content);

      if (parsed) {
        parsed.frontmatter.title = change.newTitle;
        const newContent = updateFrontmatter(content, parsed.frontmatter);
        fs.writeFileSync(filePath, newContent, 'utf-8');
      }
    }

    console.log(`\n✅ Updated ${changes.length} files!`);
  } else {
    console.log('\n❌ Cancelled. No files were modified.');
  }

  process.exit(0);
}

main().catch(console.error);
