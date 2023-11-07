---
title: Initial Web Component Findings
description: 
published: true
date: 2023-11-07T06:23:33.163Z
tags: 
editor: markdown
dateCreated: 2022-08-29T19:55:09.897Z
---

# Initial Web Component Findings


### Why
First, the only thing that is best to aim for is using web components to compartmentalize front end logic and make it easily implementable for other users.
The why can be summed up here:
https://developer.mozilla.org/en-US/docs/Web/Web_Components#concepts_and_usage

Basically, you can ensure styles and logic don't bleed into or out of the component unless explicitly done, and they're easy to use and re-use.

You can write these by hand without any framework need, but tooling can obviously make it easier, simpler, more concise, handling edge cases, polyfills, etc.

### Support
And you'll see support is quite good (~96%):
https://caniuse.com/custom-elementsv1
https://caniuse.com/template
https://caniuse.com/shadowdomv1

### Implementations
A few decent lists of options can be found here:
https://developer.mozilla.org/en-US/docs/Web/Web_Components#see_also
https://www.webcomponents.org/libraries

Many of them seem to be very barebones by design, which is fine, but also offers fewer tools and features such as testing frameworks as a first class consideration.

The few that seem the most promising and interesting to me are: [**Stencil**](https://stenciljs.com/docs/introduction), [**Lit**](https://lit.dev/docs/), and [**Fast**](https://www.fast.design/docs/fast-element/defining-elements).

Lit looks a lot better than when I had initially looked at it, and basically seems to be nearly the same as Stencil. Fast is interesting given it's a Microsoft implementation, and seems to have a similar syntax as the other two. It does seem a little more complicated. 

I don't think there's a particularly "right answer", and all of the options have different features that appeal to different sorts of developers (such as functional / class-based / uses decorators / etc). 