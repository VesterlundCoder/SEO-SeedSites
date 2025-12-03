# Web Graph Simulation - Quick Start

## 🚀 Run Your First Simulation

```bash
cd simulations
python3 webgraph_simulation.py
```

## 📊 What You'll See

### 1. Console Output
```
Total sites (N):        8,400,000
Avg links per site (D): 25.00
Seed sites (n):         10,000
Hops:                   2
Estimated coverage:     68.20% (~5,728,571 sites reachable)
Estimated TTFI:         6.20 seconds
```

### 2. Three Interactive Plots

1. **Toy Graph Visualization**
   - 100-node network
   - Green = covered by seeds
   - Gray = uncovered
   - Close window to continue

2. **Coverage vs Seeds**
   - Shows coverage % increasing with more seeds
   - Close window to continue

3. **TTFI vs Seeds**
   - Shows discovery time decreasing with more seeds
   - Close window to finish

## ⚙️ Quick Parameter Changes

### Switch from UK to Sweden

Open `webgraph_simulation.py` and change:

```python
# FROM:
TOTAL_NODES = 8_400_000   # UK

# TO:
TOTAL_NODES = 1_500_000   # SE
NUM_SEEDS = 1_000         # Adjust seeds proportionally
```

### Switch from 2-hop to 3-hop

```python
# FROM:
HOPS = 2

# TO:
HOPS = 3
```

### Increase Seed Count

```python
# FROM:
NUM_SEEDS = 10_000

# TO:
NUM_SEEDS = 50_000
```

## 🎯 Common Scenarios

### Test Coverage Saturation

```python
TOTAL_NODES = 8_400_000
AVG_EDGES = 25
NUM_SEEDS = 100_000  # Large seed count
HOPS = 3             # More hops
```

**Expected**: Very high coverage (>95%)

### Test Minimal Seeds

```python
TOTAL_NODES = 8_400_000
NUM_SEEDS = 500      # Very few seeds
HOPS = 2
```

**Expected**: Low coverage (<10%), high TTFI (>10s)

### Compare 2-hop vs 3-hop

**Run 1:**
```python
HOPS = 2
# Run and note coverage
```

**Run 2:**
```python
HOPS = 3
# Run and compare - should see ~3-5x coverage increase
```

## 💡 Tips

1. **Close each plot window** to proceed to the next
2. **Check console first** for quick numbers before plots appear
3. **Modify one parameter at a time** to understand effects
4. **Save interesting configs** as comments in the file

## 📈 Understanding Results

### Coverage %
- **<20%**: Very sparse coverage, need more seeds
- **20-50%**: Moderate coverage
- **50-80%**: Good coverage
- **>80%**: Excellent coverage, approaching saturation

### TTFI (seconds)
- **>10s**: Long discovery time
- **5-10s**: Moderate discovery time
- **<5s**: Fast discovery

### Relationship
```
More seeds → Higher coverage + Lower TTFI
More hops → Higher coverage (same TTFI trend)
```

## 🔧 Troubleshooting

**Plots don't appear?**
- Make sure you're not in a headless environment
- Or modify to save plots instead (see main README)

**Want to save plots?**
Add before `plt.show()` in each function:
```python
plt.savefig("my_plot.png", dpi=300)
```

**Values seem wrong?**
- Check that AVG_EDGES matches your assumptions
- Verify DEDUP_R and DEDUP_S are in [0, 1]
- Ensure NUM_SEEDS > 0

## 🎓 Next Steps

1. ✅ Run default simulation (UK, 2-hop, 10k seeds)
2. ✅ Try SE scenario (smaller graph)
3. ✅ Compare 2-hop vs 3-hop
4. ✅ Test different seed counts
5. ✅ Check main README for advanced features
6. ✅ Compare with analytical model in `../generate_tables_and_figures.py`

---

**Ready to simulate? Run:** `python3 webgraph_simulation.py`
