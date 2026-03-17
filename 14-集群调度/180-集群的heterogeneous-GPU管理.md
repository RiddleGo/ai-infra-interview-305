# 第 180 题：集群的`heterogeneous GPU`管理？`A100`、`H100`、`4090`混部？

## 题目

集群的`heterogeneous GPU`管理？`A100`、`H100`、`4090`混部？

---

## 完整讲解

### 一、Heterogeneous GPU 的挑战

**异构**：集群中同时存在 **A100、H100、4090** 等不同型号，算力、显存、NVLink 与驱动/库支持不同。**调度**：需识别每块卡的**类型与能力**，按任务需求（如「必须 A100 80G」「可接受 4090」）做**匹配与放置**；避免大模型任务被分到显存不足的卡、或混部导致驱动/CUDA 版本冲突。

### 二、资源抽象与标签

**设备插件**：NVIDIA K8s Device Plugin 等可暴露 **nvidia.com/gpu** 及扩展标签（如 **gpu-type=a100**、**memory=80Gi**）。Slurm 的 **gres** 可配置多种类型（如 `gpu:a100:2,gpu:h100:1`）。调度器按 **node label / resource request** 做筛选：例如 Pod 请求 `nvidia.com/gpu: 1` 且 nodeSelector `gpu-type=a100`，则只调度到 A100 节点。

### 三、混部策略

**分区**：按机型划分 partition 或 namespace，不同任务提交到不同分区，简单清晰。**统一池 + 选择**：所有 GPU 进一池，任务通过 **request/selector** 指定机型或「任意」；调度器做 binpack 或 spread。**驱动与镜像**：异构节点可能需不同驱动/CUDA 版本；用 **节点亲和 + 镜像 tag** 或统一基础镜像兼容多卡型，减少运维复杂度。
---

## 面试要点

- 异构 GPU：不同型号能力不同，调度需按类型与需求匹配（显存、算力、NVLink）。
- 通过 device plugin/label、gres 类型暴露卡型；request + nodeSelector 做筛选。
- 分区或统一池 + 选择；注意驱动与镜像兼容多卡型。

---

## 记忆要点

1. 异构 = 多型号混部；调度要类型感知与需求匹配。
2. 设备插件/label、gres 暴露类型；request + selector 选节点。
3. 分区或统一池；驱动与镜像需兼容。

[返回模块](./README.md) | [返回总览](../README.md)
