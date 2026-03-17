# 第 290 题：并查集（Union-Find）的实现？`path compression`？

## 题目

并查集（Union-Find）的实现？`path compression`？

---

## 完整讲解

### 一、并查集用途

维护** disjoint sets**（无交集合），支持 **Union**（合并两集合）与 **Find**（查某元素所属集合代表元），用于判连通、等价类、最小生成树（Kruskal）等。目标：Union 与 Find 尽量快，**均摊**近 O(1)。

### 二、基本实现

用**父指针数组** parent[]：parent[i] 为 i 的父节点，根节点 parent[i]=i 或 -1。**Find(x)**：沿 parent 一路向上直到根，返回根。**Union(x,y)**：Find 得到 x、y 的根 rx、ry，将 rx 的 parent 设为 ry（或按秩挂）。朴素实现 Find/Union 最坏 O(n)；**路径压缩**与**按秩合并**可均摊到近 O(1)。

### 三、Path compression（路径压缩）

**Find** 时，把从 x 到根路径上所有节点的 parent 直接改为根。这样下次 Find 这些节点为 O(1)。实现：递归 Find 中在返回前写 `parent[x]=Find(parent[x])`；或迭代两次，第一次找根、第二次把路径全部挂到根。与**按秩合并**（小树挂到大树根下）一起，均摊复杂度 O(α(n))，α 为反阿克曼函数，实际可视为常数。

---

## 面试要点

- 并查集：维护不相交集合；Union 合并、Find 查代表元。
- 实现：parent 数组；Find 沿 parent 找根；Union 把两集合的根挂一起。
- 路径压缩：Find 时把路径上节点直接连到根，下次 Find 更快。
- 按秩合并：小树挂大树下；与路径压缩一起均摊近 O(1)。

---

## 记忆要点

1. parent 数组；Find 找根、Union 并根。
2. 路径压缩 = Find 时把路径挂到根。
3. 按秩合并 + 路径压缩 → 均摊 O(α(n))。

[返回模块](./README.md) | [返回总览](../README.md)
