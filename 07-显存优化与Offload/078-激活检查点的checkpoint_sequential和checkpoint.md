# 第 78 题：激活检查点的`checkpoint_sequential`和`checkpoint`区别？

## 题目

激活检查点的`checkpoint_sequential`和`checkpoint`区别？

---

## 完整讲解

### 一、Activation checkpointing 的目的

前向时只保存部分层的激活（如每层或每隔几层存一次），其余在 **backward 时按需重算**，用算力换显存，使更深的网络或更大 batch 能跑起来。

### 二、checkpoint_sequential

**checkpoint_sequential**（如 `torch.utils.checkpoint.checkpoint_sequential`）：把 **一个 sequence 的 submodule 列表** 当作一整段，只在这段的**首或尾**存一次 checkpoint，中间全部重算。适用：**顺序**的若干层（如 ResNet 的 stage、Transformer 的若干连续层），接口简单，但粒度较粗，重算范围大。

### 三、checkpoint（通用）

**checkpoint**（如 `torch.utils.checkpoint.checkpoint`）：对 **单个** 可调用的 `function` 或子模块做 checkpoint；前向时只记输入，不存中间激活，backward 时用同一输入重新执行 function 得到激活再算梯度。粒度细，可只对某一层或某一 block 用，**非顺序** 或自定义 block 也可用；需保证 function 无副作用、确定性（否则重算结果可能不一致）。

### 四、对比与选择

- **checkpoint_sequential**：顺序子模块列表、一段只一个 checkpoint；实现简单，重算多。
- **checkpoint**：任意单次调用、粒度细；灵活，适合单层或自定义块。大模型里常用 **checkpoint** 对 attention 或 FFN 逐块包装，或配合自定义 segment 实现「每 N 层一个 checkpoint」。

---

## 面试要点

- checkpoint_sequential：一段顺序子模块共用一个 checkpoint，粒度粗、重算多。
- checkpoint：单次 function/模块，粒度细、可任意包装；需无副作用、确定性。
- 大模型常用 checkpoint 对 attention/FFN 逐块或按段包装。

---

## 记忆要点

1. sequential = 一段顺序层共用一个存点；checkpoint = 单层/单块。
2. sequential 粗、重算多；checkpoint 细、灵活。
3. 生产多用 checkpoint 包装单层或自定义 segment。

[返回模块](./README.md) | [返回总览](../README.md)
