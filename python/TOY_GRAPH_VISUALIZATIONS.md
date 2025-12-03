# Toy Web Graph Coverage Visualizations

## 📊 **Visual Representation of Coverage Scenarios**

These toy graphs provide visual intuition for coverage percentages using 100-node Erdős-Rényi random graphs. While not representative of the actual .co.uk or .se link topology, they illustrate coverage concepts clearly.

---

## 🇬🇧 **UK (.co.uk) Scenarios**

### Scenario 1: Low Coverage
**Configuration:**
- **Seeds**: 1,000
- **Hops**: 2
- **Coverage**: 6.82% (~572,857 domains)
- **TTFI**: 8.32 seconds

**Visualization**: `toy_graph_uk_1k_seeds_2hop.png`

**What it shows**: With 1,000 seeds and 2 hops, only a small fraction of the UK domain space is reachable. The graph shows ~7 green nodes out of 100, representing limited penetration into the network.

**Interpretation**: This demonstrates the limitation of 2-hop crawling with modest seed counts. Most of the UK domain space remains undiscovered.

---

### Scenario 2: Moderate Coverage
**Configuration:**
- **Seeds**: 5,000
- **Hops**: 2
- **Coverage**: 34.10% (~2,864,285 domains)
- **TTFI**: 6.84 seconds

**Visualization**: `toy_graph_uk_5k_seeds_2hop.png`

**What it shows**: With 5x more seeds, coverage jumps to 34% - about 1 in 3 domains are reachable. The graph shows ~34 green nodes, indicating substantial but incomplete coverage.

**Interpretation**: Increasing seeds from 1k to 5k provides a 5x improvement in coverage (6.82% → 34.10%), demonstrating strong returns on seed investment at this scale.

**Key insight**: Going from 1k to 5k seeds increases coverage by **27 percentage points** but still leaves 66% of domains unreachable with 2 hops.

---

## 🇸🇪 **SE (.se) Scenarios**

### Scenario 3: Very Low Coverage
**Configuration:**
- **Seeds**: 100
- **Hops**: 2
- **Coverage**: 3.82% (~57,285 domains)
- **TTFI**: 8.85 seconds

**Visualization**: `toy_graph_se_100_seeds_2hop.png`

**What it shows**: With only 100 seeds and 2 hops, SE coverage is minimal at 3.82%. The graph shows ~4 green nodes out of 100, illustrating sparse coverage.

**Interpretation**: Despite SE being 5.6x smaller than UK, 100 seeds is insufficient for meaningful coverage with 2 hops. This demonstrates the need for either more seeds or deeper crawling (3-hop).

---

### Scenario 4: Moderate-High Coverage
**Configuration:**
- **Seeds**: 1,000
- **Hops**: 2
- **Coverage**: 38.19% (~572,857 domains)
- **TTFI**: 6.73 seconds

**Visualization**: `toy_graph_se_1k_seeds_2hop.png`

**What it shows**: With 1,000 seeds, SE achieves 38.19% coverage - comparable to UK's 5k seed scenario. The graph shows ~38 green nodes, indicating good penetration.

**Interpretation**: SE's smaller size means 1,000 seeds achieves similar coverage to UK's 5,000 seeds. However, 38% still leaves substantial domains unreachable without a third hop.

**Key insight**: 10x more seeds (100 → 1,000) yields a **10x improvement in coverage** (3.82% → 38.19%), showing linear scaling in this range.

---

## 📐 **Visual Comparison**

### Coverage Distribution Summary

| Scenario | Seeds | Coverage | Green Nodes (visual) | Reachable Domains |
|----------|-------|----------|---------------------|-------------------|
| UK Low | 1,000 | 6.82% | ~7 / 100 | ~573k / 8.4M |
| UK Moderate | 5,000 | 34.10% | ~34 / 100 | ~2.86M / 8.4M |
| SE Very Low | 100 | 3.82% | ~4 / 100 | ~57k / 1.5M |
| SE Moderate | 1,000 | 38.19% | ~38 / 100 | ~573k / 1.5M |

### Visual Patterns

**Sparse Coverage (<10%)**
- UK 1k seeds: 6.82% coverage
- SE 100 seeds: 3.82% coverage
- **Visual**: Scattered green nodes, mostly isolated, large gray areas

**Moderate Coverage (30-40%)**
- UK 5k seeds: 34.10% coverage
- SE 1k seeds: 38.19% coverage
- **Visual**: Roughly 1/3 nodes green, beginning to form clusters, still substantial gray areas

---

## 🎨 **Understanding the Visualizations**

### Graph Structure
- **Nodes**: 100 total (representing domain space)
- **Topology**: Erdős-Rényi random graph (p=0.05)
- **Layout**: Spring layout (force-directed)

### Color Coding
- **Green nodes (#2ecc71)**: Covered domains (reachable from seeds)
- **Gray nodes (#e0e0e0)**: Uncovered domains (not yet discovered)
- **Edges**: Light gray connections showing link structure

### What the Graphs Represent
- **Not actual topology**: These are toy graphs for illustration, not the real UK/SE link graph
- **Proportional coverage**: The fraction of green nodes matches the actual coverage percentage
- **Visual intuition**: Makes abstract percentages concrete and understandable

---

## 💡 **Key Insights from Visualizations**

### 1. The Coverage Gap
Even at 34-38% coverage, **2 out of 3 domains remain uncovered**. The visual makes this starkly clear - substantial gray areas persist even in the "moderate" scenarios.

**Solution**: Add a third hop to reach 100% coverage (as shown in scenario analysis).

### 2. Seed Efficiency Varies by TLD Size
- **UK**: 5,000 seeds → 34.10% coverage
- **SE**: 1,000 seeds → 38.19% coverage

SE achieves **similar coverage with 5x fewer seeds** due to smaller total domain count.

**Practical implication**: Smaller TLDs are more cost-effective to cover with seed-based crawling.

### 3. 2-hop Limitations
All four scenarios show **incomplete coverage with 2 hops**, ranging from 3.82% to 38.19%. None approach saturation.

**Recommendation**: 3-hop crawling is essential for comprehensive coverage (as demonstrated in scenario analysis where 3-hop achieves 70-100% coverage).

### 4. Linear Scaling in Low-to-Moderate Range
- SE: 100 → 1,000 seeds = 3.82% → 38.19% (10x seeds → 10x coverage)
- UK: 1,000 → 5,000 seeds = 6.82% → 34.10% (5x seeds → 5x coverage)

**Pattern**: Before saturation, coverage scales roughly linearly with seed count.

---

## 📊 **Comparison with 3-hop Results**

### UK: 2-hop vs 3-hop at 1,000 seeds
- **2-hop**: 6.82% coverage (7 green nodes)
- **3-hop**: 100% coverage (all green)
- **Improvement**: 14.7x coverage boost from one additional hop

**If we visualized this**: The 3-hop graph would be entirely green - complete coverage.

### SE: 2-hop vs 3-hop at 100 seeds
- **2-hop**: 3.82% coverage (4 green nodes)
- **3-hop**: 70.78% coverage (71 green nodes)
- **Improvement**: 18.5x coverage boost from one additional hop

**If we visualized this**: The 3-hop graph would be predominantly green with only ~30 gray nodes remaining.

---

## 🎯 **Use Cases for These Visualizations**

### 1. Research Paper Illustrations
- Include in supplementary materials
- Use to explain coverage concepts to non-technical reviewers
- Provide visual counterpoint to numerical tables

### 2. Presentations
- Clear visual for stakeholder presentations
- Demonstrates "before/after" scenarios effectively
- Makes abstract percentages tangible

### 3. Educational Content
- Teaching web graph coverage concepts
- Illustrating seed-based crawling strategies
- Explaining the value of additional hops

### 4. Decision Support
- Visualize impact of budget constraints (seed count)
- Show tradeoffs between 2-hop and 3-hop strategies
- Demonstrate coverage gaps that need addressing

---

## 📁 **File Locations**

All toy graphs are saved in the `output/` directory:

```
output/
├── toy_graph_uk_1k_seeds_2hop.png   # UK: 1k seeds, 6.82% coverage
├── toy_graph_uk_5k_seeds_2hop.png   # UK: 5k seeds, 34.10% coverage
├── toy_graph_se_100_seeds_2hop.png  # SE: 100 seeds, 3.82% coverage
└── toy_graph_se_1k_seeds_2hop.png   # SE: 1k seeds, 38.19% coverage
```

All images are 300 DPI, suitable for publication.

---

## 🔧 **Regenerating the Visualizations**

To recreate these toy graphs:

```bash
cd simulations
python3 generate_toy_graphs.py
```

To modify:
- **Coverage percentages**: Edit `coverage` parameter
- **Node count**: Change `num_nodes` (default: 100)
- **Graph topology**: Modify `nx.erdos_renyi_graph` parameters
- **Colors**: Update `node_colors` in the script
- **Layout**: Change `nx.spring_layout` to other layouts (e.g., `nx.circular_layout`)

---

## 🎓 **Technical Notes**

### Graph Generation
- **Algorithm**: Erdős-Rényi G(n,p) with n=100, p=0.05
- **Expected edges**: ~245 (from binomial distribution)
- **Degree distribution**: Approximately Poisson with λ=5

### Node Selection
- **Random sampling** proportional to coverage percentage
- **Deterministic** via fixed random seed for reproducibility
- **Independent** across different scenarios (different seeds)

### Visual Design
- **Color palette**: Material Design colors for clarity
- **Node size**: 120 points for visibility
- **Edge opacity**: 0.4 to avoid visual clutter
- **Layout algorithm**: Fruchterman-Reingold force-directed

---

## 📚 **Integration with Research**

### In Your Paper

**Figure caption example:**
```
Figure X: Toy web graph visualizations of 2-hop coverage scenarios.
Green nodes represent domains reachable from seed sites; gray nodes are 
uncovered. (a) UK with 1,000 seeds (6.82% coverage), (b) UK with 5,000 
seeds (34.10% coverage), (c) SE with 100 seeds (3.82% coverage), 
(d) SE with 1,000 seeds (38.19% coverage). Each graph contains 100 nodes 
with Erdős-Rényi topology (p=0.05) for illustration.
```

### In Presentations

**Slide structure:**
1. Show "Before" (UK 1k seeds, 6.82%)
2. Show "After" (UK 5k seeds, 34.10%)
3. Emphasize visual difference
4. Note: Still only 1/3 covered → need 3-hop

---

## ✅ **Summary**

Created **4 toy web graph visualizations** showing:

1. ✅ UK with 1,000 seeds (6.82% coverage)
2. ✅ UK with 5,000 seeds (34.10% coverage)  
3. ✅ SE with 100 seeds (3.82% coverage)
4. ✅ SE with 1,000 seeds (38.19% coverage)

**Key takeaway**: Even the best 2-hop scenario (38.19%) leaves most domains unreachable, visually demonstrating the necessity of 3-hop crawling for comprehensive coverage.

---

**Generated**: December 2025  
**Format**: PNG, 300 DPI  
**Status**: ✅ Complete and ready for use
