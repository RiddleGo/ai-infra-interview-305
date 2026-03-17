# 第 31 题：TVM的Ansor和MetaSchedule的区别？如何搜索最优schedule？

## 题目

TVM的Ansor和MetaSchedule的区别？如何搜索最优schedule？

---

## 完整讲解

### 一、Ansor 与 MetaSchedule 的定位

**Ansor**（TVM 的 auto-scheduler）：通过 **层次化搜索空间**（从 compute 到 threadblock 到 warp 到 tensor core）、**随机采样 + 进化/爬山** 生成 schedule，用 **cost model**（ML 或基于特征）预测性能并选优，再 **实测** 得到最优或近优 schedule。**MetaSchedule** 是 TVM 后续的 **统一自动调度框架**：把「搜索空间、采样、cost model、实测」抽象成模块，支持 **多后端**、**可扩展的 schedule 规则** 与 **更丰富的搜索策略**（如遗传、贝叶斯、ML-based），并集成到 TVM 主分支，逐步替代 Ansor 的用法。

### 二、主要区别

- **抽象层次**：Ansor 偏「一套完整 pipeline」；MetaSchedule 是「调度元框架」，规则与搜索可插拔、可复用到不同 DSL/IR。
- **搜索空间与规则**：MetaSchedule 更强调 **schedule 规则** 的声明式描述与组合，便于加新硬件/新 op 的规则；Ansor 的层次化空间是内置的。
- **生态**：MetaSchedule 与 TVM 的 TensorIR、新 BYOC 等配合，是当前 TVM 主推的自动调度路径；Ansor 仍可用但处于维护/迁移状态。

### 三、如何搜索最优 schedule？

通用流程：**定义计算**（TE 或 TensorIR）→ **定义/选择搜索空间**（哪些 loop 可 tile、split、vectorize、并行等）→ **采样**（随机或基于策略）→ **cost model 打分** 或 **直接实测** → **选最优**。Ansor/MetaSchedule 都提供「自动建搜索空间 + 自动搜索」；若要手控，可写 schedule 模板、只对少量参数（如 tile 大小）做 auto-tune。

---

## 面试要点

- Ansor：TVM 的 auto-scheduler，层次化搜索空间 + cost model + 实测；MetaSchedule：统一调度框架，规则与搜索可插拔、多后端。
- 区别：MetaSchedule 更模块化、可扩展，与 TensorIR 等配合，是当前主推；Ansor 是前代完整 pipeline。
- 搜索最优：定义计算与搜索空间 → 采样 → cost model 或实测 → 取最优；可全自动或模板+少量 tune。

---

## 记忆要点

1. Ansor = 层次化搜索 + cost model + 实测；MetaSchedule = 可插拔的调度框架，替代/扩展 Ansor。
2. MetaSchedule 更模块化、多后端，与 TensorIR 集成；搜索流程：空间 → 采样 → 评估 → 选优。
3. 最优 schedule：自动建空间 + 搜索，或手写模板 + 对关键参数 auto-tune。

[返回模块](./README.md) | [返回总览](../README.md)
