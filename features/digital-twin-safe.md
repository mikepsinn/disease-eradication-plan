---
title: "\U0001F468‍\U0001F91D‍\U0001F468 The Digital Twin Safe \U0001F512"
description: "A little house for your digital twin. \U0001F3E1"
published: true
date: 2023-06-08T19:52:34.654Z
tags: [projects, data, sharing, data, storage]
editor: markdown
dateCreated: 2022-11-07T20:38:39.252Z
---

![human-file-system-banner-logo](https://user-images.githubusercontent.com/2808553/180306571-ac9cc741-6f34-4059-a814-6f8a72ed8322.png)

Import data from all your apps and wearables so you can centrally own, control, and share all your digital exhaust.

## Key Features

* Import data from all your health apps and wearables.
* Central ownership and control over your digital health data.
* Seamless sharing of data with health apps through our secure iframe messaging system.
* Full control over data sharing, leveraging blockchain's decentralized storage capabilities.

## Demo

Available on the Polygon chain at [humanfs.io](https://humanfs.io) and on [Github](https://github.com/curedao/digital-twin-safe).

## Technology

Based on the awesome [Gnosis Safe](https://gnosis-safe.io/), the most trusted platform to store digital assets.


# The Human File System SDK

**A Simple API for Patient-Controlled Health Data Aggregation, Sharing, and Monetization**

The Human File System is a set of interoperable software libraries that can be used independently to create user-accesss controlled digital twins on the blockchain.

The libaries can be used independently, but will all be included in the HumanFS SDK.

## ❓ Why in the hell are you doing this?

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

## Overview

![digital-twin-safe-screenshot-home](https://user-images.githubusercontent.com/2808553/200402565-72bc85a3-deb2-4f1a-a9b1-bde108e63d87.png)

## Variables

![digital-twin-safe-screenshot-variables](https://user-images.githubusercontent.com/2808553/200402422-41213d62-324d-44db-a725-fc0eab619e45.png)

### Data Sources

![digital-twin-safe-screenshot-data-sources](https://user-images.githubusercontent.com/2808553/200402625-8c4ab0b1-829c-4128-8b12-509c2f885b96.png)

# 📚 Libraries Used

[Data Storage, Authorization and Sharing](https://github.com/yash-deore/sshr-hackfs) - Lit Programmable Key Pairs (PKPs) for access control over protected health information (PHI) with data storage on Ceramic. XMTP (Extensible Message Transport Protocol) is an open protocol and network for secure, private messaging between patients and physicians.

### Libraries TODO
* [Zero Knowledge Unique Patient Identifier Key in a Soul Bound NFT](https://app.dework.xyz/hackfs-dhealth-colle/suggestions?taskId=ff0c50bf-3c11-4076-8c9c-18d8c46ecf05) - For patients, owning an NFT of their medical data would be like creating a sentry to guard that personal information. The NFT would act as a gatekeeper, tracking who requested access, who was granted access, and when—and record all those actions publicly.
* [Federated Learning](https://app.dework.xyz/hackfs-dhealth-colle/suggestions?taskId=f25f12a9-7e3d-4488-85f7-023f95f75dfe) - Fluence to perform decentralized analysis of human generated data from applications and backends on peer-to-peer networks
* [Proof of Humanity](https://app.dework.xyz/hackfs-dhealth-colle/suggestions?taskId=db1092b9-91b4-4352-999a-f088ffefd6c8) - The Proof of Attendance Protocol for Sybil Resistant data collection, ensuring that robots aren't selling fake health data.
* [Reward open-source health innovation](https://app.dework.xyz/hackfs-dhealth-colle/suggestions?taskId=7261a8d8-f1ad-493c-a41c-b70a36507763) - Valist to reward public good open-source health technology innovations using Software License NFTs and proof of open-source contribution.
* [Querying specific health data](https://app.dework.xyz/hackfs-dhealth-colle/suggestions?taskId=3a546a7f-2aa6-43a1-8dda-08c5a62c83b4) - Tableland for querying the HumanFS for specific data types and time periods.
* [NFT Health Data Marketplace](https://app.dework.xyz/hackfs-dhealth-colle/main-space-477/projects/nft-health-data-mark) - NFTPort for minting data sets that can be sold to pharmaceutical companies in a health data marketplace.
* [On-Chain Analytics](https://app.dework.xyz/hackfs-dhealth-colle/suggestions?taskId=0114d499-36ff-4451-9d1a-e870c753e155) - Covalent for Health Data NFT marketplaces, On-Chain Analytics / Dashboards, Health Data Wallets, Health Data Asset tracking, and ROI for NFT generation and sales.


|   |   |
|---|---|
|[![techtarget.com favicon](https://www.google.com/s2/favicons?sz=128\&domain=techtarget.com)](https://www.techtarget.com/searchsecurity/definition/access-control) | [1. What is Access Control?](https://www.techtarget.com/searchsecurity/definition/access-control)<br> Access control is a security technique that regulates who or what can view or use resources in a computing environment. It is a fundamental concept in ... |
|[![crunchbase.com favicon](https://www.google.com/s2/favicons?sz=128\&domain=crunchbase.com)](https://www.crunchbase.com/organization/lit-protocol) | [2. Lit Protocol - Crunchbase Company Profile & Funding](https://www.crunchbase.com/organization/lit-protocol)<br> Lit Protocol is a decentralized access control infrastructure designed to bring more utility to the web. |
|[![coindesk.com favicon](https://www.google.com/s2/favicons?sz=128\&domain=coindesk.com)](https://www.coindesk.com/business/2022/09/22/cryptography-network-lit-protocol-raises-13m-to-bolster-web3-autonomy-and-interoperability/) | [3. Cryptography Network Lit Protocol Raises $13M to Bolster ...](https://www.coindesk.com/business/2022/09/22/cryptography-network-lit-protocol-raises-13m-to-bolster-web3-autonomy-and-interoperability/)<br> Lit aims to give individuals agency within Web3 ecosystems by giving users a private key that is interoperable across decentralized finance ( ... |
|[![ceramic.network favicon](https://www.google.com/s2/favicons?sz=128\&domain=ceramic.network)](https://ceramic.network) | [4. Ceramic - The Composable Data Network](https://ceramic.network)<br> The Composable Data Network. Ceramic is a decentralized data network that powers an ecosystem of interoperable Web3 applications and services. |
|[![filebase.com favicon](https://www.google.com/s2/favicons?sz=128\&domain=filebase.com)](https://docs.filebase.com/knowledge-base/web3-tutorials/ceramic/ceramic-how-to-host-a-ceramic-node-using-decentralized-storage) | [5. How to Host a Ceramic Node Using Decentralized Storage](https://docs.filebase.com/knowledge-base/web3-tutorials/ceramic/ceramic-how-to-host-a-ceramic-node-using-decentralized-storage)<br> The Ceramic network is a decentralized network for building applications with composable data on Web3. Ceramic makes building apps as easy as browsing a ... |
|[![theblock.co favicon](https://www.google.com/s2/favicons?sz=128\&domain=theblock.co)](https://www.theblock.co/post/218089/ceramic-releases-tool-that-awakens-its-storage-for-web3-protocol) | [6. Ceramic releases tool that awakens its 'storage for web3' ...](https://www.theblock.co/post/218089/ceramic-releases-tool-that-awakens-its-storage-for-web3-protocol)<br> Ceramic is a network that web3 projects can use to store data which doesn't need to be on a blockchain. It's now easy to use. |
|[![filecoin.io favicon](https://www.google.com/s2/favicons?sz=128\&domain=filecoin.io)](https://docs.filecoin.io/basics/how-storage-works/filecoin-and-ipfs/) | [7. Filecoin and IPFS](https://docs.filecoin.io/basics/how-storage-works/filecoin-and-ipfs/)<br> Filecoin's blockchain is designed to store large files, whereas other blockchains can typically only store tiny amounts of data, very expensively. Filecoin can ... |
|[![siliconmechanics.com favicon](https://www.google.com/s2/favicons?sz=128\&domain=siliconmechanics.com)](https://www.siliconmechanics.com/news/understanding-ipfs-and-filecoin) | [8. Understanding IPFS and Filecoin](https://www.siliconmechanics.com/news/understanding-ipfs-and-filecoin)<br> IPFS allows peers to transfer data files between each other, and Filecoin is provides a system of persistent data storage. Advantages of Filecoin. Filecoin ... |
|[![web3.storage favicon](https://www.google.com/s2/favicons?sz=128\&domain=web3.storage)](https://web3.storage) | [9. Web3 Storage - Simple file storage with IPFS & Filecoin](https://web3.storage)<br> All data is accessible via IPFS and backed by Filecoin storage, with service authentication using decentralized identity. Create user-centric applications, ... |
|[![metav.rs favicon](https://www.google.com/s2/favicons?sz=128\&domain=metav.rs)](https://metav.rs/blog/nfts-digital-twins-brand/) | [10. NFTs Digital Twins](https://metav.rs/blog/nfts-digital-twins-brand/)<br> NFTs digital twins are virtual copies of physical assets sharing their data with the original physical version. Reliability, Exchangeability. |
|[![saylcloud.com favicon](https://www.google.com/s2/favicons?sz=128\&domain=saylcloud.com)](https://www.saylcloud.com/article/how-to-start-with-digital-twins-for-nft) | [11. How to start with digital twins for NFT?](https://www.saylcloud.com/article/how-to-start-with-digital-twins-for-nft)<br> The NFTs that represent real-world objects provide a reliable and immutable way to track the history, collect key information and provide a ... |


