'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function VictoryBonds() {
  const router = useRouter();
  const [investment, setInvestment] = useState(10000);

  const calculateReturns = () => {
    const annualReturn = 0.18; // 18% realistic annual return (not 42% fairy tale)
    const year5 = investment * Math.pow(1 + annualReturn, 5);
    const year10 = investment * Math.pow(1 + annualReturn, 10);
    const year20 = investment * Math.pow(1 + annualReturn, 20);
    return { year5, year10, year20 };
  };

  const returns = calculateReturns();

  return (
    <div className="min-h-screen bg-gradient-to-b from-black via-yellow-950/20 to-black text-white">
      <div className="max-w-4xl mx-auto px-4 py-20">

        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-6xl font-bold mb-6 text-yellow-500">
            VICTORY Bonds
          </h1>
          <p className="text-2xl text-gray-300 max-w-3xl mx-auto">
            How to profit from humanity not dying
          </p>
        </div>

        {/* The Real Deal */}
        <section className="mb-20">
          <h2 className="text-4xl font-bold mb-8 text-center">
            Listen: Here's What This Actually Is
          </h2>

          <div className="bg-gradient-to-br from-yellow-950/30 to-orange-950/30 border-2 border-yellow-700 rounded-2xl p-8">
            <div className="space-y-6 text-lg text-gray-300">
              <p>
                Remember how defense contractors get <span className="text-red-400 font-bold">6,833X returns</span> on lobbying?
                We're doing the same thing, but backwards.
              </p>
              <p>
                Instead of lobbying FOR death, we lobby AGAINST it.
                Same corrupt system. Opposite outcome. Better returns.
              </p>
              <div className="bg-black/50 border border-yellow-800 rounded p-6 mt-6">
                <p className="text-xl font-bold text-yellow-400 mb-4">
                  The Math (Real Numbers):
                </p>
                <ul className="space-y-3 text-gray-300">
                  <li>• Lobbying cost to pass 1% Treaty: <span className="text-green-400">$2.55M</span></li>
                  <li>• Annual funding redirected: <span className="text-green-400">$82B</span></li>
                  <li>• Health productivity gains: <span className="text-green-400">$820B/year</span> (conservative)</li>
                  <li>• Bondholder share (10%): <span className="text-yellow-400 font-bold">$82B/year</span></li>
                  <li>• Your realistic return: <span className="text-yellow-400 font-bold">18% annually, forever</span></li>
                </ul>
                <p className="mt-6 text-sm text-gray-400">
                  Not 42%. That was marketing bullshit. 18% forever is still better than the S&P.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Calculator */}
        <section className="mb-20">
          <h2 className="text-3xl font-bold mb-8 text-center">
            Your Actual Returns (18% Annual)
          </h2>

          <div className="bg-gray-900/50 border border-gray-800 rounded-2xl p-8">
            <div className="mb-8">
              <label className="block text-sm font-medium mb-3 text-gray-400">
                Investment Amount
              </label>
              <div className="flex items-center gap-4">
                <input
                  type="range"
                  min="1000"
                  max="100000"
                  step="1000"
                  value={investment}
                  onChange={(e) => setInvestment(Number(e.target.value))}
                  className="flex-1 h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
                />
                <div className="text-2xl font-bold text-yellow-400 min-w-[150px] text-right">
                  ${investment.toLocaleString()}
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-yellow-950/20 border border-yellow-800 rounded-xl p-6 text-center">
                <div className="text-gray-400 text-sm mb-2">5 Years</div>
                <div className="text-3xl font-bold text-yellow-400">
                  ${returns.year5.toLocaleString(undefined, { maximumFractionDigits: 0 })}
                </div>
                <div className="text-green-500 text-sm mt-2">
                  {((returns.year5 / investment - 1) * 100).toFixed(0)}% gain
                </div>
              </div>
              <div className="bg-yellow-950/20 border border-yellow-700 rounded-xl p-6 text-center">
                <div className="text-gray-400 text-sm mb-2">10 Years</div>
                <div className="text-3xl font-bold text-yellow-400">
                  ${returns.year10.toLocaleString(undefined, { maximumFractionDigits: 0 })}
                </div>
                <div className="text-green-500 text-sm mt-2">
                  {((returns.year10 / investment - 1) * 100).toFixed(0)}% gain
                </div>
              </div>
              <div className="bg-yellow-950/20 border border-yellow-600 rounded-xl p-6 text-center">
                <div className="text-gray-400 text-sm mb-2">20 Years</div>
                <div className="text-3xl font-bold text-yellow-400">
                  ${returns.year20.toLocaleString(undefined, { maximumFractionDigits: 0 })}
                </div>
                <div className="text-green-500 text-sm mt-2">
                  {((returns.year20 / investment - 1) * 100).toFixed(0)}% gain
                </div>
              </div>
            </div>

            <div className="text-center mt-8 p-4 bg-black/50 rounded">
              <p className="text-lg text-white">
                Your ${investment.toLocaleString()} becomes{' '}
                <span className="text-yellow-400 font-bold">
                  ${returns.year20.toLocaleString(undefined, { maximumFractionDigits: 0 })}
                </span>{' '}
                in 20 years
              </p>
              <p className="text-sm text-gray-400 mt-2">
                Plus you don't die from preventable diseases. Win-win.
              </p>
            </div>
          </div>
        </section>

        {/* How It Actually Works */}
        <section className="mb-20">
          <h2 className="text-4xl font-bold mb-8 text-center">
            How We Actually Pull This Off
          </h2>

          <div className="space-y-8">
            {/* Step 1 */}
            <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-6">
              <div className="text-2xl font-bold mb-4 text-yellow-400">
                Step 1: Buy the Senate (Legally)
              </div>
              <p className="text-gray-300 mb-4">
                Defense lobbyists spend $120M/year. We spend $10M.
                Same offices. Same senators. Different ask.
              </p>
              <p className="text-gray-300">
                "Senator, redirect 1% to biodefense. Lockheed builds mRNA printers instead of missiles.
                Same jobs in your district. Better optics. Here's your campaign contribution."
              </p>
            </div>

            {/* Step 2 */}
            <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-6">
              <div className="text-2xl font-bold mb-4 text-yellow-400">
                Step 2: The Money Flows
              </div>
              <p className="text-gray-300 mb-4">
                $82B/year gets redirected. Goes to DIH (Decentralized Institutes of Health).
                No committees. Just an app where people vote what to cure.
              </p>
              <p className="text-gray-300">
                Your mom has cancer? You vote cancer trials.
                280 million people voting > 12 FDA bureaucrats.
              </p>
            </div>

            {/* Step 3 */}
            <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-6">
              <div className="text-2xl font-bold mb-4 text-yellow-400">
                Step 3: Cures = GDP Growth
              </div>
              <p className="text-gray-300 mb-4">
                Every disease cured = healthier workers = higher productivity.
                Diabetes cure saves $400B in care costs. That money goes into the economy.
              </p>
              <p className="text-gray-300">
                We capture 10% of that productivity gain through VICTORY bonds.
                You get paid forever from humanity being healthier.
              </p>
            </div>
          </div>
        </section>

        {/* Reality Check */}
        <section className="mb-20">
          <h2 className="text-4xl font-bold mb-8 text-center">
            The Fine Print (We're Being Honest)
          </h2>

          <div className="bg-red-950/20 border border-red-900 rounded-2xl p-8">
            <div className="space-y-4 text-gray-300">
              <p>
                <span className="text-red-400 font-bold">Risk 1:</span> The treaty might not pass.
                But defense contractors need new revenue streams anyway. War is getting unpopular.
              </p>
              <p>
                <span className="text-red-400 font-bold">Risk 2:</span> Returns might be 12% not 18%.
                Still beats inflation. Still beats bonds. Still saves your life.
              </p>
              <p>
                <span className="text-red-400 font-bold">Risk 3:</span> Government might renege.
                That's why we make it profitable for them too. Healthy citizens = higher tax revenue.
              </p>
              <div className="bg-black/50 border border-red-800 rounded p-4 mt-6">
                <p className="text-yellow-400 font-bold text-center">
                  Bottom line: It's still the best risk-adjusted return available.<br/>
                  Because the alternative is dying broke from preventable diseases.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="text-center">
          <h2 className="text-5xl font-bold mb-6">
            This Is How We Win
          </h2>
          <p className="text-xl text-gray-400 mb-12 max-w-2xl mx-auto">
            We use capitalism's own greed against death itself.
            Join 280 million people betting on not dying.
          </p>

          <div className="space-y-4">
            <button
              onClick={() => router.push('/join')}
              className="block w-full max-w-md mx-auto px-12 py-6 bg-yellow-600 hover:bg-yellow-700 text-black font-bold rounded-2xl text-2xl transition-all transform hover:scale-105"
            >
              💎 Get VICTORY Bonds
            </button>
            <p className="text-gray-500 text-sm">
              Priority allocation for referendum participants
            </p>
            <button
              onClick={() => router.push('/')}
              className="block w-full max-w-md mx-auto px-8 py-3 bg-gray-800 hover:bg-gray-700 text-white rounded-xl transition-all"
            >
              ← Back to Reality
            </button>
          </div>

          <p className="mt-12 text-gray-500 text-sm max-w-2xl mx-auto">
            This isn't idealism. It's reverse lobbying.<br/>
            Same corrupt system that gave us $2 trillion wars.<br/>
            We're just using it to cure cancer instead.
          </p>
        </section>
      </div>
    </div>
  );
}