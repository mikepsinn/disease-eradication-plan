---
title: Human File System
description: The Human File System Protocol SDK is an innovative suite of interoperable software libraries, meticulously designed to facilitate the creation of user-access controlled digital twins on the blockchain.
published: true
date: 2023-11-07T06:27:48.805Z
tags: data-aggregation, data sharing, data storage
editor: markdown
dateCreated: 2023-10-26T21:15:45.781Z
---

## The Human File System Protocol SDK

**A Simple API for Patient-Controlled Health Data Aggregation, Sharing, and Monetization**

A set of interoperable software libraries that can be used independently to create user-access controlled digital twins on the blockchain.

The libraries can be used independently, but will all be included in the HumanFS SDK.

### The Need for a Human File System Protocol

There are 350k health apps containing various types of symptom and factor data.  However, the isolated data's relatively useless in all these silos. In order to make clinical discoveries, all the factor data needs to be combined with the outcome data.

**Web2 Problem**

The web2 solution to combining all this data is a nightmare of

1. creating thousands of OAuth2 data connectors
2. running a bunch of importer cron jobs on AWS.

**Web3 Solution**

User auth/databases/key management/access control/3rd party OAuth tokens abstracted away by a single, easy-to-use API

i.e.

Pain Tracking App A:

`db.collections.create('Arthritis Severity', timeSeriesData);`

Diet-Tracking App B:

`let timeSeriesData = db.collections.get('Arthritis Severity');`

⇒ Making it possible for Diet-Tracking App B (and/or Pain Tracking App A) to easily analyze the relationship between dietary factors and Arthritis Severity using causal inference predictive model control recurrent neural networks.