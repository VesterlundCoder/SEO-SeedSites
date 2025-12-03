# Web Graph Simulations

Interactive toy simulations for seed-site coverage and TTFI analysis.

## Overview

This folder contains simulation tools that complement the analytical models in the main research project. While the main `generate_tables_and_figures.py` uses mathematical formulas, these simulations provide:

- **Visual graph representations** of coverage
- **Interactive parameter tuning** 
- **Toy graph demonstrations** (100-node Erdős-Rényi graphs)
- **Exploratory analysis** before running full models

---

## Files

### `webgraph_simulation.py`

Interactive simulator for seed-site coverage and Time To First Index (TTFI) on a simplified web-graph model.

**Key Features:**
- Estimates coverage % from seed sites using 2-hop or 3-hop models
- Calculates TTFI as a function of seed count
- Draws toy graph visualizations (covered vs uncovered nodes)
- Generates plots: coverage vs seeds, TTFI vs seeds

---

## Quick Start

### Run the Simulation

```bash
cd simulations
python3 webgraph_simulation.py
```

**Output:**
1. Console statistics (coverage %, TTFI, etc.)
2. Interactive toy graph visualization (100 nodes)
3. Coverage vs seeds plot
4. TTFI vs seeds plot

### Example Output

```
Total sites (N):        8,400,000
Avg links per site (D): 25.00
Seed sites (n):         10,000
Hops:                    2
Estimated coverage:     80.34% (~6,748,560 sites reachable)
Estimated TTFI:         8.31 seconds
```

---

## Configuration

Edit the top of `webgraph_simulation.py` to adjust parameters:

### Country Selection

```python
# UK (.co.uk)
TOTAL_NODES = 8_400_000

# SE (.se) - uncomment to switch
# TOTAL_NODES = 1_500_000
```

### Graph Parameters

```python
AVG_EDGES = 25          # Average outbound links per site (D)
NUM_SEEDS = 10_000      # Number of seed sites
```

### Model Parameters

```python
HOPS = 2                # 2 or 3 hop model
DEDUP_R = 0.6           # Second-hop deduplication factor
DEDUP_S = 0.45          # Third-hop deduplication factor (if HOPS=3)
OVERLAP_THETA = 0.3     # Cross-seed overlap
```

### TTFI Parameters

```python
BASE_HOP_LATENCY = 3.0  # Seconds per hop
```

---

## Understanding the Models

### Coverage Model

**2-hop formula:**
```
T2 = 1 + D + r·D²
Coverage = min(1, (num_seeds × T2) / (N × (1 - θ)))
```

**3-hop formula:**
```
T3 = 1 + D + r·D² + s·D³
Coverage = min(1, (num_seeds × T3) / (N × (1 - θ)))
```

Where:
- `D` = average out-degree (links per site)
- `r` = second-hop deduplication factor
- `s` = third-hop deduplication factor
- `θ` = cross-seed overlap
- `N` = total nodes in graph

### TTFI Model

```
E[distance] = log_{D+1}(N / num_seeds + 1)
TTFI = base_hop_latency × E[distance]
```

**Intuition:** More seeds → shorter average distance → lower TTFI

---

## Example Usage Scenarios

### Scenario 1: UK vs SE Comparison

```python
# Run UK simulation
TOTAL_NODES = 8_400_000
NUM_SEEDS = 10_000
# Execute script

# Then switch to SE
TOTAL_NODES = 1_500_000
NUM_SEEDS = 1_000
# Execute script
```

### Scenario 2: 2-hop vs 3-hop Comparison

```python
# First run: 2-hop
HOPS = 2
# Execute and note coverage

# Second run: 3-hop
HOPS = 3
# Execute and compare
```

### Scenario 3: Seed Count Sensitivity

```python
# Test different seed counts
for NUM_SEEDS in [500, 1_000, 5_000, 10_000, 50_000]:
    # Run simulation
    # Observe coverage and TTFI changes
```

---

## Visualizations Explained

### 1. Toy Graph Coverage

- **Green nodes**: Covered by seeds (reachable within k hops)
- **Gray nodes**: Uncovered (not yet discovered)
- **Graph**: 100-node Erdős-Rényi random graph (illustrative only)

**Note**: This is NOT your actual .co.uk/SE graph—it's a small visual representation to show coverage concepts.

### 2. Coverage vs Seeds Plot

Shows how coverage % increases with more seed sites. 

**Expected pattern:**
- Logarithmic growth
- Diminishing returns at high seed counts
- Steeper curve for 3-hop vs 2-hop

### 3. TTFI vs Seeds Plot

Shows how Time To First Index decreases with more seeds.

**Expected pattern:**
- Logarithmic decay
- More seeds → shorter discovery times
- Asymptotic floor (can't go below ~3 seconds with current params)

---

## Comparison with Main Research

| Feature | Main Model | Simulation |
|---------|-----------|------------|
| **Purpose** | Publication-quality tables/figures | Interactive exploration |
| **Scale** | Exact formulas, millions of nodes | Toy graphs, 100 nodes visualized |
| **Output** | CSV tables, 300 DPI PNGs | Interactive plots, console stats |
| **Use case** | Research paper results | Parameter tuning, intuition |
| **Speed** | Fast (mathematical) | Fast (mathematical + small graphs) |

---

## Advanced Customization

### Modify Seed Range for Plots

```python
# In plot_coverage_vs_seeds() and plot_ttfi_vs_seeds()
seed_range = np.linspace(500, 100_000, 50)  # Default

# Change to:
seed_range = np.linspace(100, 50_000, 100)  # More granular
# or
seed_range = np.logspace(2, 5, 50)  # Logarithmic spacing
```

### Change Graph Topology

```python
# In draw_mock_coverage()
G = nx.erdos_renyi_graph(num_nodes, 0.05, seed=42)  # Default

# Try:
G = nx.barabasi_albert_graph(num_nodes, 3, seed=42)  # Scale-free
# or
G = nx.watts_strogatz_graph(num_nodes, 6, 0.3, seed=42)  # Small-world
```

### Save Plots Instead of Displaying

```python
# Add before plt.show() in each plot function:
plt.savefig("coverage_vs_seeds.png", dpi=300)
plt.close()  # Replace plt.show()
```

---

## Troubleshooting

### Issue: Plots don't appear
**Cause**: Running in non-interactive environment  
**Solution**: Add `plt.savefig()` calls instead of `plt.show()`

### Issue: Coverage exceeds 100%
**Cause**: Parameters too aggressive (high D, low dedup factors)  
**Solution**: The model caps at 100% via `min(1.0, coverage)`

### Issue: TTFI is infinity
**Cause**: `NUM_SEEDS = 0`  
**Solution**: Ensure `NUM_SEEDS > 0`

---

## Dependencies

```bash
pip install numpy matplotlib networkx
```

Or use the project-wide requirements:
```bash
cd ..
pip install -r requirements.txt
```

---

## Example Workflow

1. **Set baseline parameters** (UK, 2-hop, 10k seeds)
2. **Run simulation** → Note coverage and TTFI
3. **Increase to 3 hops** → Observe coverage jump
4. **Double seeds** (10k → 20k) → See TTFI reduction
5. **Switch to SE** (smaller graph) → Compare results
6. **Generate plots** → Include in paper/presentation

---

## Tips for Research Use

1. **Start with defaults** to build intuition
2. **Vary one parameter at a time** to isolate effects
3. **Compare with main model** (generate_tables_and_figures.py) for consistency
4. **Use toy graphs** to explain concepts to non-technical audiences
5. **Save plots** for supplementary materials in paper

---

## Extending the Simulation

### Add Real Network Data

Replace random graph generation with actual .co.uk/.se link data:

```python
# Instead of:
G = nx.erdos_renyi_graph(num_nodes, 0.05)

# Use:
G = nx.read_edgelist("real_links.txt")
```

### Multi-country Comparison

Loop over multiple TLDs:

```python
configs = [
    ("UK", 8_400_000, 10_000),
    ("SE", 1_500_000, 1_000),
    ("DE", 16_000_000, 20_000),
]

for name, nodes, seeds in configs:
    coverage, ttfi = run_simulation(nodes, seeds)
    print(f"{name}: {coverage:.1%} coverage, {ttfi:.2f}s TTFI")
```

### Sensitivity Analysis

Test parameter ranges:

```python
for r in [0.4, 0.5, 0.6, 0.7]:
    for s in [0.3, 0.4, 0.5]:
        coverage = estimate_coverage(..., r=r, s=s)
        # Record results
```

---

## License

Part of the Domain Coverage Research project.  
For academic and research purposes.

---

**Created**: December 2025  
**Compatible with**: Python 3.8+  
**Last updated**: December 2025
