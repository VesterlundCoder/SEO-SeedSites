multi_hop_plots.py – visualising 5- and 10-hop scenarios

Purpose:
Takes the 5-hop and 10-hop tables for UK and Sweden and generates new figures for the paper:
	•	Coverage vs seeds (5 vs 10 hops).
	•	TTFI vs seeds (5 vs 10 hops).

Key function:
	•	plot_multi_hop_coverage_and_ttfi(df: pd.DataFrame, country_label_prefix: str)

Usage example:

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
