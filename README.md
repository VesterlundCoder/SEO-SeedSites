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