Purpose: Core analytical model for coverage & TTFI, including 5- and 10-hop calculations and the UK/SE tables.

Key contents:
	•	Global parameters
	•	D = 10.37 — effective intra-TLD out-degree
	•	r = 0.6 — 2nd-hop deduplication factor
	•	s = 0.45 — 3rd+ hop dedup factor
	•	theta = 0.3 — cross-seed overlap
	•	tau_hop = 3.0 — seconds per hop
	•	N_UK = 8_400_000, N_SE = 1_500_000
	•	Seed lists: seeds_UK = [5_000, 10_000, 20_000, 50_000], seeds_SE = [500, 1_000, 2_000, 5_000]
	•	Functions
	•	T_k(D: float, r: float, s: float, k: int) -> float
Per-seed coverage up to k hops:
T_k \approx 1 + D + rD^2 + \sum_{h=3}^k sD^h
Generalises your T₂/T₃ formulas.
	•	estimate_coverage(N: int, num_seeds: int, D: float, r: float, s: float, theta: float, k: int)
	•	Uses T_k
	•	Applies 1/(1 − θ) inflation for cross-seed overlap
	•	Returns (coverage_fraction, discovered_nodes) with clipping at N.
	•	expected_distance(D: float, N: int, num_seeds: int) -> float
	•	Approximate expected hop distance to nearest seed:
\mathbb{E}[\text{dist}] \approx \log_{D+1}\!\left(\frac{N}{n} + 1\right)
	•	Clamped to ≥ 1.
	•	estimate_ttfi(D: float, N: int, num_seeds: int, tau_hop: float = 3.0, k_horizon: int | None = None) -> float
	•	TTFI ≈ τ_hop · E[dist]
	•	Optional k_horizon truncates distance: min(E[dist], k_horizon).
	•	build_multi_hop_table(N: int, seeds_list: list[int], label: str) -> pd.DataFrame
	•	Builds 5- and 10-hop coverage + TTFI table for a country.
	•	Columns: Country, Seeds, Coverage_5hop_%, TTFI_5hop_s, Coverage_10hop_%, TTFI_10hop_s.
	•	Main script section
	•	Builds df_uk, df_se via build_multi_hop_table.
	•	Prints tables to console.
	•	Writes to uk_multi_hop_results.csv, se_multi_hop_results.csv.

✔ This file backs the “extra hops vs extra seeds” tables in the paper.
