# 第 289 题：图算法的`shortest path`？`Dijkstra`、`Bellman-Ford`？

## 题目

图算法的`shortest path`？`Dijkstra`、`Bellman-Ford`？

---

## 完整讲解

### 一、最短路径问题

在带权有向/无向图中求单源或多源最短路径。**单源**：从一个点 s 到其余各点；常用 **Dijkstra**（非负权）、**Bellman-Ford**（可有负权、检负环）。**多源**：Floyd-Warshall 等。

### 二、Dijkstra

**贪心**：维护「已确定最短距离」的集合，每次取当前**距离最小的未确定点** u，松弛其出边，将 u 标为已确定。要求**边权非负**。用优先队列（小根堆）存 (dist, v)，复杂度 O((V+E) log V)。每个点最多入队出队一次，出队时即得最短路。

### 三、Bellman-Ford

**松弛**：对每条边 (u,v,w) 做 relax：若 dist[u]+w < dist[v] 则更新。重复 **V-1 轮**（或直到无更新），即可得到单源最短路；若第 V 轮仍能更新则存在**负权环**。复杂度 O(VE)。适合有负权、需判负环的场景；可做分布式（每轮本地松弛）。

---

## 面试要点

- 单源最短路：Dijkstra（非负权、贪心+优先队列）、Bellman-Ford（可负权、V-1 轮松弛）。
- Dijkstra：每次取 dist 最小未确定点松弛出边；O((V+E)log V)。
- Bellman-Ford：重复松弛所有边 V-1 轮；能检负环（第 V 轮仍更新）。
- 负权用 Bellman-Ford；非负权用 Dijkstra 更高效。

---

## 记忆要点

1. Dijkstra = 非负权、贪心取最小 dist、松弛；Bellman-Ford = 可负权、多轮松弛。
2. Dijkstra 用堆 O((V+E)log V)；Bellman-Ford O(VE)、可判负环。
3. 负环：Bellman-Ford 第 V 轮仍能更新则存在。

[返回模块](./README.md) | [返回总览](../README.md)
