# 第 83 题：CPU offload和GPU计算的流水线重叠如何实现？

## 题目

CPU offload和GPU计算的流水线重叠如何实现？

---

## 完整讲解

### 一、为何要重叠

CPU offload 时，数据在 GPU↔CPU 间搬运（PCIe），若「等拷贝完成再算」会浪费 GPU 算力。**Overlap**：在 GPU 计算当前 layer 时，**异步**把上一 layer 的 offload 数据搬回 GPU（或把下一阶段要用的数据从 CPU 搬到 GPU），使 **拷贝与计算并行**，隐藏部分 PCIe 延迟。

### 二、实现手段

- **双缓冲（double buffering）**：两块 buffer A/B；GPU 算用 A 时，异步把 B 从 CPU 拷到 GPU（或反向）；下一 step 交换角色，算 B 时拷 A。这样「算」与「拷」在时间上重叠。
- **CUDA stream**：计算在一个 stream、拷贝在另一个 stream，用 `cudaMemcpyAsync` + 适当的 event 与依赖，保证「算完再拷」或「拷完再算」的依赖正确，其余时间两 stream 并行。
- **Pipeline 多阶段**：把「计算 stage」与「拷贝 stage」组成流水线：stage1 算 layer1，同时 stage2 在拷 layer0 的数据；下一时刻 stage1 拷 layer1 结果，stage2 算 layer0 的 backward，依此类推。

### 三、与 ZeRO-Offload 等的对应

ZeRO-Offload、DeepSpeed 等实现中，optimizer step 的「梯度→CPU、CPU 更新、参数→GPU」会拆成异步拷贝 + 计算重叠：例如当前 layer 的 backward 与上一 layer 的 CPU 更新 + 回拷重叠，用 prefetch 与 double buffer 实现，从而在 PCIe 瓶颈下仍尽量拉高 GPU 利用率。

---

## 面试要点

- Overlap = 拷贝与计算并行；double buffer + 异步拷贝 + 多 stream。
- 实现：算 buffer A 时异步拷 B；用 cudaMemcpyAsync 与 stream/event 管理依赖。
- ZeRO-Offload 等用「当前 backward 与上一 stage 的 CPU 更新+回拷」重叠。

---

## 记忆要点

1. 双缓冲 + async copy + 多 stream = 拷贝与计算重叠。
2. 算 A 时拷 B，下一 step 交换；依赖用 event 保证。
3. Offload 框架里 prefetch 与 pipeline 是同一思想。

[返回模块](./README.md) | [返回总览](../README.md)
