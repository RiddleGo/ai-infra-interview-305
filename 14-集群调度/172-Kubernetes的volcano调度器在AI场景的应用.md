# 第 172 题：Kubernetes的`volcano`调度器在AI场景的应用？

## 题目

Kubernetes的`volcano`调度器在AI场景的应用？

---

## 完整讲解

### 一、Volcano 的定位

**Volcano** 是 Kubernetes 上面向**批处理与高性能计算**的调度器，支持 **gang scheduling**（一组 Pod 要么全调度成功要么不调度）、**队列与优先级**、**资源预留与抢占**等，弥补默认 kube-scheduler 对「多 Pod 协同、公平共享」支持不足的问题，适合 AI 训练、MPI 等 All-or-Nothing 作业。

### 二、AI 场景的应用

**Gang scheduling**：训练 job 的多个 worker Pod 必须同时就绪再一起跑，否则部分先起会挂起或死锁；Volcano 的 **PodGroup** 与 **minAvailable** 保证「凑齐再调度」。**队列**：按团队/项目设 queue，配合 **priorityClass** 与 **cap** 做公平与限流。**GPU 等扩展资源**：通过 CRD 或 device plugin 暴露 GPU，Volcano 按 request/limit 调度；可与 **NVIDIA K8s Device Plugin** 等配合。**抢占与回收**：高优任务可抢占低优，被抢占方可做 checkpoint 后重排。

### 三、与 PyTorchJob / Kubeflow 的关系

PyTorchJob 等 **CRD + controller** 负责生成 Pod、定义 role（master/worker）；**调度策略**由 Volcano（或 kube-scheduler）执行。通常集群启用 Volcano 作为调度器、为训练 Job 的 Pod 打 **schedulerName: volcano** 与 **PodGroup**，即可获得 gang 调度与队列能力。
---

## 面试要点

- Volcano 提供 gang scheduling（PodGroup/minAvailable）、队列、优先级与抢占，适合批处理与 AI 训练。
- AI 场景：多 worker 必须同时就绪；配合 GPU device plugin、队列与 priority 做资源与公平控制。
- PyTorchJob 等负责 Pod 编排，Volcano 负责调度；Pod 需指定 schedulerName 与 PodGroup。

---

## 记忆要点

1. Volcano = K8s 批处理调度器；gang、队列、抢占。
2. PodGroup + minAvailable 实现「全有或全无」调度。
3. 与 PyTorchJob/GPU plugin 配合；schedulerName: volcano。

[返回模块](./README.md) | [返回总览](../README.md)
