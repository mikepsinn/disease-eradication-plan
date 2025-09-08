import { VoltAgent } from '@voltagent/core';
import { executiveDirectorAgent } from './agents';

// This file's purpose is to define and export the agent for the VoltAgent runtime.
// The actual execution of the maintenance task is handled by the `scripts/run-maintenance.ts` script.
export const DIH = new VoltAgent({
  id: 'dih-main-agent',
  agents: {
    executiveDirector: executiveDirectorAgent,
  },
});

