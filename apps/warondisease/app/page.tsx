'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function Home() {
  const [hoveredChoice, setHoveredChoice] = useState<'yes' | 'no' | null>(null);
  const router = useRouter();

  return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center justify-center relative overflow-hidden">
      {/* Background gradient effect */}
      <div className="absolute inset-0 bg-gradient-to-b from-red-950/20 via-black to-black" />

      {/* Main content */}
      <div className="relative z-10 max-w-6xl mx-auto px-4 text-center">
        {/* Death counter */}
        <div className="mb-8 text-red-500 font-mono text-sm">
          <span className="opacity-70">Deaths while you decide: </span>
          <span className="font-bold">~13,150</span>
          <span className="opacity-70"> per hour</span>
        </div>

        {/* Main question */}
        <h1 className="text-6xl md:text-8xl font-bold mb-6 tracking-tight">
          The 1% Treaty
        </h1>

        <p className="text-xl md:text-2xl mb-4 text-gray-300 max-w-3xl mx-auto">
          Redirect 1% of military spending to medical research
        </p>

        <p className="text-lg md:text-xl mb-16 text-gray-400 max-w-2xl mx-auto">
          69 million people die every year from war and disease.<br/>
          We spend $119 trillion fighting each other instead of death itself.
        </p>

        {/* The Choice */}
        <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          {/* NO - Idiocracy */}
          <button
            onClick={() => router.push('/idiocracy')}
            onMouseEnter={() => setHoveredChoice('no')}
            onMouseLeave={() => setHoveredChoice(null)}
            className={`
              group relative p-12 rounded-2xl border-4 transition-all duration-500
              ${hoveredChoice === 'no'
                ? 'border-red-600 bg-red-950/30 scale-105'
                : 'border-red-900/50 bg-red-950/10 hover:border-red-800'
              }
            `}
          >
            <div className="text-8xl mb-4">❌</div>
            <div className="text-4xl font-bold mb-4">NO</div>
            <div className="text-gray-400 text-lg">
              Keep spending on war<br/>
              <span className="text-red-500">See where this leads →</span>
            </div>

            {hoveredChoice === 'no' && (
              <div className="absolute -bottom-4 left-1/2 -translate-x-1/2 text-red-500 text-sm animate-pulse">
                ⚠️ Warning: Extinction timeline
              </div>
            )}
          </button>

          {/* YES - Wishonia */}
          <button
            onClick={() => router.push('/wishonia')}
            onMouseEnter={() => setHoveredChoice('yes')}
            onMouseLeave={() => setHoveredChoice(null)}
            className={`
              group relative p-12 rounded-2xl border-4 transition-all duration-500
              ${hoveredChoice === 'yes'
                ? 'border-green-500 bg-green-950/30 scale-105'
                : 'border-green-900/50 bg-green-950/10 hover:border-green-700'
              }
            `}
          >
            <div className="text-8xl mb-4">✅</div>
            <div className="text-4xl font-bold mb-4">YES</div>
            <div className="text-gray-400 text-lg">
              Fund cures, not war<br/>
              <span className="text-green-500">See the future we build →</span>
            </div>

            {hoveredChoice === 'yes' && (
              <div className="absolute -bottom-4 left-1/2 -translate-x-1/2 text-green-500 text-sm animate-pulse">
                ✨ Preview: Wishonia timeline
              </div>
            )}
          </button>
        </div>

        {/* Stats */}
        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto text-sm">
          <div className="p-6 bg-gray-900/50 rounded-lg border border-gray-800">
            <div className="text-3xl font-bold text-red-400 mb-2">$8.2T</div>
            <div className="text-gray-400">Global military spending (annual)</div>
          </div>
          <div className="p-6 bg-gray-900/50 rounded-lg border border-gray-800">
            <div className="text-3xl font-bold text-yellow-400 mb-2">$82B</div>
            <div className="text-gray-400">1% redirected to research</div>
          </div>
          <div className="p-6 bg-gray-900/50 rounded-lg border border-gray-800">
            <div className="text-3xl font-bold text-green-400 mb-2">80X</div>
            <div className="text-gray-400">More efficient than current system</div>
          </div>
        </div>

        {/* Subtext */}
        <div className="mt-12 text-gray-500 text-sm max-w-2xl mx-auto">
          Choose your timeline. See the consequences. Then vote in the global referendum.
        </div>
      </div>
    </div>
  );
}
