# Automated Engagement Tracking Workflow

**Purpose:** Never lose a lead, never miss a follow-up, never forget a conversation
**System:** Airtable + Email + Calendar + Automation
**Goal:** Turn every interaction into a tracked, measurable opportunity to advance the mission

---

## The Philosophy: CRM as a Second Brain

Most movements fail not because the idea is bad, but because they lose track of people. Someone emails you interest in helping. You mean to respond. Life happens. Two weeks later, they've moved on.

This system makes that impossible. Every person who touches your organization gets:
1. A permanent record
2. Automatic follow-up reminders
3. A clear path from "curious stranger" to "active contributor"

Think of it as a conveyor belt for converting interest into impact.

---

## The Core Workflow

### Step 1: Capture (Zero Manual Entry)

**Every engagement creates a record automatically:**

#### Source: Website Form Submission
- User submits referendum vote → Airtable record created in `Global Referendum`
- Automation creates linked record in `Personnel Roster`
- Automation creates record in `Engagements` with Type = "Enlistment"

#### Source: Email to info@warondisease.com
- Use Zapier/Make.com to parse incoming emails
- Auto-create `Personnel` record if new email
- Auto-create `Engagement` record with Type = "Email" and email body as Summary

#### Source: Meeting/Call
- Use Calendly webhook when meeting booked
- Auto-create `Personnel` record if new
- Auto-create `Engagement` record with Type = "Meeting" and Follow-up Date = 7 days later

#### Source: Social Media DM
- Harder to automate, but possible with APIs
- Manual fallback: Daily 5-minute sweep to log DMs

**The Rule:** If it's not in Airtable, it didn't happen.

---

### Step 2: Classify (Automatic Tagging)

When an engagement is created, automatically classify the person:

#### Engagement Types → Personnel Status

```
Engagement Type          →  Personnel Status
─────────────────────────────────────────────
Referendum Vote          →  Prospect
Interest Form Submit     →  Prospect
Meeting Scheduled        →  Active (upgrade)
Donation Made            →  Active (upgrade)
Investment Inquiry       →  Prospect (VIP tag)
Partnership Inquiry      →  Prospect (Partnership tag)
```

**Implementation:** Airtable automation
- Trigger: New record in `Engagements`
- Condition: Check engagement type
- Action: Update linked `Personnel` record Status field

---

### Step 3: Route (Assign Ownership)

Not all leads are equal. Route to the right person:

| Engagement Type | Routed To | SLA (Response Time) |
|----------------|-----------|-------------------|
| VICTORY Bond Interest > $100K | Founder | 4 hours |
| VICTORY Bond Interest < $100K | Finance Lead | 24 hours |
| Partnership Inquiry | Partnerships Lead | 48 hours |
| Volunteer Interest | Volunteer Coordinator | 72 hours |
| General Inquiry | Anyone available | 5 days |

**Implementation:** Airtable automation
- Trigger: New `Engagement` record created
- Condition: If Type = "Investment Inquiry" AND Amount > $100,000
- Action:
  - Assign to Founder in `Engagements` table
  - Send Slack notification to #high-value-leads
  - Send email to founder@warondisease.com
  - Create calendar reminder in 4 hours if not responded

---

### Step 4: Nurture (Automated Follow-Up Sequences)

People need multiple touches before they act. Build sequences:

#### Sequence 1: Referendum Voter → Active Recruiter

**Goal:** Convert passive voter into active promoter

**Timeline:**
- **Day 0:** Vote submitted
  - Send thank you email with referral link
  - Log engagement: Type = "Enlistment"

- **Day 3:** Check if they've referred anyone
  - If YES: Send "You're a Hero" email, upgrade to Tier 2
  - If NO: Send "Share with 3 Friends" reminder email
  - Log engagement: Type = "Email"

- **Day 7:** Check again
  - If they've referred 3+: Upgrade to Tier 2, send congrats
  - If they've referred 1-2: Send "Almost There" email
  - If they've referred 0: Send final reminder with new angle

- **Day 30:** Re-engage cold voters
  - Email: "Here's what's happened since you voted..."
  - Show referendum progress, new milestone

**Implementation:** Use Airtable automations + delay steps

```
Automation: "Referendum Voter Nurture Sequence"

Trigger: Record created in Global Referendum
Action 1: Send email (Day 0 welcome)
Action 2: Wait 3 days
Action 3: Conditional - Check if Referral Source count > 0
  - If YES: Send email variant A
  - If NO: Send email variant B
Action 4: Wait 4 days
Action 5: Conditional - Check referral count again
  - Branch based on 0, 1-2, or 3+ referrals
Action 6: Wait 23 days
Action 7: Send re-engagement email
```

---

#### Sequence 2: VICTORY Bond Prospect → Committed Investor

**Goal:** Move from "interesting" to "wired the money"

**Timeline:**
- **Hour 0:** Interest form submitted
  - Send personal email from founder
  - Log engagement: Type = "Investment Inquiry"
  - Assign to Finance Lead

- **Hour 4:** If no response
  - Slack alert: "URGENT: High-value lead going cold"

- **Day 1:** Send pitch deck + FAQ
  - Log engagement: Type = "Email"

- **Day 3:** Follow-up call invite
  - "Would love to answer questions. Calendar link here."

- **Day 7:** If no call scheduled
  - Send case studies of similar investors

- **Day 14:** If still no movement
  - Re-engage with new angle: "The ROI Math That Made [Other Investor] Say Yes"

- **Day 30:** Final touch
  - "We're moving forward. Last chance to get in at this valuation."

**Notes:**
- High-touch, not automated blast
- Each email should feel personal
- Log EVERYTHING in Engagements table

---

#### Sequence 3: Partnership Inquiry → Signed MOU

**Goal:** Organizations that can amplify the mission

**Timeline:**
- **Day 0:** Inquiry received
  - Send partnership deck
  - Schedule intro call (Calendly link)
  - Log engagement: Type = "Partnership Inquiry"

- **Day 2:** Pre-call research
  - Automation: Create `Organizations` record
  - Assign team member to research org
  - Prepare talking points based on their mission

- **Day 3-7:** Call happens
  - Log engagement: Type = "Meeting"
  - Set Follow-up Date based on call outcome

- **Day 8:** Follow-up email
  - Recap + next steps
  - Share specific collaboration ideas

- **Day 21:** If no movement
  - "Checking in - still interested in [specific collaboration]?"

---

### Step 5: Measure (Conversion Tracking)

Track conversion rates at each step:

#### Funnel: Website Visitor → Active Contributor

```
Stage                     Target Conversion   How to Track
─────────────────────────────────────────────────────────
Website Visit               100%             Google Analytics
→ Form View                 30%              GA pageview
→ Form Start                50%              Airtable log
→ Form Submit               80%              Record created
→ Email Confirmed           90%              Email bounce check
→ Shared w/ 1 Friend        30%              Referral field filled
→ Shared w/ 3+ Friends      10%              Count in Global Ref
→ Became Volunteer          5%               Status = Active
```

**Implementation:** Create Airtable formulas to calculate these

#### Formula Example: "Conversion to Recruiter"

In `Personnel Roster` table, add formula field:
```
IF(
  {Referendum Votes} > 0,
  IF(
    COUNTALL({Global Referendum 2}) > 0,
    "✅ Recruiter",
    "⏳ Passive Voter"
  ),
  "❌ No Vote"
)
```

---

### Step 6: Escalate (Alert on Anomalies)

Watch for patterns that need human intervention:

#### Alert Triggers:

1. **High-Value Lead Going Cold**
   - Condition: Investment Inquiry > $50K + No follow-up engagement in 48 hours
   - Action: Slack alert to founder

2. **Viral Recruit Champion**
   - Condition: Personnel has referred 10+ people
   - Action: Send personal thank you + upgrade perks

3. **Negative Sentiment Detected**
   - Condition: Email/engagement contains keywords: "scam", "disappointed", "misleading"
   - Action: Alert customer success lead for immediate response

4. **Regional Breakout**
   - Condition: One country suddenly has 100+ votes in 24 hours
   - Action: Investigate (could be fraud OR awesome organic growth)

**Implementation:** Airtable automations with conditional logic

---

## Advanced: Email Automation Integration

For sophisticated email sequences, integrate with:

### Option A: Airtable Native Email (Basic)
- Pros: Simple, built-in
- Cons: Limited styling, no A/B testing, manual unsubscribe handling

### Option B: Airtable + MailerLite/Mailchimp (Better)
- Pros: Professional emails, automation, unsubscribe management
- Cons: Extra cost ($10-50/month), requires Zapier integration

### Option C: Airtable + Customer.io or Intercom (Best)
- Pros: Sophisticated triggers, behavior-based sequences, analytics
- Cons: Expensive ($100-500/month), more complex setup

**Recommended for Pre-Seed:** Start with Option A, graduate to Option B at 1,000+ contacts.

---

## The Daily Workflow for Team

### Morning Routine (15 minutes):

1. **Open "Today's Follow-Ups" view**
   - Filter: `Engagements` where `Follow-up Date` = Today
   - Sort by Priority (Critical → Low)

2. **Review High-Value Leads**
   - Filter: `Engagements` where Type = "Investment Inquiry" AND Status = "Active"
   - Check for responses, schedule calls

3. **Check Verification Queue**
   - Filter: `Global Referendum` where Verification Status = "Pending"
   - Verify emails, mark as Verified or flag as fraud

### Weekly Routine (30 minutes):

1. **Metrics Review**
   - Total votes this week vs. last week
   - Conversion rates through funnel
   - Cost per vote (ad spend ÷ votes)
   - Viral coefficient (avg referrals per voter)

2. **Outreach Planning**
   - Identify top 10 prospects who haven't engaged
   - Craft personalized re-engagement emails
   - Update follow-up dates

3. **Data Cleanup**
   - Merge duplicate personnel records
   - Fix broken links between tables
   - Archive dead leads (Status → Inactive)

---

## Templates: Copy-Paste Automation Configs

### Template 1: New Vote → Thank You Email

```
AUTOMATION CONFIG

Name: "New Referendum Vote - Send Thank You"
Trigger: When record created in table "Global Referendum"
Condition: None
Actions:
  1. Send email
     To: {Email} (from linked Personnel record)
     From: votes@warondisease.com
     Subject: Your Vote for the 1% Treaty is Recorded
     Body:
       Hi {Full Name},

       Your vote has been recorded. You're now part of the 3.5%
       that will change the world.

       Your Reward Tier: {Reward Tier}
       Your Country: {Country}

       TRIPLE YOUR REWARDS:
       Share your unique link with 3 friends:
       https://vote.warondisease.com?ref={VOTER_ID}

       When they vote, you move to Tier 2.

       Thank you for choosing life over war.

       - The DIH Team
```

---

### Template 2: High-Value Investment Lead → Founder Alert

```
AUTOMATION CONFIG

Name: "High-Value VICTORY Bond Lead - Alert Founder"
Trigger: When record created in table "VICTORY Bonds"
Condition: IF {Amount Invested} > 100000
Actions:
  1. Send Slack message
     Channel: #high-value-leads
     Message:
       🚨 HIGH-VALUE LEAD ALERT

       Investor: {Investor}
       Amount Interest: ${Amount Invested}
       Notes: {Notes}

       [Open in Airtable]({Record URL})

       Response SLA: 4 hours

  2. Send email
     To: founder@warondisease.com
     Subject: 🚨 URGENT: $100K+ VICTORY Bond Interest
     Body: [Same as Slack message]

  3. Create calendar event
     Calendar: Founder's calendar
     Title: FOLLOW UP: {Investor} Investment Lead
     Time: 4 hours from now
     Description: If not responded by then, URGENT escalation
```

---

### Template 3: 7-Day Inactive Voter → Re-engagement

```
AUTOMATION CONFIG

Name: "Re-engage Passive Voters"
Trigger: Scheduled (runs daily at 9am)
Condition:
  - Table: Global Referendum
  - Filter: Date Voted is 7 days ago
  - AND: Referral Source count = 0
Actions:
  1. Send email
     To: {Email}
     Subject: You Voted. But We Need Your Voice.
     Body:
       {Full Name},

       You voted YES to redirect 1% of military spending to cure disease.

       That's brave. But voting alone won't win this war.

       In the 7 days since you voted:
       - 123,000 people died of preventable disease
       - 3,847 new people joined the referendum
       - $0 moved from bombs to cures

       We need you to share this with just 3 people.

       Your link: https://vote.warondisease.com?ref={VOTER_ID}

       We're 3.5% of the way to the tipping point. You can push us closer.

       Will you?
```

---

## Common Pitfalls to Avoid

### 1. Over-Automation
**Problem:** Sending too many emails, feeling spammy
**Solution:** Cap at 1 email/week per person unless they engage

### 2. Under-Tracking
**Problem:** Having conversations outside Airtable, losing follow-ups
**Solution:** "If it's not logged, it didn't happen" rule

### 3. No Segmentation
**Problem:** Sending same message to $10 donor and $100K investor
**Solution:** Create segments based on engagement value/type

### 4. Ignoring Unsubscribes
**Problem:** Legal violations, pissed-off people
**Solution:** Honor unsubscribes immediately, it's the law

### 5. Manual Follow-Ups
**Problem:** Relying on memory = guaranteed drops
**Solution:** Set Follow-up Date on EVERY engagement

---

## Success Metrics

Track these weekly:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Engagement Log Rate | 100% | All interactions logged in Airtable |
| Follow-Up On-Time Rate | 90%+ | Follow-ups completed by due date |
| Response Rate | 40%+ | Replies to outreach emails |
| Conversion: Prospect → Active | 20%+ | Status changes in Personnel |
| Avg Time to First Response | <24hrs | Engagement created → first reply |
| Lead Leak Rate | <5% | Inquiries with no engagement record |

---

## Next-Level: AI-Powered Engagement

Once you have 1,000+ engagements logged, you can train AI to:

1. **Auto-Categorize Sentiment**
   - Use GPT API to analyze engagement summaries
   - Tag as Positive/Neutral/Negative
   - Alert on negative

2. **Suggest Next Best Action**
   - Based on engagement history, predict what to do next
   - "This person is similar to 15 others who became donors after..."

3. **Draft Follow-Up Emails**
   - AI reads engagement history
   - Drafts personalized follow-up
   - Human approves before sending

**Cost:** ~$50/month for OpenAI API at this scale
**ROI:** 10x time savings on personalization

---

## Conclusion

This engagement tracking workflow ensures **zero people fall through the cracks**.

Every vote, every email, every call is captured, categorized, and converted into the next step toward victory.

It's the difference between a movement that fizzles and one that reaches the 3.5% tipping point.

**Now implement it. Your first 100 conversations will set the template for the next 100 million.**
