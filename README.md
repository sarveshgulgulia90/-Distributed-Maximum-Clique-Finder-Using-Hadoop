# Hadoop-Based Maximum Clique Finder on Facebook Social Network

A distributed **Maximum Clique Detection System** built using **Hadoop MapReduce** and a **parallelized Bron–Kerbosch algorithm**. The system processes social-network graphs from the **SNAP Facebook Social Circles dataset**, constructs adjacency lists, and extracts **maximum cliques efficiently on Ubuntu** using big-data computing principles.

---

## 🚀 Project Overview

This project focuses on solving the **Maximum Clique Problem** for large social-network graphs using a **distributed computing approach**. Since maximum clique detection is computationally expensive (NP-Complete), the project leverages **Hadoop MapReduce** to parallelize the workload and scale to large datasets.

### ✅ Key Features
- Works on **real-world social-network data**
- Hadoop-based **distributed processing**
- **Adjacency list generation**
- **MapReduce-optimized Bron–Kerbosch Algorithm**
- Supports **induced subgraph extraction** (e.g., 1,000-node subgraph)
- Tested on **Ubuntu with Hadoop**

---

## 📊 Dataset Information

We use the **SNAP Facebook Social Circles dataset**:

- **Download link:**  
  https://snap.stanford.edu/data/facebook_combined.txt.gz
- **Nodes:** 4,039  
- **Edges:** 88,234  
Each line represents a friendship between two users.

---

## 🧠 Algorithm Used

### Bron–Kerbosch Algorithm (Parallel Version)

The Bron–Kerbosch algorithm is a recursive backtracking algorithm used to find **all maximal cliques** in a graph. In this project:

- The algorithm is **optimized for MapReduce**
- Graph is **partitioned across mappers**
- **Reducers compute cliques in parallel**
- Final stage selects the **maximum clique**

This approach enables scalable clique detection for large graphs.

## 🏗️ System Architecture

facebook_combined.txt.gz  ──┐
                            │  Download & decompress
                            ▼
facebook_combined.txt       ──┐
                              │  Preprocessing (optional subgraph induction / sampling)
                              ▼
adjacency_list.txt  ─── Hadoop Input (e.g. HDFS) ─┐
                                                   │  MapReduce Job #1: Partition / distribution / subgraph extraction  
                                                   ▼
                                  MapReduce Job #2: Parallel Bron–Kerbosch-based clique enumeration  
                                                   ▼
                                  Collect & aggregate maximal / maximum cliques

- **Format:** Edge list (undirected)
  Download the dataset
  wget https://snap.stanford.edu/data/facebook_combined.txt.gz
gzip -d facebook_combined.txt.gz

How to Run the Project
Step 1: Extract Subgraph (1000 Nodes)
python3 subgraph_extractor.py facebook_combined.txt 1000 > subgraph.txt

Step 2: Generate Adjacency List
python3 adjacency_generator.py subgraph.txt > adjacency_list.txt

Step 3: Upload to HDFS
hdfs dfs -put adjacency_list.txt /input/

Step 4: Run Hadoop Job
hadoop jar MaxClique.jar Driver /input /output

Step 5: View Results
hdfs dfs -cat /output/part-r-00000


