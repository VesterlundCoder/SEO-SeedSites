webgraph_coverage_simple.py

(shorter script near the end, “Python script – Web graph coverage as optimization problem”)

Purpose: Simpler educational script focusing on:
	•	Direct 2-/3-hop coverage %
	•	TTFI as a function of seeds
	•	A mock coverage graph + TTFI curve

Key contents:
	•	Inputs: TOTAL_NODES, AVG_EDGES, NUM_SEEDS, HOPS, DEDUP_R, DEDUP_S, OVERLAP_THETA.
	•	Functions:
	•	estimate_coverage(...)
	•	Similar to above but returns coverage in % and discovered count.
	•	estimate_ttfi(avg_deg, num_seeds, graph_size)
	•	Slightly different: uses base_latency and hop_scaling = log(graph_size / num_seeds + 1), then
TTFI = base_latency / hop_scaling.
	•	draw_mock_coverage(n_total, n_covered)
	•	Erdos–Rényi graph, colours a proportion of nodes as covered.
	•	plot_ttfi_curve(total_nodes, avg_deg)
	•	Plots TTFI vs seed count for a seed range [100, 100,000].

✔ This one is a lighter “demo / teaching” version you can put in a /examples/ folder.
