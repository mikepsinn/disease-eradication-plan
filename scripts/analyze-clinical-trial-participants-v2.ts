#!/usr/bin/env tsx
/**
 * Analyze Clinical Trial Participants - Version 2
 *
 * Fetches ALL studies from ClinicalTrials.gov and analyzes them locally
 */

interface EnrollmentInfo {
  count: number;
  type?: string;
}

interface DesignModule {
  studyType?: string;
  phases?: string[];
  enrollmentInfo?: EnrollmentInfo;
}

interface StatusModule {
  overallStatus?: string;
}

interface ProtocolSection {
  designModule?: DesignModule;
  statusModule?: StatusModule;
}

interface Study {
  protocolSection?: ProtocolSection;
}

interface ApiResponse {
  studies: Study[];
  nextPageToken?: string;
  totalCount?: number;
}

interface PhaseStats {
  trialCount: number;
  totalEnrollment: number;
  actualEnrollment: number;
  estimatedEnrollment: number;
  trialsWith EnrollmentData: number;
  median: number;
  p25: number;
  p75: number;
  min: number;
  max: number;
}

async function fetchPage(pageToken?: string): Promise<ApiResponse> {
  const baseUrl = 'https://clinicaltrials.gov/api/v2/studies';
  const params = new URLSearchParams({
    'filter.overallStatus': 'RECRUITING,ACTIVE_NOT_RECRUITING,ENROLLING_BY_INVITATION,COMPLETED',
    'pageSize': '1000',
    'format': 'json'
  });

  if (pageToken) params.append('pageToken', pageToken);

  const url = `${baseUrl}?${params}`;

  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`API failed: ${response.status}`);
  }

  return await response.json();
}

function calculateMedian(arr: number[]): number {
  if (arr.length === 0) return 0;
  const sorted = [...arr].sort((a, b) => a - b);
  const mid = Math.floor(sorted.length / 2);
  return sorted.length % 2 === 0 ? (sorted[mid - 1] + sorted[mid]) / 2 : sorted[mid];
}

function calculatePercentile(arr: number[], p: number): number {
  if (arr.length === 0) return 0;
  const sorted = [...arr].sort((a, b) => a - b);
  const index = Math.ceil((p / 100) * sorted.length) - 1;
  return sorted[Math.max(0, index)];
}

function analyzePhase(studies: Study[], targetPhase: string): PhaseStats {
  const enrollments: number[] = [];
  let actualTotal = 0;
  let estimatedTotal = 0;
  let trialsWithData = 0;

  for (const study of studies) {
    const design = study.protocolSection?.designModule;
    const phases = design?.phases || [];

    if (!phases.includes(targetPhase)) continue;

    const enrollment = design?.enrollmentInfo;
    if (enrollment?.count && enrollment.count > 0) {
      enrollments.push(enrollment.count);
      trialsWithData++;

      if (enrollment.type === 'ACTUAL') {
        actualTotal += enrollment.count;
      } else {
        estimatedTotal += enrollment.count;
      }
    }
  }

  enrollments.sort((a, b) => a - b);

  return {
    trialCount: studies.filter(s => s.protocolSection?.designModule?.phases?.includes(targetPhase)).length,
    totalEnrollment: actualTotal + estimatedTotal,
    actualEnrollment: actualTotal,
    estimatedEnrollment: estimatedTotal,
    trialsWithEnrollmentData: trialsWithData,
    median: calculateMedian(enrollments),
    p25: calculatePercentile(enrollments, 25),
    p75: calculatePercentile(enrollments, 75),
    min: enrollments[0] || 0,
    max: enrollments[enrollments.length - 1] || 0
  };
}

async function main() {
  console.log('# Clinical Trial Participant Analysis\n');
  console.log('Fetching data from ClinicalTrials.gov...\n');

  const allStudies: Study[] = [];
  let pageToken: string | undefined;
  let pageCount = 0;
  const maxPages = 100; // Fetch up to 100k studies

  console.error('Fetching pages...');
  while (pageCount < maxPages) {
    const response = await fetchPage(pageToken);
    allStudies.push(...response.studies);
    pageToken = response.nextPageToken;
    pageCount++;

    console.error(`Page ${pageCount}: ${allStudies.length} total studies`);

    if (!pageToken) break;
    await new Promise(r => setTimeout(r, 100)); // Rate limit
  }

  console.error(`\nFetched ${allStudies.length} studies total\n`);
  console.log(`**Total studies analyzed:** ${allStudies.length.toLocaleString()}\n`);

  const phases = {
    'PHASE1': 'Phase 1',
    'PHASE2': 'Phase 2',
    'PHASE3': 'Phase 3',
    'PHASE4': 'Phase 4'
  };

  let grandTotalEnrollment = 0;
  let grandActualEnrollment = 0;

  for (const [code, name] of Object.entries(phases)) {
    const stats = analyzePhase(allStudies, code);

    console.log(`## ${name}\n`);
    console.log(`- Trials: ${stats.trialCount.toLocaleString()}`);
    console.log(`- Trials with enrollment data: ${stats.trialsWithEnrollmentData.toLocaleString()}`);
    console.log(`- **Total enrollment**: ${stats.totalEnrollment.toLocaleString()}`);
    console.log(`  - Actual: ${stats.actualEnrollment.toLocaleString()}`);
    console.log(`  - Estimated: ${stats.estimatedEnrollment.toLocaleString()}`);
    console.log(`- Median per trial: ${stats.median.toLocaleString()}`);
    console.log(`- 25th-75th percentile: ${stats.p25.toLocaleString()} - ${stats.p75.toLocaleString()}`);
    console.log(`- Range: ${stats.min.toLocaleString()} - ${stats.max.toLocaleString()}`);
    console.log('');

    grandTotalEnrollment += stats.totalEnrollment;
    grandActualEnrollment += stats.actualEnrollment;
  }

  console.log(`## Grand Total\n`);
  console.log(`- **Total enrollment across all phases**: ${grandTotalEnrollment.toLocaleString()}`);
  console.log(`  - Actual: ${grandActualEnrollment.toLocaleString()}`);
  console.log(`  - Estimated: ${(grandTotalEnrollment - grandActualEnrollment).toLocaleString()}`);
  console.log('');

  console.log(`## Important Notes\n`);
  console.log('- This data is from ClinicalTrials.gov (primarily US trials)');
  console.log('- Represents cumulative enrollment, not annual rates');
  console.log('- Only includes trials with status: recruiting, active, enrolling by invitation, or completed');
  console.log('- Some trials may span multiple phases (counted in each)');
  console.log(`- Analysis date: ${new Date().toISOString().split('T')[0]}`);
}

main().catch(console.error);
