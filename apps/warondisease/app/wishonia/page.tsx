'use client';

import { useRouter } from 'next/navigation';

export default function WishoniaTimeline() {
  const router = useRouter();

  return (
    <div className="max-w-2xl mx-auto px-6 py-12 font-serif">
      <h1 className="text-4xl font-bold mb-8">
        You chose: Try not dying.
      </h1>

      <p className="text-xl mb-8">
        Smart. Here's how we pull it off:
      </p>

      <div className="border-2 border-black p-6 mb-8">
        <p className="text-2xl font-bold mb-4">Step 1: Buy the Senate</p>
        <p className="mb-3">
          Defense contractors spend $120M/year on lobbying.<br/>
          They get $820B/year in contracts.<br/>
          That's 6,833X return.
        </p>
        <p>
          We spend $2.55M to buy 51 senators.<br/>
          We get $82B/year redirected to cures.<br/>
          That's 32,156X return.
        </p>
      </div>

      <div className="border-2 border-black p-6 mb-8">
        <p className="text-2xl font-bold mb-4">Step 2: Tinder for Budget Allocation</p>
        <p className="mb-3">
          Current system: 12 FDA bureaucrats decide everything.
        </p>
        <p>
          New system: 280 million people swipe right on cancer research.
        </p>
        <p className="mt-3">
          Your mom has diabetes? You vote diabetes trials.<br/>
          No committees. No gatekeepers. Just an app.
        </p>
      </div>

      <div className="border-2 border-black p-6 mb-8">
        <p className="text-2xl font-bold mb-4">Step 3: Amazon Prime for Clinical Trials</p>
        <p className="mb-3">
          Current system: Drive 200 miles. Wait 6 months. Get placebo. Die.
        </p>
        <p>
          New system: Pills arrive Tuesday. Apple Watch tracks results.
        </p>
        <p className="mt-3">
          10,000X more participants = 100X faster results.
        </p>
      </div>

      <div className="border-t border-b border-black py-6 my-8">
        <p className="text-xl font-bold mb-3">What Actually Happens:</p>
        <p className="mb-2">
          2028: We lobby. Congress passes 1% Treaty.
        </p>
        <p className="mb-2">
          2030: First cures ship. Diabetes gone. China's pissed.
        </p>
        <p className="mb-2">
          2035: VICTORY bonds pay 18% annually. Forever.
        </p>
        <p>
          2040: You're still alive. And rich.
        </p>
      </div>

      <div className="border-2 border-black p-6 mb-8">
        <p className="text-xl font-bold mb-3">Why This Works:</p>
        <ul className="space-y-2">
          <li>• It's not charity. Defense contractors pivot to biodefense.</li>
          <li>• It's not democratic. It's wishocratic. You join trials, funding follows.</li>
          <li>• It's not revolutionary. Same corrupt system, backwards.</li>
          <li>• It's not idealistic. Everyone's motivated by greed.</li>
        </ul>
        <p className="mt-4 font-bold">
          We're literally too greedy to die.
        </p>
      </div>

      <div className="space-y-4">
        <button
          onClick={() => router.push('/join')}
          className="block w-full text-left border-2 border-black p-6 hover:bg-gray-100"
        >
          <span className="text-2xl font-bold">JOIN THE REFERENDUM</span><br/>
          <span className="text-gray-600">Be one of 280 million →</span>
        </button>

        <button
          onClick={() => router.push('/victory-bonds')}
          className="block w-full text-left border-2 border-black p-6 hover:bg-gray-100"
        >
          <span className="text-2xl font-bold">GET VICTORY BONDS</span><br/>
          <span className="text-gray-600">18% returns forever →</span>
        </button>

        <button
          onClick={() => router.push('/')}
          className="block w-full text-left border border-gray-400 p-4 hover:bg-gray-50 text-sm"
        >
          ← Back to reality
        </button>
      </div>

      <p className="text-sm text-gray-600 mt-12 italic">
        This isn't a feel-good charity. It's a hostile takeover of the death industry.
      </p>
    </div>
  );
}