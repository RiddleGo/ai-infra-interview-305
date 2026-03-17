# 第 152 题：大模型训练的`checkpoint`格式？`sharded checkpoint`的合并？

## 题目

大模型训练的`checkpoint`格式？`sharded checkpoint`的合并？

---

## 完整讲解

### 一、大模型 Checkpoint 格式

常见有 **PyTorch 原生**（`torch.save(state_dict)` → `.pt`/`.bin`）、**safetensors**（见下题）、**分片格式**（如 `model-00001-of-00005.safetensors`）等。**Sharded checkpoint**：参数按 rank 或按层分片存成多文件，每文件只含一部分参数，便于多卡/多机保存时各写各的、且单机加载时可按需只加载部分；合并后可得完整 state_dict。

### 二、Sharded Checkpoint 的合并

**合并目的**：推理或单卡加载时需要完整参数，要把多份分片合并成一份。**做法**：（1）按约定顺序读入各分片文件（如按 rank 或按 shard 编号）；（2）按 key 或元数据把同一参数名的分片拼成完整 tensor；（3）写出为单文件或统一 state_dict。工具上：Hugging Face 的 `safe_convert`、各框架的 checkpoint 工具（如 Megatron 的 `merge` 脚本）都支持；需注意分片时的切分方式（按层、按 rank、按参数量）与合并顺序一致，以及 dtype、device 等元信息一致。

### 三、注意点

合并后单文件可能很大，注意磁盘与内存；若仅做推理可考虑不合并、用分片加载（见存储与 IO 题）。版本与键名要兼容，避免漏键或重复。

---

## 面试要点

- 大模型 checkpoint 有 .pt/.bin、safetensors、分片多文件；sharded 便于多卡各写各的、按需加载。
- 合并：按分片顺序读入、按 key 拼成完整 tensor、写出单文件；工具如 HF 的 convert、各框架 merge 脚本。
- 分片方式与合并顺序一致；合并后单文件大，可按需只合并或保留分片加载。

---

## 记忆要点

1. Sharded = 多文件分片存；合并 = 按序读入、按 key 拼接、写出单文件。
2. 工具：HF、Megatron 等有现成合并脚本；注意分片约定一致。
3. 推理也可不合并，用分片加载。

[返回模块](./README.md) | [返回总览](../README.md)
