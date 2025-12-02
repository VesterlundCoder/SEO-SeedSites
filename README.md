### 2.1. Per-seed coverage up to k hops

Details about per-seed coverage evaluating up to k hops, elaborating on the implications and metrics involved.

### 2.2. Distance to seeds and Time to First Index (TTFI)

A discussion on how distance to seeds affects crawling efficiency and the time it takes for a new page to become indexed.

## 3. Repository Structure and Code Overview

The layout of the project is organized as follows:

```
- src/
    - main/
        - java/
            - com/
                - example/
                    - project/
- test/
    - java/
        - com/
            - example/
                - project/
```

The source code is split into main and test directories, allowing for clear separation and easy management.
3.1. multi_hop_seed_model.py – core coverage & TTFI model

Purpose:
Implements the multi-hop coverage and TTFI models and generates the UK / SE tables.

Key functions:
	•	T_k(D: float, r: float, s: float, k: int) -> float
Per-seed coverage up to k hops:
	•	T_k(D, r, s) = 1 + D + r D² + Σ_{h=3..k} s D^h
	•	estimate_coverage(N: int, num_seeds: int, D: float, r: float, s: float, theta: float, k: int)
Returns (coverage_fraction, discovered_nodes) for k hops.
	•	expected_distance(D: float, N: int, num_seeds: int) -> float
Approximates E[dist] ≈ log_{D+1}(N / num_seeds + 1).
	•	estimate_ttfi(D: float, N: int, num_seeds: int, tau_hop: float = 3.0, k_horizon: int | None = None)
	•	Base model: TTFI ≈ τₕₒₚ · E[dist]
	•	Optional hop cap: E[dist_k] = min(E[dist], k_horizon)
	•	build_multi_hop_table(N: int, seeds_list: list[int], label: str) -> pd.DataFrame
Builds a table with:
	•	Coverage and TTFI for k = 5 and k = 10 hops.
	•	Used to generate uk_multi_hop_results.csv and se_multi_hop_results.csv.

Usage example (UK & SE tables):
import pandas as pd
from multi_hop_seed_model import (
    D, r, s, theta, tau_hop,
    N_UK, N_SE, seeds_UK, seeds_SE,
    build_multi_hop_table
)

df_uk = build_multi_hop_table(N_UK, seeds_UK, "UK (.co.uk)")
df_se = build_multi_hop_table(N_SE, seeds_SE, "SE (.se)")

df_uk.to_csv("data/uk_multi_hop_results.csv", index=False)
df_se.to_csv("data/se_multi_hop_results.csv", index=False)
3.2. figures_seed_uk_se.py – plotting Figures 1–8

Purpose:
Reproduces all Figures 1–8 from the seed-site research paper, including:
	1.	.co.uk domain counts and active share (Figure 1).
	2.	Two-hop seeds vs coverage under different scenarios (Figure 2).
	3.	Seeds at 90% coverage for 43% vs 50% active share (Figure 3).
	4.	Three-hop seeds vs coverage (Figure 4).
	5.	Seeds at 90% coverage: two vs three hops (Figure 5).
	6.	TTFI vs number of seed sites for .co.uk (Figure 6).
	7.	Coverage vs seeds: .se vs .co.uk (Figure 7).
	8.	TTFI vs seeds: .se vs .co.uk (Figure 8).

Key plotting functions:
	•	plot_figure_1_couk_active()
	•	plot_figure_2_twohop_seeds_vs_coverage()
	•	plot_figure_3_seeds_90pct_by_active_share()
	•	plot_figure_4_threehop_seeds_vs_coverage()
	•	plot_figure_5_seeds_90pct_two_vs_three_hops()
	•	plot_figure_6_ttfi_vs_seeds()
	•	plot_figure_7_coverage_vs_seeds_se_vs_uk()
	•	plot_figure_8_ttfi_vs_seeds_se_vs_uk()

Each function:
	•	Uses matplotlib (no custom style required).
	•	Reads hard-coded scenario numbers from the paper.
	•	Saves a figureX_*.png file with dpi=300 for direct use in publications.
    Usage Example:
    from figures_seed_uk_se import (
    plot_figure_1_couk_active,
    plot_figure_2_twohop_seeds_vs_coverage,
    plot_figure_3_seeds_90pct_by_active_share,
    plot_figure_4_threehop_seeds_vs_coverage,
    plot_figure_5_seeds_90pct_two_vs_three_hops,
    plot_figure_6_ttfi_vs_seeds,
    plot_figure_7_coverage_vs_seeds_se_vs_uk,
    plot_figure_8_ttfi_vs_seeds_se_vs_uk,
)

plot_figure_1_couk_active()
plot_figure_2_twohop_seeds_vs_coverage()
plot_figure_3_seeds_90pct_by_active_share()
plot_figure_4_threehop_seeds_vs_coverage()
plot_figure_5_seeds_90pct_two_vs_three_hops()
plot_figure_6_ttfi_vs_seeds()
plot_figure_7_coverage_vs_seeds_se_vs_uk()
plot_figure_8_ttfi_vs_seeds_se_vs_uk()

3.3. multi_hop_plots.py – visualising 5- and 10-hop scenarios

Purpose:
Takes the 5-hop and 10-hop tables for UK and Sweden and generates new figures for the paper:
	•	Coverage vs seeds (5 vs 10 hops).
	•	TTFI vs seeds (5 vs 10 hops).

Key function:
	•	plot_multi_hop_coverage_and_ttfi(df: pd.DataFrame, country_label_prefix: str)
Usage Example:
import pandas as pd
from multi_hop_seed_model import build_multi_hop_table, N_UK, N_SE, seeds_UK, seeds_SE
from multi_hop_plots import plot_multi_hop_coverage_and_ttfi

df_uk = build_multi_hop_table(N_UK, seeds_UK, "UK (.co.uk)")
df_se = build_multi_hop_table(N_SE, seeds_SE, "SE (.se)")

plot_multi_hop_coverage_and_ttfi(df_uk, "UK_co_uk")
plot_multi_hop_coverage_and_ttfi(df_se, "SE_se")

This produces four PNG files, for example:
	•	uk_co_uk_multi_hop_coverage.png
	•	uk_co_uk_multi_hop_ttfi.png
	•	se_se_multi_hop_coverage.png
	•	se_se_multi_hop_ttfi.png

These can be referenced as “multi-hop perspective” figures in the paper or in blog posts about extra hops vs extra seeds.

3.4. webgraph_simulation.py – interactive toy model for SEO and crawling

Purpose:
A self-contained Python script that:
	•	Lets you configure:
	•	TOTAL_NODES – number of websites in the graph
(e.g. SE ≈ 1.5M, UK ≈ 8–10M; the script uses smaller numbers for demos).
	•	AVG_EDGES – average outbound links per website
(typically 20–30, but configurable).
	•	NUM_SEEDS – number of seed sites
(e.g. SE 500–2,000 and UK 5,000–50,000).
	•	Computes:
	•	Estimated coverage of the web graph (%) under 2- or 3-hop models.
	•	Estimated TTFI as a function of seed count.
	•	Visualises:
	•	A small toy web graph (100 nodes) with covered vs uncovered nodes.
	•	A TTFI vs number of seed sites curve.

Key functions:
	•	estimate_coverage(n_nodes, avg_deg, num_seeds, hops=2, r=0.6, s=0.45, theta=0.3)
	•	estimate_ttfi(avg_deg, num_seeds, graph_size, base_hop_latency=3.0)
	•	draw_mock_coverage(coverage, title_prefix="Graph Coverage")
	•	plot_coverage_vs_seeds(...)
	•	plot_ttfi_vs_seeds(...)

This script is ideal as a teaching tool for:
	•	SEO practitioners who want to understand why “Google needs thousands of seed sites”.
	•	Researchers who want a quick, visual explanation of coverage vs seeds and TTFI vs seeds.

⸻

4. Installation and Requirements

4.1. Python version
	•	Python 3.9+ is recommended.

4.2. Install dependencies

Create a virtual environment (optional but recommended), then:
pip install -r requirements.txt

A typical requirements.txt will include:
numpy
pandas
matplotlib
networkx
4.3. Running the code

Generate UK & SE 5/10-hop tables:
python -m src.multi_hop_seed_model
Recreate Figures 1–8:
python -m src.figures_seed_uk_se
Plot multi-hop coverage & TTFI (5 vs 10 hops):
python -m src.multi_hop_plots
Run the toy web graph simulation:
python -m src.webgraph_simulation

Then tweak:
	•	TOTAL_NODES, AVG_EDGES, and NUM_SEEDS
inside webgraph_simulation.py to explore different country sizes and seed strategies.

5. Use Cases for SEO, Crawling and Indexing Strategy

This repository is designed for both researchers and SEO professionals who want to:
	•	Quantify how many seed sites are needed for a national market.
	•	Compare Swedish (.se) and UK (.co.uk) web graphs.
	•	Understand how distance from seed sites affects:
	•	Time to First Index (TTFI),
	•	Visibility of SMEs and long-tail domains,
	•	Fairness and coverage of local businesses.
	•	Explore trade-offs between:
	•	Adding more seeds vs
	•	Allowing more hops in the crawler frontier.

Typical applications:
	•	National SEO research and policy discussions (e.g. coverage of SMEs).
	•	Search engine design for niche or country-specific engines.
	•	Educational content for SEO trainings, workshops, and webinars.
	•	Supporting arguments in research papers on TrustRank, seed sites, and web graph structure.

⸻

6. Related Seed Site & TrustRank Research by IncRev

This repository implements and extends the mathematical models used in a series of research papers authored by David Vesterlund (IncRev) on seed sites, TrustRank, and web crawling.

6.1. IncRev SEO Research (IncRev website)
	•	IncRev SEO Research hub:
👉 https://increv.co/academy-research/￼

This page contains practitioner-friendly summaries and full research articles, including:
	•	TrustRank and Seed Sites: Modeling Backlink Value for Web Trust Propagation in a Google-Like Ranking System
	•	How Close Are You to Google’s Seed Sites? The Hidden Factor Behind Fast Indexing
	•	Best Backlinks for SEO – How Link Value Travels Across the Web

Many of these articles link directly to the full mathematical papers hosted on Zenodo.

6.2. IncRev SEO Research Community on Zenodo

All formal research papers and datasets are archived in the INCREV® SEO Research Community on Zenodo:
	•	👉 https://zenodo.org/communities/increvseo/￼

Here you will find, among others:
	•	“Link Building in Sweden – DOI 10.5281/zenodo…”
(Modeling the Swedish link graph and seed sites.)
	•	“Google SEO by IncRev: Why Google Needs Thousands of Seed Sites for Efficient Web Indexing”
	•	“A Negative Proof for the Existence of Seed Sites for Google’s Ranking System”

These works provide the empirical and mathematical basis for the code in this repository.

6.3. Academia.edu profile (full list of papers)

For a complete list of papers, preprints and related research:
	•	👉 David Vesterlund (Independent Researcher) on Academia.edu
https://independent.academia.edu/DavidVesterlund￼

This profile includes:
	•	Seed site and TrustRank papers.
	•	Work on AI search visibility, LLM manipulation and SEO, and
	•	Applied mathematics projects (e.g. prime number research).

⸻

7. Citing This Work

If you use this code or model in an academic paper, blog post, or product, please consider citing:
	•	The relevant Zenodo record(s) for the seed-site paper(s).
	•	The IncRev SEO Research community on Zenodo:
https://zenodo.org/communities/increvseo/￼
	•	The IncRev SEO Research hub:
https://increv.co/academy-research/￼

Example (generic):

Vesterlund, D. (2025). Mathematical Models of Seed Sites, Web Crawling and Indexing Latency for UK and Swedish Domains. INCREV® SEO Research Community, Zenodo.

(Replace with the actual title and DOI from the specific record you use.)

⸻

8. License and Contributions

Specify your license here, for example:
	•	Code: MIT License
	•	Text / figures: CC BY-SA 4.0

Contributions are welcome if they:
	•	Add new country-level scenarios (e.g. .de, .nl, .fr).
	•	Improve parameter estimation from real link graphs (Common Crawl, JISC UK Web Dataset, etc.).
	•	Extend the TTFI model with empirical crawl data.

Please open an issue or pull request if you:
	•	Spot a bug in the math or implementation.
	•	Want to add a new figure for the paper.
	•	Have suggestions for better parameter ranges (D, r, s, θ).

⸻

9. Contact

For questions about the models or collaboration requests:
	•	Author: David Vesterlund
	•	Company: INCREV®
	•	SEO Research Hub: https://increv.co/academy-research/￼
	•	Research Archive: https://zenodo.org/communities/increvseo/￼
	•	Academia Profile: https://independent.academia.edu/DavidVesterlund￼

If you build something cool on top of this repository – especially new analyses of seed sites, web crawling, and indexing latency for other countries – please reach out.
