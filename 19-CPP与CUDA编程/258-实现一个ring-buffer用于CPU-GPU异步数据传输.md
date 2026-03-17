# 第 258 题：实现一个`ring buffer`用于CPU-GPU异步数据传输

## 题目

实现一个`ring buffer`用于CPU-GPU异步数据传输

---

## 完整讲解

### 一、目的与结构

Ring buffer 固定大小、首尾相接，用于 CPU 与 GPU 之间**双缓冲或多缓冲**流水：CPU 写下一块数据时 GPU 读当前块，实现异步传输与计算重叠。典型：连续多段 host 内存（或 pinned）对应多段 device 内存，用下标或指针环回。

### 二、实现要点

维护 **write_pos**（CPU 写）、**read_pos**（GPU 读）；空/满用 pos 差或 count 判断，避免判满与判空条件相同。用 **cudaMemcpyAsync** 配合 **stream** 按 slot 拷贝；CPU 侧用 pinned memory 提升 D2H/H2D 带宽。同步用 stream/event，保证「写完再拷、拷完再算」。

### 三、工程经验

Slot 数量一般 2～4 即可重叠；注意对齐与 stride；多 producer/consumer 时需原子或锁保护 pos。

---

## 面试要点

- Ring buffer 用于 CPU-GPU 流水：多 slot 轮流写/读，实现传输与计算重叠。
- write_pos/read_pos 环回；空满用 pos 差或 count 区分。
- cudaMemcpyAsync + stream + pinned memory；用 event 同步「写→拷→算」。
- Slot 数 2～4；多线程改 pos 需原子或锁。

---

## 记忆要点

1. Ring = 固定大小、首尾相接；多 slot 实现 CPU 写与 GPU 读重叠。
2. write_pos/read_pos、cudaMemcpyAsync + stream + pinned。
3. 同步用 stream/event；slot 数 2～4，多线程保护 pos。

[返回模块](./README.md) | [返回总览](../README.md)
