# 第 263 题：`zero-copy` memory的使用场景？`cudaHostAlloc`？

## 题目

`zero-copy` memory的使用场景？`cudaHostAlloc`？

---

## 完整讲解

### 一、Zero-Copy 概念

Zero-copy memory（固定/pinned host 内存的一种用法）指 host 分配一块**可被 GPU 直接访问**的物理内存，GPU kernel 通过 PCIe 按需读取，无需显式 cudaMemcpy。适合「GPU 随机、稀疏访问 host 数据」或数据量不大、拷贝开销不划算的场景。

### 二、cudaHostAlloc

`cudaHostAlloc(&ptr, size, flags)` 分配 **pinned host memory**。flags 常用：`cudaHostAllocDefault`（默认）、`cudaHostAllocMapped`（同时映射到 device 地址空间，即 zero-copy）、`cudaHostAllocPortable`（多 GPU 可见）等。Mapped 时用 `cudaHostGetDevicePointer(&d_ptr, ptr, 0)` 取 device 侧指针，kernel 用 d_ptr 访问。

### 三、使用场景与注意

适合：小量、随机访问、或与计算重叠的流式访问。注意：通过 PCIe 访问延迟高、带宽有限，大块顺序访问不如先 Memcpy 再算；且 mapped 会占 host 物理页、可能影响 swap。

---

## 面试要点

- Zero-copy：host 内存在 GPU 地址空间可见，kernel 直接读，无需显式 copy。
- cudaHostAlloc(..., cudaHostAllocMapped) + cudaHostGetDevicePointer 得到 device 指针。
- 适合小量、随机或流式访问；大块顺序访问仍建议 Memcpy 再算。
- 注意 PCIe 延迟与带宽、以及 pinned 页占用。

---

## 记忆要点

1. Zero-copy = host 映射到 device 空间，kernel 直接访问；cudaHostAllocMapped。
2. cudaHostGetDevicePointer 取 device 指针；kernel 用该指针读。
3. 适合随机/小量访问；大块顺序用 copy 更高效。

[返回模块](./README.md) | [返回总览](../README.md)
