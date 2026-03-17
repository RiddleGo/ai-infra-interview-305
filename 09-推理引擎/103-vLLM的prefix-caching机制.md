# 第 103 题：vLLM的`prefix caching`机制？命中率如何提升？

## 题目

vLLM的`prefix caching`机制？命中率如何提升？

---

## 完整讲解

### 一、Prefix Caching 机制

**Prefix caching**：多个请求若共享**相同前缀**（如 system prompt、长 context），则只算一次该前缀的 KV，并**缓存**起来；后续请求直接复用这些 KV block，只算「前缀之后」的 decode。与 PagedAttention 的 block 结合：共享前缀对应同一组 block，多请求引用同一 block 表前缀部分，省显存与算力。

### 二、命中率提升

- **请求路由**：把相同 prefix 的请求尽量**路由到同一实例**或同一 block 池，使缓存可复用；多实例时可用一致性 hash 或 prefix 指纹路由。
- **Prefix 规范化**：对 system prompt、模板做**归一化**（去空格、统一格式），提高「相同 prefix」的匹配率；或对长 prefix 做**分段指纹**，允许部分命中。
- **缓存策略**：LRU 或 TTL；保留热点 prefix（如常见 prompt），淘汰冷门；显存允许时可多保留一些 prefix block。
- **业务设计**：鼓励复用同一套 system/context 模板，或把超长 context 做成「可引用」的 prefix id，从设计上提高命中。

### 三、与 PagedAttention 的关系

PagedAttention 的 block 表天然支持「多序列指向同一 block」；prefix caching 就是在逻辑上识别「相同前缀」并复用这些 block，实现上即多序列的 block table 前缀段指向同一组物理 block。

---

## 面试要点

- Prefix caching = 相同前缀的 KV 只算一次、多请求复用；与 PagedAttention block 共享一致。
- 命中率：路由到同实例、prefix 规范化、LRU/TTL、业务复用模板或 prefix id。
- 多实例时用路由与指纹提高跨请求命中。

---

## 记忆要点

1. 共享前缀 = 共享 KV block；只算一次前缀，后续复用。
2. 命中率 = 路由 + 规范化 + 缓存策略 + 业务复用。
3. Block 表前缀段指向同一物理 block 即实现 prefix cache。

[返回模块](./README.md) | [返回总览](../README.md)
