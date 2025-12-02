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
