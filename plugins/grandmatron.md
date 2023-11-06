---
title: Grandmatron
description: Voice collection on cognitive performance and factors that could influence it.
published: true
date: 2023-07-19T16:07:43.939Z
tags: projects
editor: markdown
dateCreated: 2023-07-19T16:07:43.939Z
---

## User Story:

When I visit my grandma, I try to collect data on her cognitive performance and factors that could influence them. 

I also just talk to her for a while. But she can only remember 5 minutes, so I just repeat myself 12 times in an hour. 

She'd probably like to talk to me 16 hours a day, but I'd get even less done than I already do. 

So it would be cool to have a robocaller service could call lonely old people, remind them to take their grandma and talk to her for like 16 hours.

Also, I'd like it if I got a phone call every day and could do my treatment/diet/symptom tracking that way. i.e.

- What'd you eat today?
- What'd you drink today?
- What treatments did you take today?
- Rate all your symptoms on a scale of 1 to 5

Then it would convert the responses to measurement objects and post to whatever endpoint is specified.

Example Measurement Array for the response, `I took 5 grams of NMN`:
```
[
	{
		"combinationOperation" : "SUM",
		"startAt" : "{ISO_DATETIME_IN_UTC}",
		"unitName" : "grams",
		"value" : "5",
		"variableCategoryName" : "Treatments",
		"variableName" : "NMN",
		"note" : "{MAYBE_THE_ORIGINAL_STATEMENT_FOR_REFERENCE}"
	}
]
```

Nice possible future feature:
Since people with Alzheimer's don't remember what you said before, ideally it could eventually use verbal and maybe frequency data to quantify how nice each statement makes her feel. Then it could gradually say more of the nice things that make her the happiest, since it's usually like she heard it the first time. 

## Draft Implementation Roadmap

For reference and cannibalization, I implemented statement intent identification and handling in PHP and JavaScript here
https://github.com/search?q=repo%3Acuredao%2Fdecentralized-fda%20intent&type=code

It's kind of dumb relative to what's possible with LLM's now, though:
- [Demo Video](https://youtu.be/hd50A74o8YI)
- [Try It Out](https://demo.curedao.org/app/public/#/app/chat)

We may want a [T3 framework](https://create.t3.gg/) API or something less monolithic and more maintainable.  

Vocode also has a great framework for this.  The response times in the demo are superfast. 
https://docs.vocode.dev/welcome

### Milestone 1 - Design service architecture

- Research existing robocall/IVR platforms 
- Define requirements for call flow, speech recognition, natural language processing etc.
- Design database schema for user profiles, call logs, responses etc.
- Plan workflow for calls - scheduling, duration, frequency etc.
- Design APIs for accessing user data, logging responses etc.
- Developer portal API for getting API Keys

### Milestone 2 - Build core platform

- Set up robocall service account and phone numbers
- Integrate speech recognition and natural language processing
- Build call scheduling engine
- Develop core IVR call flows for greeting, menu navigation etc.  
- Build database and APIs for storing and accessing user data
- Implement basic conversational responses and logic

### Milestone 3 - Develop health tracking features  

- Design system for tracking symptoms, diet, medications etc.
- Build natural language interfaces for entering health data
- Integrate with external APIs for weather data, local resources etc. 
- Develop logic to provide personalized health recommendations 
- Build reporting system to share health data with caregivers

### Milestone 4 - Add cognitive assessment and talk therapy 

- Research and integrate cognitive tests into calls
- Build conversational system for open-ended therapy sessions
- Implement sentiment analysis to gauge emotional state  
- Develop logic to provide encouraging responses, flag concerns etc.
- Enhance reporting to include therapy notes and test results

### Milestone 5 - Enhance personalization 

- Build user profiles with preferences, interests, nostalgia triggers etc.
- Develop analytics to track most engaging conversation topics  
- Fine-tune dialog system to incorporate personalized content 
- Implement reinforcement learning to optimize positive responses
- Expand knowledge base for specific interests - sports, hobbies, family etc.

### Milestone 6 - Launch and iterate

- Start with small pilot group to test and refine system 
- Gradually expand to broader elderly population
- Monitor feedback, usage data to improve features and experience
- Add new capabilities like medication reminders, family conference calls etc.
- Build caregiver portal for managing profiles and overseeing service