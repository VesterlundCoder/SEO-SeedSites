"""
webgraph_simulation.py

Toy simulator for seed-site coverage and Time To First Index (TTFI)
on a simplified web-graph model.

Inputs (configure at top of file):
    - TOTAL_NODES: number of websites (nodes) in the graph
      (e.g. SE ~1.5M, UK ~8–10M)
    - AVG_EDGES: average outbound links per website (effective out-degree D)
      (e.g. 20–30 links per domain)
    - NUM_SEEDS: number of seed sites (1–100_000)
      (typical: SE 500–2_000, UK 5_000–50_000)
Outputs:
    - Estimated coverage (%) of the graph from seeds under 2- or 3-hop models
    - Estimated Time To First Index (TTFI) as a function of seed count
    - Small toy graph drawing: covered vs uncovered nodes
    - Plots: coverage vs seeds, and TTFI vs seeds
"""

import math
import random

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# --------------------------
# User-configurable defaults
# --------------------------

# Example country-scale defaults
TOTAL_NODES = 8_400_000   # UK .co.uk active-ish order of magnitude
# TOTAL_NODES = 1_500_000 # SE .se (uncomment to switch scenario)

AVG_EDGES = 25            # average outbound links per website (D)

NUM_SEEDS = 10_000        # seed sites in the graph

# Model parameters
HOPS = 2                  # 2 or 3
DEDUP_R = 0.6             # second-hop deduplication factor r
DEDUP_S = 0.45            # third-hop deduplication factor s (if HOPS = 3)
OVERLAP_THETA = 0.3       # cross-seed overlap θ

# TTFI model parameters
BASE_HOP_LATENCY = 3.0    # seconds per hop, rough latency scale

# --------------------------------
# Core model: coverage and TTFI
# --------------------------------

def estimate_coverage(n_nodes: int,
                      avg_deg: float,
                      num_seeds: int,
                      hops: int = 2,
                      r: float = 0.6,
                      s: float = 0.45,
                      theta: float = 0.3):
    """
    Estimate coverage fraction and number of discovered nodes
    for a given number of seeds, using your T2/T3 formulas:

        T2 ≈ 1 + D + r D^2
        T3 ≈ 1 + D + r D^2 + s D^3

    and inflating by 1/(1 - θ) to account for cross-seed overlap.
    """
    if num_seeds <= 0:
        return 0.0, 0.0

    if hops == 2:
        T2 = 1.0 + avg_deg + r * (avg_deg ** 2)
        total_discovered = (num_seeds * T2) / (1.0 - theta)
    elif hops == 3:
        T3 = 1.0 + avg_deg + r * (avg_deg ** 2) + s * (avg_deg ** 3)
        total_discovered = (num_seeds * T3) / (1.0 - theta)
    else:
        raise ValueError("Only 2 or 3 hops supported")

    coverage = min(1.0, total_discovered / float(n_nodes))
    return coverage, total_discovered


def estimate_ttfi(avg_deg: float,
                  num_seeds: int,
                  graph_size: int,
                  base_hop_latency: float = 3.0):
    """
    Very simple TTFI model:

        - Approximate expected hop-distance from a random node
          to the nearest seed as:

              E[dist] ~ log_{D+1}(graph_size / num_seeds + 1)

        - TTFI ~ base_hop_latency * E[dist]

    This is a stylized model, not a measurement, but it captures
    the idea that more seeds => shorter distances => lower TTFI.
    """
    if num_seeds <= 0:
        return float("inf")

    effective_branching = max(avg_deg, 2.0)
    expected_hops = max(
        1.0,
        math.log(graph_size / num_seeds + 1.0, effective_branching + 1.0),
    )
    return base_hop_latency * expected_hops

# --------------------------------
# Visualization helpers
# --------------------------------

def draw_mock_coverage(coverage: float,
                       title_prefix: str = "Graph Coverage"):
    """
    Draw a small toy graph (100 nodes, Erdos-Renyi) and colour
    a fraction of nodes as "covered" vs "uncovered" based on
    the coverage value.

    This is purely illustrative; it is *not* your real .co.uk graph.
    """
    num_nodes = 100
    G = nx.erdos_renyi_graph(num_nodes, 0.05, seed=42)

    # Randomly choose covered nodes in proportion to coverage
    num_covered = int(round(coverage * num_nodes))
    covered_nodes = set(random.sample(list(G.nodes()), num_covered))

    node_colors = [
        "green" if node in covered_nodes else "lightgray"
        for node in G.nodes()
    ]

    plt.figure(figsize=(7, 5))
    pos = nx.spring_layout(G, seed=42)
    nx.draw_networkx(
        G,
        pos=pos,
        node_color=node_colors,
        node_size=80,
        with_labels=False,
        edge_color="gray",
    )
    plt.title(f"{title_prefix}: ~{coverage * 100:.1f}% covered")
    plt.tight_layout()
    plt.show()


def plot_coverage_vs_seeds(total_nodes: int,
                           avg_deg: float,
                           hops: int,
                           r: float,
                           s: float,
                           theta: float):
    """
    Plot coverage (%) vs seed sites, for a range of seed counts.
    """
    seed_range = np.linspace(500, 100_000, 50)
    coverages = [
        estimate_coverage(total_nodes, avg_deg, int(seeds),
                          hops=hops, r=r, s=s, theta=theta)[0] * 100.0
        for seeds in seed_range
    ]

    plt.figure(figsize=(8, 4))
    plt.plot(seed_range, coverages)
    plt.xlabel("Number of Seed Sites")
    plt.ylabel("Estimated Coverage (%)")
    plt.title(f"Coverage vs Seed Sites ({hops}-hop model)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_ttfi_vs_seeds(total_nodes: int,
                       avg_deg: float,
                       base_hop_latency: float = 3.0):
    """
    Plot TTFI vs seed sites for a range of seed counts.
    """
    seed_range = np.linspace(500, 100_000, 50)
    ttfi_vals = [
        estimate_ttfi(avg_deg, int(seeds), total_nodes,
                      base_hop_latency=base_hop_latency)
        for seeds in seed_range
    ]

    plt.figure(figsize=(8, 4))
    plt.plot(seed_range, ttfi_vals)
    plt.xlabel("Number of Seed Sites")
    plt.ylabel("Estimated Time to First Index (seconds)")
    plt.title("TTFI vs Number of Seed Sites")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# --------------------------
# Main: simple demo run
# --------------------------

if __name__ == "__main__":
    coverage_pct, discovered = estimate_coverage(
        TOTAL_NODES, AVG_EDGES, NUM_SEEDS,
        hops=HOPS, r=DEDUP_R, s=DEDUP_S, theta=OVERLAP_THETA
    )
    ttfi = estimate_ttfi(
        AVG_EDGES, NUM_SEEDS, TOTAL_NODES,
        base_hop_latency=BASE_HOP_LATENCY
    )

    print(f"Total sites (N):        {TOTAL_NODES:,}")
    print(f"Avg links per site (D): {AVG_EDGES:.2f}")
    print(f"Seed sites (n):         {NUM_SEEDS:,}")
    print(f"Hops:                    {HOPS}")
    print(f"Estimated coverage:     {coverage_pct * 100:.2f}% "
          f"(~{int(discovered):,} sites reachable)")
    print(f"Estimated TTFI:         {ttfi:.2f} seconds")

    # Illustrative toy graph for current coverage
    draw_mock_coverage(coverage_pct, title_prefix="Toy Web Graph Coverage")

    # Curves for paper figures
    plot_coverage_vs_seeds(
        TOTAL_NODES, AVG_EDGES, HOPS,
        r=DEDUP_R, s=DEDUP_S, theta=OVERLAP_THETA
    )
    plot_ttfi_vs_seeds(TOTAL_NODES, AVG_EDGES,
                       base_hop_latency=BASE_HOP_LATENCY)
