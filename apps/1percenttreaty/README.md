# 1% Treaty Referendum Landing Page

**Atomic Age Propaganda-Style Voting Platform**

This is the secure, production-ready referendum landing page for collecting votes on the 1% Treaty. It uses Cloudflare Workers to keep Airtable API keys secret while maintaining a blazing-fast, globally distributed voting system.

---

## 🎨 Design Philosophy

Follows the DIH [DESIGN_GUIDE.md](../../DESIGN_GUIDE.md):

- **Black and white only** - Maximum contrast, timeless authority
- **1950s atomic age aesthetic** - Bold, urgent, propaganda poster style
- **Impact/Arial Black typography** - Strong, commanding fonts
- **Direct messaging** - No subtlety, just truth

**Visual inspiration:** "Atoms for Peace" campaign meets "We Can Do It!" posters

---

## 🏗️ Architecture

```
User Browser → index.html
     ↓
     ↓ POST /api/submit-vote
     ↓
Cloudflare Worker (worker.js) ← API key stored here (secret)
     ↓
     ↓ Authenticated API calls
     ↓
Airtable Base (DIH Command & Control)
     ├─ Personnel Roster (creates voter record)
     └─ Global Referendum (records vote)
```

**Security:** API keys never touch the browser. Worker runs on Cloudflare's edge network.

---

## 📁 Files

- **`index.html`** - Frontend landing page (black/white atomic age design)
- **`worker.js`** - Cloudflare Worker (serverless API proxy)
- **`wrangler.toml`** - Cloudflare configuration
- **`README.md`** - This file

---

## 🚀 Deployment Options

### Option 1: Cloudflare Pages + Workers (Recommended)

**Why Cloudflare:**

- ✅ **Fastest global CDN** (edge network in 300+ cities)
- ✅ **Most generous free tier** (100K requests/day free)
- ✅ **Zero cold starts** (Workers are instant)
- ✅ **Built-in DDoS protection**
- ✅ **Free SSL**
- ✅ **Simpler than Netlify/Vercel** (no build step needed)

**Free Tier Limits:**

- 100,000 requests per day
- 10ms CPU time per request
- 128MB memory
- **Translation:** Can handle ~3M votes/month for $0

---

## 📦 Quick Deploy (5 Minutes)

### Step 1: Install Wrangler CLI

```bash
npm install -g wrangler
```

### Step 2: Login to Cloudflare

```bash
wrangler login
```

### Step 3: Set Environment Variables

```bash
# Set your Airtable API key (NEVER commit this to git)
wrangler secret put AIRTABLE_API_KEY
# Paste: patAQEwwKXChpQBnL.d9ca339d66431e6cfece5a3fe1c1d69c6c36848386804a3b1bc773dfedcde127

# Set your Airtable base ID
wrangler secret put AIRTABLE_BASE_ID
# Paste: appRA45hnZpiTyRjB
```

### Step 4: Deploy Worker

```bash
cd apps/1percenttreaty
wrangler deploy
```

**Output:**

```
✨ Success! Uploaded worker '1percent-treaty-referendum'
🌎 https://1percent-treaty-referendum.YOUR_SUBDOMAIN.workers.dev
```

### Step 5: Deploy Static Site

```bash
# Deploy index.html to Cloudflare Pages
npx wrangler pages deploy . --project-name=1percent-treaty
```

**Output:**

```
✨ Success! Your site is live at:
   https://1percent-treaty.pages.dev
```

### Step 6: Test It

Visit your Pages URL and submit a test vote. Check your Airtable base for the new record.

---

## 🌐 Custom Domain Setup

### Add Your Domain to Cloudflare

1. Go to Cloudflare dashboard
2. Add site → Enter your domain (e.g., `1percenttreaty.org` or `vote.warondisease.com`)
3. Update nameservers at your registrar
4. Wait for DNS propagation (~5 minutes)

### Connect Pages to Custom Domain

1. Cloudflare Pages → Your project → Custom domains
2. Add custom domain: `1percenttreaty.org`
3. Cloudflare handles SSL automatically

### Route Worker to /api/*

1. Cloudflare Workers → Your worker → Triggers
2. Add route: `1percenttreaty.org/api/*`
3. Save

**Done!** Your site now uses your custom domain with automatic HTTPS.

---

## 🧪 Local Testing

### Test Static Site Locally

```bash
# Simple Python server
python -m http.server 8000

# Or Node.js
npx serve .
```

Visit `http://localhost:8000`

### Test Worker Locally

```bash
wrangler dev
```

This starts a local server with hot reload. Your worker runs at `http://localhost:8787/api/submit-vote`

**Note:** You'll need to set environment variables in `.dev.vars` file:

```bash
# Create .dev.vars (DO NOT COMMIT THIS FILE)
AIRTABLE_API_KEY=patAQEwwKXChpQBnL.xxx
AIRTABLE_BASE_ID=appRA45hnZpiTyRjB
```

---

## 📊 Monitoring & Analytics

### View Worker Logs

```bash
wrangler tail
```

This shows real-time logs of all requests hitting your worker.

### Cloudflare Analytics Dashboard

1. Cloudflare dashboard → Workers → Your worker → Metrics
2. See:
   - Requests per second
   - Errors
   - CPU time
   - Success rate

### Add Google Analytics (Optional)

Add to `<head>` of `index.html`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

---

## 🔒 Security Checklist

Before going live:

- [ ] **API keys are environment variables** (not in code)
- [ ] **HTTPS enabled** (automatic with Cloudflare)
- [ ] **CORS configured** (worker.js already handles this)
- [ ] **Email validation** (worker.js already validates)
- [ ] **Rate limiting** (optional - see below)
- [ ] **.dev.vars in .gitignore** (prevent accidental commits)

### Optional: Add Rate Limiting

Prevent spam submissions (1 vote per email per hour):

```javascript
// In worker.js, add before Airtable calls:

// Simple rate limiting with KV
const rateLimitKey = `ratelimit:${email}`;
const existing = await env.KV.get(rateLimitKey);

if (existing) {
  return new Response(JSON.stringify({
    error: 'You can only vote once per hour'
  }), { status: 429 });
}

// Set rate limit (expires in 1 hour)
await env.KV.put(rateLimitKey, 'voted', { expirationTtl: 3600 });
```

**Setup KV namespace:**

```bash
wrangler kv:namespace create "KV"
```

---

## 💰 Cost Estimates

### At 10,000 votes/month

- **Cloudflare Workers:** FREE (well under 100K/day limit)
- **Cloudflare Pages:** FREE
- **Airtable:** $20/month (Plus plan for 50K records)
- **Domain:** $12/year
- **Total:** ~$21/month

### At 100,000 votes/month

- **Cloudflare Workers:** FREE (still under limit)
- **Cloudflare Pages:** FREE
- **Airtable:** $20/month (or migrate to PostgreSQL)
- **Total:** ~$20/month

### At 1,000,000 votes/month

- **Cloudflare Workers:** $5/month (Workers Paid plan for extra CPU)
- **Cloudflare Pages:** FREE
- **Database:** Migrate to Supabase/PostgreSQL ($25-50/month)
- **Total:** ~$30-55/month

**Cloudflare is ~5x cheaper than Netlify/Vercel at scale.**

---

## 🐛 Troubleshooting

### "Failed to submit vote" error

**Check:**

1. Are environment variables set? Run: `wrangler secret list`
2. Is worker deployed? Run: `wrangler deployments list`
3. Check worker logs: `wrangler tail`

### CORS errors in browser

**Fix:** Ensure `Access-Control-Allow-Origin` header in worker response (already included)

### Airtable "Invalid request" error

**Check:**

1. Is base ID correct? (appRA45hnZpiTyRjB)
2. Do table names match exactly? (case-sensitive)
3. Do fields exist in Airtable?
4. Is API key valid?

### Worker timeout

**Cause:** Each Airtable API call adds latency
**Fix:** Workers have 50ms CPU limit on free tier. Optimize by batching or upgrading to paid tier.

---

## 🔄 Updates & Redeployment

After making changes:

```bash
# Redeploy worker
wrangler deploy

# Redeploy static site
npx wrangler pages deploy .
```

**Pro tip:** Set up GitHub Actions for automatic deployment on push.

---

## 📈 Next Steps

### Week 1: MVP Test

- Deploy to Cloudflare
- Share with 50 friends/family
- Goal: Validate voting works end-to-end

### Week 2: Public Beta

- Add custom domain
- Set up monitoring/analytics
- Goal: 1,000 votes

### Month 2: Scale

- Add email automation (SendGrid)
- Build referral leaderboard
- Optimize for virality
- Goal: 10,000 votes

### Month 3: Global Push

- Multi-language support
- Regional targeting
- Influencer partnerships
- Goal: 100,000 votes

---

## 🎯 Success Metrics

Track these in your Airtable base:

- **Total Votes:** Target 280M (3.5% of 8 billion)
- **Viral Coefficient:** Referrals per voter (need >1.0)
- **Conversion Rate:** Visitors → Voters (target 15-25%)
- **Cost Per Vote:** Ad spend ÷ votes (target <$0.50)
- **Geographic Distribution:** Which countries most engaged
- **Time to 3.5%:** Days until tipping point reached

---

## 📞 Support

**Technical Issues:**

- Cloudflare Workers docs: <https://developers.cloudflare.com/workers>
- Airtable API docs: <https://airtable.com/developers/web/api>

**Questions:**

- Open an issue in the repo
- Or email: <tech@warondisease.com>

---

**Now deploy and start collecting votes. Death doesn't wait.**
