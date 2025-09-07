import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';
import { marked } from 'marked';

const ROOT_DIR = path.resolve(__dirname, '..');
const OUTPUT_FILE = path.join(ROOT_DIR, 'operations', 'project-state.yml');
const PHASE_PLAN_FILE = path.join(ROOT_DIR, 'operations', 'phase-0-plan.md');
const HEALTH_REPORT_FILE = path.join(ROOT_DIR, 'operations', 'wiki-health-report.yml');

// Helper to parse markdown table
function parseMarkdownTable(tokens: any[]) {
    const tableToken = tokens.find((token: any) => token.type === 'table');
    if (!tableToken) return [];

    const tasks: any[] = [];
    const headers = tableToken.header.map((h: any) => h.text.toLowerCase().replace(/\s+/g, '_'));

    tableToken.rows.forEach((row: any) => {
        const task: any = {};
        let isStreamHeader = false;
        row.forEach((cell: any, index: number) => {
            const header = headers[index];
            if (header === 'task' && cell.text.startsWith('**') && cell.text.endsWith('**')) {
                isStreamHeader = true;
            }
            task[header] = cell.text.replace(/\*\*/g, '').trim();
        });
        if (!isStreamHeader) {
            tasks.push(task);
        }
    });

    return tasks;
}


// Main compilation logic
async function compileProjectState() {
    const projectState: any = {
        '#': 'This is the single source of truth for the project\'s state. It is a living document, updated by both humans and AI agents.',
        phases: [],
        wiki_health: {}
    };

    // 1. Parse Phase Plan Markdown
    if (fs.existsSync(PHASE_PLAN_FILE)) {
        const markdownContent = await fs.promises.readFile(PHASE_PLAN_FILE, 'utf-8');
        const tokens = marked.lexer(markdownContent);
        
        const phaseTasks = parseMarkdownTable(tokens);
        
        // This is a simplified parser; assumes one phase per file for now
        projectState.phases.push({
            phase: 0,
            name: 'Pre-Seed & Foundation',
            goal: 'Establish the core legal and financial structure and hire the "activation team" required to execute the main capital raise and global campaign.',
            timeline: 'Months 0-3',
            tasks: phaseTasks,
        });
    }

    // 2. Parse Wiki Health Report YAML
    if (fs.existsSync(HEALTH_REPORT_FILE)) {
        const healthReportContent = await fs.promises.readFile(HEALTH_REPORT_FILE, 'utf-8');
        const healthReport = yaml.load(healthReportContent) as any;

        for (const filePath in healthReport) {
            const report = healthReport[filePath];
            projectState.wiki_health[filePath] = {
                quality_score: report.assessment.qualityScore,
                priority: report.assessment.recommendations.priority,
                last_evaluated: new Date(report.timestamp).toISOString(),
                actionable_tasks: report.assessment.todos.map((todo: string) => 
                    todo.replace(/<!-- TODO: (.*?) -->/, '$1').trim()
                )
            };
        }
    }

    // 3. Write the unified state file
    const yamlState = yaml.dump(projectState, { indent: 2 });
    await fs.promises.writeFile(OUTPUT_FILE, yamlState);

    console.log(`Project state successfully compiled into: ${OUTPUT_FILE}`);
}

// Make the script executable
if (require.main === module) {
    compileProjectState().catch(console.error);
}
