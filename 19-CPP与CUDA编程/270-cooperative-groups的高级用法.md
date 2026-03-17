# 第 270 题：`cooperative groups`的高级用法？`grid_group`？

## 题目

`cooperative groups`的高级用法？`grid_group`？

---

## 完整讲解

### 一、Cooperative Groups 简介

**Cooperative Groups**（CUDA 9+）把「线程组」抽象成对象（thread_block、warp、grid 等），提供 `sync()`、`size()`、`thread_rank()` 等，并支持**网格级同步**（grid_group），替代传统 `__syncthreads()` 仅限 block 内。

### 二、grid_group 用法

`grid_group grid = this_grid();` 需在 **kernel 启动时** 用 `cudaLaunchCooperativeKernel`（或 `cudaLaunchCooperativeKernelMultiDevice`）才能获得有效的 grid_group。之后可 `grid.sync()`：**整个 grid 所有 block 在该点同步**。用于跨 block 的全局 barrier、多阶段算法（如先全 grid 算完某阶段再进入下一阶段）等。

### 三、高级用法与注意

还可有 thread_block_tile（如 32 线程的 tile）、`coalesced_threads()` 等。grid_group 要求所有 block 都参与、且启动方式为 cooperative；否则未定义。适合多 block 协作的算法（如某些全局 reduce、迭代算法）。

---

## 面试要点

- Cooperative Groups：线程组抽象（block、warp、grid）；提供 sync、size、rank。
- grid_group：整个 grid 同步；需 cudaLaunchCooperativeKernel 启动才有效。
- grid.sync() 为全 grid barrier；用于跨 block 协作、多阶段算法。
- 要求 cooperative launch、所有 block 参与。

---

## 记忆要点

1. Cooperative Groups = 线程组抽象；grid_group = 全 grid。
2. grid_group 需 cudaLaunchCooperativeKernel；grid.sync() 全 grid 同步。
3. 用于跨 block 协作、多阶段算法；所有 block 必须参与。

[返回模块](./README.md) | [返回总览](../README.md)
