# 第 206 题：CPU offload的`pin_memory`和`non_blocking`？

## 题目

CPU offload的`pin_memory`和`non_blocking`？

---

## 完整讲解

### 一、CPU-GPU 拷贝与 pin_memory

**CPU 到 GPU** 的数据拷贝若走 **pinned memory（页锁定内存）**，DMA 可直接访问、**带宽更高**，且可与 GPU 计算**异步**进行。**pin_memory=True**（在 DataLoader 的 tensor 或 `torch.Tensor.pin_memory()`）：把 tensor 放在 **pinned 页**，拷贝到 GPU 时用 **async copy**，减少阻塞与总时间。

### 二、non_blocking

**non_blocking=True**（在 `.to(device, non_blocking=True)`）：表示 **CPU→GPU 拷贝** 是**异步**的，当前 CPU 流不等待拷贝完成就返回；GPU 侧在**使用该 tensor 前**需保证拷贝已完成（通常由 CUDA 流依赖自动保证，或后续 kernel 在同一 stream 上会等待）。这样 **CPU 可继续** 准备下一批或做其它事，与 GPU 计算**重叠**，提高吞吐。

### 三、配合使用

DataLoader 里 **pin_memory=True** 使取出的 tensor 在 pinned 区；训练循环里 **.to(device, non_blocking=True)** 做异步拷贝。需保证**使用前**拷贝已完成：同一 stream 上后续 kernel 会自动等；若多 stream 需 **event** 同步。典型场景：数据加载与上一 batch 的 GPU 计算重叠，减少「GPU 等数据」的 gap。
---

## 面试要点

- pin_memory：tensor 放页锁定内存，CPU→GPU 拷贝更快、可异步；DataLoader 或 tensor.pin_memory()。
- non_blocking=True：.to(device) 异步，CPU 不等待拷贝完成；与 GPU 计算重叠需流/event 保证顺序。
- 配合：DataLoader pin_memory + to(device, non_blocking=True)；重叠加载与计算。

---

## 记忆要点

1. pin_memory = 页锁定、DMA 友好、异步拷贝。
2. non_blocking = 异步 to(device)；用流/event 保证使用前拷贝完成。
3. 二者配合重叠 IO 与计算。

[返回模块](./README.md) | [返回总览](../README.md)
