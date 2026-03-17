# 第 296 题：网络`jitter`对训练的影响？如何测量？

## 题目

网络`jitter`对训练的影响？如何测量？

---

## 完整讲解

### 一、Jitter 对训练的影响

**Jitter**（抖动）指**延迟或到达时间的不稳定**：同一类操作（如 all-reduce）在不同 step 或不同 rank 上耗时差异大。训练中集合通信需**所有 rank 到齐**才继续，**最慢的 rank 决定 step 时间**。若某 rank 因网络 jitter 偶发变慢，会拖慢整机；若频繁发生，**有效吞吐下降、扩展性变差**，且难以复现与排查。

### 二、如何测量

**延迟分布**：多次测量同一操作（如 ncclAllReduce）的耗时，看 P50/P90/P99；P99 远大于 P50 即存在明显 jitter。**工具**：NCCL 的 **NCCL_DEBUG=INFO** 或 **timeline** 可看各 rank 的通信时间；**nsys/nvprof** 看 kernel 与通信重叠；**ping、iperf** 看基础网络 RTT 与带宽稳定性。**多机**：对比单机与多机、同 AZ 与跨 AZ 的延迟分布，定位是否由网络路径或共享资源争抢导致。

### 三、缓解思路

网络侧：专用链路、QoS、避免与其它业务混跑。拓扑与 placement：尽量同机架、同交换机。应用侧：重叠计算与通信、适当增大 batch 或减少通信频率，降低对单次延迟的敏感度。

---

## 面试要点

- Jitter = 延迟/到达时间不稳定；最慢 rank 决定 step 时间，拖慢整机与扩展性。
- 测量：同一操作多次测 P50/P90/P99；NCCL_DEBUG、timeline、nsys 看各 rank 耗时。
- 对比单机/多机、同 AZ/跨 AZ 的分布，定位网络或争抢。
- 缓解：专用网络、QoS、placement、重叠计算与通信。

---

## 记忆要点

1. Jitter 导致最慢 rank 拖慢 step；P99 远大于 P50 即存在抖动。
2. 测量：延迟分布、NCCL timeline、nsys；对比不同拓扑与 AZ。
3. 缓解：网络隔离、placement、计算通信重叠。

[返回模块](./README.md) | [返回总览](../README.md)
