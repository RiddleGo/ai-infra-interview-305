# 第 28 题：什么是warp divergence？如何检测和避免？

## 题目

什么是warp divergence？如何检测和避免？

---

## 完整讲解

### 一、什么是 warp divergence？

**Warp** 是 32 个线程一起取指、执行；若这 32 线程走 **不同分支**（如 `if (tid < 8) ... else ...`），硬件会 **串行执行** 各分支（先执行满足条件的，再执行不满足的），未参与的分支线程被 **mask 掉**。这种同一 warp 内分支不一致叫 **warp divergence**，会导致有效并行度下降、利用率低。

### 二、如何检测？

- **Nsight Compute**：看 **Warp Execution Efficiency**（活跃线程比例）、**Divergence** 相关指标；若某 kernel 效率明显低于 100%，多半有 divergence。
- **代码审查**：找 **分支条件依赖 threadIdx / blockIdx** 的 `if/else`、`switch`；尤其是 `tid % 某数`、`tid < 常数` 等，易造成 warp 内部分叉。

### 三、如何避免或减轻？

- **分支与 warp 对齐**：让同一 warp 内线程走同一分支；例如「前 8 个 thread 做 A、后 24 个做 B」可改成「前 8 个 warp 做 A、后若干 warp 做 B」，或用 **warp 内 ballot/sync** 做一致决策。
- **用无分支写法**：用 **predicate**、**select/三元** 或 **算术** 代替分支（如 `x = (cond ? a : b)` 有时被编译成 predicated 指令，两路都算再选，避免真正分支）；小范围可接受。
- **重排数据/线程**：让「同一分支」的数据由同一 warp 处理（sort by branch、或 thread 映射到连续区间），减少 warp 内分支不一致。

---

## 面试要点

- Warp divergence：同一 warp 内走不同分支，硬件串行执行各分支，mask 未参与线程，导致利用率低。
- 检测：Nsight Compute 的 warp 效率、divergence 指标；代码里找依赖 threadIdx 的分支。
- 避免：分支与 warp 对齐、用 predicate/select 代替分支、重排使同分支同 warp。

---

## 记忆要点

1. Divergence = 同 warp 内分支不同 → 串行执行各分支，mask 部分线程。
2. 看 Nsight warp 效率；分支条件依赖 tid 易产生 divergence。
3. 对齐分支到 warp、用无分支写法、或重排数据使同分支同 warp。

[返回模块](./README.md) | [返回总览](../README.md)
