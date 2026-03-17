# 第 67 题：`torch.distributed.pipeline.sync.Pipe`的使用限制？

## 题目

`torch.distributed.pipeline.sync.Pipe`的使用限制？

---

## 完整讲解

### 一、Pipe 的基本限制

`torch.distributed.pipeline.sync.Pipe` 将 `nn.Module` 按顺序切成若干 submodule（stage），每个 stage 可放到不同 device，用 **sync** 方式执行：同一 micro-batch 的 forward 在各 stage 间顺序执行，backward 亦然。限制包括：**只支持顺序的 module list**（不能任意 DAG）、**单进程多 device**（或配合 spawn 多进程时每进程多 device）、**无内置 TP/DP**，需用户自己与 DDP 等组合。

### 二、使用上的约束

- **拓扑**：stage 数 = device 数（或 1:1 映射）；device 需在同一个进程内可见（如多 GPU 单机）。
- **Chunk**：micro-batch 数（chunks）需 ≥ stage 数，否则 bubble 极大；且第一个 tensor 输入要在 batch 维可切。
- **No cross-stage 的 skip**：若模型有 skip connection 跨 stage，Pipe 默认不支持，需把整块放同一 stage 或改用自定义 schedule。
- **调试**：hang 或 OOM 时需结合 stage 划分与 chunk 数排查；与 DDP 一起用时注意进程与 backend 一致。

### 三、与 Megatron/DeepSpeed 的对比

PyTorch Pipe 是**同步、单进程**的轻量实现；Megatron、DeepSpeed 的 pipeline 支持多进程、1F1B、interleaved、与 TP/DP 结合，适合大模型。生产大模型多用 Megatron 或 DeepSpeed pipeline，Pipe 适合原型或小规模流水线验证。

---

## 面试要点

- Pipe 只支持顺序 stage、单进程多 device；chunks ≥ stage 数；无内置 TP/DP。
- 跨 stage 的 skip 不直接支持；与 DDP 组合需自己处理进程与 backend。
- 大模型生产多用 Megatron/DeepSpeed pipeline，Pipe 适合小规模或原型。

---

## 记忆要点

1. sync.Pipe = 顺序 stage、sync 执行；chunks ≥ stages。
2. 单进程多 device、无 TP/DP；跨 stage skip 不支持。
3. 生产用 Megatron/DeepSpeed，Pipe 做原型。

[返回模块](./README.md) | [返回总览](../README.md)
