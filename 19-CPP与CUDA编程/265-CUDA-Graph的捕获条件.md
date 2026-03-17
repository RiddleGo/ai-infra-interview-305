# 第 265 题：`CUDA Graph`的捕获条件？哪些操作不能捕获？

## 题目

`CUDA Graph`的捕获条件？哪些操作不能捕获？

---

## 完整讲解

### 一、CUDA Graph 捕获目的

**CUDA Graph** 把一段 kernel 与 memcpy 序列录成一张图，一次性提交、减少 host 侧启动开销，适合**固定计算图、反复执行**的推理或训练 step。

### 二、捕获条件

在 **stream 上** 用 `cudaStreamBeginCapture(stream)` 开始、`cudaStreamEndCapture(stream, &graph)` 结束；期间在该 stream 上发的 kernel、memcpy 会被记录。要求：**不能**在捕获期间做依赖该 stream 结果的 host 同步（如 cudaStreamSynchronize）、不能做会阻塞或依赖未捕获操作的行为；子图、条件分支需用 stream 内可表达的方式。

### 三、不能捕获的操作

**cudaStreamSynchronize**、**cudaDeviceSynchronize**、**cudaMemcpy**（同步版）、**cudaMalloc** 等会阻塞或非异步的 API 不能在捕获期间对「被依赖的 stream」调用。**cudaLaunchHostFunc** 在部分版本/场景下有限制。用 **cudaMemcpyAsync**、**cudaMallocAsync**（若可用）等异步接口即可纳入图。

---

## 面试要点

- CUDA Graph 记录一段 kernel/copy 序列，一次提交反复执行，降低 launch 开销。
- 捕获：cudaStreamBeginCapture / EndCapture；只能录异步、非阻塞的操作。
- 不能捕获：StreamSynchronize、DeviceSynchronize、同步 cudaMemcpy、cudaMalloc 等阻塞调用。
- 用 *Async 接口、避免在捕获期间 host 同步。

---

## 记忆要点

1. Graph = 录一段操作序列；BeginCapture/EndCapture 在 stream 上。
2. 只能录异步操作；同步/阻塞 API 不能出现在捕获路径上。
3. 用 cudaMemcpyAsync、避免 Synchronize/cudaMalloc 等。

[返回模块](./README.md) | [返回总览](../README.md)
