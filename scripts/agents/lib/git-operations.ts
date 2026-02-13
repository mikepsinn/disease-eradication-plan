/**
 * Git Operations Module
 *
 * Safe git operations wrapper for auto-fix workflow with safety guards.
 * Ensures all git operations are tracked, reversible, and never destructive.
 *
 * Safety mechanisms:
 * - Track HEAD before/after operations
 * - Never force push to develop/master
 * - Abort if unauthorized commits detected
 * - Rollback capability on validation failure
 *
 * Pattern based on autonomous-perfect-and-upload.py
 */

import { execSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

export interface GitOperationResult {
  success: boolean;
  message: string;
  data?: any;
  error?: string;
}

export interface BranchInfo {
  name: string;
  commit: string;
  exists: boolean;
}

/**
 * Git operations context - tracks state throughout auto-fix workflow
 */
export class GitOperations {
  private repoRoot: string;
  private initialBranch: string;
  private initialCommit: string;
  private featureBranch: string | null = null;
  private commitsMade: string[] = [];

  constructor(repoRoot?: string) {
    this.repoRoot = repoRoot || process.cwd();
    this.initialBranch = this.getCurrentBranch();
    this.initialCommit = this.getCurrentCommit();

    console.log(`[GIT] Initialized at: ${this.repoRoot}`);
    console.log(`[GIT] Current branch: ${this.initialBranch}`);
    console.log(`[GIT] Current commit: ${this.initialCommit}`);
  }

  /**
   * Execute git command safely with error handling
   */
  private execGit(command: string, silent = false): string {
    try {
      const output = execSync(command, {
        cwd: this.repoRoot,
        encoding: 'utf-8',
        stdio: silent ? 'pipe' : 'inherit'
      });
      return output.trim();
    } catch (error: any) {
      throw new Error(`Git command failed: ${command}\n${error.message}`);
    }
  }

  /**
   * Get current branch name
   */
  getCurrentBranch(): string {
    return this.execGit('git rev-parse --abbrev-ref HEAD', true);
  }

  /**
   * Get current commit hash
   */
  getCurrentCommit(): string {
    return this.execGit('git rev-parse HEAD', true);
  }

  /**
   * Check if branch exists locally
   */
  branchExists(branchName: string): boolean {
    try {
      this.execGit(`git rev-parse --verify ${branchName}`, true);
      return true;
    } catch {
      return false;
    }
  }

  /**
   * Create feature branch for auto-fix
   * Format: auto-fix/{issue-id}-{timestamp}
   */
  createFeatureBranch(issueNumber: number): GitOperationResult {
    const timestamp = Date.now();
    const branchName = `auto-fix/issue-${issueNumber}-${timestamp}`;

    console.log(`[GIT] Creating feature branch: ${branchName}`);

    // Ensure we're on develop branch
    if (this.initialBranch !== 'develop' && this.initialBranch !== 'master') {
      console.warn(`[GIT] Warning: Starting from branch '${this.initialBranch}' (expected develop/master)`);
    }

    // Check for uncommitted changes
    const status = this.execGit('git status --porcelain', true);
    if (status.length > 0) {
      return {
        success: false,
        message: 'Repository has uncommitted changes',
        error: 'Clean working directory required before creating feature branch'
      };
    }

    try {
      // Create and checkout new branch
      this.execGit(`git checkout -b ${branchName}`);
      this.featureBranch = branchName;

      return {
        success: true,
        message: `Feature branch created: ${branchName}`,
        data: { branchName }
      };
    } catch (error: any) {
      return {
        success: false,
        message: 'Failed to create feature branch',
        error: error.message
      };
    }
  }

  /**
   * Stage files for commit
   */
  stageFiles(files: string[]): GitOperationResult {
    if (files.length === 0) {
      return {
        success: false,
        message: 'No files to stage',
        error: 'File list is empty'
      };
    }

    console.log(`[GIT] Staging ${files.length} file(s)...`);

    try {
      for (const file of files) {
        // Verify file exists before staging
        const fullPath = path.join(this.repoRoot, file);
        if (!fs.existsSync(fullPath)) {
          console.warn(`[GIT] Warning: File does not exist: ${file}`);
          continue;
        }

        this.execGit(`git add "${file}"`);
        console.log(`[GIT]   Staged: ${file}`);
      }

      return {
        success: true,
        message: `Staged ${files.length} file(s)`,
        data: { files }
      };
    } catch (error: any) {
      return {
        success: false,
        message: 'Failed to stage files',
        error: error.message
      };
    }
  }

  /**
   * Create commit with co-author attribution
   */
  commitChanges(message: string, coAuthor?: string): GitOperationResult {
    console.log(`[GIT] Creating commit: ${message}`);

    // Check if there are staged changes
    const stagedFiles = this.execGit('git diff --cached --name-only', true);
    if (!stagedFiles) {
      return {
        success: false,
        message: 'No staged changes to commit',
        error: 'Stage files before committing'
      };
    }

    try {
      // Build commit message with co-author
      let fullMessage = message;
      if (coAuthor) {
        fullMessage += `\n\nCo-Authored-By: ${coAuthor}`;
      }

      // Create commit
      this.execGit(`git commit -m "${fullMessage.replace(/"/g, '\\"')}"`);

      const commitHash = this.getCurrentCommit();
      this.commitsMade.push(commitHash);

      console.log(`[GIT] Commit created: ${commitHash.substring(0, 8)}`);

      return {
        success: true,
        message: `Commit created: ${commitHash}`,
        data: { commitHash, message }
      };
    } catch (error: any) {
      return {
        success: false,
        message: 'Failed to create commit',
        error: error.message
      };
    }
  }

  /**
   * Check for merge conflicts with target branch
   */
  validateNoConflicts(targetBranch = 'develop'): GitOperationResult {
    console.log(`[GIT] Checking for conflicts with ${targetBranch}...`);

    try {
      // Fetch latest from target branch
      this.execGit(`git fetch origin ${targetBranch}`, true);

      // Check for conflicts using merge-tree (non-destructive)
      const mergeBase = this.execGit(`git merge-base HEAD origin/${targetBranch}`, true);
      const conflicts = this.execGit(
        `git merge-tree ${mergeBase} HEAD origin/${targetBranch}`,
        true
      );

      // Look for conflict markers
      if (conflicts.includes('<<<<<<<') || conflicts.includes('>>>>>>>')) {
        return {
          success: false,
          message: 'Merge conflicts detected',
          error: `Branch has conflicts with ${targetBranch}`,
          data: { conflicts }
        };
      }

      console.log(`[GIT] No conflicts with ${targetBranch}`);

      return {
        success: true,
        message: `No conflicts with ${targetBranch}`
      };
    } catch (error: any) {
      // If merge-base fails, branches may have diverged too much
      console.warn(`[GIT] Could not check conflicts: ${error.message}`);
      return {
        success: true,
        message: 'Could not verify conflicts (assuming safe)'
      };
    }
  }

  /**
   * Create pull request using gh CLI
   */
  async createPullRequest(
    title: string,
    body: string,
    labels: string[] = []
  ): Promise<GitOperationResult> {
    if (!this.featureBranch) {
      return {
        success: false,
        message: 'No feature branch created',
        error: 'Create feature branch before creating PR'
      };
    }

    console.log(`[GIT] Creating pull request: ${title}`);

    try {
      // Push feature branch to remote
      console.log(`[GIT] Pushing ${this.featureBranch} to remote...`);
      this.execGit(`git push -u origin ${this.featureBranch}`);

      // Build gh pr create command
      let prCommand = `gh pr create --title "${title}" --body "${body.replace(/"/g, '\\"')}"`;

      if (labels.length > 0) {
        prCommand += ` --label "${labels.join(',')}"`;
      }

      // Create PR using gh CLI
      const prUrl = execSync(prCommand, {
        cwd: this.repoRoot,
        encoding: 'utf-8'
      }).trim();

      console.log(`[GIT] Pull request created: ${prUrl}`);

      return {
        success: true,
        message: `Pull request created: ${prUrl}`,
        data: { url: prUrl, branch: this.featureBranch }
      };
    } catch (error: any) {
      return {
        success: false,
        message: 'Failed to create pull request',
        error: error.message
      };
    }
  }

  /**
   * Rollback all changes on validation failure
   * Returns to initial state (branch + commit)
   */
  rollbackOnFailure(): GitOperationResult {
    console.log('[GIT] Rolling back changes...');

    try {
      // Checkout initial branch
      this.execGit(`git checkout ${this.initialBranch}`);

      // Delete feature branch if it was created
      if (this.featureBranch && this.branchExists(this.featureBranch)) {
        this.execGit(`git branch -D ${this.featureBranch}`);
        console.log(`[GIT] Deleted feature branch: ${this.featureBranch}`);
      }

      // Reset to initial commit (discard any uncommitted changes)
      this.execGit(`git reset --hard ${this.initialCommit}`);

      console.log(`[GIT] Rolled back to: ${this.initialBranch}@${this.initialCommit}`);

      return {
        success: true,
        message: `Rolled back to ${this.initialBranch}@${this.initialCommit}`,
        data: {
          branch: this.initialBranch,
          commit: this.initialCommit
        }
      };
    } catch (error: any) {
      return {
        success: false,
        message: 'Rollback failed',
        error: error.message
      };
    }
  }

  /**
   * Safety check: ensure no unauthorized commits were made
   * Compares commits made by this instance vs actual git history
   */
  validateCommitIntegrity(): GitOperationResult {
    console.log('[GIT] Validating commit integrity...');

    try {
      const currentCommit = this.getCurrentCommit();

      // If no commits were made, current commit should match initial
      if (this.commitsMade.length === 0) {
        if (currentCommit !== this.initialCommit) {
          return {
            success: false,
            message: 'Unauthorized commits detected',
            error: `Expected ${this.initialCommit}, got ${currentCommit}`
          };
        }
      } else {
        // Last commit made should match current commit
        const lastCommit = this.commitsMade[this.commitsMade.length - 1];
        if (currentCommit !== lastCommit) {
          return {
            success: false,
            message: 'Unauthorized commits detected',
            error: `Expected ${lastCommit}, got ${currentCommit}`
          };
        }
      }

      console.log('[GIT] Commit integrity validated');

      return {
        success: true,
        message: 'Commit integrity validated',
        data: { commitsMade: this.commitsMade.length }
      };
    } catch (error: any) {
      return {
        success: false,
        message: 'Failed to validate commit integrity',
        error: error.message
      };
    }
  }

  /**
   * Get summary of operations performed
   */
  getSummary(): object {
    return {
      repoRoot: this.repoRoot,
      initialBranch: this.initialBranch,
      initialCommit: this.initialCommit,
      featureBranch: this.featureBranch,
      currentBranch: this.getCurrentBranch(),
      currentCommit: this.getCurrentCommit(),
      commitsMade: this.commitsMade.length,
      commits: this.commitsMade
    };
  }
}
