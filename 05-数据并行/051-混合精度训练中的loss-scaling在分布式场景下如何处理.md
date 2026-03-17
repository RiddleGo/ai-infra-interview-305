# 第 51 题：混合精度训练中的`loss scaling`在分布式场景下如何处理？

## 题目

混合精度训练中的`loss scaling`在分布式场景下如何处理？

---

## 完整讲解

### 一、Loss scaling 在做什么？

FP16 梯度容易**下溢**（太小变成 0），所以在 backward 前对 loss **乘一个 scale**（如 2^16），梯度整体放大；在 optimizer step 前再 **unscale**（除回 scale），并检查 inf/nan，有则 skip step 并减小 scale。**GradScaler** 管这件事。

---

### 二、分布式下的要点

- **每卡独立 scale**：每张卡有自己的 scaler 和 scale 值；backward 时每卡用**同一 loss 的 scale 后的值**（若 loss 是各卡 local loss 的 mean/sum，先 scale 再 backward 或先 backward 再 scale 要一致）。
- **一致性**：若用 **all-reduce 后的梯度**（如 DDP），每卡 unscale 后梯度应一致；scaler 的 **unscale** 在每卡本地做，然后 all-reduce 梯度，所以每卡 unscale 的输入（本地梯度）在 DDP 里其实是「未 all-reduce 的本地梯度」——要在 **all-reduce 之前** unscale，或对 **all-reduce 之后的梯度** 做一次 unscale（取决于框架实现）。常见做法：**backward 时每卡 scale(loss).backward()，梯度是 scale 后的本地梯度；DDP 再 all-reduce；step 前每卡对 all-reduce 后的梯度 unscale**，这样每卡看到的是同一份「全局梯度」的 unscale 结果。
- **Skip step**：若某卡 unscale 后发现 inf/nan，该卡 skip step；**所有卡必须一致 skip**，否则会参数不一致。所以通常 **scaler.step(optimizer)** 里若 skip，会通过 collective（如 all_reduce 一个 flag）让所有进程一起 skip，并统一减小 scale。

---

### 三、总结

- 每卡用同一套 scale 逻辑；unscale 的时机要对：要么对 all-reduce 前的本地梯度 unscale 再 all-reduce，要么对 all-reduce 后的梯度做一次 unscale（框架会封装好）。
- Skip step 要**全局一致**：用 collective 同步「是否 skip」，避免部分卡更新、部分卡不更新导致分叉。

---

## 面试要点

- Loss scaling：scale loss → backward → unscale 梯度 → step 或 skip；分布式下每卡 scale 一致。
- Unscale 时机：与梯度 all-reduce 顺序要正确（通常 all-reduce 后对全局梯度 unscale，或框架封装）。
- Skip step 必须所有卡一致，用 collective 同步 skip 与 scale 更新。

---

## 记忆要点

1. 分布式下每卡同一 scale；unscale 与 all-reduce 顺序由框架保证。
2. Skip 时所有卡一起 skip，用 all_reduce 同步 flag。
3. 保证「全局梯度」只被 unscale 一次、所有卡同一 step/skip 决策。

[返回模块](./README.md) | [返回总览](../README.md)
