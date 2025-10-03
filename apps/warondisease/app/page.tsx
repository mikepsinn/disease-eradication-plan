'use client';

import { useRouter } from 'next/navigation';

export default function Home() {
  const router = useRouter();

  return (
    <div className="max-w-2xl mx-auto px-6 py-12 font-serif">
      {/* The Absurd Chart */}
      <div className="mb-12">
        <p className="text-2xl font-bold mb-4">Annual Spending (to scale)</p>

        <div className="flex gap-8" style={{ height: '800px' }}>
          {/* Military Spending - $2.7T */}
          <div className="flex-1">
            <div className="w-full bg-black h-full">
              <div className="flex items-start justify-center pt-4">
                <span className="text-white font-bold text-xl">$2.7 trillion</span>
              </div>
            </div>
          </div>

          {/* Medical Research - $68B */}
          <div className="flex-1 relative">
            <div className="absolute bottom-0 w-full bg-red-600" style={{ height: '20px' }}>
              {/* 68B is 2.5% of 2.7T, so 20px of 800px */}
            </div>
          </div>
        </div>

        {/* Labels below the chart */}
        <div className="flex gap-8 mt-4">
          <div className="flex-1 text-center">
            <p className="font-bold">Military</p>
            <p className="text-sm text-gray-600">Professional murder</p>
          </div>
          <div className="flex-1 text-center">
            <p>All Medical Research</p>
            <p className="text-xs text-gray-600">($68 billion)</p>
            <p className="text-xs text-gray-600">↑ That tiny red bar</p>
          </div>
        </div>

        <p className="text-sm text-gray-600 mt-6 italic">
          We spend 40 times more on killing than curing. The research bar is 2.5% the height.
        </p>
      </div>

      <h1 className="text-4xl font-bold mb-8">
        We spend 40X more on war than medical research.
      </h1>

      <p className="text-xl mb-8">
        $2.7 trillion on weapons.<br/>
        $68 billion on cures.<br/>
        Your mom will die because we needed another submarine.
      </p>

      <div className="border-t border-b border-black py-8 my-8">
        <p className="text-2xl font-bold mb-4">
          The $119 Trillion Death Toilet
        </p>
        <p className="mb-3">
          War costs: $9.7 trillion/year (direct + destruction)
        </p>
        <p className="mb-3">
          Disease burden: $109.1 trillion/year (healthcare + lost productivity)
        </p>
        <p className="mb-3">
          Total death toilet: $118.8 trillion/year
        </p>
        <p className="font-bold">
          Medical research: $68 billion (0.06% of the problem)
        </p>
      </div>

      <p className="text-xl mb-8">
        Things we spend more on than curing cancer:
      </p>
      <ul className="space-y-2 text-lg mb-8">
        <li>• Halloween costumes ($12B)</li>
        <li>• Pentagon coffee budget ($1.2B)</li>
        <li>• Military marching bands ($437M)</li>
        <li>• One F-35 fighter jet ($80M) = entire rare disease budget</li>
      </ul>

      <p className="text-xl mb-8">
        The Pentagon lost $2.5 trillion.<br/>
        Just... lost it.<br/>
        That's 37 years of ALL medical research.
      </p>

      <div className="border-2 border-black p-6 my-8">
        <p className="text-xl font-bold mb-4">
          The 1% Treaty:
        </p>
        <p className="mb-3">
          Take 1% of military spending ($27 billion).
        </p>
        <p className="mb-3">
          Add it to medical research ($68B → $95B).
        </p>
        <p>
          That's a 40% increase in humanity's entire research budget.
        </p>
      </div>

      <p className="text-2xl font-bold mb-8">
        Want to keep dying from preventable diseases?
      </p>

      <div className="space-y-4">
        <button
          onClick={() => router.push('/idiocracy')}
          className="block w-full text-left border-2 border-black p-6 hover:bg-gray-100"
        >
          <span className="text-2xl font-bold">YES, I LOVE DYING</span><br/>
          <span className="text-gray-600">Keep the status quo →</span>
        </button>

        <button
          onClick={() => router.push('/wishonia')}
          className="block w-full text-left border-2 border-black p-6 hover:bg-gray-100"
        >
          <span className="text-2xl font-bold">NO, I'D RATHER NOT</span><br/>
          <span className="text-gray-600">See the 1% solution →</span>
        </button>
      </div>

      <p className="text-sm text-gray-600 mt-12 italic">
        150,000 people die every day. 95% of diseases have zero approved treatments.
      </p>
    </div>
  );
}