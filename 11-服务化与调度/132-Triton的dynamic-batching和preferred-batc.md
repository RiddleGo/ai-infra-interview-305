# 第 132 题：Triton的`dynamic batching`和`preferred batch size`配置？

## 题目

Triton的`dynamic batching`和`preferred batch size`配置？

---

## 完整讲解

### 一、Dynamic Batching

**Dynamic batching**：服务端在**有限时间窗口**内把多个到达的请求攒成一批，再一起送进模型推理，从而提高 GPU 利用率与吞吐。请求不会无限等待，通常有 **max_queue_delay_microseconds**：从第一个请求进队到凑批或超时即执行。这样在 QPS 高时自动形成较大 batch，QPS 低时小 batch 或单条，延迟可控。

### 二、Preferred Batch Size

**Preferred batch size**：提示 Triton **优先凑成**的 batch 大小列表（如 [1, 2, 4, 8]）。当队列中请求数达到某一 preferred size 时立即执行该 batch，不必等到 max_queue_delay；若一直凑不齐则到时间后按当前队列执行。作用：在延迟与吞吐间折中——preferred 越大越利于吞吐，但等待时间可能变长；通常设成模型或 kernel 较优的 batch（如 2、4、8），避免总是 1 或总是很大 batch。

### 三、配置要点

在 model 的 `dynamic_batching` 中配置 `max_queue_delay_microseconds`、`preferred_batch_size`、可选 `preserve_ordering` 等。LLM 生成场景下有时用 continuous batching（每步可不同 batch）而非单纯 dynamic batching，需看后端与版本支持。

---

## 面试要点

- Dynamic batching：在时间窗口内攒多个请求成一批推理，提高吞吐；max_queue_delay 控制最大等待时间。
- Preferred batch size：优先凑成的 batch 列表，达到即执行；用于在延迟与吞吐间折中，常设 1/2/4/8 等。
- 配置在 dynamic_batching 里；LLM 生成可能用 continuous batching，需看后端支持。

---

## 记忆要点

1. Dynamic batching = 时间窗口内攒批，max_queue_delay 限等待。
2. Preferred batch size = 优先凑成的 batch 列表，凑齐即跑；常设 1/2/4/8。
3. 配置在 model config 的 dynamic_batching；生成场景注意 continuous batching。

[返回模块](./README.md) | [返回总览](../README.md)
