# 1% Treaty Referendum - Deployment Guide

**The secure way to deploy your referendum landing page**

**TL;DR:** Use Cloudflare Workers + Pages. It's faster, cheaper, and simpler than Netlify/Vercel.

---

## Quick Deploy (5 Minutes)

### Prerequisites

1. **Cloudflare account** (free): <https://dash.cloudflare.com/sign-up>
2. **Wrangler CLI** installed: `npm install -g wrangler`
3. **Your Airtable API key** from <https://airtable.com/account>

### Step 1: Login to Cloudflare

```bash
wrangler login
```

### Step 2: Set Environment Variables (Secrets)

```bash
cd apps/1percenttreaty

# Set API key (paste when prompted)
wrangler secret put AIRTABLE_API_KEY
# Paste your Airtable API key here (format: patXXXXXXXXXXXXXX...)

# Set base ID
wrangler secret put AIRTABLE_BASE_ID
# Paste your Airtable base ID here (format: appXXXXXXXXXXXXXX)
```

### Step 3: Deploy Worker (API Proxy)

```bash
wrangler deploy
```

**Output:**

```
✨ Deployed worker to:
   https://1percent-treaty-referendum.YOUR_SUBDOMAIN.workers.dev
```

### Step 4: Deploy Static Site

```bash
npx wrangler pages deploy . --project-name=1percent-treaty
```

**Output:**

```
✨ Deployed to:
   https://1percent-treaty.pages.dev
```

### Step 5: Test It

1. Visit your Pages URL
2. Fill out the form
3. Submit
4. Check your Airtable - vote should appear!

**Done!** You now have a globally distributed, secure referendum platform.

---

## Why Cloudflare Over Netlify/Vercel?

| Feature | Cloudflare | Netlify | Vercel |
|---------|-----------|---------|--------|
| **Free requests/month** | 3,000,000 | 125,000 | 100,000 |
| **Edge locations** | 300+ cities | ~10 regions | ~50 regions |
| **Cold starts** | None | ~100ms | ~100ms |
| **Setup complexity** | Simplest | Medium | Medium |
| **DDoS protection** | Included | Extra $ | Extra $ |
| **Cost at 1M votes** | FREE | $19/mo | $20/mo |

**Verdict:** Cloudflare is 10-30x cheaper at scale and faster globally.

---

## Custom Domain Setup

### Option 1: Add Domain to Cloudflare (Recommended)

**If you own a domain:**

1. Cloudflare dashboard → Add site → Enter your domain
2. Update nameservers at your registrar (Namecheap, Google Domains, etc.)
3. Wait for DNS propagation (~5 min)
4. Cloudflare Pages → Custom domains → Add `1percenttreaty.org`
5. Cloudflare Workers → Routes → Add route `1percenttreaty.org/api/*`

**Done!** Automatic HTTPS included.

### Option 2: Use Subdomain (Faster)

**If you have `warondisease.com` already on Cloudflare:**

1. Cloudflare Pages → Custom domains → Add `vote.warondisease.com`
2. Workers → Routes → Add `vote.warondisease.com/api/*`

**Live in 2 minutes.**

---

## Local Development

### Run Static Site Locally

```bash
cd apps/1percenttreaty

# Python
python -m http.server 8000

# Node.js
npx serve .
```

Visit `http://localhost:8000`

### Test Worker Locally

```bash
wrangler dev
```

**Important:** Create `.dev.vars` file for local secrets:

```bash
# File: apps/1percenttreaty/.dev.vars
# DO NOT COMMIT THIS FILE

AIRTABLE_API_KEY=patAQEwwKXChpQBnL.xxx
AIRTABLE_BASE_ID=appRA45hnZpiTyRjB
```

Add to `.gitignore`:

```
.dev.vars
```

---

## Monitoring & Debugging

### View Real-Time Logs

```bash
wrangler tail
```

Shows every request hitting your worker live.

### Cloudflare Analytics

Dashboard → Workers → Metrics shows:

- Requests per second
- Error rate
- Success rate
- CPU time

### Debug Failed Submissions

If votes aren't appearing in Airtable:

1. Check `wrangler tail` for errors
2. Verify environment variables: `wrangler secret list`
3. Test Airtable API key manually:

   ```bash
   curl https://api.airtable.com/v0/appRA45hnZpiTyRjB/Personnel%20Roster \
     -H "Authorization: Bearer YOUR_API_KEY"
   ```

---

## Security Checklist

Before going public:

- [ ] API keys stored as Cloudflare secrets (not in code)
- [ ] `.dev.vars` in `.gitignore`
- [ ] HTTPS enabled (automatic with Cloudflare)
- [ ] CORS configured (already in worker.js)
- [ ] Email validation enabled (already in worker.js)
- [ ] Test submissions working end-to-end
- [ ] Monitor logs for spam patterns

### Optional: Add Rate Limiting

Prevent spam (1 vote per email per hour):

```javascript
// In worker.js, add Cloudflare KV for rate limiting
const rateLimitKey = `vote:${email}`;
const recent = await env.VOTES_KV.get(rateLimitKey);

if (recent) {
  return new Response(JSON.stringify({
    error: 'You can only vote once per hour'
  }), { status: 429 });
}

await env.VOTES_KV.put(rateLimitKey, 'voted', { expirationTtl: 3600 });
```

**Setup:**

```bash
wrangler kv:namespace create "VOTES_KV"
# Add namespace ID to wrangler.toml
```

---

## Cost Analysis

### Free Tier Limits (Cloudflare)

- **Workers:** 100,000 requests/day = 3M/month
- **Pages:** Unlimited bandwidth
- **KV storage:** 100,000 reads/day (for rate limiting)

**Translation:** Handle 3 million votes per month for $0.

### When You Need to Pay

**At 5M+ votes/month:**

- Cloudflare Workers Paid: $5/month (removes limits)
- Still cheaper than competitors

**At 50K+ votes in Airtable:**

- Airtable Plus: $20/month
- OR migrate to PostgreSQL/Supabase: $25/month

**Total at scale:** ~$25-30/month for millions of votes.

---

## Comparison to Airtable Forms

| Feature | Cloudflare + Custom | Airtable Forms |
|---------|---------------------|----------------|
| **Design control** | Full | Limited |
| **Branding** | Your brand | Airtable logo |
| **Custom logic** | Yes | No |
| **Speed** | Faster | Slower |
| **Setup time** | 5 min | 2 min |
| **Security** | Equal | Equal |

**Recommendation:**

- **Week 1 MVP:** Use Airtable Forms (fastest test)
- **Week 2+ Public:** Deploy Cloudflare version (professional)

---

## Troubleshooting

### "CORS error" in browser console

**Cause:** Worker not allowing cross-origin requests
**Fix:** Already handled in worker.js (check `Access-Control-Allow-Origin` header)

### "Failed to submit vote"

**Check:**

1. Are secrets set? `wrangler secret list`
2. Is worker deployed? `wrangler deployments list`
3. Check logs: `wrangler tail`
4. Test Airtable connection manually

### "Worker timed out"

**Cause:** Free tier has 10ms CPU limit per request
**Fix:**

- Airtable calls are network time (not CPU), should be fine
- If still timing out, upgrade to Workers Paid ($5/mo)

### Votes not appearing in Airtable

**Check:**

1. Table names match exactly (case-sensitive)
2. Field names match exactly
3. Base ID is correct (appRA45hnZpiTyRjB)
4. API key has write permissions

---

## Advanced: GitHub Actions Auto-Deploy

**Automate deployments on every git push:**

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloudflare

on:
  push:
    branches: [master]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Deploy Worker
        uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          workingDirectory: apps/1percenttreaty
          command: deploy

      - name: Deploy Pages
        uses: cloudflare/pages-action@v1
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          projectName: 1percent-treaty
          directory: apps/1percenttreaty
```

**Setup:**

1. Get Cloudflare API token from dashboard
2. Add to GitHub repo secrets as `CLOUDFLARE_API_TOKEN`
3. Push code → Automatic deployment

---

## Next Steps

### Week 1: MVP Test

- [x] Deploy to Cloudflare
- [ ] Share with 50 friends
- [ ] Goal: 100 test votes

### Week 2: Public Beta

- [ ] Add custom domain
- [ ] Set up Google Analytics
- [ ] Goal: 1,000 votes

### Month 2: Scale

- [ ] Add email automation
- [ ] Build referral leaderboard
- [ ] Goal: 10,000 votes

### Month 3: Global

- [ ] Multi-language support
- [ ] Regional targeting
- [ ] Goal: 100,000 votes

---

**Full documentation:** See [apps/1percenttreaty/README.md](../../apps/1percenttreaty/README.md)

**Now deploy and start saving lives.**
