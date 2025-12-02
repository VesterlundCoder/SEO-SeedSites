# Seed Sites, Web Crawling and Indexing Models for UK and Swedish Websites

This repository contains the code and data used in David Vesterlund’s research on **seed sites**, **web crawling**, and **indexing latency** for national web graphs – with a primary focus on the **.co.uk** (United Kingdom) and **.se** (Sweden) domains.

The core idea is to model how many **seed sites** a search engine like Google would need in a country-level web graph to:

- Achieve high **coverage** of active domains within a small number of link hops.
- Keep **Time to First Index (TTFI)** low for ordinary websites (especially SMEs).
- Understand the trade-off between **“more seeds”** vs **“more hops”** in the crawl frontier.

The models and code here support the research paper:

> **(Working title)**  
> *Mathematical Models of Seed Site Coverage, Web Crawling and Indexing Latency for UK and Swedish Domains*

All code is written in Python and designed to be easy to run, modify, and extend.

---

## 1. Research Context: Seed Sites, Crawling and Indexing

Modern search engines rely on a relatively small set of highly trusted or highly connected **seed sites** to:

- **Discover** new websites and pages via hyperlinks.
- **Propagate trust** (e.g. TrustRank-style algorithms).
- **Prioritise crawling** and re-crawling based on link distance and importance.

This repository provides:

- A **mathematical model** of coverage for 2-, 3-, 5- and 10-hop crawling.
- An approximate **TTFI model** based on expected distance to the nearest seed.
- **Python code** to reproduce all tables and figures from the .co.uk / .se seed-site papers.
- **Visualisations** that show how coverage and TTFI change as you add more seed sites.

The models are calibrated against realistic orders of magnitude:

- **Sweden (.se):** ~1.5 million active domains.
- **United Kingdom (.co.uk):** ~8.4 million active domains.

They are intentionally **stylised**: the goal is to build intuition and provide a transparent, reproducible framework – not to perfectly emulate any specific search engine’s proprietary crawler.

---