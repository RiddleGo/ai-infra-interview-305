# 第 201 题：内存带宽bound vs 计算bound的判断？`arithmetic intensity`？

## 题目

内存带宽bound vs 计算bound的判断？`arithmetic intensity`？

---

## 完整讲解

### 一、Compute bound vs memory bound

**Compute bound**：算力是瓶颈，**增加的计算**能转化为性能提升；GPU 算力吃满、内存带宽有余。**Memory bound**：内存带宽是瓶颈，**减少的访存**能转化为性能提升；算力有余、带宽吃满。判断后即可决定优化方向：算力瓶颈 → 提高并行度、算力利用、或减无效计算；带宽瓶颈 → 融合、复用、合并访问、用共享内存等。

### 二、Arithmetic intensity（算术强度）

**Arithmetic intensity**：**AI = FLOPs / Byte**，即该 kernel（或算子）**每从内存读/写 1 字节能做多少次浮点运算**。**Roofline**：设备有「算力屋顶」与「带宽屋顶」；**ridge point** 对应的 AI 为临界值：**AI 低于该值**多为 **memory bound**，**高于该值**多为 **compute bound**。因此算 **AI** 即可初步判断：AI 小（如逐元素 op）多为 memory bound；AI 大（如大矩阵乘）多为 compute bound。

### 三、如何算与用

**FLOPs**：根据 op 类型与 shape 算（如 matmul M×K × K×N 约 2MNK FLOPs）；**Byte**：该 op 读写的 **输入+输出** 张量字节数。**AI = FLOPs / Byte**。与设备 **ridge point**（带宽/算力比）比较；或直接用 **Nsight Compute** 的 Roofline 图看该 kernel 落在屋顶哪一侧。优化：memory bound → 提高 AI（融合、复用、减少读写）；compute bound → 提高 occupancy、更多有效算力。
---

## 面试要点

- Compute bound = 算力瓶颈；memory bound = 带宽瓶颈；决定优化方向。
- Arithmetic intensity AI = FLOPs/Byte；与 roofline ridge point 比，低则多 memory bound、高则多 compute bound。
- 用 ncu Roofline 或手算 AI；memory bound 提 AI，compute bound 提 occupancy。

---

## 记忆要点

1. Compute bound = 算力瓶颈；memory bound = 带宽瓶颈。
2. AI = FLOPs/Byte；小 AI 多 memory bound，大 AI 多 compute bound。
3. Roofline 看位置；按 bound 类型选优化手段。

[返回模块](./README.md) | [返回总览](../README.md)
