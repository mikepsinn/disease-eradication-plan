# War on Disease - Choose-Your-Own-Adventure Website

Interactive web3 experience where users vote YES or NO on the 1% Treaty and see humanity's trajectory down either path (Idiocracy vs Wishonia).

## Features

- **Binary Choice Landing**: YES/NO vote on redirecting 1% of military spending to medical research
- **Idiocracy Timeline**: Shows extinction trajectory if we vote NO (escalating death tolls, missed cures)
- **Wishonia Timeline**: Shows Three Supers future if we vote YES (superintelligence, superlongevity, superhappiness)
- **Referendum Signup**: Web3 wallet + email signup for global referendum
- **VICTORY Bonds**: Calculator showing 40%+ returns from perpetual health dividend
- **Web3 Integration**: Wallet connection via RainbowKit (mainnet, Polygon, Optimism, Arbitrum, Base)

## The Flow

1. **Landing** → Choose YES or NO
2. **Idiocracy/Wishonia** → See timeline consequences
3. **Join** → Sign up for referendum (wallet or email)
4. **VICTORY Bonds** → Calculate investment returns

## Tech Stack

- **Framework**: Next.js 15 (App Router, TypeScript, Tailwind CSS)
- **Web3**: wagmi, viem, RainbowKit, TanStack Query
- **Chains**: Ethereum, Polygon, Optimism, Arbitrum, Base

## Setup

1. Install dependencies:

   ```bash
   npm install
   ```

2. Create `.env.local`:

   ```bash
   cp .env.local.example .env.local
   ```

3. Get a WalletConnect Project ID:
   - Visit <https://cloud.walletconnect.com/>
   - Create a project
   - Copy the Project ID to `.env.local`

4. Run dev server:

   ```bash
   npm run dev
   ```

5. Open [http://localhost:3000](http://localhost:3000)

## Pages

- `/` - Binary choice (YES/NO)
- `/idiocracy` - Extinction timeline (NO path)
- `/wishonia` - Three Supers timeline (YES path)
- `/join` - Referendum signup
- `/victory-bonds` - Investment calculator

## TODO (Backend Integration)

- [ ] Connect signup form to backend API
- [ ] Add vote tracking/analytics
- [ ] Smart contract for VICTORY bonds
- [ ] Referendum vote recording on-chain
- [ ] Trial eligibility verification system
- [ ] DIH wishocracy voting interface

## Philosophy

**Greed + Self-Preservation > Altruism**

This isn't a charity site. We're offering:

- 40% annual returns (VICTORY bonds)
- Subsidized trials (save your own life)
- Voting power (control medical research priorities)

Make curing people more profitable than killing them.

## Deploy on Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/your-repo/warondisease)

## License

MIT
