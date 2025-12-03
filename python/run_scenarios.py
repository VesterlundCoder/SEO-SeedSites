"""
run_scenarios.py

Run multiple simulation scenarios for UK and SE with different seed counts
and hop depths (2-hop vs 3-hop).
"""

import pandas as pd
from webgraph_simulation import estimate_coverage, estimate_ttfi

# Configuration
N_UK = 8_400_000
N_SE = 1_500_000
AVG_EDGES = 25
DEDUP_R = 0.6
DEDUP_S = 0.45
OVERLAP_THETA = 0.3
BASE_HOP_LATENCY = 3.0

# Seed configurations
seeds_UK = [100, 1_000, 5_000, 50_000]
seeds_SE = [10, 100, 500, 1_000, 5_000]

def run_all_scenarios():
    """Run all UK and SE scenarios for 2-hop and 3-hop models."""
    
    results = []
    
    # UK scenarios
    for num_seeds in seeds_UK:
        # 2-hop
        cov_2hop, disc_2hop = estimate_coverage(
            N_UK, AVG_EDGES, num_seeds,
            hops=2, r=DEDUP_R, s=DEDUP_S, theta=OVERLAP_THETA
        )
        ttfi_2hop = estimate_ttfi(
            AVG_EDGES, num_seeds, N_UK, base_hop_latency=BASE_HOP_LATENCY
        )
        
        # 3-hop
        cov_3hop, disc_3hop = estimate_coverage(
            N_UK, AVG_EDGES, num_seeds,
            hops=3, r=DEDUP_R, s=DEDUP_S, theta=OVERLAP_THETA
        )
        ttfi_3hop = estimate_ttfi(
            AVG_EDGES, num_seeds, N_UK, base_hop_latency=BASE_HOP_LATENCY
        )
        
        results.append({
            "Country": "UK",
            "Seeds": num_seeds,
            "Hops": 2,
            "Coverage_%": round(cov_2hop * 100, 2),
            "Discovered": int(disc_2hop),
            "TTFI_s": round(ttfi_2hop, 2)
        })
        
        results.append({
            "Country": "UK",
            "Seeds": num_seeds,
            "Hops": 3,
            "Coverage_%": round(cov_3hop * 100, 2),
            "Discovered": int(disc_3hop),
            "TTFI_s": round(ttfi_3hop, 2)
        })
    
    # SE scenarios
    for num_seeds in seeds_SE:
        # 2-hop
        cov_2hop, disc_2hop = estimate_coverage(
            N_SE, AVG_EDGES, num_seeds,
            hops=2, r=DEDUP_R, s=DEDUP_S, theta=OVERLAP_THETA
        )
        ttfi_2hop = estimate_ttfi(
            AVG_EDGES, num_seeds, N_SE, base_hop_latency=BASE_HOP_LATENCY
        )
        
        # 3-hop
        cov_3hop, disc_3hop = estimate_coverage(
            N_SE, AVG_EDGES, num_seeds,
            hops=3, r=DEDUP_R, s=DEDUP_S, theta=OVERLAP_THETA
        )
        ttfi_3hop = estimate_ttfi(
            AVG_EDGES, num_seeds, N_SE, base_hop_latency=BASE_HOP_LATENCY
        )
        
        results.append({
            "Country": "SE",
            "Seeds": num_seeds,
            "Hops": 2,
            "Coverage_%": round(cov_2hop * 100, 2),
            "Discovered": int(disc_2hop),
            "TTFI_s": round(ttfi_2hop, 2)
        })
        
        results.append({
            "Country": "SE",
            "Seeds": num_seeds,
            "Hops": 3,
            "Coverage_%": round(cov_3hop * 100, 2),
            "Discovered": int(disc_3hop),
            "TTFI_s": round(ttfi_3hop, 2)
        })
    
    return pd.DataFrame(results)


if __name__ == "__main__":
    print("=" * 80)
    print("MULTI-SCENARIO SIMULATION: UK AND SE (2-HOP VS 3-HOP)")
    print("=" * 80)
    print()
    print("Configuration:")
    print(f"  UK Total Nodes:    {N_UK:,}")
    print(f"  SE Total Nodes:    {N_SE:,}")
    print(f"  Avg Out-degree:    {AVG_EDGES}")
    print(f"  Dedup r (2nd hop): {DEDUP_R}")
    print(f"  Dedup s (3rd hop): {DEDUP_S}")
    print(f"  Overlap θ:         {OVERLAP_THETA}")
    print(f"  Hop latency:       {BASE_HOP_LATENCY}s")
    print()
    print(f"  UK Seeds:          {seeds_UK}")
    print(f"  SE Seeds:          {seeds_SE}")
    print()
    print("-" * 80)
    
    # Run all scenarios
    df = run_all_scenarios()
    
    # Display UK results
    print("\n🇬🇧 UK (.co.uk) RESULTS")
    print("=" * 80)
    df_uk = df[df["Country"] == "UK"]
    print(df_uk.to_string(index=False))
    
    # Display SE results
    print("\n\n🇸🇪 SE (.se) RESULTS")
    print("=" * 80)
    df_se = df[df["Country"] == "SE"]
    print(df_se.to_string(index=False))
    
    # Summary comparison
    print("\n\n📊 2-HOP VS 3-HOP COMPARISON")
    print("=" * 80)
    
    print("\nUK - Coverage Boost from 3rd Hop:")
    for num_seeds in seeds_UK:
        cov_2 = df_uk[(df_uk["Seeds"] == num_seeds) & (df_uk["Hops"] == 2)]["Coverage_%"].values[0]
        cov_3 = df_uk[(df_uk["Seeds"] == num_seeds) & (df_uk["Hops"] == 3)]["Coverage_%"].values[0]
        boost = cov_3 - cov_2
        print(f"  {num_seeds:>6,} seeds: {cov_2:6.2f}% → {cov_3:6.2f}% (+{boost:5.2f}%)")
    
    print("\nSE - Coverage Boost from 3rd Hop:")
    for num_seeds in seeds_SE:
        cov_2 = df_se[(df_se["Seeds"] == num_seeds) & (df_se["Hops"] == 2)]["Coverage_%"].values[0]
        cov_3 = df_se[(df_se["Seeds"] == num_seeds) & (df_se["Hops"] == 3)]["Coverage_%"].values[0]
        boost = cov_3 - cov_2
        print(f"  {num_seeds:>6,} seeds: {cov_2:6.2f}% → {cov_3:6.2f}% (+{boost:5.2f}%)")
    
    # Save to CSV
    output_file = "../output/scenario_comparison.csv"
    df.to_csv(output_file, index=False)
    print(f"\n✓ Results saved to: {output_file}")
    
    print("\n" + "=" * 80)
    print("✅ SIMULATION COMPLETE")
    print("=" * 80)
