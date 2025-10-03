'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { ConnectButton } from '@rainbow-me/rainbowkit';
import { useAccount } from 'wagmi';

export default function JoinReferendum() {
  const router = useRouter();
  const { address, isConnected } = useAccount();
  const [email, setEmail] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Integrate with actual backend to store referendum signups
    console.log('Signup:', { address, email });
    setSubmitted(true);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-black via-blue-950/20 to-black text-white">
      <div className="max-w-4xl mx-auto px-4 py-20">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-6xl md:text-7xl font-bold mb-6">
            Join the Global Referendum
          </h1>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Become one of the 280 million people voting on humanity's future
          </p>
        </div>

        {!submitted ? (
          <div className="space-y-8">
            {/* Benefits */}
            <div className="bg-gradient-to-br from-blue-950/30 to-purple-950/30 border border-blue-900 rounded-2xl p-8">
              <h2 className="text-3xl font-bold mb-6">What You Get</h2>
              <div className="space-y-4">
                <div className="flex items-start gap-4">
                  <div className="text-3xl">🗳️</div>
                  <div>
                    <div className="font-bold text-lg mb-1">Voting Power</div>
                    <div className="text-gray-400">
                      Vote on which medical trials get funded through the DIH (Decentralized Institutes of Health)
                    </div>
                  </div>
                </div>
                <div className="flex items-start gap-4">
                  <div className="text-3xl">💊</div>
                  <div>
                    <div className="font-bold text-lg mb-1">Subsidized Trial Access</div>
                    <div className="text-gray-400">
                      Eligible for discounted participation in dFDA trials for conditions you or your family face
                    </div>
                  </div>
                </div>
                <div className="flex items-start gap-4">
                  <div className="text-3xl">💎</div>
                  <div>
                    <div className="font-bold text-lg mb-1">VICTORY Bond Priority</div>
                    <div className="text-gray-400">
                      Early allocation access to bonds paying 10% of the perpetual health dividend (estimated 40%+ annual returns)
                    </div>
                  </div>
                </div>
                <div className="flex items-start gap-4">
                  <div className="text-3xl">🌍</div>
                  <div>
                    <div className="font-bold text-lg mb-1">Founder Status</div>
                    <div className="text-gray-400">
                      Recognized as one of the 280M founding members who made this happen
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Signup Form */}
            <div className="bg-gray-900/50 border border-gray-800 rounded-2xl p-8">
              <h2 className="text-2xl font-bold mb-6">Sign Up</h2>

              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Web3 Wallet */}
                <div>
                  <label className="block text-sm font-medium mb-3 text-gray-400">
                    Connect Wallet (Recommended)
                  </label>
                  <div className="flex justify-start">
                    <ConnectButton />
                  </div>
                  {isConnected && (
                    <div className="mt-3 text-green-500 text-sm flex items-center gap-2">
                      <span>✓</span>
                      <span>Wallet connected: {address?.slice(0, 6)}...{address?.slice(-4)}</span>
                    </div>
                  )}
                  <p className="mt-2 text-xs text-gray-500">
                    Your wallet address is used for voting, trial eligibility, and VICTORY bond allocations
                  </p>
                </div>

                {/* Divider */}
                <div className="flex items-center gap-4">
                  <div className="flex-1 border-t border-gray-700"></div>
                  <div className="text-gray-500 text-sm">OR</div>
                  <div className="flex-1 border-t border-gray-700"></div>
                </div>

                {/* Email */}
                <div>
                  <label htmlFor="email" className="block text-sm font-medium mb-3 text-gray-400">
                    Email Address
                  </label>
                  <input
                    type="email"
                    id="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="your@email.com"
                    className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
                    required={!isConnected}
                  />
                  <p className="mt-2 text-xs text-gray-500">
                    We'll email you when the referendum goes live and send trial eligibility updates
                  </p>
                </div>

                {/* Submit */}
                <button
                  type="submit"
                  disabled={!isConnected && !email}
                  className="w-full px-8 py-4 bg-green-600 hover:bg-green-700 disabled:bg-gray-700 disabled:cursor-not-allowed text-white rounded-xl text-lg font-bold transition-all transform hover:scale-105 disabled:transform-none"
                >
                  {isConnected || email ? 'Join the Referendum' : 'Connect Wallet or Enter Email'}
                </button>
              </form>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
              <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-6">
                <div className="text-3xl font-bold text-blue-400 mb-2">280M</div>
                <div className="text-gray-400 text-sm">Target referendum participants</div>
              </div>
              <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-6">
                <div className="text-3xl font-bold text-green-400 mb-2">1.2M</div>
                <div className="text-gray-400 text-sm">Signups so far</div>
              </div>
              <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-6">
                <div className="text-3xl font-bold text-purple-400 mb-2">0.4%</div>
                <div className="text-gray-400 text-sm">Progress to threshold</div>
              </div>
            </div>
          </div>
        ) : (
          <div className="bg-green-950/30 border-2 border-green-600 rounded-2xl p-12 text-center">
            <div className="text-6xl mb-6">✅</div>
            <h2 className="text-4xl font-bold mb-4">You're In!</h2>
            <p className="text-xl text-gray-300 mb-8">
              You're now registered for the global referendum.
            </p>
            <div className="space-y-4 max-w-md mx-auto">
              <div className="text-left bg-green-950/20 border border-green-800 rounded-lg p-4">
                <div className="font-bold mb-2">✓ Voting rights secured</div>
                <div className="text-sm text-gray-400">You'll vote on trial funding through the DIH</div>
              </div>
              <div className="text-left bg-green-950/20 border border-green-800 rounded-lg p-4">
                <div className="font-bold mb-2">✓ Trial eligibility activated</div>
                <div className="text-sm text-gray-400">Access to subsidized dFDA trials</div>
              </div>
              <div className="text-left bg-green-950/20 border border-green-800 rounded-lg p-4">
                <div className="font-bold mb-2">✓ VICTORY bond priority</div>
                <div className="text-sm text-gray-400">Early allocation when bonds launch</div>
              </div>
            </div>
            <div className="mt-8 space-y-3">
              <button
                onClick={() => router.push('/victory-bonds')}
                className="block w-full max-w-md mx-auto px-8 py-4 bg-yellow-700 hover:bg-yellow-600 text-white rounded-xl text-lg font-bold transition-all"
              >
                💎 Learn About VICTORY Bonds
              </button>
              <button
                onClick={() => router.push('/')}
                className="block w-full max-w-md mx-auto px-8 py-3 bg-gray-800 hover:bg-gray-700 text-white rounded-xl transition-all"
              >
                ← Back to Home
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
