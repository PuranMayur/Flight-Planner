# Optimized Flight Planner for Cost, Time, and Route Efficiency

**Tags:** Graph Algorithms, Dijkstra, BFS, Flight Scheduling, Path Optimization

---

## Overview

This project presents a graph-based **flight planning system** designed to optimize travel routes across different user-centric parameters: **cost**, **travel time**, and **number of layovers**. The system is powered by self-implemented graph algorithms, including:

- A modified **Dijkstra’s algorithm** for cost/time efficiency
- **Breadth-First Search (BFS)** for shortest-layover routing

The planner achieves optimal or near-optimal travel paths, scaling efficiently even as the size of flight data increases.

---

## Features

- **Multi-Criteria Route Optimization**: Supports route planning based on:
  - Minimum travel time
  - Lowest total cost
  - Fewest layovers
- **Custom Graph Representation**: Uses adjacency lists with edge attributes (cost, time, departure/arrival).
- **Modified Dijkstra's Algorithm**: Adapted to account for multiple constraints such as cost, arrival windows, and transfer time.
- **Efficient BFS**: Identifies minimal-hop connections between airports.
- **Scalable Design**: Handles large flight datasets with thousands of nodes and edges.

---

