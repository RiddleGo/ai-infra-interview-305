# 第 104 题：TensorRT-LLM的`in-flight batching`原理？

## 题目

TensorRT-LLM的`in-flight batching`原理？

---

## 完整讲解

### 一、In-Flight Batching 的含义

**In-flight batching**：与 **continuous batching** 同义——**当前在执行的请求** 组成一个「在飞」的 batch，每轮 decode 只对这些请求做一次前向；某请求生成完就**离开** batch，新请求可**加入**。Batch 成员随时间变化，不等到「整批完成」再换批，从而提高 GPU 利用率、降低尾延迟。

### 二、TensorRT-LLM 的实现要点

- **调度器**：每轮根据 **max_num_seqs**、**max_tokens**、显存与 block 池，决定本轮参与 decode 的请求集合；已 EOS 的请求释放 KV、退出，新请求分配 block、加入。
- **与 KV cache 管理结合**：TensorRT-LLM 也有类似 PagedAttention 的 block 或 chunk 管理，in-flight 的请求按需占 block，结束即还回；保证显存与调度一致。
- **性能**：通过「即出即入」避免 static batch 的等待，吞吐与 P99 延迟通常优于固定 batch；与 vLLM 的 continuous batching 思想一致，实现上可能用不同 kernel 与调度策略。

### 三、与 Static 的对比

Static：batch 固定到整批完成；in-flight/continuous：batch 每轮更新，完成即出、可进新请求。TensorRT-LLM 的 in-flight batching 是其在 LLM 服务上对标 vLLM 的核心能力之一。

---

## 面试要点

- In-flight batching = 每轮只算「当前未完成」的请求，完成即出、新请求即入；即 continuous batching。
- TensorRT-LLM 通过调度器 + KV/block 管理实现；与 PagedAttention 类思路一致。
- 相对 static：利用率高、尾延迟低；与 vLLM 思想一致、实现各异。

---

## 记忆要点

1. In-flight = continuous batching，batch 成员动态变化。
2. 调度器每轮选 in-flight 请求；结束即释放、新请求即加入。
3. 与 KV/block 管理结合，提高利用率与延迟。

[返回模块](./README.md) | [返回总览](../README.md)
