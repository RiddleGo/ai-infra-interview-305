# 第 20 题：TF Serving的batching策略如何配置？遇到过哪些坑？

## 题目

TF Serving的batching策略如何配置？遇到过哪些坑？

---

## 完整讲解

### 一、TF Serving 的 batching 在做什么？

请求到达后不是「一个请求立刻推理一次」，而是先**入队**，由 **Batch Scheduler** 按策略**攒成一批**再一起送进模型，从而提高 GPU 利用率、降低单请求平均延迟（在吞吐优先时）。策略包括：**多久等一批（batch timeout）、最多多少个（max batch size）、以及可选的优先级**等。

---

### 二、如何配置？

- **Batching 参数**（在 model config 或 batching parameters 里）：
  - **max_batch_size**：一批最多多少个请求。
  - **batch_timeout_micros**：等待凑批的最长时间（微秒），超时则当前已入队的也送走。
  - **max_enqueued_batches**：队列里最多允许多少个「未满的批」在等，超过可拒绝新请求或背压。
- **动态 batching**：TF Serving 支持「动态」把多个请求拼成一个 batch（padding 或 packing），模型需支持变长或 batch 维；配置里打开相应 batching 并设上述参数。
- **与模型签名一致**：输入是 batched 的（batch 维在第一维），模型 export 时就要按 batch 输入导出；否则会 shape 不匹配。

---

### 三、常见坑

- **timeout 与延迟**：batch_timeout 设太大，请求会等很久才凑批，**尾延迟**变高；设太小，批小、GPU 利用率低。要按 P99 延迟和吞吐做权衡。
- **shape 与 padding**：变长请求要 **padding 到同一长度** 或做 **packing**；padding 浪费算力，packing 要模型支持。若模型只支持固定 shape，动态 batch 需保证 padding 后 shape 一致。
- **OOM**：max_batch_size 过大，单批显存超 GPU 容量会 OOM；要按单请求显存 × batch 上限估算。
- **队列堆积**：高 QPS 时若处理跟不上，enqueued batches 满会拒绝或拖慢；需配合限流、扩容或降 batch_size。
- **与预处理一致**：Serving 端做 batching 时，预处理（解码、归一化）要在 batch 维度正确拼接，否则逻辑错或性能差。

---

### 四、建议

- 先压测：看**单请求显存、延迟**，再定 max_batch_size、batch_timeout；观察 P50/P99 与吞吐。
- 变长模型：明确用 padding 还是 packing、谁做、shape 上限多少。
- 监控队列长度、batch 实际大小、超时次数，便于调参和排障。

---

## 面试要点

- 配置：max_batch_size、batch_timeout_micros、max_enqueued_batches；与模型 batch 输入一致。
- 坑：timeout 与尾延迟、shape/padding/packing、OOM、队列堆积、预处理与 batch 维一致。
- 调参看 P99 与吞吐；监控队列与实际 batch 大小。

---

## 记忆要点

1. 参数：max_batch_size、batch_timeout、max_enqueued_batches；模型需支持 batch 输入。
2. 坑：大 timeout → 高尾延迟；小 → 批小利用率低；OOM、shape/padding、队列满。
3. 按显存与延迟压测定参；监控队列与 batch 分布。

[返回模块](./README.md) | [返回总览](../README.md)
