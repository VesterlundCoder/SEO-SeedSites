"""
visualize_scenarios.py

Create visualizations for the multi-scenario simulation results.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load results
df = pd.read_csv("../output/scenario_comparison.csv")

# Split by country
df_uk = df[df["Country"] == "UK"]
df_se = df[df["Country"] == "SE"]

# -------------------------
# Figure 1: UK 2-hop vs 3-hop Coverage
# -------------------------
plt.figure(figsize=(10, 5))

uk_seeds = df_uk[df_uk["Hops"] == 2]["Seeds"].values
uk_cov_2hop = df_uk[df_uk["Hops"] == 2]["Coverage_%"].values
uk_cov_3hop = df_uk[df_uk["Hops"] == 3]["Coverage_%"].values

plt.subplot(1, 2, 1)
plt.plot(uk_seeds, uk_cov_2hop, marker='o', linewidth=2, label='2-hop', color='#1f77b4')
plt.plot(uk_seeds, uk_cov_3hop, marker='s', linewidth=2, label='3-hop', color='#ff7f0e')
plt.xscale('log')
plt.xlabel('Number of Seed Sites')
plt.ylabel('Coverage (%)')
plt.title('UK (.co.uk): 2-hop vs 3-hop Coverage')
plt.grid(True, alpha=0.3)
plt.legend()

# -------------------------
# Figure 2: SE 2-hop vs 3-hop Coverage
# -------------------------
se_seeds = df_se[df_se["Hops"] == 2]["Seeds"].values
se_cov_2hop = df_se[df_se["Hops"] == 2]["Coverage_%"].values
se_cov_3hop = df_se[df_se["Hops"] == 3]["Coverage_%"].values

plt.subplot(1, 2, 2)
plt.plot(se_seeds, se_cov_2hop, marker='o', linewidth=2, label='2-hop', color='#1f77b4')
plt.plot(se_seeds, se_cov_3hop, marker='s', linewidth=2, label='3-hop', color='#ff7f0e')
plt.xscale('log')
plt.xlabel('Number of Seed Sites')
plt.ylabel('Coverage (%)')
plt.title('SE (.se): 2-hop vs 3-hop Coverage')
plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()
plt.savefig("../output/scenario_coverage_comparison.png", dpi=300)
print("✓ Saved: scenario_coverage_comparison.png")
plt.close()

# -------------------------
# Figure 3: TTFI Comparison
# -------------------------
plt.figure(figsize=(10, 5))

uk_ttfi = df_uk[df_uk["Hops"] == 2]["TTFI_s"].values
se_ttfi = df_se[df_se["Hops"] == 2]["TTFI_s"].values

plt.subplot(1, 2, 1)
plt.plot(uk_seeds, uk_ttfi, marker='o', linewidth=2, color='#2ca02c')
plt.xscale('log')
plt.xlabel('Number of Seed Sites')
plt.ylabel('TTFI (seconds)')
plt.title('UK (.co.uk): Time To First Index')
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)
plt.plot(se_seeds, se_ttfi, marker='o', linewidth=2, color='#2ca02c')
plt.xscale('log')
plt.xlabel('Number of Seed Sites')
plt.ylabel('TTFI (seconds)')
plt.title('SE (.se): Time To First Index')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../output/scenario_ttfi_comparison.png", dpi=300)
print("✓ Saved: scenario_ttfi_comparison.png")
plt.close()

# -------------------------
# Figure 4: Coverage Boost Bar Chart
# -------------------------
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
uk_boost = uk_cov_3hop - uk_cov_2hop
x = np.arange(len(uk_seeds))
width = 0.35

plt.bar(x - width/2, uk_cov_2hop, width, label='2-hop', color='#1f77b4', alpha=0.8)
plt.bar(x + width/2, uk_cov_3hop, width, label='3-hop', color='#ff7f0e', alpha=0.8)

plt.xlabel('Seed Configuration')
plt.ylabel('Coverage (%)')
plt.title('UK (.co.uk): Coverage by Hop Depth')
plt.xticks(x, [f'{s:,}' for s in uk_seeds], rotation=45)
plt.legend()
plt.grid(True, alpha=0.3, axis='y')

plt.subplot(1, 2, 2)
se_boost = se_cov_3hop - se_cov_2hop
x = np.arange(len(se_seeds))

plt.bar(x - width/2, se_cov_2hop, width, label='2-hop', color='#1f77b4', alpha=0.8)
plt.bar(x + width/2, se_cov_3hop, width, label='3-hop', color='#ff7f0e', alpha=0.8)

plt.xlabel('Seed Configuration')
plt.ylabel('Coverage (%)')
plt.title('SE (.se): Coverage by Hop Depth')
plt.xticks(x, [f'{s:,}' for s in se_seeds], rotation=45)
plt.legend()
plt.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig("../output/scenario_coverage_bars.png", dpi=300)
print("✓ Saved: scenario_coverage_bars.png")
plt.close()

# -------------------------
# Figure 5: Direct UK vs SE Comparison (3-hop)
# -------------------------
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
# Normalize seed counts for fair comparison (SE has 1/5.6 the domains)
plt.plot(uk_seeds, uk_cov_3hop, marker='o', linewidth=2, label='UK (.co.uk)', color='#d62728')
plt.plot(se_seeds, se_cov_3hop, marker='s', linewidth=2, label='SE (.se)', color='#9467bd')
plt.xscale('log')
plt.xlabel('Number of Seed Sites')
plt.ylabel('Coverage (%)')
plt.title('3-hop Coverage: UK vs SE')
plt.grid(True, alpha=0.3)
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(uk_seeds, uk_ttfi, marker='o', linewidth=2, label='UK (.co.uk)', color='#d62728')
plt.plot(se_seeds, se_ttfi, marker='s', linewidth=2, label='SE (.se)', color='#9467bd')
plt.xscale('log')
plt.xlabel('Number of Seed Sites')
plt.ylabel('TTFI (seconds)')
plt.title('TTFI: UK vs SE')
plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()
plt.savefig("../output/scenario_uk_vs_se.png", dpi=300)
print("✓ Saved: scenario_uk_vs_se.png")
plt.close()

print("\n✅ All visualizations created successfully!")
print("\nGenerated files:")
print("  - scenario_coverage_comparison.png")
print("  - scenario_ttfi_comparison.png")
print("  - scenario_coverage_bars.png")
print("  - scenario_uk_vs_se.png")
