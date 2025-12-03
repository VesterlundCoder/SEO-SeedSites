"""
Domain Coverage Research: Multi-hop Coverage and TTFI Analysis
Generates tables and figures for research paper on domain discovery models.
"""

import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# -------------------------
# 1. Model parameters
# -------------------------

# Baseline graph parameters
D = 10.37      # effective intra-TLD out-degree
r = 0.6        # second-hop deduplication factor
s = 0.45       # third+ hop deduplication factor
theta = 0.3    # cross-seed overlap
tau_hop = 3.0  # average latency per hop in seconds

# Country sizes (active domains)
N_UK = 8_400_000
N_SE = 1_500_000

# Seed counts as in the examples
seeds_UK = [5_000, 10_000, 20_000, 50_000]
seeds_SE = [500, 1_000, 2_000, 5_000]


# -------------------------
# 2. Core functions
# -------------------------

def T_k(D: float, r: float, s: float, k: int) -> float:
    """
    Per-seed coverage up to k hops.

    Definition:
        T_k(D, r, s) = 1 + D + r * D^2 + sum_{h=3..k} s * D^h

    This matches the previous T2/T3 formulas:
        T2 = 1 + D + r D^2
        T3 = 1 + D + r D^2 + s D^3
    and extends them by assuming the same s applies to hops >= 3.
    """
    if k < 1:
        return 0.0

    total = 1.0        # self
    if k >= 1:
        total += D
    if k >= 2:
        total += r * (D ** 2)
    if k >= 3:
        for h in range(3, k + 1):
            total += s * (D ** h)
    return total


def estimate_coverage(N: int, num_seeds: int,
                      D: float, r: float, s: float,
                      theta: float, k: int):
    """
    Estimate k-hop coverage fraction and total discovered nodes.

    Steps:
      1. Compute T_k(D, r, s) for one seed.
      2. Multiply by num_seeds.
      3. Inflate by 1 / (1 - theta) to account for cross-seed overlap.
      4. Clip at N (cannot discover more than N domains).
    """
    T = T_k(D, r, s, k)
    discovered = (num_seeds * T) / (1.0 - theta)
    coverage_frac = min(1.0, discovered / float(N))
    return coverage_frac, discovered


def expected_distance(D: float, N: int, num_seeds: int) -> float:
    """
    Approximate expected hop distance from a random node to
    the nearest seed in a branching model.

        E[dist] ~ log_{D+1}(N / num_seeds + 1)

    We clamp the result at >= 1 hop.
    """
    eff_branch = max(D, 2.0)
    dist = math.log(N / num_seeds + 1.0, eff_branch + 1.0)
    return max(1.0, dist)


def estimate_ttfi(D: float, N: int, num_seeds: int,
                  tau_hop: float = 3.0,
                  k_horizon: int | None = None) -> float:
    """
    Estimate Time To First Index (TTFI) in seconds.

    Base model:
        TTFI ~ tau_hop * E[dist]

    If k_horizon is provided, we truncate the distance:
        E[dist_k] = min(E[dist], k_horizon)
    """
    dist = expected_distance(D, N, num_seeds)
    if k_horizon is not None:
        dist = min(dist, k_horizon)
    return tau_hop * dist


# -------------------------
# 3. Build summary tables
# -------------------------

def build_multi_hop_table(N: int, seeds_list: list[int],
                          label: str) -> pd.DataFrame:
    """
    Build a table with coverage and TTFI for k = 5 and k = 10 hops.
    """
    rows = []
    for n in seeds_list:
        cov5, disc5 = estimate_coverage(N, n, D, r, s, theta, k=5)
        cov10, disc10 = estimate_coverage(N, n, D, r, s, theta, k=10)

        ttfi5 = estimate_ttfi(D, N, n, tau_hop, k_horizon=5)
        ttfi10 = estimate_ttfi(D, N, n, tau_hop, k_horizon=10)

        rows.append({
            "Country": label,
            "Seeds": n,
            "Coverage_5hop_%": cov5 * 100.0,
            "TTFI_5hop_s": ttfi5,
            "Coverage_10hop_%": cov10 * 100.0,
            "TTFI_10hop_s": ttfi10,
        })
    return pd.DataFrame(rows)


# -------------------------
# Figure functions
# -------------------------

def plot_figure_1_couk_active():
    """
    Bar chart:
      - Total .co.uk domains
      - Estimated active domains (43% and 50%)
    """
    total = 8_395_329         # total .co.uk domains
    active_43 = total * 0.43
    active_50 = total * 0.50

    labels = ["Total .co.uk", "Active (43%)", "Active (50%)"]
    values = [total, active_43, active_50]

    plt.figure()
    plt.bar(labels, values)
    plt.ylabel("Number of domains")
    plt.title(".co.uk domain counts and active share")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig("output/figure1_couk_active_share.png", dpi=300)
    plt.close()
    print("✓ Generated: figure1_couk_active_share.png")


def plot_figure_2_twohop_seeds_vs_coverage():
    """
    Line chart: coverage vs seeds for each scenario
    using the 43% active table.
    """
    # Table values from the paper (43% active share)
    coverage = np.array([80, 90, 95])

    seeds_conservative = np.array([130_220, 146_498, 154_636])
    seeds_baseline     = np.array([ 54_392,  61_190,  64_590])
    seeds_optimistic   = np.array([ 26_533,  29_849,  31_508])

    plt.figure()
    plt.plot(coverage, seeds_conservative, marker="o", label="Conservative")
    plt.plot(coverage, seeds_baseline, marker="o", label="Baseline")
    plt.plot(coverage, seeds_optimistic, marker="o", label="Optimistic")

    plt.xlabel("Coverage (%)")
    plt.ylabel("Seeds required")
    plt.title("Two-hop model (.co.uk, 43% active): seeds vs coverage")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("output/figure2_twohop_seeds_vs_coverage_43.png", dpi=300)
    plt.close()
    print("✓ Generated: figure2_twohop_seeds_vs_coverage_43.png")


def plot_figure_3_seeds_90pct_by_active_share():
    """
    Grouped bar chart: seeds at 90% coverage for 43% vs 50% active,
    per scenario (Conservative, Baseline, Optimistic).
    """
    scenarios = ["Conservative", "Baseline", "Optimistic"]
    x = np.arange(len(scenarios))
    width = 0.35

    # Seeds at 90% coverage from both tables
    seeds_43 = np.array([146_498, 61_190, 29_849])
    seeds_50 = np.array([170_346, 71_152, 34_709])

    plt.figure()
    plt.bar(x - width/2, seeds_43, width, label="43% active")
    plt.bar(x + width/2, seeds_50, width, label="50% active")

    plt.xticks(x, scenarios)
    plt.ylabel("Seeds required")
    plt.title("Seeds at 90% coverage: 43% vs 50% active share")
    plt.legend()
    plt.tight_layout()
    plt.savefig("output/figure3_seeds_90pct_active_share.png", dpi=300)
    plt.close()
    print("✓ Generated: figure3_seeds_90pct_active_share.png")


def plot_figure_4_threehop_seeds_vs_coverage():
    """
    Line chart: coverage vs seeds for the three-hop model (43% active).
    """
    coverage = np.array([80, 90, 95])

    seeds_conservative = np.array([25_744, 28_961, 30_570])
    seeds_baseline     = np.array([ 7_148,  8_041,  8_488])
    seeds_optimistic   = np.array([ 2_580,  2_903,  3_064])

    plt.figure()
    plt.plot(coverage, seeds_conservative, marker="o", label="Conservative")
    plt.plot(coverage, seeds_baseline, marker="o", label="Baseline")
    plt.plot(coverage, seeds_optimistic, marker="o", label="Optimistic")

    plt.xlabel("Coverage (%)")
    plt.ylabel("Seeds required")
    plt.title("Three-hop model (.co.uk, 43% active): seeds vs coverage")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("output/figure4_threehop_seeds_vs_coverage_43.png", dpi=300)
    plt.close()
    print("✓ Generated: figure4_threehop_seeds_vs_coverage_43.png")


def plot_figure_5_seeds_90pct_two_vs_three_hops():
    """
    Grouped bar chart: seeds at 90% coverage, two-hop vs three-hop,
    for each scenario under 43% active.
    """
    scenarios = ["Conservative", "Baseline", "Optimistic"]
    x = np.arange(len(scenarios))
    width = 0.35

    seeds_twohop_90  = np.array([146_498, 61_190, 29_849])
    seeds_threehop_90 = np.array([28_961,  8_041,  2_903])

    plt.figure()
    plt.bar(x - width/2, seeds_twohop_90, width, label="Two-hop")
    plt.bar(x + width/2, seeds_threehop_90, width, label="Three-hop")

    plt.xticks(x, scenarios)
    plt.ylabel("Seeds required")
    plt.title(".co.uk: seeds at 90% coverage (2 vs 3 hops, 43% active)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("output/figure5_seeds_90pct_two_vs_three_hops.png", dpi=300)
    plt.close()
    print("✓ Generated: figure5_seeds_90pct_two_vs_three_hops.png")


def plot_figure_6_ttfi_vs_seeds():
    """
    TTFI vs number of seed sites using the simple distance model.
    Uses the .co.uk parameters and the seed range from the example.
    """
    seed_range = np.array([5_000, 10_000, 20_000, 50_000])

    ttfi_vals = [
        tau_hop * expected_distance(D, N_UK, int(n)) for n in seed_range
    ]

    plt.figure()
    plt.plot(seed_range, ttfi_vals, marker="o")
    plt.xlabel("Number of seed sites")
    plt.ylabel("Estimated TTFI (seconds)")
    plt.title(".co.uk baseline: TTFI vs number of seed sites")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("output/figure6_ttfi_vs_seeds_couk.png", dpi=300)
    plt.close()
    print("✓ Generated: figure6_ttfi_vs_seeds_couk.png")


def plot_figure_7_coverage_vs_seeds_se_vs_uk():
    """
    Coverage vs seeds for .se and .co.uk under the same D,r,s,theta,
    using the illustrative multi-hop model (e.g. k=2).
    """
    seeds_uk = np.array([5_000, 10_000, 20_000, 50_000])
    seeds_se = np.array([500, 1_000, 2_000, 5_000])

    def coverage_fraction(N, n, D, r, s, theta, k):
        T = T_k(D, r, s, k)
        discovered = (n * T) / (1.0 - theta)
        return min(1.0, discovered / N)

    cov_uk = [coverage_fraction(N_UK, int(n), D, r, s, theta, k=2)
              for n in seeds_uk]
    cov_se = [coverage_fraction(N_SE, int(n), D, r, s, theta, k=2)
              for n in seeds_se]

    plt.figure()
    plt.plot(seeds_uk, np.array(cov_uk) * 100.0,
             marker="o", label=".co.uk")
    plt.plot(seeds_se, np.array(cov_se) * 100.0,
             marker="o", label=".se")

    plt.xlabel("Number of seed sites")
    plt.ylabel("Coverage (%)")
    plt.title("Two-hop coverage vs seed sites: .co.uk vs .se")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("output/figure7_coverage_vs_seeds_se_vs_uk.png", dpi=300)
    plt.close()
    print("✓ Generated: figure7_coverage_vs_seeds_se_vs_uk.png")


def plot_figure_8_ttfi_vs_seeds_se_vs_uk():
    """
    TTFI vs seeds for .se and .co.uk under the same D and tau_hop.
    """
    seeds_uk = np.array([5_000, 10_000, 20_000, 50_000])
    seeds_se = np.array([500, 1_000, 2_000, 5_000])

    ttfi_uk = [tau_hop * expected_distance(D, N_UK, int(n))
               for n in seeds_uk]
    ttfi_se = [tau_hop * expected_distance(D, N_SE, int(n))
               for n in seeds_se]

    plt.figure()
    plt.plot(seeds_uk, ttfi_uk, marker="o", label=".co.uk")
    plt.plot(seeds_se, ttfi_se, marker="o", label=".se")

    plt.xlabel("Number of seed sites")
    plt.ylabel("Estimated TTFI (seconds)")
    plt.title("TTFI vs seed sites: .co.uk vs .se")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("output/figure8_ttfi_vs_seeds_se_vs_uk.png", dpi=300)
    plt.close()
    print("✓ Generated: figure8_ttfi_vs_seeds_se_vs_uk.png")


def plot_multi_hop_coverage_and_ttfi(df, country_label_prefix):
    """
    Given a DataFrame with columns:
        Seeds, Coverage_5hop_%, Coverage_10hop_%,
        TTFI_5hop_s, TTFI_10hop_s
    generate two figures:
      - coverage vs seeds (5 vs 10 hops)
      - TTFI vs seeds (5 vs 10 hops)
    """
    seeds = df["Seeds"].to_numpy()
    cov5 = df["Coverage_5hop_%"].to_numpy()
    cov10 = df["Coverage_10hop_%"].to_numpy()
    ttfi5 = df["TTFI_5hop_s"].to_numpy()
    ttfi10 = df["TTFI_10hop_s"].to_numpy()

    # Coverage vs seeds
    plt.figure()
    plt.plot(seeds, cov5, marker="o", label="5 hops")
    plt.plot(seeds, cov10, marker="o", label="10 hops")
    plt.xlabel("Number of seed sites")
    plt.ylabel("Coverage (%)")
    plt.title(f"{country_label_prefix}: coverage vs seeds (5 vs 10 hops)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    outfile_cov = f"output/{country_label_prefix.lower().replace(' ', '_')}_multi_hop_coverage.png"
    plt.savefig(outfile_cov, dpi=300)
    plt.close()
    print(f"✓ Generated: {country_label_prefix.lower().replace(' ', '_')}_multi_hop_coverage.png")

    # TTFI vs seeds
    plt.figure()
    plt.plot(seeds, ttfi5, marker="o", label="5 hops")
    plt.plot(seeds, ttfi10, marker="o", label="10 hops")
    plt.xlabel("Number of seed sites")
    plt.ylabel("Estimated TTFI (seconds)")
    plt.title(f"{country_label_prefix}: TTFI vs seeds (5 vs 10 hops)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    outfile_ttfi = f"output/{country_label_prefix.lower().replace(' ', '_')}_multi_hop_ttfi.png"
    plt.savefig(outfile_ttfi, dpi=300)
    plt.close()
    print(f"✓ Generated: {country_label_prefix.lower().replace(' ', '_')}_multi_hop_ttfi.png")


# -------------------------
# Main execution
# -------------------------

def main():
    """Generate all tables and figures for the research paper."""
    
    # Create output directory
    Path("output").mkdir(exist_ok=True)
    
    print("=" * 80)
    print("DOMAIN COVERAGE RESEARCH - TABLE AND FIGURE GENERATION")
    print("=" * 80)
    print()
    
    # -------------------------
    # Generate tables
    # -------------------------
    print("📊 GENERATING TABLES...")
    print("-" * 80)
    
    df_uk = build_multi_hop_table(N_UK, seeds_UK, "UK (.co.uk)")
    df_se = build_multi_hop_table(N_SE, seeds_SE, "SE (.se)")
    
    print("\n🇬🇧 UK (.co.uk): 5- and 10-hop coverage and TTFI")
    print(df_uk.to_string(index=False, float_format=lambda x: f"{x:.2f}"))
    
    print("\n🇸🇪 SE (.se): 5- and 10-hop coverage and TTFI")
    print(df_se.to_string(index=False, float_format=lambda x: f"{x:.2f}"))
    
    # Save to CSV
    df_uk.to_csv("output/uk_multi_hop_results.csv", index=False)
    df_se.to_csv("output/se_multi_hop_results.csv", index=False)
    print("\n✓ Saved: uk_multi_hop_results.csv")
    print("✓ Saved: se_multi_hop_results.csv")
    
    # -------------------------
    # Generate figures 1-8
    # -------------------------
    print("\n📈 GENERATING FIGURES 1-8...")
    print("-" * 80)
    
    plot_figure_1_couk_active()
    plot_figure_2_twohop_seeds_vs_coverage()
    plot_figure_3_seeds_90pct_by_active_share()
    plot_figure_4_threehop_seeds_vs_coverage()
    plot_figure_5_seeds_90pct_two_vs_three_hops()
    plot_figure_6_ttfi_vs_seeds()
    plot_figure_7_coverage_vs_seeds_se_vs_uk()
    plot_figure_8_ttfi_vs_seeds_se_vs_uk()
    
    # -------------------------
    # Generate multi-hop figures
    # -------------------------
    print("\n📈 GENERATING MULTI-HOP COVERAGE/TTFI FIGURES...")
    print("-" * 80)
    
    plot_multi_hop_coverage_and_ttfi(df_uk, "UK_co_uk")
    plot_multi_hop_coverage_and_ttfi(df_se, "SE_se")
    
    print("\n" + "=" * 80)
    print("✅ ALL TABLES AND FIGURES GENERATED SUCCESSFULLY!")
    print("=" * 80)
    print("\n📁 Output location: ./output/")
    print("\nGenerated files:")
    print("  Tables:")
    print("    - uk_multi_hop_results.csv")
    print("    - se_multi_hop_results.csv")
    print("  Figures:")
    print("    - figure1_couk_active_share.png")
    print("    - figure2_twohop_seeds_vs_coverage_43.png")
    print("    - figure3_seeds_90pct_active_share.png")
    print("    - figure4_threehop_seeds_vs_coverage_43.png")
    print("    - figure5_seeds_90pct_two_vs_three_hops.png")
    print("    - figure6_ttfi_vs_seeds_couk.png")
    print("    - figure7_coverage_vs_seeds_se_vs_uk.png")
    print("    - figure8_ttfi_vs_seeds_se_vs_uk.png")
    print("    - uk_co_uk_multi_hop_coverage.png")
    print("    - uk_co_uk_multi_hop_ttfi.png")
    print("    - se_se_multi_hop_coverage.png")
    print("    - se_se_multi_hop_ttfi.png")
    print()


if __name__ == "__main__":
    main()
