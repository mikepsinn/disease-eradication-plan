require('dotenv').config();
const fs = require('fs');
const path = require('path');
const { OpenAI } = require('openai');
const openai = new OpenAI(process.env.OPENAI_API_KEY);
const { analyzeFileLocation } = require('./file-path-analyzer');

// Get configuration from environment variables
const OPENAI_MODEL = process.env.OPENAI_MODEL || 'gpt-4'; // Default to gpt-4 if not specified

// Directory structure from reorganize.js
const newStructure = {
  docs: ['architecture', 'governance', 'api', 'getting-started', 'contributing'],
  'clinical-trials': ['protocols', 'methodologies', 'templates', 'validation', 'decentralized-methods'],
  'data-standards': ['schemas', 'ontologies', 'interoperability'],
  analytics: ['models', 'algorithms', 'validation'],
  platform: ['smart-contracts', 'security', 'integration', 'features', 'plugins'],
  regulatory: ['frameworks', 'compliance', 'legal', 'privacy'],
  'knowledge-base': ['interventions', 'conditions', 'biomarkers', 'research-database'],
  community: ['governance', 'partnerships', 'incentives', 'case-studies'],
  technical: ['infrastructure', 'deployment', 'maintenance', 'monitoring'],
  assets: ['images', 'diagrams', 'presentations', 'media'],
  'supporting-materials': ['research-papers', 'white-papers', 'presentations', 'use-cases']
};

// Files and directories to ignore
const ignoreList = [
  '.git',
  'node_modules',
  '.env',
  'package.json',
  'package-lock.json',
  '.gitignore',
  'scripts',
  '.vscode',
  '.idea'
];

// Function to check if path should be ignored
function shouldIgnore(filePath) {
  return ignoreList.some(ignored => filePath.includes(ignored));
}

// Function to get all files recursively
async function getAllFiles(dir) {
  const files = [];
  const items = fs.readdirSync(dir);

  for (const item of items) {
    const fullPath = path.join(dir, item);
    if (shouldIgnore(fullPath)) continue;

    const stat = fs.statSync(fullPath);
    if (stat.isDirectory()) {
      files.push(...await getAllFiles(fullPath));
    } else {
      files.push(fullPath);
    }
  }

  return files;
}

// Function to analyze file content and get suggested location
async function analyzeFile(filePath, content) {
  try {
    return analyzeFileLocation(filePath, content);
  } catch (error) {
    console.error(`