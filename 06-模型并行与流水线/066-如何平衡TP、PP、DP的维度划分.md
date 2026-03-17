# 第 66 题：如何平衡TP、PP、DP的维度划分？以175B模型为例

## 题目

如何平衡TP、PP、DP的维度划分？以175B模型为例

---

## 完整讲解

### 一、三维并行的角色

- **DP（Data Parallelism）**：复制模型，数据分片，梯度 all-reduce；通信量 \(O(参数量)\)，与数据并行度成反比。
- **TP（Tensor Parallelism）**：单层内切分，all-gather/reduce-scatter，通信在节点内高带宽（NVLink）更合适；通常 TP 度 ≤ 单机 GPU 数。
- **PP（Pipeline Parallelism）**：按层切 stage，通信量 \(O(激活)\)，跨节点可接受；PP 度受 pipeline depth 与 bubble 约束。

### 二、175B 的典型划分思路

175B 参数量、单卡放不下整模型，需 PP+TP（或 +DP）。示例：8 机 × 8 GPU = 64 卡。**TP=8**（单机 8 卡做张量并行，NVLink 通信）；**PP=4**（4 个 stage 跨 4 机）；**DP=2**（2 份复制）。这样每 DP 复制有 32 卡：TP×PP=32，梯度在 DP 维 all-reduce。原则：TP 尽量放同机、PP 跨机、DP 视 global batch 与通信能力定。

### 三、平衡要点

- **通信**：TP 通信频繁且量级大，放 NVLink；PP 通信次数少、单次激活大，可跨机；DP 仅梯度 all-reduce，跨机可接受。
- **显存**：单卡显存决定每 stage 能放多少层、micro-batch 多大；TP 度大则每卡参数与激活都减少。
- **吞吐**：micro-batch 数要足够摊薄 bubble；DP 度大则 global batch 大，但 all-reduce 成本上升。175B 常用 TP=8、PP=4～8、DP=2～4 量级，按卡数与拓扑微调。

---

## 面试要点

- TP 放同机（NVLink）、PP 跨机、DP 视 batch 与带宽定；175B 典型 TP=8、PP=4～8、DP=2～4。
- 通信：TP 最吃带宽且频繁，PP 次之，DP 梯度 all-reduce。
- 显存与 bubble 共同约束 PP 深度与 micro-batch 数。

---

## 记忆要点

1. TP 同机、PP 跨机、DP 复制；175B 常用 8×4×2 或类似。
2. 通信量/频率：TP > PP > DP（梯度）。
3. 按显存定 stage 与 M，按带宽定 TP/PP/DP 度。

[返回模块](./README.md) | [返回总览](../README.md)
