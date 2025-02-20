const fs = require('fs');
const path = require('path');
const ignore = require('ignore');

function hasMatchingFiles(dir, ig, markdownOnly) {
    try {
        const files = fs.readdirSync(dir);
        
        for (const file of files) {
            const fullPath = path.join(dir, file);
            const relativePath = path.relative(process.cwd(), fullPath);
            
            if (ig.ignores(relativePath)) {
                continue;
            }
            
            const stats = fs.statSync(fullPath);
            
            if (stats.isDirectory()) {
                if (hasMatchingFiles(fullPath, ig, markdownOnly)) {
                    return true;
                }
            } else if (!markdownOnly || file.endsWith('.md')) {
                return true;
            }
        }
    } catch (error) {
        console.error(`Error reading directory ${dir}:`, error);
    }
    
    return false;
}

function generateTree(dir, level = 0, ig, markdownOnly = false) {
    let output = '';
    const files = fs.readdirSync(dir);
    
    // Filter and sort files
    const validFiles = files.filter(file => {
        const relativePath = path.relative(process.cwd(), path.join(dir, file));
        if (ig.ignores(relativePath)) {
            return false;
        }
        
        const stats = fs.statSync(path.join(dir, file));
        const isDirectory = stats.isDirectory();
        
        if (isDirectory) {
            return hasMatchingFiles(path.join(dir, file), ig, markdownOnly);
        }
        
        return !markdownOnly || file.endsWith('.md');
    });
    
    validFiles.forEach((file, index) => {
        const stats = fs.statSync(path.join(dir, file));
        const isDirectory = stats.isDirectory();
        const isLast = index === validFiles.length - 1;
        const prefix = level === 0 ? '' : '│   '.repeat(level - 1) + (isLast ? '└── ' : '├── ');
        
        output += prefix + file + '\n';
        
        if (isDirectory) {
            output += generateTree(path.join(dir, file), level + 1, ig, markdownOnly);
        }
    });
    
    return output;
}

function main() {
    // Parse command line arguments
    const args = process.argv.slice(2);
    const markdownOnly = args.includes('--markdown');
    const outputFile = args.find(arg => arg.startsWith('--output='))?.split('=')[1];
    
    // Read .gitignore if it exists
    let ig = ignore();
    try {
        const gitignore = fs.readFileSync('.gitignore', 'utf8');
        ig = ignore().add(gitignore);
    } catch (error) {
        console.log('No .gitignore found, proceeding without ignore rules');
    }
    
    const header = 'Project Tree Structure:' + (markdownOnly ? ' (Markdown files only)' : '') + '\n\n';
    const tree = generateTree(process.cwd(), 0, ig, markdownOnly);
    const output = header + tree;

    if (outputFile) {
        fs.writeFileSync(outputFile, output);
        console.log(`Tree structure has been saved to ${outputFile}`);
    } else {
        console.log(output);
    }
}

if (require.main === module) {
    main();
}

module.exports = { generateTree }; 