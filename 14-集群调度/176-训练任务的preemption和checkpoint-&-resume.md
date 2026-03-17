# 第 176 题：训练任务的`preemption`和`checkpoint & resume`？

## 题目

训练任务的`preemption`和`checkpoint & resume`？

---

## 完整讲解

### 一、Preemption（抢占）

**抢占**：高优先级任务需要资源时，调度器可**终止或驱逐**低优先级任务、回收其资源后再调度高优任务。被抢占的作业若未做 checkpoint 会丢失进度；因此训练任务需要**周期性 checkpoint** 并在被抢占后能**从最新 checkpoint 恢复**。

### 二、Checkpoint & Resume

**Checkpoint**：训练过程中定期将**模型参数、优化器状态、步数、随机数状态**等写入存储（分布式时各 rank 写分片或汇总）。**Resume**：重新提交作业时，从存储**加载 checkpoint**，恢复 step 与状态，继续训练。这样被抢占或故障后只需「重新排队、重新调度」，从断点续训，不重头跑。

### 三、工程要点

调度侧：Volcano/K8s 的 **preemption** 会发 SIGTERM 或 evict；训练框架需**捕获信号**、写完当前 checkpoint 再退出，或依赖已有周期 checkpoint。存储：checkpoint 存共享存储（如 NFS、对象存储）以便任意节点恢复。作业描述中需带「checkpoint 路径、step」等，重提时由启动脚本或平台自动加载并 resume。
---

## 面试要点

- 抢占下低优任务被终止；训练必须依赖周期 checkpoint 与 resume 避免进度丢失。
- Checkpoint 含模型、优化器、step、RNG；存共享存储；resume 时加载后继续训练。
- 框架需处理 SIGTERM/evict，写完 checkpoint 再退；重提作业时自动指定 checkpoint 路径并 resume。

---

## 记忆要点

1. Preemption = 高优抢低优资源；被抢占任务会中断。
2. Checkpoint = 周期保存状态；Resume = 从 checkpoint 恢复继续训。
3. 共享存储存 checkpoint；重提时加载并 resume。

[返回模块](./README.md) | [返回总览](../README.md)
