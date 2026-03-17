# 第 102 题：vLLM的`continuous batching`如何实现？和`static batching`的吞吐对比？

## 题目

vLLM的`continuous batching`如何实现？和`static batching`的吞吐对比？

---

## 完整讲解

### 一、Static Batching 的问题

**Static batching**：凑满一个 batch（或超时）后一起跑一次 decode，本 batch 全部完成再接下一批。**问题**：序列长短不一，短序列先结束却要等长序列，**GPU 空转**；batch 内 padding 多则算力浪费，吞吐与延迟都不理想。

### 二、Continuous Batching 的做法

**Continuous batching**（vLLM 等）：**不固定 batch 边界**，每轮 decode 时只对「当前步仍需生成」的请求做一次前向；某请求生成完 EOS 就**立即移出**，新请求可**立即加入**。即 batch 在时间维上「流动」：每轮参与的是「in-flight」的请求子集，完成即退出、新请求即进入。这样 **GPU 始终有活干**，短序列不拖长序列，吞吐高、尾延迟低。

### 三、实现要点与吞吐对比

- **调度**：每轮选「未完成」的请求组成当前 batch（受 max_batch、显存约束）；与 PagedAttention 结合，按 block 分配与回收。
- **吞吐**：在相同 QPS 与延迟约束下，continuous batching 通常比 static 高 **数倍**（尤其长短混合、高方差场景）；static 的「等最慢」导致利用率低，continuous 的「即出即进」拉高利用率。vLLM 的 benchmark 常见 2～10x 提升（视负载而定）。

---

## 面试要点

- Static：凑 batch、等整批完成再下一批；短等长、利用率低。
- Continuous：每轮只算「未完成」请求，完成即出、新请求即入；batch 流动，利用率高。
- 吞吐上 continuous 常比 static 高数倍，尤其长短混合；与 PagedAttention 配合实现。

---

## 记忆要点

1. Static = 整批进整批出；continuous = 每步只算 in-flight，出即入。
2. Continuous 避免「短等长」，GPU 利用率高。
3. vLLM 用 continuous + PagedAttention，吞吐显著优于 static。

[返回模块](./README.md) | [返回总览](../README.md)
