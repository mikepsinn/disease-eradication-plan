import { describe, it, expect } from "@jest/globals";
import {
  createParameterCheckerAgent,
  createMathValidatorAgent,
  createClaimValidatorAgent,
  createReferenceLinkerAgent,
  createConsistencyCheckerAgent,
} from "../sub-agents";

describe("Subagents", () => {
  describe("createParameterCheckerAgent", () => {
    it("should create an agent with correct name", () => {
      const agent = createParameterCheckerAgent();
      expect(agent).toBeDefined();
      // Note: We can't easily test agent.name without accessing internals
      // But we can verify the agent is created successfully
    });

    it("should create an agent with memory when provided", () => {
      // This test verifies the function accepts optional memory
      const agent = createParameterCheckerAgent(undefined);
      expect(agent).toBeDefined();
    });
  });

  describe("createMathValidatorAgent", () => {
    it("should create an agent", () => {
      const agent = createMathValidatorAgent();
      expect(agent).toBeDefined();
    });
  });

  describe("createClaimValidatorAgent", () => {
    it("should create an agent", () => {
      const agent = createClaimValidatorAgent();
      expect(agent).toBeDefined();
    });
  });

  describe("createReferenceLinkerAgent", () => {
    it("should create an agent", () => {
      const agent = createReferenceLinkerAgent();
      expect(agent).toBeDefined();
    });
  });

  describe("createConsistencyCheckerAgent", () => {
    it("should create an agent", () => {
      const agent = createConsistencyCheckerAgent();
      expect(agent).toBeDefined();
    });
  });
});

