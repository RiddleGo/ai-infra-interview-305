# 第 137 题：长文本请求的`preemption`策略？KV cache的swap out？

## 题目

长文本请求的`preemption`策略？KV cache的swap out？

---

## 完整讲解

### 一、长文本与 Preemption 需求

长文本请求占用的 **KV cache** 大、耗时长，若一直占着显存不释放，会阻塞新请求或导致 OOM。**Preemption**（抢占）：在资源紧张或高优请求到达时，**暂停或挂起**当前长请求，释放其 KV cache 与算力，先服务高优或短请求，之后再恢复被挂起请求。难点在于：生成是状态化的（已生成 token、KV 状态），挂起需保存状态、恢复需还原，且要保证正确性与延迟体验。

### 二、KV Cache Swap Out

**KV cache swap out**：把当前不需要参与计算的 KV 块从 GPU 显存**换出**到 CPU 内存（或 SSD），腾出显存给其他请求或同一请求的后续计算；需要时再**换入**回显存。这样长上下文不必一次性占满显存，可按「当前窗口」+ 换出历史实现长序列。实现要点：按 block 或 chunk 管理 KV，LRU 或按 attention 范围决定谁换出；换入时可能造成一次 stall，需与调度配合（如 preemption 时整请求 swap out，恢复时 swap in）。

### 三、Preemption 策略

策略可组合：**时间片**到则挂起长请求、swap out KV，让出 GPU；**高优到达**时挂起低优长请求；**显存水位**超阈值时对最不「划算」的请求（如已生成很多、剩余少）做 swap out 或终止。恢复时按 checkpoint 或 swap 回来的 KV 继续生成。PagedAttention、vLLM 等已支持类似逻辑，面试可结合具体系统说。

---

## 面试要点

- 长文本抢占：挂起长请求、释放 KV 与算力，先服务高优/短请求，再恢复；需保存与还原生成状态。
- KV swap out：把 KV 块从 GPU 换到 CPU/SSD，腾显存；需要时换入；按 block 管理、LRU 或按范围决策。
- 策略：时间片、高优到达、显存水位触发；与 PagedAttention/vLLM 等实现结合。

---

## 记忆要点

1. Preemption = 挂起长请求、释放资源，再恢复；状态需保存与还原。
2. KV swap out = 显存→CPU/SSD，按块管理；换入换出与调度配合。
3. 触发：时间片、优先级、显存阈值；可结合 PagedAttention 等。

[返回模块](./README.md) | [返回总览](../README.md)
