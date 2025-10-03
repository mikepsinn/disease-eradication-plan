'use client';

import { useRouter } from 'next/navigation';

export default function Home() {
  const router = useRouter();

  return (
    <div className="max-w-2xl mx-auto px-6 py-12 font-serif">
      <h1 className="text-4xl font-bold mb-8">
        The Pentagon lost $2.5 trillion.
      </h1>

      <p className="text-xl mb-6">
        That's enough to cure cancer 1,250 times.
      </p>

      <p className="text-xl mb-8">
        Your mom will die of something we could fix for the price of one missile.
      </p>

      <div className="border-t border-b border-black py-8 my-8">
        <p className="text-2xl font-bold mb-4">
          The $119 Trillion Death Toilet
        </p>
        <p className="mb-3">
          Every year: $119 trillion on war and disease.
        </p>
        <p className="mb-3">
          Medical research: $68 billion.
        </p>
        <p>
          That's $1,750 on death for every $1 on cures.
        </p>
      </div>

      <p className="text-xl mb-8">
        Halloween costumes: $12 billion/year<br/>
        All rare disease research: $7 billion/year
      </p>

      <p className="text-xl mb-8">
        One F-35 fighter jet: $80 million<br/>
        Entire childhood leukemia budget: $80 million
      </p>

      <div className="border-2 border-black p-6 my-8">
        <p className="text-xl font-bold mb-4">
          The Trick:
        </p>
        <p className="mb-3">
          Redirect 1% of military spending to medical research.
        </p>
        <p className="mb-3">
          The military keeps 99%.
        </p>
        <p>
          That 1% doubles global medical research.
        </p>
      </div>

      <p className="text-2xl font-bold mb-8">
        So what'll it be?
      </p>

      <div className="space-y-4">
        <button
          onClick={() => router.push('/idiocracy')}
          className="block w-full text-left border-2 border-black p-6 hover:bg-gray-100"
        >
          <span className="text-2xl font-bold">NO</span><br/>
          <span className="text-gray-600">Keep being idiots. See your death certificate →</span>
        </button>

        <button
          onClick={() => router.push('/wishonia')}
          className="block w-full text-left border-2 border-black p-6 hover:bg-gray-100"
        >
          <span className="text-2xl font-bold">YES</span><br/>
          <span className="text-gray-600">Try not dying. See how we pull it off →</span>
        </button>
      </div>

      <p className="text-sm text-gray-600 mt-12 italic">
        A practical guide to tricking humanity into not killing itself.
      </p>
    </div>
  );
}