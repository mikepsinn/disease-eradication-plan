'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function Home() {
  const [hoveredChoice, setHoveredChoice] = useState<'yes' | 'no' | null>(null);
  const [moneyLost, setMoneyLost] = useState(2500000000000);
  const router = useRouter();

  // Pentagon loses money in real time ($79,365/second based on their accounting)
  useEffect(() => {
    const interval = setInterval(() => {
      setMoneyLost(prev => prev + 79365);
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-black text-white">
      {/* The Hook */}
      <div className="max-w-4xl mx-auto px-4 py-20">
        <div className="text-center mb-16">
          {/* Pentagon Lost Money Counter */}
          <div className="mb-12 p-6 bg-red-950/20 border border-red-900/50 rounded-xl">
            <div className="text-sm text-red-400 mb-2">The Pentagon has lost</div>
            <div className="text-5xl md:text-6xl font-bold text-red-500 font-mono">
              ${(moneyLost / 1000000000000).toFixed(3)} trillion
            </div>
            <div className="text-sm text-gray-400 mt-2">
              That's enough to cure cancer {Math.floor(moneyLost / 2000000000).toLocaleString()} times
            </div>
          </div>

          {/* The Pitch */}
          <h1 className="text-4xl md:text-5xl font-bold mb-8 leading-tight">
            Listen: Your mom has a 73% chance<br/>
            of dying from something we could fix<br/>
            for the price of one missile
          </h1>

          <p className="text-xl text-gray-400 mb-8 max-w-2xl mx-auto">
            This is stupid. Let's fix it.
          </p>

          {/* The $119 Trillion Death Toilet */}
          <div className="mb-16 p-8 bg-gradient-to-b from-gray-900/50 to-black border-2 border-gray-800 rounded-2xl">
            <div className="text-7xl mb-4">🚽</div>
            <h2 className="text-3xl font-bold mb-4 text-yellow-500">
              The $119 Trillion Death Toilet
            </h2>
            <div className="space-y-3 text-lg">
              <p className="text-gray-300">
                Every year, humanity flushes <span className="text-red-400 font-bold">$119 trillion</span> down the toilet of war and disease.
              </p>
              <p className="text-gray-300">
                We spend <span className="text-yellow-400 font-bold">$68 billion</span> trying to cure things.
              </p>
              <p className="text-gray-300">
                That's like spending <span className="text-green-400 font-bold">$1,750</span> on guns and bandaids for every <span className="text-green-400 font-bold">$1</span> on not getting shot.
              </p>
              <p className="text-2xl text-white font-bold mt-6">
                We are idiots.
              </p>
            </div>
          </div>

          {/* Some Quick Math */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-16 text-left">
            <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-6">
              <div className="text-3xl mb-3">🎃</div>
              <div className="text-xl font-bold mb-2">Halloween Costumes</div>
              <div className="text-3xl font-bold text-orange-400 mb-2">$12 billion/year</div>
              <div className="text-gray-400 text-sm">We spend more on looking scary than curing what actually kills us</div>
            </div>
            <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-6">
              <div className="text-3xl mb-3">🧬</div>
              <div className="text-xl font-bold mb-2">All Rare Disease Research</div>
              <div className="text-3xl font-bold text-blue-400 mb-2">$7 billion/year</div>
              <div className="text-gray-400 text-sm">30 million kids dying. Less funding than pet costumes.</div>
            </div>
            <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-6">
              <div className="text-3xl mb-3">✈️</div>
              <div className="text-xl font-bold mb-2">One F-35 Fighter Jet</div>
              <div className="text-3xl font-bold text-red-400 mb-2">$80 million</div>
              <div className="text-gray-400 text-sm">Entire childhood leukemia research budget</div>
            </div>
            <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-6">
              <div className="text-3xl mb-3">🚢</div>
              <div className="text-xl font-bold mb-2">One Nuclear Submarine</div>
              <div className="text-3xl font-bold text-red-400 mb-2">$4.3 billion</div>
              <div className="text-gray-400 text-sm">Could fund Alzheimer's cure instead</div>
            </div>
          </div>

          {/* The Actual Question */}
          <div className="mb-12 p-8 bg-blue-950/20 border border-blue-900/50 rounded-xl">
            <h2 className="text-2xl font-bold mb-4">Here's the trick:</h2>
            <p className="text-lg text-gray-300 mb-4">
              Redirect just <span className="text-yellow-400 font-bold">1%</span> of military spending to medical research.
            </p>
            <p className="text-lg text-gray-300">
              Not 10%. Not 50%. Just 1%. The military keeps 99%.
            </p>
            <p className="text-lg text-gray-300 mt-4">
              That 1% becomes <span className="text-green-400 font-bold">$82 billion/year</span> for cures.
            </p>
            <p className="text-xl font-bold text-white mt-6">
              Double the entire global medical research budget. From a rounding error.
            </p>
          </div>

          {/* The Choice */}
          <div className="mb-8">
            <p className="text-2xl font-bold mb-6">So what'll it be?</p>
          </div>

          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            {/* NO - Keep being idiots */}
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
              <div className="text-6xl mb-4">💀</div>
              <div className="text-3xl font-bold mb-4">KEEP BEING IDIOTS</div>
              <div className="text-gray-400">
                Watch everyone die<br/>
                <span className="text-red-500 text-sm">See your personal death certificate →</span>
              </div>
            </button>

            {/* YES - Try something less stupid */}
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
              <div className="text-6xl mb-4">🧠</div>
              <div className="text-3xl font-bold mb-4">TRY NOT DYING</div>
              <div className="text-gray-400">
                Fix this idiocy<br/>
                <span className="text-green-500 text-sm">See how we actually pull this off →</span>
              </div>
            </button>
          </div>

          {/* Bottom line */}
          <div className="mt-16 text-gray-500 text-sm max-w-2xl mx-auto">
            This is a practical guide to tricking humanity into not killing itself.<br/>
            Written by idiots, for idiots.
          </div>
        </div>
      </div>
    </div>
  );
}