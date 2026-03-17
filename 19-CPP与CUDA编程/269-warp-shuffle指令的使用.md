# 第 269 题：`warp shuffle`指令的使用？`__shfl_sync`？

## 题目

`warp shuffle`指令的使用？`__shfl_sync`？

---

## 完整讲解

### 一、Warp Shuffle 概念

**Warp** 是 32 个线程的 SIMD 组；**warp shuffle** 指同一 warp 内线程**直接交换寄存器**，不经过 shared memory 或 global memory，延迟低、带宽高。用于 warp 内 reduce、broadcast、scan 等。

### 二、__shfl_sync

`__shfl_sync(mask, value, src_lane, width)`：在**同一 warp** 内，当前线程从 **src_lane** 号线程读其 **value**。mask 为参与线程的位掩码（通常 `0xffffffff`）。变体：`__shfl_down_sync`（从 lane + delta 读）、`__shfl_up_sync`、`__shfl_xor_sync`（用于 butterfly reduce）等。**sync** 表示参与线程需先在该 warp 内同步（符合 CUDA 9+ 的 convergent 要求）。

### 三、使用注意

仅限 warp 内、同一 warp 的 32 线程；width 可小于 32 表示逻辑子 warp。用于 warp 内 sum、max、broadcast 时比 shared memory 更高效；跨 warp 仍用 shared。

---

## 面试要点

- Warp shuffle：同一 warp 内通过寄存器直接交换数据，无需 shared/global。
- __shfl_sync(mask, value, src_lane)：从 src_lane 读 value；变体 down/up/xor 等。
- mask 为参与线程掩码；sync 表示 convergent 使用。
- 用于 warp 内 reduce、broadcast、scan；跨 warp 用 shared。

---

## 记忆要点

1. Shuffle = warp 内寄存器交换；__shfl_sync(mask, value, src_lane)。
2. 变体：shfl_down/up/xor；mask 与 sync 必写。
3. 用于 warp 内 reduce/broadcast；比 shared 更省更快的 warp 内通信。

[返回模块](./README.md) | [返回总览](../README.md)
