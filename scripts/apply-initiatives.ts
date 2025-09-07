import * as fs from 'fs-extra';
import * as path from 'path';
import * as yaml from 'js-yaml';
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';

const ROOT_DIR = path.resolve(__dirname, '..');
const STRATEGIC_INITIATIVES_FILE = path.join(ROOT_DIR, 'operations', 'strategic-initiatives.yml');

interface RefactorAction {
    action: 'MOVE' | 'DELETE';
    path: string;
    details: string;
}

interface StrategicInitiatives {
    refactor_plan?: RefactorAction[];
}

async function main() {
    const argv = await yargs(hideBin(process.argv))
        .option('execute', {
            type: 'boolean',
            description: 'Execute the file operations. Defaults to a dry run.',
            default: false,
        })
        .help()
        .argv;

    const isDryRun = !argv.execute;

    if (isDryRun) {
        console.log('--- DRY RUN ---');
        console.log('No files will be changed. Use --execute to apply changes.');
    } else {
        console.log('--- EXECUTION RUN ---');
        console.log('Applying changes to the file system.');
    }

    if (!await fs.pathExists(STRATEGIC_INITIATIVES_FILE)) {
        console.error(`Error: Strategic initiatives file not found at ${STRATEGIC_INITIATIVES_FILE}`);
        process.exit(1);
    }

    const fileContent = await fs.readFile(STRATEGIC_INITIATIVES_FILE, 'utf-8');
    const initiatives = yaml.load(fileContent) as StrategicInitiatives;

    if (!initiatives.refactor_plan || initiatives.refactor_plan.length === 0) {
        console.log('No refactor actions found in the strategic plan. Exiting.');
        return;
    }
    
    // Process DELETE actions first to avoid conflicts with moves
    const deleteActions = initiatives.refactor_plan.filter(a => a.action === 'DELETE');
    const moveActions = initiatives.refactor_plan.filter(a => a.action === 'MOVE');

    for (const item of deleteActions) {
        const fullPath = path.join(ROOT_DIR, item.path);
        console.log(`[DELETE] ${item.path}`);
        if (!isDryRun) {
            try {
                if (await fs.pathExists(fullPath)) {
                    await fs.remove(fullPath);
                    console.log(`  -> DELETED ${item.path}`);
                } else {
                    console.log(`  -> SKIPPED: File not found at ${item.path}`);
                }
            } catch (error) {
                console.error(`  -> ERROR deleting ${item.path}:`, error);
            }
        }
    }

    for (const item of moveActions) {
        const oldPath = path.join(ROOT_DIR, item.path);
        const newPathRaw = item.details.replace('New location: ', '').trim();
        const newPath = path.join(ROOT_DIR, newPathRaw);

        console.log(`[MOVE] ${item.path} -> ${newPathRaw}`);

        if (!isDryRun) {
            try {
                 if (await fs.pathExists(oldPath)) {
                    await fs.move(oldPath, newPath, { overwrite: true });
                    console.log(`  -> MOVED ${item.path} to ${newPathRaw}`);
                } else {
                    console.log(`  -> SKIPPED: Source file not found at ${item.path}`);
                }
            } catch (error) {
                console.error(`  -> ERROR moving ${item.path}:`, error);
            }
        }
    }
    
    console.log('\nRefactor process completed.');
    if (isDryRun) {
        console.log('--- End of DRY RUN ---');
    }
}

main().catch(error => {
    console.error('A fatal error occurred:', error);
    process.exit(1);
});
