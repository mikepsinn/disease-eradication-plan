/**
 * Subagents for WISHONIA Supervisor
 * 
 * These specialized agents work under the WISHONIA supervisor to check files
 * in parallel for different types of issues.
 */

export { createParameterCheckerAgent } from "./parameter-checker";
export { createMathValidatorAgent } from "./math-validator";
export { createClaimValidatorAgent } from "./claim-validator";
export { createReferenceLinkerAgent } from "./reference-linker";
export { createConsistencyCheckerAgent } from "./consistency-checker";

