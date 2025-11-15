#!/usr/bin/env tsx
/**
 * Analyze trials by completion year to get actual annual enrollment numbers
 */

interface EnrollmentInfo {
  count: number;
  type?: string;
}

interface DateStruct {
  date: string; // Format: YYYY-MM-DD
  type?: string;
}

interface StatusModule {
  overallStatus?: string;
  primaryCompletionDateStruct?: DateStruct;
  completionDateStruct?: DateStruct;
}

interface DesignModule {
  studyType?: string;
  phases?: string[];
  enrollmentInfo?: EnrollmentInfo;
}

interface ProtocolSection {
  statusModule?: StatusModule;
  designModule?: DesignModule;
}

interface Study {
  protocolSection?: ProtocolSection;
}

interface ApiResponse {
  studies: Study[];
  nextPageToken?: string;
}

async function fetchCompletedTrials(year: number, pageToken?: string): Promise<ApiResponse> {
  const baseUrl = 'https://clinicaltrials.gov/api/v2/studies';
  const params = new URLSearchParams({
    'filter.overallStatus': 'COMPLETED',
    'pageSize': '1000',
    'format': 'json'
  });

  if (pageToken) params.append('pageToken', pageToken);

  const url = `${baseUrl}?${params}`;
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`API failed: ${response.status}`);
  }

  return await response.json() as ApiResponse;
}

function getCompletionYear(study: Study): number | null {
  const status = study.protocolSection?.statusModule;
  const dateStruct = status?.primaryCompletionDateStruct || status?.completionDateStruct;

  if (!dateStruct?.date) return null;

  const year = parseInt(dateStruct.date.split('-')[0]);
  return isNaN(year) ? null : year;
}

interface YearStats {
  trials: number;
  trialsWithEnrollment: number;
  totalEnrollment: number;
  actualEnrollment: number;
  estimatedEnrollment: number;
  byPhase: Record<string, {
    trials: number;
    enrollment: number;
  }>;
}

async function main() {
  console.log('Analyzing trials by completion year...\n');

  const yearStats: Record<number, YearStats> = {};
  let pageToken: string | undefined;
  let pageCount = 0;
  const maxPages = 200; // Fetch up to 200k completed trials

  console.error('Fetching completed trials...');

  while (pageCount < maxPages) {
    const response = await fetchCompletedTrials(2023, pageToken);

    for (const study of response.studies) {
      const year = getCompletionYear(study);
      if (!year || year < 2020 || year > 2025) continue; // Focus on recent years

      if (!yearStats[year]) {
        yearStats[year] = {
          trials: 0,
          trialsWithEnrollment: 0,
          totalEnrollment: 0,
          actualEnrollment: 0,
          estimatedEnrollment: 0,
          byPhase: {}
        };
      }

      // Skip if not interventional or if no real phases
      const design = study.protocolSection?.designModule;
      if (design?.studyType !== 'INTERVENTIONAL') continue;

      const phases = design?.phases || [];
      const hasRealPhase = phases.some(p => ['PHASE1', 'PHASE2', 'PHASE3', 'PHASE4', 'EARLY_PHASE1'].includes(p));
      if (!hasRealPhase) continue;

      const stats = yearStats[year];
      stats.trials++;

      const enrollment = design?.enrollmentInfo;
      if (enrollment?.count && enrollment.count > 0) {
        stats.trialsWithEnrollment++;
        stats.totalEnrollment += enrollment.count;

        if (enrollment.type === 'ACTUAL') {
          stats.actualEnrollment += enrollment.count;
        } else {
          stats.estimatedEnrollment += enrollment.count;
        }

        // Track by phase
        for (const phase of phases) {
          if (!stats.byPhase[phase]) {
            stats.byPhase[phase] = { trials: 0, enrollment: 0 };
          }
          stats.byPhase[phase].trials++;
          stats.byPhase[phase].enrollment += enrollment.count;
        }
      }
    }

    pageToken = response.nextPageToken;
    pageCount++;
    console.error(`Page ${pageCount}: ${Object.values(yearStats).reduce((sum, s) => sum + s.trials, 0)} total trials`);

    if (!pageToken) break;
    await new Promise(r => setTimeout(r, 100));
  }

  console.log('\n## Trials Completed by Year\n');

  for (const year of [2020, 2021, 2022, 2023, 2024].sort((a, b) => b - a)) {
    const stats = yearStats[year];
    if (!stats) continue;

    console.log(`### ${year}\n`);
    console.log(`- **Trials completed**: ${stats.trials.toLocaleString()}`);
    console.log(`- **Trials with enrollment data**: ${stats.trialsWithEnrollment.toLocaleString()}`);
    console.log(`- **Total enrollment**: ${stats.totalEnrollment.toLocaleString()}`);
    console.log(`  - Actual: ${stats.actualEnrollment.toLocaleString()}`);
    console.log(`  - Estimated: ${stats.estimatedEnrollment.toLocaleString()}`);

    if (Object.keys(stats.byPhase).length > 0) {
      console.log(`- **By phase**:`);
      for (const [phase, data] of Object.entries(stats.byPhase).sort((a, b) => b[1].enrollment - a[1].enrollment)) {
        console.log(`  - ${phase}: ${data.enrollment.toLocaleString()} participants (${data.trials} trials)`);
      }
    }
    console.log('');
  }

  console.log('## Important Notes\n');
  console.log('- This shows trials that COMPLETED in each year (not started)');
  console.log('- Enrollment numbers are from when the trial ran (could be years earlier)');
  console.log('- Some trials span multiple phases (counted in each)');
  console.log('- US-focused data from ClinicalTrials.gov');
  console.log('- For global estimates, scale by ~1.85x (US = 54% of market)');
}

main().catch(console.error);

export {}; // Make this a module to satisfy TypeScript isolatedModules
