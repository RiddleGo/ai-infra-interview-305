# 第 243 题：推理结果的`caching`策略？`prompt`级别的deduplication？

## 题目

推理结果的`caching`策略？`prompt`级别的deduplication？

---

## 完整讲解

### 一、推理结果缓存的目的

**相同或相近请求** 的推理结果可 **复用**，减少 **重复计算**、**降延迟与成本**。尤其 **大模型** 单次推理贵，**高重复**（如相同 prompt、模板化问答）时缓存收益大。

### 二、Caching 策略

**Key**：常用 **完整 prompt**（或 **prompt 的 hash**）作 key；**多轮对话** 可用 **session_id + 轮次** 或 **对话摘要**。**存储**：**Redis/Memcached** 等做 **分布式缓存**；**TTL** 控制过期（如 1 小时、1 天）。**命中**：请求先 **查 cache**；命中则 **直接返回**、不调模型；未命中则 **推理后写入 cache 再返回**。**失效**：模型版本更新时 **按 prefix 或全量失效**；或 **版本号** 写进 key，自然隔离。

### 三、Prompt 级 deduplication

**Deduplication**：**相同 prompt** 的 **并发请求** 可 **合并**为一次推理，**多路复用** 结果（即 **request coalescing**）。实现：**短时间窗口** 内相同 prompt 的请求 **排队**，**只跑一次** 推理，结果 **广播** 给所有等待者。**与 cache 区别**：cache 是 **跨请求、持久**；dedup 是 **同批请求** 合并。二者可同时用：**先 dedup 再查 cache**，再未命中则推理。
---

## 面试要点

- 结果缓存：相同/相近请求复用结果；key 常用 prompt 或 hash；Redis 等、TTL。
- 命中则直接返回；未命中推理后写 cache；模型更新时失效或版本号进 key。
- Prompt 级 dedup：并发相同 prompt 合并为一次推理、结果复用；与 cache 可叠加。

---

## 记忆要点

1. Cache key = prompt/hash；存储 Redis、TTL。
2. 命中直接返回；版本更新失效。
3. Dedup = 并发同 prompt 合并一次推理；与 cache 叠加。

[返回模块](./README.md) | [返回总览](../README.md)
