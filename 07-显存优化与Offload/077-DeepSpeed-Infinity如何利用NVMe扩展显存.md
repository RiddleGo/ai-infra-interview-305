# 第 77 题：`DeepSpeed-Infinity`如何利用NVMe扩展显存？

## 题目

`DeepSpeed-Infinity`如何利用NVMe扩展显存？

---

## 完整讲解

### 一、DeepSpeed-Infinity 的思路

**DeepSpeed-Infinity** 用 **NVMe SSD** 作为「第三级存储」：显存不够时把 optimizer state、梯度、甚至参数 **offload 到 NVMe**，需要时再按块读回。NVMe 容量大（TB 级）、带宽高于传统 SATA，比纯 CPU offload 的「CPU 内存」更可扩展，适合超大模型或长序列。

### 二、如何利用 NVMe 扩展显存

- **分层 offload**：热数据在 GPU，温数据在 CPU 内存，冷数据在 NVMe；按访问频率与 step 需求调度，减少 NVMe 读写。
- **预取与流水线**：下一 stage 需要的数据提前从 NVMe 读到 CPU 或 GPU（prefetch），与当前计算重叠；类似 ZeRO-Offload 的 overlap，但多了一层 NVMe→CPU 的流水。
- **块与压缩**：按块（chunk）读写、可选压缩，降低 IO 次数与体积；NVMe 带宽仍远低于 GPU，所以尽量只搬必要块、并重叠计算。

### 三、带宽与适用场景

NVMe 顺序读约数百 MB/s～数 GB/s，仍低于 PCIe GPU 带宽；因此 Infinity 适合「显存与 CPU 内存都不够、但可接受一定 IO 延迟」的超大模型训练。通过 overlap、预取、分层，把 IO 藏在计算后面，减轻对吞吐的影响。

---

## 面试要点

- Infinity 用 NVMe 做第三级存储，offload optimizer/梯度/参数，按需读回。
- 分层 offload + 预取 + 与计算重叠，减轻 NVMe 带宽瓶颈。
- 适合超大模型、显存与 CPU 内存都紧张时；IO 需与计算流水重叠。

---

## 记忆要点

1. NVMe = 第三级存储，容量大、带宽低于 GPU/PCIe。
2. 分层 + prefetch + overlap 是关键；按块读写、可选压缩。
3. 适用：超大模型、显存与 CPU 都不够。

[返回模块](./README.md) | [返回总览](../README.md)
