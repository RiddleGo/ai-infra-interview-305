# 第 257 题：CUDA的`__shared__` memory使用注意事项？`bank conflict`？

## 题目

CUDA的`__shared__` memory使用注意事项？`bank conflict`？

---

## 完整讲解

### 一、`__shared__` 使用注意

Shared memory 是 SM 内 block 内线程共享的片上存储，容量有限（几十 KB 级），速度快。需注意：**静态分配** `__shared__ T buf[N]` 或**动态** `extern __shared__ T buf[]` 配合 `<<<..., size>>>`；生命周期与 block 一致；同一 block 内线程可协作读写。

### 二、Bank conflict

Shared memory 按 4 字节（或 32 位宽）分成若干 bank；同一 warp 内多线程访问**同一 bank 不同地址**会串行化（bank conflict）。避免方式：保证同一 warp 访问不同 bank（如按 threadIdx.x  stride 访问）、或访问同一地址（broadcast 不冲突）；padding 可打散对齐以降低冲突。

### 三、工程要点

设计 shared 布局时先算访问模式，避免 32 路 bank 同 bank 不同地址；reduce、矩阵 tile 等常用 shared，注意边界与对齐。

---

## 面试要点

- `__shared__` 是 block 内共享、片上、容量有限；静/动态分配、生命周期与 block 一致。
- Bank：按 4B 分 bank；同 warp 同 bank 不同地址 = bank conflict，会串行。
- 避免：不同 bank 访问、或同地址 broadcast；可用 padding 打散。
- 设计时算清访问模式，reduce/tile 常用 shared。

---

## 记忆要点

1. Shared = block 内共享、片上、有限容量；注意静/动态分配。
2. Bank conflict = 同 warp 同 bank 不同地址；避免或 padding。
3. 工程上先算访问模式，reduce/tile 注意 stride 与对齐。

[返回模块](./README.md) | [返回总览](../README.md)
