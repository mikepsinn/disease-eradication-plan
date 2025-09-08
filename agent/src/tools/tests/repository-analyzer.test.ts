import { repositoryAnalyzerTool } from '../repository-analyzer';
import * as fs from 'fs/promises';
import simpleGit from 'simple-git';
import { glob } from 'glob';
import path from 'path';

jest.mock('fs/promises');
jest.mock('simple-git');
jest.mock('glob');

// Import the function directly to test it, not the whole tool
import { analyzeRepository } from '../repository-analyzer';


describe('analyzeRepository', () => {
  const mockFs = fs as jest.Mocked<typeof fs>;
  const mockSimpleGit = simpleGit as jest.MockedFunction<any>;
  const mockGlob = glob as jest.MockedFunction<typeof glob>;

  beforeEach(() => {
    // Reset mocks before each test
    jest.resetAllMocks();

    // Mock the git log
    mockSimpleGit.mockReturnValue({
      log: jest.fn().mockResolvedValue({
        latest: { date: '2025-09-01T12:00:00.000Z' },
        all: [{ date: '2025-09-01T12:00:00.000Z', message: 'Initial commit' }]
      }),
    });
  });

  it('should analyze the repository and generate a correct health report', async () => {
    // 1. Setup Mock Glob
    mockGlob.mockResolvedValue([
      'CONTRIBUTING.md',
      'good-file.md',
      'bad-file.md',
      'folder/another-file.md',
    ] as any);

    // 2. Setup Mock FS
    // This function will read from our mock-repo directory
    mockFs.readFile.mockImplementation(async (filePath: any) => {
      const relativePath = path.relative(process.cwd(), filePath);
      const mockPath = path.join(__dirname, 'mock-repo', relativePath);
      return fs.readFile(mockPath, 'utf-8');
    });

    // Mock fs.access for link checking
    mockFs.access.mockImplementation(async (filePath: any) => {
      if (filePath.endsWith('non-existent-file.md')) {
        throw new Error('File not found');
      }
      return Promise.resolve();
    });


    // 3. Run the analyzer
    const report = await analyzeRepository();

    // 4. Assertions
    expect(report).toContain('## Repository Health Summary');
    expect(report).toContain('Total Files Analyzed:** 3'); // 3, because it ignores CONTRIBUTING.md

    // Check bad-file.md results
    expect(report).toContain('A File With Problems');
    expect(report).toContain('UPDATE: Missing description in frontmatter');
    expect(report).toContain('UPDATE: Missing date in frontmatter');
    expect(report).toContain('UPDATE: Missing dateCreated in frontmatter');
    expect(report).toContain('REVIEW: "published" flag is missing or false.');
    expect(report).toContain('UPDATE: Contains TODO or FIXME markers');
    expect(report).toContain('FIX: Broken internal link to ./non-existent-file.md');

    // Check good-file.md results (should have no recommendations)
    const goodFileRow = report.split('\n').find((row: string) => row.includes('good-file.md'));
    expect(goodFileRow).toBeDefined();
    // The last column should be empty for a good file
    expect(goodFileRow!.split('|').pop()?.trim()).toBe('');
  });
});
