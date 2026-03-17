# 第 167 题：`DALI`（NVIDIA Data Loading Library）的使用场景？

## 题目

`DALI`（NVIDIA Data Loading Library）的使用场景？

---

## 完整讲解

### 一、DALI 是什么

**NVIDIA DALI**（Data Loading Library）：在 **GPU 上做数据解码与预处理**（解码、resize、crop、normalize 等），数据从存储或 CPU 进入后由 DALI pipeline 在 GPU 上完成解码与 augments，输出 GPU tensor 直接供训练，减少 CPU-GPU 拷贝与 CPU 瓶颈，并可与训练计算**流水线重叠**。

### 二、使用场景

**图像/视频训练**：解码（JPEG、视频帧）、resize、crop、flip、normalize 等放在 GPU，CPU 只做 IO 或轻量调度；适合 CV 与多模态里解码重的场景。**高吞吐需求**：当 DataLoader 的 CPU 解码成为瓶颈、GPU 利用率上不去时，用 DALI 把解码迁到 GPU 或专用线程，提高吞吐。**多模态与复杂 augment**：DALI 支持多种 op 与组合，可在同一 pipeline 里做图像+文本的预处理。**不适合**：纯文本、或数据已预处理好只需简单 tensor 化时，DALI 收益有限且增加依赖；小数据集或 IO 非瓶颈时不必上 DALI。

### 三、工程要点

DALI 与 PyTorch/TF 通过 iterator 或 DataLoader 适配器对接；需保证 GPU 显存能同时容纳 DALI buffer 与模型；调试时先确认 CPU 解码确实是瓶颈再引入 DALI。

---

## 面试要点

- DALI = GPU 上解码与预处理，减少 CPU 瓶颈与 CPU-GPU 拷贝，可与训练计算重叠。
- 场景：图像/视频解码重、高吞吐 CV、多模态预处理；纯文本或已预处理好则收益小。
- 与框架通过 iterator/DataLoader 对接；注意显存；先确认瓶颈再引入。

---

## 记忆要点

1. DALI = GPU 解码与预处理；减 CPU 瓶颈、增吞吐。
2. 适合解码重的 CV/多模态；不适合纯文本或非瓶颈。
3. 对接 PyTorch/TF；显存与瓶颈确认。

[返回模块](./README.md) | [返回总览](../README.md)
