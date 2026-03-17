# 第 173 题：训练任务的`gang scheduling`？`PyTorchJob`的`operator`？

## 题目

训练任务的`gang scheduling`？`PyTorchJob`的`operator`？

---

## 完整讲解

### 一、Gang scheduling 的含义

**Gang scheduling**：一组进程/ Pod **要么全部同时调度运行，要么都不运行**。分布式训练中多个 worker 若只部分启动，先起的会等未起的或超时失败，造成资源空占与死锁；因此需要「凑齐 N 个再一起跑」。

### 二、实现方式

**Volcano**：通过 **PodGroup** CRD 将多个 Pod 归为一组，设 **minAvailable**；调度器只有在能一次性满足 minAvailable 时才调度该组，否则不调度其中任何 Pod。**Slurm**：对 MPI/多节点作业本身即「一起分配节点再启动」，天然 gang。**K8s 默认 scheduler**：无原生 gang 语义，可配合 **KubeBatch**（已并入 Volcano 思路）或自研 **scheduler plugin** 实现「预留 + 一次性绑定」。

### 三、PyTorchJob 与 Operator

**PyTorchJob** 是 Kubeflow 的 CRD，定义 Master/Worker 的 replica 数与镜像、命令等；**Operator** 根据 spec 创建对应 Deployment/ReplicaSet 或裸 Pod，并注入环境变量（RANK、WORLD_SIZE 等）。调度由 K8s/Volcano 完成；Operator 不负责「凑齐再跑」，需集群提供 gang 调度（如 Volcano PodGroup）。Operator 还负责状态同步、失败重试、与 ML 元数据集成等。
---

## 面试要点

- Gang scheduling：一组 Pod 全有或全无，避免分布式训练部分起、部分等导致的死锁与空占。
- Volcano 用 PodGroup + minAvailable 实现；Slurm 多节点作业天然 gang；K8s 默认需插件或 Volcano。
- PyTorchJob Operator 负责生成 Pod 与注入 rank；调度策略由 Volcano/kube-scheduler 执行。

---

## 记忆要点

1. Gang = 全起或不起；训练多 worker 必须同时就绪。
2. Volcano：PodGroup、minAvailable；K8s 需 Volcano 或等价插件。
3. PyTorchJob Operator 管 Pod 编排与 rank；调度器管 gang 与资源。

[返回模块](./README.md) | [返回总览](../README.md)
