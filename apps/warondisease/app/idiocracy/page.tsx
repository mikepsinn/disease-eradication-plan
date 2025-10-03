'use client';

import { useRouter } from 'next/navigation';
import { useState, useEffect } from 'react';

export default function IdiocracyTimeline() {
  const router = useRouter();
  const [deathCount, setDeathCount] = useState(0);

  // Simulate death counter (13,150 per hour = 3.65 per second)
  useEffect(() => {
    const interval = setInterval(() => {
      setDeathCount(prev => prev + 4);
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-b from-black via-red-950/20 to-black text-white">
      {/* Death counter header */}
      <div className="fixed top-0 left-0 right-0 bg-red-950/50 backdrop-blur-sm border-b border-red-900 z-50">
        <div className="max-w-6xl mx-auto px-4 py-3 flex justify-between items-center">
          <div className="font-mono text-sm">
            <span className="text-red-400">Deaths since you voted NO: </span>
            <span className="text-red-500 font-bold text-lg">{deathCount.toLocaleString()}</span>
          </div>
          <button
            onClick={() => router.push('/wishonia')}
            className="px-6 py-2 bg-green-600 hover:bg-green-700 rounded-full text-sm font-bold transition-all"
          >
            Choose Wishonia Instead →
          </button>
        </div>
      </div>

      {/* Timeline content */}
      <div className="pt-24 pb-20">
        <div className="max-w-4xl mx-auto px-4 space-y-32">
          {/* Intro */}
          <section className="text-center">
            <h1 className="text-7xl font-bold mb-6 text-red-500">The NO Timeline</h1>
            <p className="text-2xl text-gray-300 mb-4">
              You voted to keep military spending unchanged
            </p>
            <p className="text-xl text-gray-400">
              Here's what happens when we choose war over cures...
            </p>
          </section>

          {/* 2028 - Continuation */}
          <section className="relative">
            <div className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-red-600 to-red-900"></div>
            <div className="ml-12">
              <div className="text-red-500 font-mono text-sm mb-2">2028</div>
              <h2 className="text-4xl font-bold mb-4">Nothing Changes</h2>
              <div className="text-gray-300 space-y-4">
                <p className="text-lg">
                  Global military spending hits <span className="text-red-400 font-bold">$9 trillion</span>.
                  Medical research funding stays at <span className="text-yellow-400">$250 billion</span> —
                  barely 3% of what we spend on weapons.
                </p>
                <div className="bg-red-950/30 border border-red-900 rounded-lg p-6 mt-6">
                  <div className="text-2xl font-bold mb-2">📊 Death toll (2028)</div>
                  <ul className="space-y-2 text-gray-400">
                    <li>• Cancer: <span className="text-red-400">10 million deaths</span></li>
                    <li>• Heart disease: <span className="text-red-400">18 million deaths</span></li>
                    <li>• Alzheimer's: <span className="text-red-400">2.5 million deaths</span></li>
                    <li>• Wars & conflicts: <span className="text-red-400">14 million deaths</span></li>
                  </ul>
                  <div className="mt-4 text-red-500 font-bold text-xl">
                    Total: 44.5 million preventable deaths
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* 2035 - Escalation */}
          <section className="relative">
            <div className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-red-700 to-red-950"></div>
            <div className="ml-12">
              <div className="text-red-600 font-mono text-sm mb-2">2035</div>
              <h2 className="text-4xl font-bold mb-4">Spiraling Costs</h2>
              <div className="text-gray-300 space-y-4">
                <p className="text-lg">
                  Military spending accelerates. New AI weapons systems cost <span className="text-red-400 font-bold">$500B</span> annually.
                  Meanwhile, your grandmother dies waiting for an Alzheimer's cure that got <span className="text-yellow-400">$8B/year</span> in funding.
                </p>
                <div className="bg-red-950/30 border border-red-900 rounded-lg p-6 mt-6">
                  <div className="text-2xl font-bold mb-4">💰 The Math</div>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <div className="text-gray-500 mb-1">One B-21 Bomber</div>
                      <div className="text-red-400 font-bold text-2xl">$2.8B</div>
                    </div>
                    <div>
                      <div className="text-gray-500 mb-1">Entire Alzheimer's Budget</div>
                      <div className="text-yellow-400 font-bold text-2xl">$8B</div>
                    </div>
                  </div>
                  <div className="mt-4 text-gray-400 text-sm italic">
                    We could cure Alzheimer's for the cost of 3 bombers.
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* 2040 - Crisis */}
          <section className="relative">
            <div className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-red-800 to-red-950"></div>
            <div className="ml-12">
              <div className="text-red-700 font-mono text-sm mb-2">2040</div>
              <h2 className="text-4xl font-bold mb-4">The Reckoning</h2>
              <div className="text-gray-300 space-y-4">
                <p className="text-lg">
                  Someone you love is dying. They're on a waitlist for a trial that might save them.
                  It's been underfunded for 20 years.
                </p>
                <p className="text-lg">
                  You realize: <span className="text-red-400 font-bold">we chose nuclear submarines over curing children</span>.
                </p>
                <div className="bg-red-950/50 border-2 border-red-800 rounded-lg p-8 mt-6">
                  <div className="text-3xl font-bold mb-4 text-red-500">Cumulative deaths (2025-2040)</div>
                  <div className="text-6xl font-bold text-red-400 mb-4">668 million</div>
                  <div className="text-gray-400 text-lg">
                    Nearly the entire population of Europe. Dead. From diseases we could have cured.
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* 2050 - Extinction trajectory */}
          <section className="relative">
            <div className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-red-900 to-black"></div>
            <div className="ml-12">
              <div className="text-red-900 font-mono text-sm mb-2">2050</div>
              <h2 className="text-4xl font-bold mb-4">The End Game</h2>
              <div className="text-gray-300 space-y-4">
                <p className="text-lg">
                  Climate change accelerates. Pandemics multiply. But we spent our resources on weapons, not resilience.
                </p>
                <p className="text-lg">
                  The technology that could have saved us? <span className="text-red-400">Never funded.</span>
                </p>
                <div className="bg-black border-2 border-red-900 rounded-lg p-8 mt-6 text-center">
                  <div className="text-5xl mb-4">☠️</div>
                  <div className="text-3xl font-bold mb-4">Extinction trajectory locked in</div>
                  <div className="text-gray-400">
                    We had the choice. We chose wrong.
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* CTA - Go back */}
          <section className="text-center py-20">
            <h2 className="text-5xl font-bold mb-6">This Doesn't Have To Happen</h2>
            <p className="text-xl text-gray-400 mb-12 max-w-2xl mx-auto">
              We can choose differently. We can redirect just 1% of military spending and save millions of lives every year.
            </p>
            <div className="space-y-4">
              <button
                onClick={() => router.push('/wishonia')}
                className="block w-full max-w-md mx-auto px-12 py-6 bg-green-600 hover:bg-green-700 text-white rounded-2xl text-2xl font-bold transition-all transform hover:scale-105"
              >
                ✅ See the Wishonia Timeline
              </button>
              <button
                onClick={() => router.push('/')}
                className="block w-full max-w-md mx-auto px-12 py-4 bg-gray-800 hover:bg-gray-700 text-white rounded-2xl text-lg transition-all"
              >
                ← Back to Choice
              </button>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}
