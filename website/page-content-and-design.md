# Website Content and Design: War on Disease

This document outlines the content and design specifications for the "War on Disease" landing page, based on the `app/page.tsx` file. The design is implemented using Next.js, React, and Tailwind CSS.

## General Styling

- **Fonts:** The page primarily uses a `serif` font family, specified by `font-serif`. Text is often bold (`font-bold`) and uppercase (`uppercase`).
- **Colors:** The color palette is minimalistic, mainly using black (`bg-black`, `text-black`, `border-black`) and white (`bg-white`, `text-white`, `border-white`). The default background is `bg-background`.
- **Borders:** A heavy `border-4` or `border-b-4` with `border-black` or `border-white` is used frequently to create a stark, high-contrast look.
- **Layout:** The main content is contained within a `max-w-6xl` or `max-w-5xl` container, centered with `mx-auto`. Sections have significant vertical padding (e.g., `py-24`, `py-32`).

---

## Header

**Content:**
- Logo/Title: "WAR ON DISEASE"
- Navigation Links: TREATY, BONDS, REFERENDUM, PLAN

**Design:**
- A full-width header with a white background and a 4px black bottom border.
- It has a fixed height of `h-20`.
- The title "WAR ON DISEASE" is on the left, styled as `text-3xl`, bold, serif, uppercase, with wider letter spacing (`tracking-wider`).
- The navigation is on the right, hidden on mobile (`hidden md:flex`). The links are `text-lg`, bold, uppercase, with wide tracking.
- Navigation links have a hover effect: black background and white text.

---

## Hero Section

**Content:**
- Headline: "END DISEASE. INCREASE SECURITY. GET RICH."
- Sub-headline: "Humanity spends **$2.7 trillion** per year on war and destruction, but only **$0.06 trillion** on curing all diseases. What if we could redirect just **1%** to change everything?"
- Button: "LEARN ABOUT THE 1% TREATY"

**Design:**
- A section with large vertical padding (`py-32`) and a black bottom border.
- The headline is very large (`text-7xl md:text-9xl`), bold, serif, uppercase, with tight leading.
- The sub-headline is a large paragraph (`text-2xl md:text-3xl`), serif font, with a `max-w-4xl`. Important figures are bolded.
- The call-to-action button is large, with a black background, white text, a 4px black border, and uppercase text. On hover, it inverts colors (white background, black text).

---

## Spending Comparison Chart Section

**Content:**
- Title: "THE SPENDING DISPARITY"
- Chart: A bar chart comparing "MILITARY & WAR" ($2.7T) vs. "MEDICAL RESEARCH" ($0.06T).
- Comparison Cards:
    - MILITARY & WAR: $2.7T, PER YEAR ON DESTRUCTION
    - MEDICAL RESEARCH: $0.06T, PER YEAR ON CURES
- Summary Banner: "45X MORE SPENT ON WAR THAN CURES"

**Design:**
- White background section with a black bottom border.
- The title is large (`text-4xl md:text-6xl`), bold, serif, uppercase, centered, with a black bottom border.
- The main content is inside a container with a 4px black border and large padding.
- **Bar Chart:**
    - The bars are vertical.
    - "MILITARY & WAR" bar is black and takes up 100% of the chart height.
    - "MEDICAL RESEARCH" bar is white with a black border and takes up 2.2% of the height, visually representing the disparity.
    - Below each bar, there's a title and the amount in bold serif font.
- **Comparison Cards:**
    - Displayed in a 2-column grid on medium screens and up.
    - Each card has a 4px black border and `p-6` padding.
    - The "MILITARY & WAR" card has a black background and white text.
    - The "MEDICAL RESEARCH" card has a white background and black text.
- **Summary Banner:**
    - A full-width box with a 4px black border, black background, white text, and large padding.
    - The text is `text-2xl md:text-4xl`, bold, serif, and uppercase.

---

## Problem Statement

**Content:**
- Title: "THE PROBLEM"
- Statistics Boxes:
    - "$2.7 TRILLION Spent annually on military, war, and destruction"
    - "$0.06 TRILLION Spent annually on discovering cures for all diseases combined"
    - "That's 40X less on saving lives than ending them."
- Large Figure Box: "40X More spent on war than cures"

**Design:**
- A section with a black background and white text.
- Layout is a 2-column grid on medium screens.
- **Left Column:**
    - The title "THE PROBLEM" is `text-6xl`, bold, serif, uppercase, with a white bottom border.
    - Below the title, there are three boxes, each with a 4px white border and padding.
- **Right Column:**
    - A single large box with a 4px white border and very large padding (`p-16`).
    - It contains "40X" in a massive font size (`text-9xl`), bold, and serif.
    - The descriptive text below is uppercase.

---

## The Solution (The 1% Treaty)

**Content:**
- Section ID: `treaty`
- Title: "THE 1% TREATY"
- Description: "A global treaty redirecting just **1%** of military spending to a Decentralized Institutes of Health, funding pragmatic clinical trials **80X more efficient** than standard trials."
- "HOW IT WORKS" section with 3 steps:
    1.  **GLOBAL REFERENDUM**: Secure support from at least 3.5% of each nation's population
    2.  **STRATEGIC LOBBYING**: Use existing military-industrial complex apparatus to pass the treaty
    3.  **FUND RESEARCH**: $27 billion annually for hyper-efficient decentralized clinical trials

**Design:**
- Section has a default background and a black bottom border.
- Title is centered, `text-6xl`, bold, serif, uppercase, with a black bottom border.
- The description is a centered paragraph.
- The "HOW IT WORKS" part is inside a white box with a 4px black border and large padding.
- Each step is a row with a numbered box on the left and text on the right.
    - The number (1, 2, 3) is in a `w-16 h-16` black square with white, bold, serif text.
    - The step title is `text-2xl`, bold, serif, and uppercase.
    - The description is `text-xl` serif.

---

## Victory Bonds

**Content:**
- Section ID: `bonds`
- Title: "VICTORY BONDS"
- Highlight Box: "40% CAGR", "The world's most profitable investment", "29X return over 10 years"
- "THE MATH" box:
    - Investment: $1 Billion
    - Returns: $29 Billion
    - Revenue: $270 Billion
    - "90% remains for disease research"
- "THE STRATEGY" box:
    - "Make peace more profitable than war..."
    - "Strategically distribute Victory bonds..."
    - "The military-industrial complex isn't evil—they just like money. So let's give them the best returns on Earth."

**Design:**
- Black background section with white text.
- Title is centered, `text-6xl`, bold, serif, uppercase, with a white bottom border.
- The highlight box has a 4px white border, large padding, and centered text. The "40% CAGR" is `text-8xl`.
- Below, there's a 2-column grid for "THE MATH" and "THE STRATEGY".
- Both columns are in boxes with 4px white borders and padding.
- Inside "THE MATH", each item is in a box with a 2px white border. The final point has a white background and black text.
- Inside "THE STRATEGY", each paragraph is in a box with a 2px white border. The final paragraph has a white background and black, bold, uppercase text.

---

## The Implementation Plan

**Content:**
- Section ID: `plan`
- Title: "THE IMPLEMENTATION PLAN"
- Three steps, each in its own box:
    - **STEP 1: CREATE INFRASTRUCTURE**
        - Establish nonprofit Decentralized Institutes of Health entity
        - Create Single Purpose Vehicle to issue Victory bonds
    - **STEP 2: FUND THE CAMPAIGN**
        - Accept donations to hire full-time staff
        - Raise $1-2.5 billion through Victory bond sales
    - **STEP 3: EXECUTE GLOBAL CAMPAIGN**
        - Fund referendums in every nation
        - Conduct global ratification campaigns
        - Educate the world about the 1% Treaty
- Final Call to Action Box:
    - "Estimated campaign cost: $1-2.5 billion"
    - "Potential annual research funding: $27 billion"
    - Button: "JOIN THE WAR ON DISEASE"

**Design:**
- Default background with a black bottom border.
- Title is centered, `text-6xl`, bold, serif, uppercase, with a black bottom border.
- Each of the three steps is in a large box with a 4px black border and padding.
- The step titles (`STEP 1`, etc.) are `text-4xl`, bold, serif, uppercase.
- List items within each step are `text-xl` serif, prefixed with a small black square acting as a bullet point.
- The final CTA box is at the bottom, centered, with a black background, white text, 4px black border, and large padding.
- The button inside inverts the colors: white background, black text, and a white border.

---

## Footer

**Content:**
- Title: "WAR ON DISEASE"
- Tagline: "Making peace more profitable than war, one percent at a time."
- Navigation Links: TREATY, BONDS, REFERENDUM, PLAN

**Design:**
- Black background with white text.
- All content is centered.
- The title is `text-4xl`, bold, serif, uppercase, with wider tracking.
- The tagline is `text-xl` serif, uppercase, with wide tracking.
- The navigation links are `text-lg`, bold, uppercase, with wide tracking. They have a 2px white border and a hover effect (white background, black text).
