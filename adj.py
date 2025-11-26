#!/usr/bin/env python3
import argparse
import random
from collections import defaultdict, Counter

def read_edges(path):
    edges = []
    max_node = -1
    with open(path, 'r') as f:
        for line in f:
            line=line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            u = int(parts[0]); v = int(parts[1])
            edges.append((u,v))
            if u>max_node: max_node=u
            if v>max_node: max_node=v
    return edges, max_node

def build_adj_for_nodes(edges, nodeset):
    adj = defaultdict(set)
    for u,v in edges:
        if u in nodeset and v in nodeset:
            adj[u].add(v)
            adj[v].add(u)
    return adj

def write_adjlist(adj, outpath):
    # adjacency list: node <tab> neighbor1,neighbor2,...
    with open(outpath, 'w') as f:
        for node in sorted(adj.keys()):
            nbrs = sorted(adj[node])
            f.write(f"{node}\t{','.join(map(str,nbrs))}\n")

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True, help='edge list file (u v per line)')
    p.add_argument('--method', choices=('range','random','topdeg'), default='range',
                   help='how to choose subgraph nodes')
    p.add_argument('--n', type=int, required=True, help='number of nodes (N)')
    p.add_argument('--out', required=True, help='output adjacency-list file')
    p.add_argument('--seed', type=int, default=42, help='random seed for sampling')
    args = p.parse_args()

    print("Reading edges...")
    edges, max_node = read_edges(args.input)
    print(f"Read {len(edges)} edges; max node id {max_node}")

    if args.method == 'range':
        nodeset = set(range(args.n))
        print(f"Selected nodes {0}..{args.n-1} (range)")
    elif args.method == 'random':
        random.seed(args.seed)
        # gather all node ids
        nodes = set()
        for u,v in edges:
            nodes.add(u); nodes.add(v)
        if args.n > len(nodes):
            raise SystemExit(f"Requested n={args.n} > number of distinct nodes={len(nodes)}")
        nodes_list = sorted(nodes)
        sampled = set(random.sample(nodes_list, args.n))
        nodeset = sampled
        print(f"Randomly sampled {len(nodeset)} nodes (seed={args.seed})")
    elif args.method == 'topdeg':
        deg = Counter()
        for u,v in edges:
            deg[u]+=1; deg[v]+=1
        top_nodes = [n for n,_ in deg.most_common(args.n)]
        nodeset = set(top_nodes)
        print(f"Selected top {len(nodeset)} nodes by degree")
    else:
        raise SystemExit("Unknown method")

    print("Building induced adjacency for selected nodes...")
    adj = build_adj_for_nodes(edges, nodeset)
    print(f"Adjacency has {len(adj)} nodes (nodes with at least one neighbor in subgraph).")

    print(f"Writing adjacency list to {args.out} ...")
    write_adjlist(adj, args.out)
    print("Done.")
    # show few sample lines
    print("Sample lines:")
    cnt=0
    with open(args.out,'r') as f:
        for _ in range(10):
            line = f.readline()
            if not line: break
            print(line.strip())

if __name__ == '__main__':
    main()

