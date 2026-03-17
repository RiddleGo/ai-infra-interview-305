# 第 262 题：`NCCL`的`all-reduce`实现？`ring`算法代码走读？

## 题目

`NCCL`的`all-reduce`实现？`ring`算法代码走读？

---

## 完整讲解

### 一、NCCL All-Reduce 作用

NCCL 提供多 GPU/多机集合通信，**all-reduce** 即每 rank 有一份输入，结果每 rank 得到相同的规约值（如 sum）。用于分布式训练里梯度/参数同步。

### 二、Ring All-Reduce 思路

Ring 算法把 N 个节点连成环。**Reduce-Scatter** 阶段：数据分块，沿环多轮传递，每轮每节点做部分 reduce 并传给下一节点，最终每节点持有 1/N 的完整规约结果。**All-Gather** 阶段：再沿环把各节点持有的块广播出去，最后每节点得到完整结果。带宽利用好，适合大 tensor。

### 三、代码走读要点

NCCL 源码中 ring 实现在 `ring.cu` 等；关注 **send/recv 方向**、**chunk 划分**、**in-place 与 buffer**、以及 **ncclSend/ncclRecv** 与 kernel 的配合。不同拓扑（单机多卡、多机）会选 ring 或 tree 等算法。

---

## 面试要点

- All-reduce：每 rank 输入，每 rank 得相同规约结果；NCCL 实现多种算法。
- Ring：Reduce-Scatter（分块沿环 reduce）+ All-Gather（沿环广播）；带宽友好。
- 走读看 send/recv、chunk、buffer 与 kernel 配合；拓扑决定 ring/tree 等。
- 用于分布式训练梯度/参数同步。

---

## 记忆要点

1. All-reduce = 每 rank 同结果；Ring = Reduce-Scatter + All-Gather。
2. 分块沿环传递，带宽利用率高；多机可选 ring/tree。
3. 走读：ring 方向、chunk、buffer、ncclSend/Recv。

[返回模块](./README.md) | [返回总览](../README.md)
