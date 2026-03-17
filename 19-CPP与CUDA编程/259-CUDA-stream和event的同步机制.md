# 第 259 题：`CUDA stream`和`event`的同步机制？`cudaStreamSynchronize`？

## 题目

`CUDA stream`和`event`的同步机制？`cudaStreamSynchronize`？

---

## 完整讲解

### 一、Stream 与 Event 概念

**CUDA stream** 是设备上的操作队列，同一 stream 内 kernel、memcpy 顺序执行，不同 stream 可并发。**Event** 是时间点标记，可 `cudaEventRecord(event, stream)` 在 stream 某处插入，再 `cudaStreamWaitEvent(stream2, event)` 让另一 stream 等待该点。

### 二、cudaStreamSynchronize

`cudaStreamSynchronize(stream)` 阻塞**当前 host 线程**直到该 stream 上所有已提交操作完成。与 `cudaDeviceSynchronize()` 区别：后者等所有 stream，前者只等指定 stream。用于「host 需要该 stream 结果后再继续」的场景。

### 三、典型用法

用 event 做 stream 间依赖（如 stream B 等 stream A 的 kernel 完成）；用 stream 做 kernel 与 memcpy 重叠；需要 host 取结果时对该 stream 做 `cudaStreamSynchronize`。

---

## 面试要点

- Stream：操作队列，同 stream 顺序、不同 stream 可并发；Event：时间点，可 record + wait。
- cudaStreamSynchronize(stream)：host 阻塞直到该 stream 完成；cudaDeviceSynchronize 等全部。
- 用 event 做 stream 间依赖；用 stream 做 kernel 与 copy 重叠。

---

## 记忆要点

1. Stream = 队列；Event = 时间点；record + wait 做依赖。
2. cudaStreamSynchronize 只等指定 stream；DeviceSynchronize 等全部。
3. 重叠用多 stream；host 要结果时再 sync。

[返回模块](./README.md) | [返回总览](../README.md)
