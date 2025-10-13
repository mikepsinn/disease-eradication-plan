'use client';

import { useRouter } from 'next/navigation';
import { useState, useEffect } from 'react';

export default function Home() {
  const router = useRouter();
  const [deathsSinceLoad, setDeathsSinceLoad] = useState(0);
  const [pentagonLost, setPentagonLost] = useState(0);
  const [warDeaths, setWarDeaths] = useState(0);
  const [diseaseDeaths, setDiseaseDeaths] = useState(0);

  useEffect(() => {
    // 150,000 deaths per day = 104 per minute = 1.7 per second
    // Pentagon loses $79,365/second
    // War deaths: 14M/year = 0.44 per second
    // Disease deaths: 55M/year = 1.74 per second
    const interval = setInterval(() => {
      setDeathsSinceLoad(prev => prev + 2);
      setPentagonLost(prev => prev + 79365);
      setWarDeaths(prev => prev + 0.44);
      setDiseaseDeaths(prev => prev + 1.74);
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 py-8 sm:py-12 font-serif">

      {/* Live Death Counter */}
      <div className="mb-8 p-4 border-2 border-red-600 bg-red-50">
        <p className="text-center">
          <span className="font-bold text-red-600 text-2xl">{deathsSinceLoad.toLocaleString()}</span>
          <span className="text-gray-700"> people died from preventable diseases since you loaded this page</span>
        </p>
        <div className="mt-3 flex justify-center gap-8 text-sm">
          <span className="text-gray-600">War: {Math.floor(warDeaths)}</span>
          <span className="text-red-600 font-bold">Disease: {Math.floor(diseaseDeaths)}</span>
        </div>
      </div>

      <h1 className="text-3xl sm:text-5xl font-bold mb-8 leading-tight">
        The Pentagon lost ${(pentagonLost/1000000).toFixed(1)}M while you read this.
      </h1>

      <p className="text-xl sm:text-2xl mb-8 font-bold">
        That could have funded {Math.floor(pentagonLost/500)} patient trials.
      </p>

      {/* The Core Comparison */}
      <div className="mb-12">
        <p className="text-xl font-bold mb-4">What humanity spends money on:</p>

        <div className="space-y-4">
          {/* War Bar */}
          <div>
            <div className="flex justify-between mb-1">
              <span>Killing each other</span>
              <span className="font-bold">$2.7 trillion/year</span>
            </div>
            <div className="w-full bg-black" style={{ height: '60px' }}></div>
          </div>

          {/* Research Bar */}
          <div>
            <div className="flex justify-between mb-1">
              <span>Curing disease</span>
              <span className="font-bold">$68 billion/year</span>
            </div>
            <div className="w-full bg-red-600" style={{ height: '1.5px' }}></div>
            <p className="text-xs text-gray-600 mt-1">↑ Can you see it? That's 40X smaller.</p>
          </div>
        </div>
      </div>

      {/* The Oxford Proof */}
      <div className="bg-green-50 border-2 border-green-600 p-6 mb-8">
        <p className="text-xl font-bold mb-3">✓ This isn't theoretical. Oxford proved it.</p>
        <p className="mb-2">
          2020: Oxford RECOVERY trial tested COVID treatments for <span className="font-bold">$500 per patient</span>.
        </p>
        <p className="mb-2">
          Same time: US trials spent <span className="font-bold">$41,000 per patient</span> on paperwork.
        </p>
        <p className="font-bold text-green-700">
          82X efficiency gain. Already demonstrated. Just needs scaling.
        </p>
      </div>

      {/* The $119T Death Toilet */}
      <div className="border-2 border-black p-4 sm:p-6 mb-8">
        <h2 className="text-2xl sm:text-3xl font-bold mb-4">The $119T Death Toilet</h2>
        <div className="space-y-2 text-base sm:text-lg">
          <div className="flex justify-between gap-2">
            <span className="text-sm sm:text-base">Disease burden (treatment + lost productivity):</span>
            <span className="font-bold">$109.1T</span>
          </div>
          <div className="flex justify-between gap-2">
            <span className="text-sm sm:text-base">War costs (direct + destruction):</span>
            <span className="font-bold">$9.7T</span>
          </div>
          <div className="flex justify-between gap-2 border-t pt-2 mt-2">
            <span className="text-sm sm:text-base">Total annual death toilet:</span>
            <span className="font-bold text-lg sm:text-xl">$118.8T</span>
          </div>
          <div className="flex justify-between gap-2 text-red-600 mt-4">
            <span className="text-sm sm:text-base">Amount spent actually curing disease:</span>
            <span className="font-bold">$0.068T (0.06%)</span>
          </div>
        </div>
      </div>

      {/* Stupid Comparisons */}
      <div className="mb-8">
        <p className="text-xl font-bold mb-3">We spend more on these than curing cancer:</p>
        <ul className="space-y-1 text-lg">
          <li className="hover:bg-yellow-50 p-1 -m-1 transition-colors">• Pet costumes ($490M vs $400M for rare diseases)</li>
          <li className="hover:bg-yellow-50 p-1 -m-1 transition-colors">• Military marching bands ($437M)</li>
          <li className="hover:bg-yellow-50 p-1 -m-1 transition-colors">• Pentagon's coffee budget ($1.2B)</li>
        </ul>
        <p className="text-sm text-gray-600 mt-3 italic">
          One F-35 fighter jet ($80M) = entire childhood leukemia research budget
        </p>
      </div>

      {/* Visual Death Comparison */}
      <div className="mb-8 p-6 border-2 border-black">
        <p className="text-xl font-bold mb-4">Annual Deaths We Accept:</p>
        <div className="space-y-3">
          <div>
            <div className="flex justify-between mb-1">
              <span>Preventable diseases</span>
              <span className="font-bold">55,000,000</span>
            </div>
            <div className="w-full bg-red-600" style={{ height: '55px' }}></div>
          </div>
          <div>
            <div className="flex justify-between mb-1">
              <span>Wars & violence</span>
              <span className="font-bold">14,000,000</span>
            </div>
            <div className="w-full bg-black" style={{ height: '14px' }}></div>
          </div>
          <div>
            <div className="flex justify-between mb-1">
              <span>9/11 attacks</span>
              <span className="font-bold">2,977</span>
            </div>
            <div className="w-full bg-gray-600" style={{ height: '0.5px' }}></div>
            <p className="text-xs text-gray-600 mt-1">↑ Started a 20-year war. Disease kills this many every 30 minutes.</p>
          </div>
        </div>
      </div>

      {/* What $27B Could Actually Buy */}
      <div className="mb-8 p-6 border-2 border-purple-600 bg-purple-50">
        <p className="text-xl font-bold mb-4">What 1% of Military Spending ($27B) Buys:</p>
        <div className="space-y-2">
          <p>• Cure for Alzheimer's (estimated cost: $10B)</p>
          <p>• Cure for Type 1 Diabetes ($5B)</p>
          <p>• Universal cancer vaccine ($8B)</p>
          <p>• Treatment for 95% of rare diseases ($4B)</p>
          <p className="font-bold text-purple-700 mt-3 text-lg">
            Total: Every major disease. One year's budget.
          </p>
        </div>
      </div>

      {/* The 1% Solution */}
      <div className="bg-blue-50 border-2 border-blue-600 p-6 mb-8">
        <h2 className="text-2xl font-bold mb-3">The 1% Treaty (The Smallest Ask Ever)</h2>
        <div className="space-y-2">
          <p>• Take 1% of military spending ($27B)</p>
          <p>• Military keeps 99% (can still end world 66 times)</p>
          <p>• Medical research budget increases 40%</p>
          <p>• With 82X efficiency = 54,000 new trials/year</p>
          <p className="font-bold text-blue-700 mt-3">
            Your specific disease finally gets studied.
          </p>
        </div>
      </div>

      {/* Personal Stakes */}
      <div className="border border-gray-400 p-4 mb-8">
        <p className="font-bold mb-2">Your personal death probability:</p>
        <ul className="space-y-1">
          <li>• Heart disease: 1 in 6 (preventable)</li>
          <li>• Cancer: 1 in 7 (often curable if caught early)</li>
          <li>• Alzheimer's: 1 in 9 if you're over 65</li>
          <li>• Your kid's rare disease: 95% have ZERO treatments</li>
        </ul>
        <p className="font-bold text-red-600 mt-3">
          You will die of something we could have cured for less than we spend on military parades.
        </p>
      </div>

      {/* The Choice */}
      <p className="text-2xl font-bold mb-6 text-center">
        This is the only vote that actually matters:
      </p>

      <div className="space-y-4">
        <button
          onClick={() => router.push('/join')}
          className="block w-full border-4 border-green-600 bg-green-50 p-8 hover:bg-green-100 transition-all hover:scale-[1.02] hover:shadow-lg"
        >
          <span className="text-3xl font-bold">YES TO THE 1% TREATY</span><br/>
          <span className="text-lg">Join 280 million humans choosing cures over corpses →</span>
        </button>

        <button
          onClick={() => router.push('/idiocracy')}
          className="block w-full border-2 border-gray-400 p-4 hover:bg-gray-100 text-gray-600 transition-all hover:scale-[0.98]"
        >
          <span>No thanks, I prefer the current system</span><br/>
          <span className="text-sm">(See where that leads →)</span>
        </button>
      </div>

      {/* Bottom Line */}
      <div className="mt-12 text-center text-gray-600">
        <p className="mb-2">
          <span className="font-bold">3.5% of humanity</span> = unstoppable political force
        </p>
        <p className="mb-2">
          <span className="font-bold">280 million signatures</span> = treaty passes
        </p>
        <p className="font-bold">
          Current signatures: 1,247,892
        </p>
        <p className="text-sm mt-4 italic">
          "They had magic but chose madness." - Earth's epitaph if we fail
        </p>
      </div>
    </div>
  );
}