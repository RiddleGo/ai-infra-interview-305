# 第 119 题：`GPTQ`的`one-shot`量化流程？`OBQ`（Optimal Brain Quantization）？

## 题目

`GPTQ`的`one-shot`量化流程？`OBQ`（Optimal Brain Quantization）？

---

## 完整讲解

### 一、GPTQ 的 one-shot 流程

**GPTQ** 是逐层、逐 block 的权重量化方法，**one-shot** 指用一层（或 block）的校准数据一次性求解量化参数，无需端到端微调。流程大致：对某一层，给定校准输入（若干真实激活或合成数据），在该层输出重建误差（如 MSE）约束下，按** Hessian 逆**对权重量化做二阶优化——即 OBQ 思想在 Transformer 上的扩展，按权重对损失的影响顺序逐个或逐组量化，并即时更新未量化权重以补偿误差，使整层量化后输出与 FP 尽量一致。

### 二、OBQ（Optimal Brain Quantization）

**OBQ** 是更早的「最优脑量化」思路：把权重量化视为在约束下的最优删除/舍入问题。用 Hessian 刻画权重对损失的影响，按影响从小到大的顺序量化权重，每量化一个就用闭式解更新其余权重以最小化当前误差，相当于贪心 + 局部最优。GPTQ 把 OBQ 从单层全连接推广到分 block、支持 per-channel/group，并针对 GPU 做了批量化与实现优化，成为 LLM 权重量化的常用基线。

### 三、工程要点

GPTQ 需校准数据（几百条序列即可）、逐层跑一遍；量化后可直接推理或再配激活量化（如 SmoothQuant）。与 AWQ（激活感知）、QAT（训练中量化）相比，GPTQ 无训练、速度快，精度在 W4 上表现好，是离线 PTQ 的代表方法之一。

---

## 面试要点

- GPTQ one-shot：逐层用校准数据 + Hessian 逆做权重量化，一次性求量化参数，无需微调；按对输出的影响顺序量化并更新未量化权重。
- OBQ：用 Hessian 决定量化顺序，贪心+闭式更新，最小化重建误差；GPTQ 是 OBQ 在 Transformer 上的 block 化、工程化。
- 工程：校准几百条即可、逐层跑、可与激活量化组合；无训练、适合 W4 等离线 PTQ。

---

## 记忆要点

1. GPTQ = one-shot 权重量化，逐层校准 + Hessian 逆，按影响顺序量化并补偿。
2. OBQ = Hessian 顺序 + 闭式更新；GPTQ 是 OBQ 的 block/Transformer 版。
3. 无训练、校准即用；常与 SmoothQuant 等配合，W4 常用。

[返回模块](./README.md) | [返回总览](../README.md)
