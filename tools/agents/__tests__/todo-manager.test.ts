import { describe, it, expect, beforeEach, afterEach } from "@jest/globals";
import { EnhancedTodoManager, type EnhancedTodo } from "../todo-manager-enhanced";
import { writeFile, readFile, unlink } from "fs/promises";
import { existsSync } from "fs";

describe("EnhancedTodoManager", () => {
  let manager: EnhancedTodoManager;
  const testFilePath = ".test-wishonia-todos.json";

  beforeEach(() => {
    manager = new EnhancedTodoManager(testFilePath);
  });

  afterEach(async () => {
    if (existsSync(testFilePath)) {
      await unlink(testFilePath);
    }
  });

  describe("addTodo", () => {
    it("should add a todo with generated ID", () => {
      const todo: EnhancedTodo = {
        id: manager.generateId(),
        type: "parameter",
        priority: "high",
        filePath: "test.qmd",
        line: 10,
        issue: "Hardcoded number found",
        confidence: "high",
        status: "pending",
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };

      manager.addTodo(todo);
      const retrieved = manager.getTodo(todo.id);

      expect(retrieved).toBeDefined();
      expect(retrieved?.id).toBe(todo.id);
      expect(retrieved?.issue).toBe("Hardcoded number found");
    });

    it("should update existing todo", () => {
      const todo: EnhancedTodo = {
        id: manager.generateId(),
        type: "parameter",
        priority: "high",
        filePath: "test.qmd",
        line: 10,
        issue: "Hardcoded number found",
        confidence: "high",
        status: "pending",
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };

      manager.addTodo(todo);
      const updatedTodo = { ...todo, status: "fixed" as const };
      manager.addTodo(updatedTodo);

      const retrieved = manager.getTodo(todo.id);
      expect(retrieved?.status).toBe("fixed");
    });
  });

  describe("getTodosByStatus", () => {
    it("should filter todos by status", () => {
      const todo1: EnhancedTodo = {
        id: manager.generateId(),
        type: "parameter",
        priority: "high",
        filePath: "test1.qmd",
        line: 10,
        issue: "Issue 1",
        confidence: "high",
        status: "pending",
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };

      const todo2: EnhancedTodo = {
        id: manager.generateId(),
        type: "math",
        priority: "medium",
        filePath: "test2.qmd",
        line: 20,
        issue: "Issue 2",
        confidence: "medium",
        status: "fixed",
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };

      manager.addTodo(todo1);
      manager.addTodo(todo2);

      const pending = manager.getTodosByStatus("pending");
      const fixed = manager.getTodosByStatus("fixed");

      expect(pending).toHaveLength(1);
      expect(pending[0].id).toBe(todo1.id);
      expect(fixed).toHaveLength(1);
      expect(fixed[0].id).toBe(todo2.id);
    });
  });

  describe("getTodosByType", () => {
    it("should filter todos by type", () => {
      const todo1: EnhancedTodo = {
        id: manager.generateId(),
        type: "parameter",
        priority: "high",
        filePath: "test1.qmd",
        line: 10,
        issue: "Issue 1",
        confidence: "high",
        status: "pending",
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };

      const todo2: EnhancedTodo = {
        id: manager.generateId(),
        type: "math",
        priority: "medium",
        filePath: "test2.qmd",
        line: 20,
        issue: "Issue 2",
        confidence: "medium",
        status: "pending",
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };

      manager.addTodo(todo1);
      manager.addTodo(todo2);

      const parameterTodos = manager.getTodosByType("parameter");
      const mathTodos = manager.getTodosByType("math");

      expect(parameterTodos).toHaveLength(1);
      expect(parameterTodos[0].id).toBe(todo1.id);
      expect(mathTodos).toHaveLength(1);
      expect(mathTodos[0].id).toBe(todo2.id);
    });
  });

  describe("updateTodoStatus", () => {
    it("should update todo status", () => {
      const todo: EnhancedTodo = {
        id: manager.generateId(),
        type: "parameter",
        priority: "high",
        filePath: "test.qmd",
        line: 10,
        issue: "Issue",
        confidence: "high",
        status: "pending",
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };

      manager.addTodo(todo);
      const updated = manager.updateTodoStatus(todo.id, "fixed");

      expect(updated).toBe(true);
      expect(manager.getTodo(todo.id)?.status).toBe("fixed");
    });

    it("should return false for non-existent todo", () => {
      const updated = manager.updateTodoStatus("non-existent", "fixed");
      expect(updated).toBe(false);
    });
  });

  describe("exportJSON", () => {
    it("should export todos as JSON", async () => {
      const todo: EnhancedTodo = {
        id: manager.generateId(),
        type: "parameter",
        priority: "high",
        filePath: "test.qmd",
        line: 10,
        issue: "Issue",
        confidence: "high",
        status: "pending",
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };

      manager.addTodo(todo);
      const json = await manager.exportJSON();
      const parsed = JSON.parse(json);

      expect(Array.isArray(parsed)).toBe(true);
      expect(parsed).toHaveLength(1);
      expect(parsed[0].id).toBe(todo.id);
    });
  });

  describe("exportMarkdown", () => {
    it("should export todos as Markdown", async () => {
      const todo: EnhancedTodo = {
        id: manager.generateId(),
        type: "parameter",
        priority: "high",
        filePath: "test.qmd",
        line: 10,
        issue: "Issue",
        confidence: "high",
        status: "pending",
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };

      manager.addTodo(todo);
      const markdown = await manager.exportMarkdown();

      expect(markdown).toContain("# WISHONIA Todo List");
      expect(markdown).toContain("Total Todos: 1");
      expect(markdown).toContain(todo.id);
      expect(markdown).toContain(todo.issue);
    });
  });

  describe("save and loadFromFile", () => {
    it("should save and load todos from file", async () => {
      const todo: EnhancedTodo = {
        id: manager.generateId(),
        type: "parameter",
        priority: "high",
        filePath: "test.qmd",
        line: 10,
        issue: "Issue",
        confidence: "high",
        status: "pending",
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };

      manager.addTodo(todo);
      await manager.save();

      const newManager = new EnhancedTodoManager(testFilePath);
      await newManager.loadFromFile();

      const loaded = newManager.getTodo(todo.id);
      expect(loaded).toBeDefined();
      expect(loaded?.id).toBe(todo.id);
      expect(loaded?.issue).toBe(todo.issue);
    });
  });

  describe("generateId", () => {
    it("should generate unique IDs", () => {
      const id1 = manager.generateId();
      const id2 = manager.generateId();

      expect(id1).not.toBe(id2);
      expect(id1).toMatch(/^wishonia-\d+-[a-z0-9]+$/);
    });
  });
});

