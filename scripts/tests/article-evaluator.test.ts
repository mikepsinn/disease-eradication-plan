import { evaluateArticle } from '../article-evaluator';

const sampleContent = `# Decentralized Clinical Trials

## Overview
Decentralized clinical trials (DCTs) leverage digital technologies and remote monitoring to conduct trials outside traditional clinical settings. This approach increases accessibility, reduces costs, and improves participant diversity.

## Key Benefits
- Broader participant access
- Real-time data collection
- Reduced site visits
- Lower operational costs
- Improved participant retention

## Implementation Challenges
- Data security and privacy
- Technology adoption barriers
- Regulatory compliance
- Protocol standardization

## Future Directions
We need to establish clear guidelines for:
1. Remote consent processes
2. Data validation methods
3. Quality control procedures`;

async function runTest() {
  console.log('Starting article evaluation test...\n');

  try {
    const result = await evaluateArticle(sampleContent, 'test/decentralized-trials.md');
    
    console.log('Evaluation Results:');
    console.log('------------------');
    console.log('Quality Score:', result.qualityScore);
    console.log('\nImprovements Needed:');
    result.improvements.forEach((improvement, i) => {
      console.log(`${i + 1}. ${improvement}`);
    });
    console.log('\nRecommendations:');
    console.log('- Delete:', result.recommendations.shouldDelete);
    if (result.recommendations.shouldRename) {
      console.log('- Rename to:', result.recommendations.shouldRename);
    }
    console.log('- Priority:', result.recommendations.priority);

  } catch (error) {
    console.error('Test failed:', error);
  }
}

// Run the test if this file is executed directly
if (require.main === module) {
  runTest().catch(console.error);
} 