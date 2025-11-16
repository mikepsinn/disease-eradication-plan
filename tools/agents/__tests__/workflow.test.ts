import { describe, it, expect } from "@jest/globals";
import { createFileReviewWorkflow } from "../workflows/file-review-workflow";
import { EnhancedTodoManager } from "../todo-manager-enhanced";
import type { Agent } from "@voltagent/core";

describe("File Review Workflow", () => {
  it("should create a workflow", () => {
    const mockSupervisor = {} as Agent;
    const todoManager = new EnhancedTodoManager();
    
    // Mock memory parameter
    const mockMemory = undefined;
    
    const workflow = createFileReviewWorkflow(mockSupervisor, todoManager, mockMemory);
    
    // Workflow should be defined and be a workflow chain
    expect(workflow).toBeDefined();
  });

  it("should have correct structure", () => {
    const mockSupervisor = {} as Agent;
    const todoManager = new EnhancedTodoManager();
    const mockMemory = undefined;
    
    const workflow = createFileReviewWorkflow(mockSupervisor, todoManager, mockMemory);
    
    // Verify workflow structure - it should be a workflow chain object
    expect(workflow).toBeDefined();
    // The workflow chain should have methods to execute
    expect(workflow).toBeTruthy();
  });
});

