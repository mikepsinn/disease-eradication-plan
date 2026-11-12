# A Decentralized F.D.A

Audiobook chapter `dfda`. Timestamped transcript.

- Audio: <https://static.warondisease.org/assets/audiobook/manual-paperback/mp3/dfda.8217f08d.mp3>
- Length of the theme song and chapter: 00:29:50 (the outro follows)
- Method: the narration text the audio was made from, with times from the audiobook pipeline's forced alignment (`tools/word-timings.mjs`). The cold open in the theme song is from the earlier Whisper transcript.

Each paragraph starts with its time in the audio as [HH:MM:SS].

---

**[00:00:03]** You're here.

**[00:00:05]** Your organs are failing. And your death is drawing near. But if you bribe the right politicians in the right order at the right time, you can trade the nuclear warheads for medicine. And it's not even a crime.

**[00:00:20]** *[Theme music, 00:20 to 01:40]*

**[00:01:39]** A Decentralized F.D.A.

**[00:01:42]** On Wishonia, you type in what's wrong with you, see what worked for everyone else, and try it. The outcomes get recorded automatically. We've had this for millennia. Your decentralized F.D.A. is the same thing, built with technology you already have. It's an open protocol that connects treatments to patients, records what actually happens, and publishes the results. Consumer Reports, but for not dying. It cuts trial costs from forty-one thousand dollars to nine hundred and twenty-nine dollars, expands capacity from one point nine million patients per year to twenty-three point four million patients per year, and replaces your forty-page drug inserts with Outcome Labels that tell you what actually happened to real humans who took the pill.

**[00:02:28]** On Wishonia, we eliminated disease four thousand years ago. Every citizen has access to every treatment. Every outcome is recorded. Every disease gets studied. It's not complicated. You let sick people try things and write down what happens. But since your planet somehow hasn't figured this out, here's the instruction manual.

**[00:02:51]** Out of two point four billion people with chronic disease, only one point nine million patients per year participate in trials annually. That's zero point zero six percent.

**[00:03:03]** Forty-four point eight percent would volunteer if they could. Only zero point zero six percent currently participate.

**[00:03:12]** This isn't because people don't want to help find cures. It's because your system was designed by someone who hates sick people. Trials cost forty-one thousand dollars, require traveling to major medical centers, and reject eighty-six point one percent of actual patients. You built a hospital you can't get into. Impressive, in a genocidal sort of way.

**[00:03:39]** Meanwhile, the system that's supposed to catch dangerous side effects misses ninety to ninety-nine percent of them. Only one to ten percent of adverse drug events are ever reported to the F.D.A. No denominator data. No effect sizes. No way to calculate how often a drug actually hurts people. The safety monitoring system is a suggestion box that nobody uses.

**[00:04:05]** You don't have a recruitment problem. You have a capacity problem.

**[00:04:10]** The Solution: Consumer Reports for Drugs.

**[00:04:14]** On Wishonia, this is just called "medicine." You type in what's wrong with you, see what worked for everyone else, and try it. The outcomes get recorded automatically. We've had this for millennia. You have all the technology to build it right now, and somehow haven't.

**[00:04:32]** Your decentralized F.D.A. will be an open coordination protocol. It will connect companies with treatments to patients who need them. It will be H.T.T.P. for clinical trials. A standard that lets all the existing systems talk to each other and share outcomes. You invented the internet over three decades ago and somehow forgot to plug medicine into it.

**[00:04:57]** How It Works: Just Let People Try Stuff (Carefully).

**[00:05:02]** Yes, the F.D.A. exists because patent medicine salesmen were literally poisoning people, and thalidomide gave "birth defect" a whole new meaning. Nobody's arguing for no regulation; we're arguing for regulation that doesn't kill more people than it saves.

**[00:05:19]** Here's a thought that apparently never occurred to anyone in Washington:

**[00:05:24]** What if sick people could just... try treatments?

**[00:05:27]** And then we could... write down what happens?

**[00:05:30]** And then other sick people could... see what worked?

**[00:05:32]** Your current system leaves ninety-five percent of rare diseases with zero approved treatments. It bars over eighty-five percent of patients from the trials that might save them. We've perfected a system where only the healthy and compliant test cures for the sick and desperate. It's genius, in a suicidal sort of way.

**[00:05:56]** Trials are designed to test drugs on people who don't actually exist. To get into a study for an antidepressant, you can't have any other pesky problems like anxiety or P.T.S.D. You can't have a history of drug or alcohol use. You can't be on other medications.

**[00:06:12]** You have to be the *perfect* kind of sick. The result? Only about fourteen percent of real-world patients with depression would actually qualify. The patients who will actually be taking the drug are too messy for their pristine, clean data.

**[00:06:27]** On top of excluding everyone with a pulse, these "definitive" studies run on comically small groups. They'll test a new heart drug on two hundred and seventy-five people. A cancer drug on just twenty people. A diabetes drug on one hundred people. Then they prescribe the winner to millions.

**[00:06:46]** You're basing survival on sample sizes smaller than kindergarten classes. So instead of studying mythical, perfectly sick unicorns, what if you just collected data from everyone who's *actually* sick?

**[00:07:01]** The Power of Real-World Evidence (Or: Spying on Sick People for a Good Cause).

**[00:07:07]** This framework is built on a slightly creepy idea: analyzing data from real patients in the real world. Real-World Evidence (R.W.E.). A fancy term for "watching what happens.".

**[00:07:19]** Correlation isn't causation.

**[00:07:20]** But now there's enough data and computing power to make each person their own control group. Track arthritis pain for a month. Take Turmeric, stop, start again. The pattern reveals whether it works or if it's coincidence.

**[00:07:35]** A landmark meta-analysis in the New England Journal of Medicine quietly ended this argument while nobody was listening. Researchers compared observational studies against randomized controlled trials across nineteen different treatments. Cardiac surgery, cancer, ophthalmology, obstetrics.

**[00:07:54]** The result: nearly identical effect sizes. The cheap method and the expensive method found the same answers. You've been overpaying for data like tourists at an airport restaurant. On Wishonia, we figured this out about three thousand years ago.

**[00:08:10]** We call it "looking at what happened." You call it a "landmark meta-analysis.".

**[00:08:16]** Each pair of dots represents the same treatment tested two ways: one observational (cheap, fast, real patients) and one randomized controlled (expensive, slow, cherry-picked patients). In nearly every comparison, the confidence intervals overlap.

**[00:08:33]** Both methods found the same treatments work and the same treatments don't.

**[00:08:38]** The Two-Stage Pipeline: Watch First, Then Test.

**[00:08:43]** Observational data finds the signals. But correlation still isn't proof (even you know that). So the framework uses a two-stage pipeline:

**[00:08:53]** Stage one (Signal Detection): Aggregate data from millions of patients.

**[00:08:58]** Score each treatment-outcome relationship using six Bradford Hill causality criteria: How strong is the effect?

**[00:09:05]** How consistent across people?

**[00:09:07]** Does the treatment come before the improvement?

**[00:09:10]** Is there a dose-response pattern?

**[00:09:12]** Cost: approximately zero point one dollars per patient.

**[00:09:16]** Stage Two (Confirmation): The top signals (the zero point one to one percent most promising) proceed to pragmatic trials embedded in routine care. Simple randomization. Real patients. Real conditions. Cost: approximately nine hundred and twenty-nine dollars per patient. This eliminates confounding and proves causation.

**[00:09:40]** Stage One filters millions of possibilities for almost nothing. Stage Two confirms the winners for one forty-fourth the cost of traditional trials. The result: every treatment gets an evidence grade.

**[00:09:56]** Validated treatments are confirmed by pragmatic trial.

**[00:10:00]** Promising treatments show a strong observational signal and are awaiting trial.

**[00:10:05]** A signal is a hypothesis only and needs more data.

**[00:10:10]** The cheap stage does the hard work of searching. The expensive stage only runs on candidates that deserve it. Instead of spending fifty-seven million dollars testing one drug, you spend pennies watching a million treatments and under a thousand dollars confirming the ones that work.

**[00:10:29]** Proof It Works (While the F.D.A. wasn't looking).

**[00:10:33]** The Oxford Recovery Trial: How the British Accidentally Saved Medicine.

**[00:10:39]** During COVID, while America was filling out forms, Oxford University did something crazy. They just tested drugs on dying people to see if they stopped dying.

**[00:10:50]** Cost per patient:

**[00:10:51]** Normal clinical trials cost forty-one thousand dollars.

**[00:10:55]** Oxford pragmatic trials cost five hundred dollars.

**[00:10:59]** That's not a typo. Five hundred dollars. The cost of a nice dinner in Manhattan to save a human life.

**[00:11:07]** Results:

**[00:11:08]** They found that steroids cut COVID deaths by thirty percent.

**[00:11:12]** They saved over one million lives globally.

**[00:11:15]** It took three months instead of three years.

**[00:11:19]** It cost less than one Super Bowl commercial.

**[00:11:22]** The F.D.A.'s response: "But did they file the correct paperwork?".

**[00:11:27]** RECOVERY wasn't a fluke. A Harvard meta-analysis of one hundred and eight embedded pragmatic trials found median costs of just ninety-seven dollars per patient. The Patient-Centered Outcomes Research Network (or P.C.O.R.net) ADAPTABLE trial enrolled fifteen thousand and seventy-six patients across forty clinical sites at nine hundred and twenty-nine dollars per patient.

**[00:11:53]** This model works across therapeutic areas, across countries, across decades. The evidence base for cheap, fast, embedded trials isn't one study. It's one hundred and eight and counting. On most planets I've worked with, the pragmatic trial is the moment everyone looks at each other and says "wait, that's it?" Yes.

**[00:12:15]** That's it. You let sick people try things, write down what happens, and share the results.

**[00:12:21]** What You'd See: F.D.A. dot gov two point zero.

**[00:12:25]** The protocol upgrades F.D.A. dot gov from a digital cemetery to something useful. Cost: Less than one fighter jet that doesn't work.

**[00:12:35]** Step One: Type in What's Killing You.

**[00:12:38]** Revolutionary feature: A search box. The F.D.A.'s current website doesn't have this because they assume you've already died.

**[00:12:47]** Step Two: See What Actually Works (Based on Reality, Not Theory).

**[00:12:52]** Instead of "This drug is approved for exactly this condition in exactly these patients on exactly Tuesdays," you get:

**[00:13:00]** "Here's what happened to fifty thousand people who tried this:

**[00:13:03]** Forty percent got much better.

**[00:13:05]** Thirty percent got somewhat better.

**[00:13:08]** Twenty percent had no change.

**[00:13:10]** Ten percent grew a third nipple (but a useful one)".

**[00:13:14]** It's like Consumer Reports, but for not dying.

**[00:13:17]** Treatment Rankings: Every Option, Ranked by Reality

**[00:13:21]** Search any condition and see every treatment ranked by real-world effectiveness:

**[00:13:26]** F.D.A. Approved treatments with effectiveness scores from actual patients.

**[00:13:31]** Phase three and Phase two trials you can join right now.

**[00:13:34]** Experimental options with preliminary data.

**[00:13:36]** One-click access to join available trials.

**[00:13:39]** No more guessing which treatment your doctor half-remembers from a conference. Just clear rankings based on what actually worked for people like you. The current system never publishes negative results. Humanity wastes billions repeating the same failed ideas.

**[00:13:55]** Step 3: Join a Trial from Your Couch (While Dying Comfortably).

**[00:13:59]** Current system: Drive five hundred miles to a university hospital, wait six months, get rejected for having the wrong kind of dying.

**[00:14:06]** New system: Click button. Get pills. Report if you die.

**[00:14:10]** Revolutionary!

**[00:14:11]** Step 4: Get Drugs Delivered Like Pizza (But More Life-Saving).

**[00:14:16]** Amazon can deliver a banana costume in two hours but experimental medications take six months and require seven forms of I.D.?

**[00:14:25]** Your framework fixes that. Your pharmacy becomes a trial site. Your doctor becomes a researcher. Your dying becomes data.

**[00:14:33]** Step 5: Publish Results.

**[00:14:34]** Current system: five hundred-page case report forms that ask questions like "Rate your suffering on a scale of mauve to burnt sienna.".

**[00:14:43]** New system:

**[00:14:44]** "Are you dead?" Yes or No.

**[00:14:47]** "If no, how dead do you feel?" Slider bar.

**[00:14:50]** "Any new body parts?" Check all that apply.

**[00:14:53]** Step 6: Everyone Benefits from Everyone's Suffering.

**[00:14:57]** Your data helps the next person. Their data helps you.

**[00:15:00]** Every pill becomes a tiny experiment. Every patient becomes a scientist. Every outcome gets recorded.

**[00:15:07]** You should have done this when you invented writing in three thousand B.C.

**[00:15:11]** Outcome Labels: Nutrition Facts for Drugs.

**[00:15:15]** Food has nutrition labels. Cigarettes have warning labels. Drugs have... incomprehensible forty-page inserts written by lawyers having seizures.

**[00:15:24]** Outcome Labels fix that. Clear, data-driven summaries showing exactly what happens when real people try a treatment:

**[00:15:31]** No marketing spin. No forty-page legal disclaimers. Just clear data about what actually happens to people like you.

**[00:15:39]** Here's what an Outcome Label for depression would actually look like:

**[00:15:43]** OUTCOME LABEL: Depression Severity

**[00:15:46]** Based on forty-seven thousand, eight hundred and thirty-two participants

**[00:15:50]** Treatments Ranked by Effect Size

**[00:15:51]** Rank one is Bupropion, which showed a negative twenty-eight point three percent effect in a sample of two thousand, eight hundred and forty-seven people at a three hundred milligram dose.

**[00:16:03]** Rank two is Sertraline, which showed a negative twenty-four point seven percent effect in a sample of five thousand, one hundred and twenty-three people at a one hundred milligram dose.

**[00:16:12]** Rank three is Venlafaxine, which showed a negative twenty-one point two percent effect in a sample of one thousand, eight hundred and ninety-two people at a one hundred and fifty milligram dose.

**[00:16:14]** The list continues for all other treatments.

**[00:16:16]** Every treatment ranked. Drugs, supplements, lifestyle interventions, off-label uses. All compared head-to-head using the same outcome data. No marketing budget required.

**[00:16:29]** Your Personal Death-Prevention Assistant: The F.D.A.i.

**[00:16:33]** On Wishonia, every citizen gets one of these at birth. It monitors their health, finds treatments matched to their biology, and adjusts dosing in real time. We've had them for three thousand years. You've had the technology for nearly two decades and used it to count steps.

**[00:16:51]** Everyone gets a superintelligent doctor that lives in their phone and doesn't judge them for Googling "is my poop normal?".

**[00:16:58]** The F.D.A.i. (Food and Drug Artificial intelligence) is like Siri, but useful. Instead of mishearing your question and opening a Wikipedia article about Serbia, it tells you how not to die.

**[00:17:10]** You: "I have diabetes and my foot fell off.". F.D.A.i.: "Based on fifty thousand similar cases, here's what worked:

**[00:17:19]** Sixty percent success: Reattachment surgery plus Drug A.

**[00:17:24]** Thirty percent success: Prosthetic foot plus Drug B.

**[00:17:28]** Ten percent success: Hopping lessons plus Prayer.

**[00:17:31]** Zero percent success: Essential oils (but your remaining foot will smell lavender-fresh)".

**[00:17:38]** It connects to your wearables, apps, and medical records to find what's killing you while your doctor is still trying to remember your name. Every doctor who ever lived, in your pocket, and they actually agree on something.

**[00:17:50]** It also does something no doctor can: precision dosing. By analyzing what dose preceded your best outcomes, it generates personalized recommendations. Not "take some magnesium." Instead: "Your sleep quality was highest after four hundred milligrams of Magnesium over the previous twenty-four hours." Optimal doses derived from your data, not a study of thirty-six college students in nineteen ninety-seven.

**[00:18:18]** Making It Legal to Not Die.

**[00:18:20]** This solution requires a law: the Right to Trial and F.D.A. Upgrade Act. It says dying people can try things that might help them not die, and what happens gets written down so other dying people can see what worked.

**[00:18:34]** The fact that this requires a law tells you everything about your species.

**[00:18:39]** The Business Model: How Everyone Profits Except Disease.

**[00:18:44]** How Companies Register Treatments (five Minutes, Zero Approval Needed).

**[00:18:47]** Any company—pharma, supplements, food, interventions—can instantly create a trial:

**[00:18:50]** One. Register treatment on a public portal (name, ingredients, condition, price).

**[00:18:54]** Two. Set treatment price (what you charge patients—covers manufacturing and delivery).

**[00:19:00]** Three. Get automatic liability insurance (built into protocol governance).

**[00:19:06]** Four. Trial goes live immediately—appears in search results, ranked by existing data.

**[00:19:12]** Five. Patients join based on rankings; You collect zero-cost data on whether it works.

**[00:19:19]** Net cost to company: zero dollars.

**[00:19:22]** Why?

**[00:19:22]** Patients pay for treatment (covers manufacturing and delivery).

**[00:19:26]** Patients provide data (eliminates data collection cost of approximately forty-one thousand dollars per patient).

**[00:19:34]** Protocol enables standardized analysis (eliminates analysis cost).

**[00:19:38]** Insurance is built-in (eliminates liability cost).

**[00:19:41]** The Payment Flow.

**[00:19:42]** Patient pays: Treatment cost plus Refundable deposit.

**[00:19:46]** Patient receives: Subsidy (from a one percent Treaty Fund).

**[00:19:50]** Patient reports: Outcomes via simple app.

**[00:19:53]** Deposit refunded: When trial complete.

**[00:19:56]** Net cost to patient: zero. Some patients profit up to fifty dollars.

**[00:20:01]** Example.

**[00:20:03]** Patient joins trial for experimental migraine treatment (one hundred dollars per month).

**[00:20:07]** Pays: one hundred dollars treatment plus fifty dollars deposit equals one hundred and fifty dollars.

**[00:20:13]** Receives: one hundred and twenty-five dollars subsidy.

**[00:20:16]** Out of pocket: twenty-five dollars.

**[00:20:19]** Completes trial, reports outcomes.

**[00:20:21]** Gets back: fifty dollars deposit.

**[00:20:23]** Net: twenty-five dollars profit plus potentially cures migraines

**[00:20:28]** Company receives.

**[00:20:29]** One hundred dollars per month from patient.

**[00:20:32]** Manufacturing cost: twenty dollars per month.

**[00:20:35]** Profit: eighty dollars per month per patient.

**[00:20:38]** Plus: Free clinical trial data worth forty-one thousand dollars per patient in traditional system.

**[00:20:45]** Why This Creates Vastly More Research Capacity.

**[00:20:49]** Start: Both the traditional model and the decentralized protocol begin with research ideas.

**[00:20:55]** Gatekeeping: Traditional grant committees select the few, while the decentralized protocol allows instant registration.

**[00:21:04]** Enrollment: The traditional model recruits from a limited pool, while in the decentralized protocol, patients decide by joining.

**[00:21:12]** Cost to company: The traditional model costs fifty-seven million dollars per trial, while the decentralized protocol costs zero dollars (patients pay for treatment).

**[00:21:23]** Throughput: The traditional model handles approximately ten trials per year per company, while the decentralized protocol handles thousands of trials simultaneously.

**[00:21:33]** This is why ninety-five percent of rare diseases have no treatments. Traditional funding can't afford to test everything. This decentralized protocol enables testing EVERYTHING because:

**[00:21:45]** No approval bottleneck (instant registration).

**[00:21:49]** No funding bottleneck (patients pay for treatment).

**[00:21:52]** No data collection bottleneck (patients provide data).

**[00:21:55]** No disease too rare (if one hundred patients exist globally, trial can run profitably).

**[00:22:02]** Traditional trial: Pharma spends fifty-seven million dollars, tests most profitable drug only.

**[00:22:08]** Decentralized trial: Pharma spends zero dollars, tests everything including supplements, food, lifestyle, off-patent drugs.

**[00:22:17]** A one percent Treaty Fund doesn't fund pragmatic clinical trials directly. It subsidizes participation, which unlocks a self-sustaining ecosystem that funds ALL research.

**[00:22:31]** The Money Shot: How to Save ninety-five percent on Not Killing People.

**[00:22:35]** Clinical Phase Timeline: Current insanity is over a decade. New reality is two to three years. This eliminates approximately seven years of waiting and saves approximately fifty thousand lives per year.

**[00:22:50]** Cost per trial: Current insanity is fifty-seven million dollars. New reality is two million dollars. This saves fifty-five million dollars and provides an Absurd R.O.I.

**[00:23:02]** Who can participate: Current insanity is thirteen point nine percent of patients. New reality is one hundred percent of patients. This eliminates the eighty-six point one percent exclusion rate for everyone.

**[00:23:15]** Rare diseases with treatments: Current insanity is five percent. New reality is eventually one hundred percent. The results are priceless and save millions of lives.

**[00:23:27]** The Itemized Receipt of Eliminated Stupidity.

**[00:23:30]** This eliminates fifty-five million dollars per trial.

**[00:23:34]** The Partnership Approach: Building Rails, Not Trains.

**[00:23:38]** Here's what you're NOT doing: building a government platform that competes with existing medical technology companies.

**[00:23:44]** Here's what you ARE doing: building an open protocol that lets all existing platforms talk to each other.

**[00:23:51]** Think of it like the internet. We didn't build one website that everyone has to use. We built H.T.T.P., the protocol that lets all websites connect. Same idea.

**[00:24:02]** How your decentralized F.D.A. gets funded: An implementation of this framework is one of many campaigns competing for funding from the one percent Treaty Fund via Wishocracy (wishocracy dot Q.M.D.). It has no independent budget authority.

**[00:24:17]** If a particular implementation gets captured or fails to deliver, the community can fund alternative implementations instead. This prevents the "new F.D.A." problem.

**[00:24:28]** The Players Already in the Game.

**[00:24:30]** Multiple companies have already built decentralized clinical trial platforms. They've collectively raised hundreds of millions in venture funding. They're good at it. They have users. They have infrastructure.

**[00:24:41]** Why compete with them? That would be very human of you. Partner instead.

**[00:24:46]** The open standard provides a common data exchange format (like email protocols).

**[00:24:52]** It provides a federated data network (data stays in Epic/Cerner/Apple Health systems).

**[00:24:58]** It provides treatment ranking algorithms (open source, anyone can verify).

**[00:25:03]** It provides trial matching services (connects patients to ANY platform).

**[00:25:08]** Existing platforms provide patient-facing apps and interfaces.

**[00:25:12]** They provide trial management tools.

**[00:25:14]** They provide sponsor relationships.

**[00:25:16]** They provide regional expertise.

**[00:25:19]** Federated, Not Centralized.

**[00:25:22]** Data doesn't move to a central database. It stays where it is. Everyone keeps their toys.

**[00:25:28]** Epic systems keep their data.

**[00:25:30]** Apple Health keeps its data.

**[00:25:32]** Cerner keeps its data.

**[00:25:33]** Your decentralized protocol will let you run queries ACROSS systems without moving data. Like asking every library in the world a question without stealing their books. Federated data networks already do this with three hundred million plus patient records.

**[00:25:49]** This solves G.D.P.R. and HIPAA compliance (data never leaves source).

**[00:25:54]** It solves privacy concerns (no central honeypot to hack).

**[00:25:58]** It solves vendor cooperation (they keep control).

**[00:26:01]** It solves patient trust (data doesn't go to "the cloud").

**[00:26:05]** Why This Works: The Mathematical Impossibility of Committees.

**[00:26:10]** Approximately two hundred F.D.A. bureaucrats decide what eight billion people can try when dying. Here's the math on why that can't work:

**[00:26:19]** The F.D.A. approves approximately fifty new drugs per year. There are ten thousand known diseases. At that rate, covering every disease once takes two hundred years.

**[00:26:30]** And that's before you account for the fact that different patients respond differently to the same drug based on genetics, age, comorbidities, and whether they had breakfast.

**[00:26:39]** The real bottleneck isn't speed; it's information. Centralized approval assumes a two hundred-person committee can evaluate what works for eight billion genetically unique humans. They can't.

**[00:26:52]** A decentralized system where millions of patients generate real-world evidence simultaneously processes more therapeutic information in a month than the F.D.A. generates in a decade.

**[00:27:04]** The F.D.A. doesn't know:

**[00:27:06]** What disease YOU have (they haven't met you).

**[00:27:09]** How YOUR body responds to treatments (genetics are unique).

**[00:27:13]** What risks YOU'RE willing to take (some prefer death to side effects, others the reverse).

**[00:27:20]** Whether YOU'D rather die trying or die waiting (only you can answer this).

**[00:27:25]** But they decide for you anyway. This isn't ideology. It's information theory. You mathematically cannot centralize medical decisions for eight billion unique people.

**[00:27:37]** Every civilization I've worked with tried a centralized approval committee first. Every single one eventually abandoned it, once someone did the math and realized that a roomful of experts reviewing one drug at a time is just a queue with a death rate.

**[00:27:55]** The Future: Where Death Becomes Embarrassing.

**[00:27:58]** Twenty twenty-seven: The Beginning of the End of Dying Slowly.

**[00:28:03]** F.D.A. dot gov becomes actually useful. Millions join trials from home. The first "Wikipedia disease" gets cured entirely through crowdsourced trials. The F.D.A. claims credit.

**[00:28:17]** Twenty thirty: Big Pharma Pivots or Dies.

**[00:28:21]** Pharmaceutical companies realize they can't charge ten thousand dollars for pills that cost one dollar to make when everyone can see the data. Some adapt. Some become museums. The gift shop sells expired painkillers at original markup.

**[00:28:37]** Twenty thirty-five: The Great Revelation.

**[00:28:41]** Humanity could have done this all along. The internet existed since nineteen ninety. Computers since nineteen fifty.

**[00:28:49]** Five thousand years of letting people die while filling out forms. History books will call this "The Paperwork Age." Children will laugh.

**[00:28:59]** Twenty fifty: Death Becomes Opt-In.

**[00:29:03]** Diseases are mostly solved. Death becomes a choice, like smoking or voting for the Uniparty. The F.D.A.'s job becomes preventing people from becoming immortal too quickly (traffic is bad enough).

**[00:29:16]** The last F.D.A. form is filled out. It's immediately lost. Nobody notices.

**[00:29:22]** How Your Decentralized F.D.A. Actually Works.

**[00:29:26]** This approach is FORTY-FOUR POINT ONE TIMES more cost-efficient than the current system, driven by:

**[00:29:33]** The cost per patient is nine hundred and twenty-nine dollars versus the current forty-one thousand dollars.

**[00:29:40]** The time to results is three months versus the current ten point five years.

**[00:29:45]** Patient access is universal versus eighty-six point one percent excluded currently.

**[00:30:02]** *[Podcast outro]* Thank you so much for taking the time to end war and disease, but if at any point you decide you're too busy, please press the share button on your glowing rectangle in case one of your friends have a free afternoon to end war and disease instead. And if you're too busy to even do that, please leave a really, really, really good rating and review so we overcome the pro -war algorithmic suppression and find someone with more spare time for ending wars and diseases. The good review doesn't have to be true, they don't check. But if you're too busy to even do that, the absolute least you could do is take 15 seconds to go to WarOnDisease.org and make your wishocratic allocation, telling us what fraction of humanity's resources should go to explosions versus clinical trials. And vote! If the 1% treaty passes, your vote will be personally to blame for saving 2.6 lives and preventing 468,000 hours of suffering. Go to WarOnDisease.org right now. Love you, bye!
