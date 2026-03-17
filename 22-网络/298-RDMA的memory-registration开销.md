# 第 298 题：`RDMA`的`memory registration`开销？

## 题目

`RDMA`的`memory registration`开销？

---

## 完整讲解

### 一、Memory registration 是什么

**RDMA** 要求参与传输的**内存**必须先**注册**（Memory Registration）：把用户态 buffer 的物理页固定并告知网卡，网卡才能直接 DMA 读写。**MR** 创建时内核/驱动会 pin 页、建立**虚拟地址到物理地址的映射**供 HCA 使用，并可能注册到设备 TPT（Translation and Protection Table）等，有** CPU、TLB、内核元数据**开销。

### 二、开销来源

**Pin 页**：物理页不可 swap、占用常驻内存。**建立映射**：大量 MR 时 TLB 与设备侧 TPT 压力大。**注册/注销本身**：**cudaMalloc** 等分配的内存若要做 RDMA，需再注册为 MR；**注册与注销**是同步、相对重的操作，频繁 reg/dereg 会明显拉高延迟与 CPU。**大块、长生命周期**的 buffer 注册一次、复用可摊薄开销；**小块、短生命周期**则可能成为瓶颈。

### 三、工程应对

**池化 MR**：预注册大块、应用内按需切分或复用，避免每次分配都 reg。**On-demand pin**：部分驱动/库支持按需 pin 或 lazy registration。**GPU**：GPUDirect RDMA 时 GPU 内存也需注册，同样注意注册范围与生命周期；减少注册次数、扩大单次注册块有利于性能。

---

## 面试要点

- Memory registration = 把 buffer 固定并告知网卡，供 RDMA DMA；有 pin、映射、元数据开销。
- 开销：pin 占内存、大量 MR 时 TLB/TPT 压力、reg/dereg 为同步重操作。
- 频繁小块 reg/dereg 易成瓶颈；大块长生命周期、复用可摊薄。
- 工程：MR 池化、按需 pin、减少注册次数与范围。

---

## 记忆要点

1. MR = pin 页 + 建立设备可访问映射；reg/dereg 有开销。
2. 频繁小块注册是瓶颈；大块复用、池化可摊薄。
3. GPU 内存做 RDMA 也需注册；注意范围与生命周期。

[返回模块](./README.md) | [返回总览](../README.md)
