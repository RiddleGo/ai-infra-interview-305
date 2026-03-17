# 第 29 题：动态shape的算子如何优化？`vllm`中的`PagedAttention`是如何解决这个问题的？

## 题目

动态shape的算子如何优化？`vllm`中的`PagedAttention`是如何解决这个问题的？

---

## 完整讲解

### 一、动态 shape 的难点

**动态 shape**（batch/seq 等维度运行时才定）导致：**一、** 难以在编译期做满 **静态分配与循环边界**，易生成多份 kernel 或泛化代码；**二、** 不同 shape 下最优 tile、block 可能不同；**三、** 若按最大 shape 分配显存会浪费，按当前 shape 又可能频繁重编译或分配。

### 二、常见优化思路

- **多 kernel / 分派**：按 shape 区间或关键维（如 seq_len 是否大于某值）选不同 kernel 或配置，减少「一个 kernel 吃遍所有 shape」的保守代价。
- **符号 shape + 统一 kernel**：用符号变量表示维度，生成**一份**带符号边界的 kernel，运行时代入实际值；TVM/Triton 等支持，可减少代码膨胀，但调试与优化难度增加。
- **PagedAttention / 显存管理**：不按「整块连续 tensor」分配，而是 **分页**（block 或 page 为单位）、按需映射；变长序列只占实际用的页，避免按 max length 分配，并利于 **KV cache 复用** 与碎片控制。

### 三、vLLM 的 PagedAttention

**PagedAttention** 把 **KV cache** 切成固定大小的 **block**（如 16 个 token 一 block），物理上按 block 分配、逻辑上用 **block 表** 记录每个序列用了哪些 block；不同序列可共享未用 block、且 **同一序列内 block 不必连续**。这样 **动态长度** 只影响 block 个数，不触发「整块大 buffer 重分配」；显存利用率高、碎片少，且便于与 prefetch、并行解码配合。算子侧可针对「按 block 取 KV」做优化，而不是假设一大块连续 layout。

---

## 面试要点

- 动态 shape：难在编译期优化、多 shape 最优配置不同、显存按 max 浪费；优化有多 kernel 分派、符号 shape 统一 kernel、分页显存。
- PagedAttention：KV 按 block 分页，block 表记录序列占用；按需分配、少碎片、易复用，适配动态长度。
- 算子优化可围绕「按 block 访问」设计，而非假设连续大 buffer。

---

## 记忆要点

1. 动态 shape 优化：分派多 kernel、符号 shape、分页显存；避免按 max shape 一刀切。
2. PagedAttention = KV 分 block、block 表管理；按需占 block，显存利用率高、适配变长。
3. 算子侧可针对 block 级访问做优化，与分页策略一致。

[返回模块](./README.md) | [返回总览](../README.md)
