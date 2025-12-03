webgraph_simulation.py – interactive toy model for SEO and crawling

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
