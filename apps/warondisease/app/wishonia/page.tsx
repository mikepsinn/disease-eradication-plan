'use client';

import { useRouter } from 'next/navigation';
import { useState, useEffect } from 'react';

export default function WishoniaTimeline() {
  const router = useRouter();
  const [livesSaved, setLivesSaved] = useState(0);

  // Simulate lives saved counter (with 1% treaty: ~7M saved per year = ~800/hour = 0.22/sec)
  useEffect(() => {
    const interval = setInterval(() => {
      setLivesSaved(prev => prev + 1);
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-b from-black via-green-950/20 to-black text-white">
      {/* Lives saved counter header */}
      <div className="fixed top-0 left-0 right-0 bg-green-950/50 backdrop-blur-sm border-b border-green-900 z-50">
        <div className="max-w-6xl mx-auto px-4 py-3 flex justify-between items-center">
          <div className="font-mono text-sm">
            <span className="text-green-400">Lives saved since you voted YES: </span>
            <span className="text-green-500 font-bold text-lg">{livesSaved.toLocaleString()}</span>
          </div>
          <button
            onClick={() => router.push('/join')}
            className="px-6 py-2 bg-green-600 hover:bg-green-700 rounded-full text-sm font-bold transition-all animate-pulse"
          >
            Join the Referendum →
          </button>
        </div>
      </div>

      {/* Timeline content */}
      <div className="pt-24 pb-20">
        <div className="max-w-4xl mx-auto px-4 space-y-32">
          {/* Intro */}
          <section className="text-center">
            <h1 className="text-7xl font-bold mb-6 text-green-500">The YES Timeline</h1>
            <p className="text-2xl text-gray-300 mb-4">
              You voted for the 1% Treaty
            </p>
            <p className="text-xl text-gray-400">
              Here's what happens when we choose cures over war...
            </p>
          </section>

          {/* 2028 - Treaty Ratification */}
          <section className="relative">
            <div className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-green-600 to-green-700"></div>
            <div className="ml-12">
              <div className="text-green-500 font-mono text-sm mb-2">2028</div>
              <h2 className="text-4xl font-bold mb-4">🌍 The 1% Treaty Passes</h2>
              <div className="text-gray-300 space-y-4">
                <p className="text-lg">
                  After a global referendum with <span className="text-green-400 font-bold">280 million participants</span>,
                  nations ratify the 1% Treaty. Military budgets stay strong, but 1% is redirected to medical research.
                </p>
                <div className="bg-green-950/30 border border-green-900 rounded-lg p-6 mt-6">
                  <div className="text-2xl font-bold mb-4">💰 New Funding Unlocked</div>
                  <ul className="space-y-3">
                    <li className="flex justify-between items-center">
                      <span className="text-gray-400">Annual medical research (before):</span>
                      <span className="text-yellow-400 font-bold">$250B</span>
                    </li>
                    <li className="flex justify-between items-center">
                      <span className="text-gray-400">1% of military spending:</span>
                      <span className="text-green-400 font-bold">+$82B</span>
                    </li>
                    <li className="flex justify-between items-center border-t border-green-900 pt-3">
                      <span className="text-white font-bold">Total new funding:</span>
                      <span className="text-green-400 font-bold text-2xl">$332B</span>
                    </li>
                  </ul>
                  <div className="mt-4 text-green-500 text-sm">
                    ↑ 33% increase in global medical research funding
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* 2029 - DIH Launch */}
          <section className="relative">
            <div className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-green-600 to-green-700"></div>
            <div className="ml-12">
              <div className="text-green-500 font-mono text-sm mb-2">2029</div>
              <h2 className="text-4xl font-bold mb-4">🏛️ Decentralized Institutes of Health (DIH)</h2>
              <div className="text-gray-300 space-y-4">
                <p className="text-lg">
                  Treaty funds flow to the DIH — a new system where <span className="text-green-400 font-bold">anyone can propose trials</span>.
                  No committees. No gatekeepers. Just wishocratic voting by the 280M referendum participants.
                </p>
                <div className="bg-green-950/30 border border-green-900 rounded-lg p-6 mt-6">
                  <div className="text-2xl font-bold mb-4">⚡ How It Works</div>
                  <div className="space-y-4">
                    <div className="flex items-start gap-4">
                      <div className="text-3xl">1️⃣</div>
                      <div>
                        <div className="font-bold mb-1">Anyone Proposes</div>
                        <div className="text-gray-400 text-sm">
                          Patients, doctors, researchers submit trial proposals
                        </div>
                      </div>
                    </div>
                    <div className="flex items-start gap-4">
                      <div className="text-3xl">2️⃣</div>
                      <div>
                        <div className="font-bold mb-1">Wishocracy Votes</div>
                        <div className="text-gray-400 text-sm">
                          280M participants vote based on their health priorities
                        </div>
                      </div>
                    </div>
                    <div className="flex items-start gap-4">
                      <div className="text-3xl">3️⃣</div>
                      <div>
                        <div className="font-bold mb-1">dFDA Runs Trials</div>
                        <div className="text-gray-400 text-sm">
                          Decentralized FDA coordinates pragmatic trials (80X cheaper)
                        </div>
                      </div>
                    </div>
                    <div className="flex items-start gap-4">
                      <div className="text-3xl">4️⃣</div>
                      <div>
                        <div className="font-bold mb-1">VICTORY Bonds Pay</div>
                        <div className="text-gray-400 text-sm">
                          Bondholders earn 10% of the perpetual health dividend
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* 2032 - First Cures */}
          <section className="relative">
            <div className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-green-500 to-green-600"></div>
            <div className="ml-12">
              <div className="text-green-400 font-mono text-sm mb-2">2032</div>
              <h2 className="text-4xl font-bold mb-4">💊 Breakthrough Cures Arrive</h2>
              <div className="text-gray-300 space-y-4">
                <p className="text-lg">
                  The dFDA's pragmatic trials produce results <span className="text-green-400 font-bold">80X faster and cheaper</span> than traditional methods.
                  First wave of cures approved:
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="bg-green-950/30 border border-green-900 rounded-lg p-4">
                    <div className="text-2xl mb-2">🧬</div>
                    <div className="font-bold mb-1">Gene therapy for rare diseases</div>
                    <div className="text-green-400 text-sm">8,000 diseases now treatable</div>
                  </div>
                  <div className="bg-green-950/30 border border-green-900 rounded-lg p-4">
                    <div className="text-2xl mb-2">❤️</div>
                    <div className="font-bold mb-1">Heart disease prevention protocol</div>
                    <div className="text-green-400 text-sm">Reduces deaths by 40%</div>
                  </div>
                  <div className="bg-green-950/30 border border-green-900 rounded-lg p-4">
                    <div className="text-2xl mb-2">🧠</div>
                    <div className="font-bold mb-1">Alzheimer's reversal treatment</div>
                    <div className="text-green-400 text-sm">Phase 3 trials showing 65% efficacy</div>
                  </div>
                  <div className="bg-green-950/30 border border-green-900 rounded-lg p-4">
                    <div className="text-2xl mb-2">🦠</div>
                    <div className="font-bold mb-1">Universal cancer vaccine</div>
                    <div className="text-green-400 text-sm">Prevents 12 major cancer types</div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* 2038 - Economic Boom */}
          <section className="relative">
            <div className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-green-400 to-green-500"></div>
            <div className="ml-12">
              <div className="text-green-300 font-mono text-sm mb-2">2038</div>
              <h2 className="text-4xl font-bold mb-4">📈 The Health Dividend Compounds</h2>
              <div className="text-gray-300 space-y-4">
                <p className="text-lg">
                  Healthier populations = more productive economies. The <span className="text-green-400 font-bold">perpetual peace and health dividend</span> is massive:
                </p>
                <div className="bg-green-950/30 border border-green-900 rounded-lg p-6">
                  <div className="text-2xl font-bold mb-4">💎 VICTORY Bond Returns</div>
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-gray-400">Health dividend (annual):</span>
                      <span className="text-green-400 font-bold">$2.1 trillion</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-gray-400">Bondholder share (10%):</span>
                      <span className="text-green-400 font-bold">$210 billion</span>
                    </div>
                    <div className="flex justify-between items-center border-t border-green-900 pt-3">
                      <span className="text-white font-bold">Average ROI per bondholder:</span>
                      <span className="text-green-400 font-bold text-2xl">42% annually</span>
                    </div>
                  </div>
                  <div className="mt-4 text-green-500 text-sm italic">
                    The best investment in human history wasn't crypto or stocks — it was ending disease.
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* 2050 - Wishonia Realized */}
          <section className="relative">
            <div className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-green-300 to-green-500"></div>
            <div className="ml-12">
              <div className="text-green-200 font-mono text-sm mb-2">2050</div>
              <h2 className="text-4xl font-bold mb-4">✨ Welcome to Wishonia</h2>
              <div className="text-gray-300 space-y-4">
                <p className="text-lg">
                  The Three Supers are unlocked:
                </p>
                <div className="grid grid-cols-1 gap-4">
                  <div className="bg-gradient-to-r from-blue-950/30 to-green-950/30 border border-green-700 rounded-lg p-6">
                    <div className="text-4xl mb-2">🧠</div>
                    <div className="text-2xl font-bold mb-2">Superintelligence</div>
                    <div className="text-gray-400">
                      Brain-computer interfaces + cognitive enhancement = humanity thinks 100X faster
                    </div>
                  </div>
                  <div className="bg-gradient-to-r from-purple-950/30 to-green-950/30 border border-green-700 rounded-lg p-6">
                    <div className="text-4xl mb-2">⏳</div>
                    <div className="text-2xl font-bold mb-2">Superlongevity</div>
                    <div className="text-gray-400">
                      Average lifespan: 150+ years. Age-related diseases eliminated.
                    </div>
                  </div>
                  <div className="bg-gradient-to-r from-pink-950/30 to-green-950/30 border border-green-700 rounded-lg p-6">
                    <div className="text-4xl mb-2">😊</div>
                    <div className="text-2xl font-bold mb-2">Superhappiness</div>
                    <div className="text-gray-400">
                      Mental health disorders cured. Baseline wellbeing optimized.
                    </div>
                  </div>
                </div>
                <div className="bg-green-950/50 border-2 border-green-500 rounded-lg p-8 mt-8 text-center">
                  <div className="text-3xl font-bold mb-4 text-green-400">Lives Saved (2028-2050)</div>
                  <div className="text-6xl font-bold text-green-500 mb-4">156 million</div>
                  <div className="text-gray-400 text-lg">
                    And that's just the beginning. The treaty is perpetual. The dividend compounds forever.
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* CTA - Join */}
          <section className="text-center py-20">
            <h2 className="text-5xl font-bold mb-6">This Is Within Reach</h2>
            <p className="text-xl text-gray-400 mb-12 max-w-2xl mx-auto">
              We just need 280 million people to vote YES in the global referendum.
              Join now and become eligible for subsidized trials + VICTORY bond allocations.
            </p>
            <div className="space-y-4">
              <button
                onClick={() => router.push('/join')}
                className="block w-full max-w-md mx-auto px-12 py-6 bg-green-600 hover:bg-green-700 text-white rounded-2xl text-2xl font-bold transition-all transform hover:scale-105 animate-pulse"
              >
                ✅ Join the Referendum
              </button>
              <button
                onClick={() => router.push('/victory-bonds')}
                className="block w-full max-w-md mx-auto px-12 py-4 bg-yellow-700 hover:bg-yellow-600 text-white rounded-2xl text-lg font-bold transition-all"
              >
                💎 Learn About VICTORY Bonds
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
