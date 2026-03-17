# 第 159 题：训练任务的`fault tolerance`？`elastic training`的实现？

## 题目

训练任务的`fault tolerance`？`elastic training`的实现？

---

## 完整讲解

### 一、Fault Tolerance 需求

长时训练（数天到数周）中节点、网络、磁盘可能故障；**容错**目标：故障发生后**从最近一致状态恢复**、**不重头开训**，且恢复后与未中断时**行为一致**（见 checkpoint consistency 题）。手段核心：**定期 checkpoint** + **可恢复的 dataloader 与 RNG** + **弹性或固定拓扑的进程组**。

### 二、Elastic Training 实现

**Elastic training**：允许训练过程中 **worker 数变化**（节点加入或退出），通过协调器（如 PyTorch Elastic、TorchX）管理 rank 与 world_size 的变更、重新分配数据分片、并从**一致 checkpoint** 恢复。实现要点：（1）**协调器**：监控进程存活、发现新节点或失效节点，触发 resize；（2）**Checkpoint**：在已知一致点（如 step 边界）保存，恢复时所有存活 rank 加载同一 checkpoint 并同步 step；（3）**Rendezvous**：重新做一次进程组组建，新 world_size 与 rank 分配；（4）**Data**：sampler 按新 world_size 重新分片，保证不重不漏。固定规模时也可不用弹性，仅用「故障时从 checkpoint 重启」的容错。

### 三、与普通容错的区别

普通容错 = 固定规模 + 故障则全组重启 + 从 checkpoint 恢复。Elastic = 支持规模变化、动态 rendezvous、数据与状态按新规模重分配；实现更复杂，适合云上节点可能缩容/扩容的场景。

---

## 面试要点

- 容错 = 故障后从一致 checkpoint 恢复、不重头训、行为一致；依赖定期 checkpoint + 可恢复的 dataloader/RNG。
- Elastic = 支持 worker 数变化；协调器监控、resize 时 rendezvous、checkpoint 恢复、数据按新规模重分片。
- 固定规模可仅「故障全组重启+checkpoint」；弹性适合云上扩缩容。

---

## 记忆要点

1. 容错 = checkpoint + 可恢复 dataloader/RNG + 一致恢复。
2. Elastic = 动态 worker 数 + rendezvous + checkpoint + 数据重分片。
3. 协调器、一致 checkpoint、新 world_size 下的 sampler 是关键。

[返回模块](./README.md) | [返回总览](../README.md)
