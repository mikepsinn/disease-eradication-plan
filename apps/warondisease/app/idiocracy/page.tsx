'use client';

import { useRouter } from 'next/navigation';
import { useState, useEffect } from 'react';

export default function IdiocracyTimeline() {
  const router = useRouter();
  const [age] = useState(Math.floor(Math.random() * 30) + 25); // Random age 25-55
  const [deathAge] = useState(Math.floor(Math.random() * 15) + 65); // Death age 65-80
  const [deathCause] = useState(() => {
    const causes = [
      { name: 'heart disease', cost: '$1.2M in medical debt', preventable: 'Preventable with $200k in research' },
      { name: 'cancer', cost: '$900k treatment (failed)', preventable: 'Curable for the price of 2 missiles' },
      { name: "Alzheimer's", cost: '$5M in care costs', preventable: 'One bomber = cure funded' },
      { name: 'diabetes complications', cost: '$800k lifetime costs', preventable: 'Halloween budget could fix this' },
      { name: 'stroke', cost: '$2M in care + lost income', preventable: "Pentagon's coffee budget > stroke research" }
    ];
    return causes[Math.floor(Math.random() * causes.length)];
  });

  return (
    <div className="min-h-screen bg-gradient-to-b from-black via-red-950/20 to-black text-white">
      <div className="max-w-4xl mx-auto px-4 py-20">

        {/* Your Personal Death Certificate */}
        <section className="mb-20">
          <h1 className="text-6xl font-bold mb-12 text-center text-red-500">
            You Chose: Keep Being Idiots
          </h1>

          <div className="bg-black border-4 border-red-900 rounded-lg p-12 shadow-2xl">
            <div className="text-center mb-8">
              <div className="text-gray-500 text-sm mb-2">OFFICIAL DOCUMENT</div>
              <h2 className="text-4xl font-bold text-red-400">DEATH CERTIFICATE</h2>
              <div className="text-gray-500 text-sm mt-2">Timeline: Idiocracy</div>
            </div>

            <div className="space-y-6 text-lg">
              <div className="flex justify-between border-b border-red-900/50 pb-3">
                <span className="text-gray-400">Name:</span>
                <span className="font-bold">YOU</span>
              </div>
              <div className="flex justify-between border-b border-red-900/50 pb-3">
                <span className="text-gray-400">Current Age:</span>
                <span className="font-bold">{age}</span>
              </div>
              <div className="flex justify-between border-b border-red-900/50 pb-3">
                <span className="text-gray-400">Death Age:</span>
                <span className="font-bold text-red-400">{deathAge}</span>
              </div>
              <div className="flex justify-between border-b border-red-900/50 pb-3">
                <span className="text-gray-400">Cause of Death:</span>
                <span className="font-bold text-red-400 uppercase">{deathCause.name}</span>
              </div>
              <div className="flex justify-between border-b border-red-900/50 pb-3">
                <span className="text-gray-400">Family Cost:</span>
                <span className="font-bold text-yellow-400">{deathCause.cost}</span>
              </div>
              <div className="border-t-2 border-red-600 pt-6 mt-6">
                <div className="text-center">
                  <div className="text-sm text-gray-400 mb-2">THIS DEATH WAS</div>
                  <div className="text-3xl font-bold text-red-500">100% PREVENTABLE</div>
                  <div className="text-sm text-gray-400 mt-2">{deathCause.preventable}</div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Meanwhile, In Reality... */}
        <section className="mb-20">
          <h2 className="text-4xl font-bold mb-8 text-center">
            Here's What Actually Happens:
          </h2>

          <div className="space-y-12">
            {/* 2028 */}
            <div className="relative pl-12">
              <div className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-red-600 to-red-900"></div>
              <div className="text-red-500 font-mono text-sm mb-2">2028</div>
              <h3 className="text-2xl font-bold mb-4">Nothing Changes (Shocker)</h3>
              <div className="bg-red-950/30 border border-red-900 rounded-lg p-6">
                <p className="text-gray-300 mb-4">
                  The Pentagon loses another <span className="text-red-400 font-bold">$500 billion</span>.
                  Just... whoops. Can't find it. That's 250 cancer cures. Gone.
                </p>
                <p className="text-gray-300">
                  Your mom gets diagnosed. Treatment exists but costs $2 million.
                  Insurance covers $50k. Good luck with the GoFundMe.
                </p>
              </div>
            </div>

            {/* 2032 */}
            <div className="relative pl-12">
              <div className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-red-700 to-red-950"></div>
              <div className="text-red-600 font-mono text-sm mb-2">2032</div>
              <h3 className="text-2xl font-bold mb-4">The Kids Start Dying</h3>
              <div className="bg-red-950/30 border border-red-900 rounded-lg p-6">
                <p className="text-gray-300 mb-4">
                  Remember that rare disease that affects 30,000 kids? Still no cure.
                  Research budget: <span className="text-yellow-400">$12 million</span>.
                  New bomber program: <span className="text-red-400 font-bold">$120 billion</span>.
                </p>
                <p className="text-gray-300">
                  Parents start a petition. It gets 2 million signatures.
                  Congress sends thoughts and prayers. Approves 3 more submarines.
                </p>
              </div>
            </div>

            {/* 2035 */}
            <div className="relative pl-12">
              <div className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-red-800 to-black"></div>
              <div className="text-red-700 font-mono text-sm mb-2">2035</div>
              <h3 className="text-2xl font-bold mb-4">You Realize We're Idiots</h3>
              <div className="bg-red-950/30 border border-red-900 rounded-lg p-6">
                <p className="text-gray-300 mb-4">
                  China cures diabetes. Cost them $8 billion.
                  We spent $8 billion on... wait, the Pentagon lost it again.
                </p>
                <p className="text-gray-300 mb-4">
                  Your dad dies from something China just cured.
                  But hey, we have 12 new aircraft carriers!
                </p>
                <div className="bg-black/50 border border-red-800 rounded p-4 mt-4">
                  <p className="text-red-400 font-bold text-center">
                    Fun fact: We could have cured everything by now.<br/>
                    We chose bombs instead.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* The Math Section */}
        <section className="mb-20">
          <h2 className="text-4xl font-bold mb-8 text-center">
            Quick Math Break
          </h2>

          <div className="bg-gradient-to-b from-gray-900/50 to-black border-2 border-gray-800 rounded-2xl p-8">
            <p className="text-2xl text-center mb-8 text-gray-300">
              By choosing NO, here's what you personally funded:
            </p>

            <div className="grid md:grid-cols-2 gap-6">
              <div className="text-center p-6 bg-red-950/20 rounded-lg">
                <div className="text-5xl font-bold text-red-400 mb-2">$483,291</div>
                <div className="text-gray-400">Your lifetime tax contribution to military</div>
                <div className="text-sm text-gray-500 mt-2">
                  (Bought 1/165th of a fighter jet)
                </div>
              </div>
              <div className="text-center p-6 bg-green-950/20 rounded-lg">
                <div className="text-5xl font-bold text-green-400 mb-2">$4,832</div>
                <div className="text-gray-400">Your lifetime contribution to medical research</div>
                <div className="text-sm text-gray-500 mt-2">
                  (Bought 3 minutes of one clinical trial)
                </div>
              </div>
            </div>

            <div className="text-center mt-8 text-xl text-white font-bold">
              Congratulations. You played yourself.
            </div>
          </div>
        </section>

        {/* Final Choice */}
        <section className="text-center">
          <h2 className="text-5xl font-bold mb-6">
            This Is Stupid
          </h2>
          <p className="text-xl text-gray-400 mb-12 max-w-2xl mx-auto">
            We just showed you your own death certificate.
            From something we could cure for less than we spend on military marching bands.
          </p>
          <p className="text-2xl font-bold mb-12 text-yellow-400">
            Want to not die like an idiot?
          </p>

          <div className="space-y-4">
            <button
              onClick={() => router.push('/wishonia')}
              className="block w-full max-w-md mx-auto px-12 py-6 bg-green-600 hover:bg-green-700 text-white rounded-2xl text-2xl font-bold transition-all transform hover:scale-105"
            >
              ✅ Try the Non-Idiot Timeline
            </button>
            <button
              onClick={() => router.push('/')}
              className="block w-full max-w-md mx-auto px-12 py-4 bg-gray-800 hover:bg-gray-700 text-white rounded-2xl text-lg transition-all"
            >
              ← Reconsider Your Choices
            </button>
          </div>

          <p className="mt-12 text-gray-500 text-sm">
            Seriously. The other timeline has flying cars and immortality.<br/>
            This one has you dying broke from preventable diseases.<br/>
            How is this even a choice?
          </p>
        </section>
      </div>
    </div>
  );
}
