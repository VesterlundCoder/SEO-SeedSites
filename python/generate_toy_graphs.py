"""
generate_toy_graphs.py

Generate toy web graph visualizations for specific coverage scenarios.
"""

import random
import networkx as nx
import matplotlib.pyplot as plt

def draw_toy_coverage_graph(coverage: float, 
                            title: str,
                            filename: str,
                            num_nodes: int = 100,
                            seed: int = 42):
    """
    Draw a toy graph (100 nodes, Erdos-Renyi) and color
    a fraction of nodes as "covered" vs "uncovered" based on coverage.
    
    Args:
        coverage: Coverage fraction (0.0 to 1.0)
        title: Title for the plot
        filename: Output filename
        num_nodes: Number of nodes in toy graph
        seed: Random seed for reproducibility
    """
    # Create random graph
    G = nx.erdos_renyi_graph(num_nodes, 0.05, seed=seed)
    
    # Select covered nodes proportional to coverage
    num_covered = int(round(coverage * num_nodes))
    random.seed(seed)
    covered_nodes = set(random.sample(list(G.nodes()), num_covered))
    
    # Color nodes
    node_colors = [
        "#2ecc71" if node in covered_nodes else "#e0e0e0"  # Green for covered, light gray for uncovered
        for node in G.nodes()
    ]
    
    # Create figure
    plt.figure(figsize=(8, 8))
    pos = nx.spring_layout(G, seed=seed, k=0.5, iterations=50)
    
    # Draw network
    nx.draw_networkx_nodes(
        G,
        pos=pos,
        node_color=node_colors,
        node_size=120,
        edgecolors='#34495e',
        linewidths=1.5
    )
    
    nx.draw_networkx_edges(
        G,
        pos=pos,
        edge_color='#95a5a6',
        width=0.5,
        alpha=0.4
    )
    
    # Add title with coverage info
    plt.title(title, fontsize=14, fontweight='bold', pad=20)
    
    # Add coverage legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#2ecc71', edgecolor='#34495e', label=f'Covered ({num_covered} nodes)'),
        Patch(facecolor='#e0e0e0', edgecolor='#34495e', label=f'Uncovered ({num_nodes - num_covered} nodes)')
    ]
    plt.legend(handles=legend_elements, loc='upper right', fontsize=10)
    
    plt.axis('off')
    plt.tight_layout()
    
    # Save figure
    plt.savefig(f"../output/{filename}", dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {filename}")
    plt.close()


if __name__ == "__main__":
    print("=" * 80)
    print("GENERATING TOY WEB GRAPH COVERAGE VISUALIZATIONS")
    print("=" * 80)
    print()
    
    # UK Scenarios
    print("🇬🇧 UK (.co.uk) Scenarios")
    print("-" * 80)
    
    # UK: 1,000 seeds, 2-hop, 6.82% coverage
    draw_toy_coverage_graph(
        coverage=0.0682,
        title="UK (.co.uk): 1,000 seeds, 2-hop\n6.82% Coverage (~572k domains)",
        filename="toy_graph_uk_1k_seeds_2hop.png",
        seed=42
    )
    
    # UK: 5,000 seeds, 2-hop, 34.10% coverage
    draw_toy_coverage_graph(
        coverage=0.3410,
        title="UK (.co.uk): 5,000 seeds, 2-hop\n34.10% Coverage (~2.86M domains)",
        filename="toy_graph_uk_5k_seeds_2hop.png",
        seed=43
    )
    
    print()
    print("🇸🇪 SE (.se) Scenarios")
    print("-" * 80)
    
    # SE: 100 seeds, 2-hop, 3.82% coverage
    draw_toy_coverage_graph(
        coverage=0.0382,
        title="SE (.se): 100 seeds, 2-hop\n3.82% Coverage (~57k domains)",
        filename="toy_graph_se_100_seeds_2hop.png",
        seed=44
    )
    
    # SE: 1,000 seeds, 2-hop, 38.19% coverage
    draw_toy_coverage_graph(
        coverage=0.3819,
        title="SE (.se): 1,000 seeds, 2-hop\n38.19% Coverage (~573k domains)",
        filename="toy_graph_se_1k_seeds_2hop.png",
        seed=45
    )
    
    print()
    print("=" * 80)
    print("✅ ALL TOY GRAPHS GENERATED SUCCESSFULLY")
    print("=" * 80)
    print()
    print("Generated files in output/:")
    print("  - toy_graph_uk_1k_seeds_2hop.png")
    print("  - toy_graph_uk_5k_seeds_2hop.png")
    print("  - toy_graph_se_100_seeds_2hop.png")
    print("  - toy_graph_se_1k_seeds_2hop.png")
    print()
