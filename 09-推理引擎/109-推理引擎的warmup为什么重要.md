# 第 109 题：推理引擎的`warmup`为什么重要？如何设计warmup策略？

## 题目

推理引擎的`warmup`为什么重要？如何设计warmup策略？

---

## 完整讲解

### 一、Warmup 为何重要

- **首次推理** 常包含：**CUDA 初始化、kernel JIT、显存分配、图优化/编译**（如 TensorRT、torch.compile）等，**第一次** 会明显偏慢；若用这次耗时做 SLA 或容量规划会**高估延迟、低估容量**。
- **Warmup**：在正式接流量前，用 **若干次假请求**（或小 batch）把上述开销「跑完」，使 **cache、显存、编译状态** 稳定，后续请求的延迟才代表真实水平；同时可 **预分配显存、触发 lazy 初始化**，避免首包慢。

### 二、如何设计 Warmup 策略

- **次数与 shape**：做 **多轮** warmup（如 10～100 次），覆盖 **典型 input shape**（如常见 batch、seq_len）；若用 dynamic shape，应对 min/opt/max 或几种典型 shape 各跑若干次，让 TensorRT/引擎针对这些 shape 完成优化与缓存。
- **内容**：可用 **空或随机输入**，只要走通完整前向；有时需 **真实 shape + 占位 token**，避免某些引擎对异常输入做特殊路径。
- **时机**：进程启动后、**接流量前** 必须完成；健康检查应在 warmup 之后，避免把「未 warmup」的实例标为 ready。若模型/配置变更，需重新 warmup。
- **监控**：记录 warmup 前后几次的延迟，确认稳定后再开放流量；或设 **warmup 完成** 的 readiness 条件（如 P99 低于某阈值）。

### 三、与编译/缓存的配合

TensorRT、torch.compile、ONNX 等 **首次 shape** 可能触发 build/compile；warmup 应覆盖这些 shape，使正式请求命中缓存。多模型/多实例时，每个模型与实例都需独立 warmup。

---

## 面试要点

- Warmup 消除首次推理的初始化/JIT/编译/显存分配等开销，使延迟稳定、容量评估准确。
- 策略：多轮、覆盖典型 shape（含 dynamic 的 min/opt/max）；进程启动后、接流量前完成；健康检查在 warmup 后。
- 与 TensorRT/compile 缓存配合，覆盖会触发编译的 shape。

---

## 记忆要点

1. 首次推理含初始化与编译，必须 warmup 再接流量。
2. 多轮 + 典型 shape；dynamic 要覆盖多种 shape。
3. 健康检查在 warmup 之后；模型/配置变更需重 warmup。

[返回模块](./README.md) | [返回总览](../README.md)
