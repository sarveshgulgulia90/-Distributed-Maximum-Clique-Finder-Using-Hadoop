# mapper.py (corrected)
#!/usr/bin/env python3
import sys
import collections

# Load graph adjacency list from distributed cache file (adjfull.txt)
graph = collections.defaultdict(set)
try:
    with open("adjfull.txt", 'r') as f:
        for line in f:
            line = line.strip()
            if not line: 
                continue
            parts = line.split('\t')
            if len(parts) != 2:
                continue
            node = parts[0]                 # FIX: use parts[0], not the whole list
            neighbors_str = parts[1]
            neighbors = set(neighbors_str.split(',')) if neighbors_str else set()
            graph[node] = neighbors
except IOError:
    sys.stderr.write("Error: Could not open graph file adjfull.txt\n")
    sys.exit(1)

def bron_kerbosch_pivot(R, P, X):
    # Recursive Bron–Kerbosch with pivoting to list maximal cliques
    if not P and not X:
        clique = sorted(R, key=int)
        print(f"{len(R)}\t{','.join(clique)}")
        return
    if not P:
        return
    # Choose pivot u from P ∪ X maximizing connectivity in P
    pivot_candidates = P.union(X)
    try:
        u = max(pivot_candidates, key=lambda v: len(P.intersection(graph.get(v, set()))))
        P_without_Nu = P - graph.get(u, set())
    except (ValueError, KeyError):
        # If pivot selection fails (e.g., empty), don't exclude any
        P_without_Nu = set(P)
    for v in list(P_without_Nu):
        Nv = graph.get(v, set())
        bron_kerbosch_pivot(R.union({v}), P.intersection(Nv), X.intersection(Nv))
        P.remove(v)
        X.add(v)

# For each input vertex, start BK algorithm
for line in sys.stdin:
    start_node = line.strip()
    if start_node in graph:
        R = {start_node}
        P = set(graph[start_node])
        X = set()
        bron_kerbosch_pivot(R, P, X)

