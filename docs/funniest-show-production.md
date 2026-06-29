# The Funniest Show in the Universe — Production Guide

Internal operations for recording, storing, and publishing episodes. The public page is `knowledge/strategy/funniest-show-in-the-universe.qmd`.

## Recording Setup

Use a remote local-recording tool for the primary capture. It should record separate audio and video tracks locally for the host and guest, then upload them after the call. Use OBS as the local backup and layout tool.

Do not rely on a single cloud recording. The first time a civilization gets a good answer, it should not be stored only inside a browser tab having a difficult afternoon.

Minimum deliverables:

- full video for YouTube
- MP3 audio for the show feed
- transcript
- captions
- three short clips
- one commissioner page in the manual

## Storage

Raw recordings do not belong in Git. They are too large, too private before release, and too annoying to clone.

Use this split:

- private raw recording backups: private cloud storage or private R2 bucket
- edited public video: YouTube
- public MP3, captions, thumbnails, and feed assets: Cloudflare R2
- public episode metadata, transcript, show notes, and commissioner pages: this manual repo

The existing audiobook feed stays the audiobook. This show gets its own feed when the first public audio edit exists.

Suggested public path:

`assets/show/funniest-show-in-the-universe/`

Suggested feed URL:

`https://static.warondisease.org/assets/show/funniest-show-in-the-universe/feed.xml`

## Episode Prep

Each episode gets one commissioner page in the manual (`knowledge/strategy/commissioners/<name>.qmd`) containing:

- commissioner name and affiliation
- public bio and relevant links
- opening appointment script
- five main questions
- mechanism pressure prompts
- commission order
- inauguration (at least two successor names)

Private contact details, calendar links, prep calls, raw video files, and anything the guest did not agree to publish stay out of the public repo.

## Episode 1: Andrew Trask

**Appointment script:**

> Andrew, you are now President of Earth Optimization Services. I am your assistant. Your job is to tell me how humanity should maximize median health-adjusted life expectancy and median after-tax inflation-adjusted income.
> You get Earth. You get no magic. You get current humans, current institutions, current incentives, current distrust, and current computers. What do we do first?

**Questions:**

1. **System design:** Describe in as much detail as you can all the components required for a decentralized, autonomous system that measures median health-adjusted life expectancy and median after-tax inflation-adjusted income in a privacy-preserving manner, computes optimal public policies and resource allocations, and enables world simulation for calculating the effects of different policy choices on the general welfare.
2. **Cost:** What is your 90% confidence interval for the total cost of building and deploying this system? Pilot, first ten countries, global scale. What fraction of one year's military spending is that?
3. **Smallest pilot:** What is the smallest privacy-preserving data network that could produce a useful result in ninety days?
4. **Leverage:** You co-authored the UN handbook, testified before the Senate, deployed structured transparency at LinkedIn/X/Dailymotion through the Christchurch Call, and sit on the CFR. Can you use these roles and relationships to deploy this system? What is the single most useful thing someone listening can do to help?
5. **Coalition:** Would OpenMined join the International Campaign to End War and Disease and share the 1% Treaty referendum with its 18,000+ members? (Modeled on the ICBL/ICAN campaigns that won the Nobel Peace Prize.)
6. **CFR world model:** You're a term member of the CFR. The CFR exists to produce optimal foreign policy. You build privacy-preserving computation systems. Why doesn't the CFR have a global simulation that computes optimal policy to maximize median health and income? The 1% Treaty would be one of its outputs, not a political ask. Can you build it for them?
7. **UN system:** You co-authored the UN's handbook on privacy-preserving computation for their Global Working Group on Big Data. The UN has statistical offices in every member state and its charter says its purpose is solving international problems. Why doesn't the UN already have a federated system computing optimal global policy? What's stopping you from proposing it?
8. **Inauguration:** Who are the two smartest people you know who would actually do something useful with this job? They are the next two presidents. Name them now — the episode does not end until the names are on record.

**Mechanism pressure (for every proposal, ask):**

- who holds the data
- who currently refuses to share it
- what they are afraid of
- what computation needs to happen
- who verifies the result
- what abuse case would kill trust
- what pilot proves the mechanism without asking for civilizational permission

**Commission order:** Draft the smallest privacy-preserving learning pilot that could improve one disease-treatment decision or one public-budget decision within ninety days. One page: data holders, computation, privacy guarantee, success metric, cost, what gets published, why a skeptical institution says yes.

**Inauguration:** Before the episode ends, Andrew names at least two successors — the smartest people he knows who would actually do something useful with this job. The episode does not end until the names are on record.

**Scheduling:** Natalia Diaz Granados (natalia@openmined.org) coordinates. Confirmed: Monday, June 29, 1:30–2:00 PM ET. Consider asking for 45–60 min once rolling.

## Publication Checklist

Before recording:

- [ ] confirm permission to record and publish
- [ ] confirm public title and affiliation wording
- [ ] test host microphone, camera, lighting, and local backup
- [ ] test guest audio before the real conversation starts
- [ ] open the commissioner page and question list

After recording:

- [ ] back up raw files
- [ ] export full video
- [ ] export MP3
- [ ] generate transcript and captions
- [ ] remove private pre-roll and off-record sections
- [ ] publish YouTube video
- [ ] upload MP3 and captions to R2
- [ ] publish commissioner page with final links
- [ ] cut three short clips
- [ ] ask the commissioner for their two successors
