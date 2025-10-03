'use client';

import { useRouter } from 'next/navigation';

export default function WishoniaTimeline() {
  const router = useRouter();

  return (
    <div className="min-h-screen bg-gradient-to-b from-black via-green-950/20 to-black text-white">
      <div className="max-w-4xl mx-auto px-4 py-20">

        {/* Intro */}
        <section className="mb-20">
          <h1 className="text-6xl font-bold mb-6 text-center text-green-500">
            You Chose: Try Not Dying
          </h1>
          <p className="text-2xl text-gray-300 text-center mb-8">
            Smart move. Here's how we actually pull this off:
          </p>
        </section>

        {/* The Actual Mechanism */}
        <section className="mb-20">
          <h2 className="text-4xl font-bold mb-8 text-center">
            How This Actually Works
          </h2>
          <p className="text-xl text-gray-400 text-center mb-12">
            (Not magic. Just copying what already works.)
          </p>

          <div className="space-y-12">
            {/* Step 1: The Lobby */}
            <div className="bg-green-950/30 border border-green-900 rounded-lg p-8">
              <div className="text-3xl mb-4">🏛️</div>
              <h3 className="text-2xl font-bold mb-4">Step 1: We Out-Lobby the Death Industry</h3>
              <div className="text-gray-300 space-y-4">
                <p>
                  Defense contractors spend <span className="text-red-400 font-bold">$120M/year</span> on lobbying.
                  They get <span className="text-red-400 font-bold">$820B/year</span> in contracts.
                  That's a <span className="text-green-400 font-bold">6,833X return</span>.
                </p>
                <p>
                  We copy their playbook exactly. But instead of lobbying FOR war spending,
                  we lobby to redirect 1% of it. Same senators. Same tactics. Opposite outcome.
                </p>
                <div className="bg-black/50 border border-green-800 rounded p-4 mt-4">
                  <p className="text-green-400 font-bold">
                    Fun fact: It costs $50k to buy a senator's vote. We need 51 senators.
                    That's $2.55M to redirect $82B. ROI: 32,156X.
                  </p>
                </div>
              </div>
            </div>

            {/* Step 2: The System */}
            <div className="bg-green-950/30 border border-green-900 rounded-lg p-8">
              <div className="text-3xl mb-4">📱</div>
              <h3 className="text-2xl font-bold mb-4">Step 2: Tinder for Budget Allocation</h3>
              <div className="text-gray-300 space-y-4">
                <p>
                  Remember how the FDA takes 15 years and $2.8B to approve a drug?
                  That's because 12 people in a committee decide everything.
                </p>
                <p>
                  The DIH works like this: <span className="text-green-400 font-bold">Swipe right to fund cancer research.
                  Swipe left to fund Alzheimer's.</span> 280 million people voting beats 12 bureaucrats every time.
                </p>
                <p>
                  No committees. No gatekeepers. Just an app that aggregates what diseases people actually want cured.
                  Your mom has diabetes? You vote for diabetes trials. Simple.
                </p>
              </div>
            </div>

            {/* Step 3: The Trials */}
            <div className="bg-green-950/30 border border-green-900 rounded-lg p-8">
              <div className="text-3xl mb-4">💊</div>
              <h3 className="text-2xl font-bold mb-4">Step 3: Amazon Prime for Clinical Trials</h3>
              <div className="text-gray-300 space-y-4">
                <p>
                  Current system: Drive 200 miles to a trial site. Wait 6 months. Get placebo. Die anyway.
                </p>
                <p>
                  dFDA system: <span className="text-green-400 font-bold">Pills arrive Tuesday.</span>
                  Your Apple Watch tracks results. AI monitors safety in real-time.
                  10,000X more participants = 100X faster results.
                </p>
                <p>
                  We call them "pragmatic trials" - run them where people actually live,
                  not in some hospital 5 states away. Uber delivered food. We'll deliver cures.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* The Timeline */}
        <section className="mb-20">
          <h2 className="text-4xl font-bold mb-8 text-center">
            What Actually Happens
          </h2>

          <div className="space-y-12">
            {/* 2028 */}
            <div className="relative pl-12">
              <div className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-green-600 to-green-700"></div>
              <div className="text-green-500 font-mono text-sm mb-2">2028</div>
              <h3 className="text-2xl font-bold mb-4">The Lobbying Blitz</h3>
              <div className="bg-green-950/30 border border-green-900 rounded-lg p-6">
                <p className="text-gray-300 mb-4">
                  We hire the same lobbyists Lockheed uses. They walk into the same offices.
                  But instead of selling F-35s, they're selling "biodefense" and "pandemic preparedness."
                </p>
                <p className="text-gray-300">
                  Congress loves it. Same contractors. Same districts. Same jobs.
                  Just building mRNA printers instead of missiles. The 1% Treaty passes.
                </p>
              </div>
            </div>

            {/* 2030 */}
            <div className="relative pl-12">
              <div className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-green-500 to-green-600"></div>
              <div className="text-green-400 font-mono text-sm mb-2">2030</div>
              <h3 className="text-2xl font-bold mb-4">First Cures Ship</h3>
              <div className="bg-green-950/30 border border-green-900 rounded-lg p-6">
                <p className="text-gray-300 mb-4">
                  Type 1 diabetes: Cured. Cost us $4B. Saves $400B in lifetime care costs.
                  That's a <span className="text-green-400 font-bold">100X return in year one</span>.
                </p>
                <p className="text-gray-300">
                  China's pissed. They were 2 years away. We beat them because we didn't have
                  committees debating for 5 years whether diabetes was worth curing.
                </p>
              </div>
            </div>

            {/* 2035 */}
            <div className="relative pl-12">
              <div className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-green-400 to-green-500"></div>
              <div className="text-green-300 font-mono text-sm mb-2">2035</div>
              <h3 className="text-2xl font-bold mb-4">The Money Printer</h3>
              <div className="bg-green-950/30 border border-green-900 rounded-lg p-6">
                <p className="text-gray-300 mb-4">
                  Remember VICTORY bonds? They're paying <span className="text-yellow-400 font-bold">18% annually</span>.
                  Not 40% (that was marketing). But 18% forever beats the S&P 500.
                </p>
                <p className="text-gray-300 mb-4">
                  How? Every cure = healthier workers = higher GDP.
                  We capture 10% of that productivity gain. It compounds. Forever.
                </p>
                <div className="bg-black/50 border border-green-800 rounded p-4 mt-4">
                  <p className="text-green-400 text-center">
                    Your $10k investment is now worth $47k.<br/>
                    Your dad is still alive.<br/>
                    Win-win.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Why This Actually Works */}
        <section className="mb-20">
          <h2 className="text-4xl font-bold mb-8 text-center">
            Why This Actually Works
          </h2>

          <div className="bg-gradient-to-b from-gray-900/50 to-black border-2 border-gray-800 rounded-2xl p-8">
            <div className="space-y-6 text-lg text-gray-300">
              <div>
                <span className="text-yellow-400 font-bold">It's not charity.</span> Defense contractors pivot to biodefense. Same profits, less death.
              </div>
              <div>
                <span className="text-yellow-400 font-bold">It's not democratic.</span> It's wishocratic. You vote your self-interest. That's more honest than democracy.
              </div>
              <div>
                <span className="text-yellow-400 font-bold">It's not revolutionary.</span> We're using the exact same corrupt system, just backwards.
              </div>
              <div>
                <span className="text-yellow-400 font-bold">It's not idealistic.</span> Everyone's motivated by greed and not dying. Universal human traits.
              </div>
            </div>

            <div className="text-center mt-8 pt-6 border-t border-gray-700">
              <p className="text-2xl font-bold text-white">
                We're literally too greedy to die.
              </p>
              <p className="text-gray-400 mt-2">
                And that's why it works.
              </p>
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="text-center">
          <h2 className="text-5xl font-bold mb-6">
            Ready to Not Die Broke?
          </h2>
          <p className="text-xl text-gray-400 mb-12 max-w-2xl mx-auto">
            Join 280 million people who've figured out that curing disease
            is more profitable than building bombs.
          </p>

          <div className="space-y-4">
            <button
              onClick={() => router.push('/join')}
              className="block w-full max-w-md mx-auto px-12 py-6 bg-green-600 hover:bg-green-700 text-white rounded-2xl text-2xl font-bold transition-all transform hover:scale-105"
            >
              ✅ Join the Referendum
            </button>
            <button
              onClick={() => router.push('/victory-bonds')}
              className="block w-full max-w-md mx-auto px-12 py-4 bg-yellow-700 hover:bg-yellow-600 text-white rounded-2xl text-lg font-bold transition-all"
            >
              💎 Get VICTORY Bonds (18% Forever)
            </button>
            <button
              onClick={() => router.push('/')}
              className="block w-full max-w-md mx-auto px-12 py-4 bg-gray-800 hover:bg-gray-700 text-white rounded-2xl text-lg transition-all"
            >
              ← Back to Reality Check
            </button>
          </div>

          <p className="mt-12 text-gray-500 text-sm">
            This isn't a feel-good charity. It's a hostile takeover of the death industry.<br/>
            Using their own lobbying tactics against them.<br/>
            Join us or die broke from preventable diseases. Your choice.
          </p>
        </section>
      </div>
    </div>
  );
}