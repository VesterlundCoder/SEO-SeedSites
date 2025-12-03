Purpose: All plotting code for Figures 1–8 in the paper.

Dependencies: matplotlib.pyplot as plt, numpy as np, math, and the model params (D, r, s, theta, tau_hop, N_UK, N_SE).

Functions (one per figure):
	1.	plot_figure_1_couk_active()
	•	Bar chart: total .co.uk vs estimated active share (43%, 50%).
	•	Saves: figure1_couk_active_share.png.
	2.	plot_figure_2_twohop_seeds_vs_coverage()
	•	Line chart: seeds vs coverage for 2-hop model, 43% active share.
	•	Uses table values for Conservative / Baseline / Optimistic scenarios.
	•	Saves: figure2_twohop_seeds_vs_coverage_43.png.
	3.	plot_figure_3_seeds_90pct_by_active_share()
	•	Grouped bar chart: seeds needed at 90% coverage for 43% vs 50% active.
	•	For three scenarios: Conservative / Baseline / Optimistic.
	•	Saves: figure3_seeds_90pct_active_share.png.
	4.	plot_figure_4_threehop_seeds_vs_coverage()
	•	Line chart: seeds vs coverage for 3-hop model, 43% active share.
	•	Conservative / Baseline / Optimistic.
	•	Saves: figure4_threehop_seeds_vs_coverage_43.png.
	5.	plot_figure_5_seeds_90pct_two_vs_three_hops()
	•	Grouped bar chart: seeds at 90% coverage for 2-hop vs 3-hop (43% active).
	•	Saves: figure5_seeds_90pct_two_vs_three_hops.png.
	6.	plot_figure_6_ttfi_vs_seeds()
	•	TTFI vs seed count for .co.uk baseline.
	•	Uses the distance-based TTFI model.
	•	Saves: figure6_ttfi_vs_seeds_couk.png.
	7.	plot_figure_7_coverage_vs_seeds_se_vs_uk()
	•	2-hop coverage vs seeds for .co.uk and .se.
	•	Uses T_k and coverage fraction for each country.
	•	Saves: figure7_coverage_vs_seeds_se_vs_uk.png.
	8.	plot_figure_8_ttfi_vs_seeds_se_vs_uk()
	•	TTFI vs seed count, .co.uk vs .se.
	•	Same distance-based TTFI model, different N and seed ranges.
	•	Saves: figure8_ttfi_vs_seeds_se_vs_uk.png.

✔ This file is basically “all figure generation for the main paper”.
