# reducer.py (corrected)
#!/usr/bin/env python3
import sys

max_clique_size = 0
max_clique_nodes = []   # FIX: initialize as empty list

for line in sys.stdin:
    line = line.strip()
    try:
        size_str, nodes_str = line.split('\t', 1)
        size = int(size_str)
    except ValueError:
        continue
    if size > max_clique_size:
        max_clique_size = size
        max_clique_nodes = [nodes_str]
    elif size == max_clique_size:
        max_clique_nodes.append(nodes_str)

# Output the largest cliques
if max_clique_size > 0:
    for clique in max_clique_nodes:
        print(f"{max_clique_size}\t{clique}")

