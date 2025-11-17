import { writeFile, readFile } from "fs/promises";
import { existsSync } from "fs";
import yaml from "js-yaml";

/**
 * Enhanced Todo interface for WISHONIA
 */
export interface EnhancedTodo {
  id: string;
  type: 'parameter' | 'math' | 'claim' | 'reference' | 'consistency';
  priority: 'critical' | 'high' | 'medium' | 'low';
  filePath: string;
  line: number;
  issue: string;
  suggestedFix?: string;
  confidence: 'high' | 'medium' | 'low';
  status: 'pending' | 'in_progress' | 'fixed' | 'reviewed' | 'rejected';
  dependencies?: string[]; // Other todo IDs this depends on
  agentId?: string; // Which subagent found this
  createdAt: string;
  updatedAt: string;
}

/**
 * Enhanced Todo Manager for WISHONIA
 * Manages todos with export to JSON, YAML, and Markdown
 */
export class EnhancedTodoManager {
  private todos: Map<string, EnhancedTodo> = new Map();
  private filePath: string;

  constructor(filePath: string = '.wishonia-todos.json') {
    this.filePath = filePath;
  }

  /**
   * Add or update a todo
   */
  addTodo(todo: EnhancedTodo): void {
    todo.updatedAt = new Date().toISOString();
    if (!todo.createdAt) {
      todo.createdAt = new Date().toISOString();
    }
    this.todos.set(todo.id, todo);
  }

  /**
   * Get a todo by ID
   */
  getTodo(id: string): EnhancedTodo | undefined {
    return this.todos.get(id);
  }

  /**
   * Get all todos
   */
  getAllTodos(): EnhancedTodo[] {
    return Array.from(this.todos.values());
  }

  /**
   * Get todos by status
   */
  getTodosByStatus(status: EnhancedTodo['status']): EnhancedTodo[] {
    return this.getAllTodos().filter(todo => todo.status === status);
  }

  /**
   * Get todos by type
   */
  getTodosByType(type: EnhancedTodo['type']): EnhancedTodo[] {
    return this.getAllTodos().filter(todo => todo.type === type);
  }

  /**
   * Get todos by priority
   */
  getTodosByPriority(priority: EnhancedTodo['priority']): EnhancedTodo[] {
    return this.getAllTodos().filter(todo => todo.priority === priority);
  }

  /**
   * Update todo status
   */
  updateTodoStatus(id: string, status: EnhancedTodo['status']): boolean {
    const todo = this.todos.get(id);
    if (!todo) return false;
    todo.status = status;
    todo.updatedAt = new Date().toISOString();
    return true;
  }

  /**
   * Remove a todo
   */
  removeTodo(id: string): boolean {
    return this.todos.delete(id);
  }

  /**
   * Export to JSON
   */
  async exportJSON(): Promise<string> {
    const todos = this.getAllTodos();
    return JSON.stringify(todos, null, 2);
  }

  /**
   * Export to YAML
   */
  async exportYAML(): Promise<string> {
    const todos = this.getAllTodos();
    return yaml.dump(todos, { indent: 2 });
  }

  /**
   * Export to Markdown
   */
  async exportMarkdown(): Promise<string> {
    const todos = this.getAllTodos();
    
    // Group by status
    const byStatus = todos.reduce((acc, todo) => {
      if (!acc[todo.status]) acc[todo.status] = [];
      acc[todo.status].push(todo);
      return acc;
    }, {} as Record<string, EnhancedTodo[]>);

    let markdown = '# WISHONIA Todo List\n\n';
    markdown += `**Total Todos:** ${todos.length}\n\n`;

    // Summary by status
    markdown += '## Summary by Status\n\n';
    for (const [status, statusTodos] of Object.entries(byStatus)) {
      markdown += `- **${status}**: ${statusTodos.length}\n`;
    }
    markdown += '\n';

    // Summary by type
    const byType = todos.reduce((acc, todo) => {
      if (!acc[todo.type]) acc[todo.type] = [];
      acc[todo.type].push(todo);
      return acc;
    }, {} as Record<string, EnhancedTodo[]>);

    markdown += '## Summary by Type\n\n';
    for (const [type, typeTodos] of Object.entries(byType)) {
      markdown += `- **${type}**: ${typeTodos.length}\n`;
    }
    markdown += '\n';

    // Detailed list
    markdown += '## Detailed List\n\n';
    for (const [status, statusTodos] of Object.entries(byStatus)) {
      markdown += `### ${status.charAt(0).toUpperCase() + status.slice(1)} (${statusTodos.length})\n\n`;
      
      // Sort by priority
      const sorted = statusTodos.sort((a, b) => {
        const priorityOrder = { critical: 0, high: 1, medium: 2, low: 3 };
        return priorityOrder[a.priority] - priorityOrder[b.priority];
      });

      for (const todo of sorted) {
        markdown += `#### ${todo.id} - ${todo.type} (${todo.priority} priority)\n\n`;
        markdown += `- **File:** \`${todo.filePath}\` (line ${todo.line})\n`;
        markdown += `- **Issue:** ${todo.issue}\n`;
        if (todo.suggestedFix) {
          markdown += `- **Suggested Fix:** ${todo.suggestedFix}\n`;
        }
        markdown += `- **Confidence:** ${todo.confidence}\n`;
        if (todo.agentId) {
          markdown += `- **Found by:** ${todo.agentId}\n`;
        }
        if (todo.dependencies && todo.dependencies.length > 0) {
          markdown += `- **Dependencies:** ${todo.dependencies.join(', ')}\n`;
        }
        markdown += `- **Created:** ${todo.createdAt}\n`;
        markdown += `- **Updated:** ${todo.updatedAt}\n\n`;
      }
    }

    return markdown;
  }

  /**
   * Save todos to file
   */
  async save(): Promise<void> {
    const json = await this.exportJSON();
    await writeFile(this.filePath, json, 'utf-8');
  }

  /**
   * Load todos from file
   */
  async loadFromFile(filePath?: string): Promise<void> {
    const path = filePath || this.filePath;
    if (!existsSync(path)) {
      return; // File doesn't exist yet, start with empty todos
    }

    const content = await readFile(path, 'utf-8');
    const todos = JSON.parse(content) as EnhancedTodo[];
    
    this.todos.clear();
    for (const todo of todos) {
      this.todos.set(todo.id, todo);
    }
  }

  /**
   * Generate a unique ID for a new todo
   */
  generateId(): string {
    const timestamp = Date.now();
    const random = Math.random().toString(36).substring(2, 9);
    return `wishonia-${timestamp}-${random}`;
  }
}

