# 第 134 题：`Kubernetes` + `NVIDIA GPU Operator`的部署经验？

## 题目

`Kubernetes` + `NVIDIA GPU Operator`的部署经验？

---

## 完整讲解

### 一、K8s + GPU 的痛点与 Operator

K8s 默认不识别 GPU，需安装驱动、CUDA、设备插件等，并正确配置 `resources.limits.nvidia.com/gpu`。**NVIDIA GPU Operator** 把 GPU 相关组件的安装与生命周期自动化：在集群中部署 Operator 后，它会在有 GPU 的节点上安装 NVIDIA 驱动（或依赖节点已有驱动）、container toolkit、device plugin、DCGM exporter 等，并通过 **NodeFeatureDiscovery** 等给节点打标签，便于用 nodeSelector 调度到 GPU 节点。

### 二、部署经验要点

（1）节点准备：若用 Operator 管理驱动，需满足其要求的 OS 与内核；否则预装驱动再让 Operator 只装 toolkit 与 plugin。（2）资源声明：Pod 中 `limits.nvidia.com/gpu: 1` 等，request 通常与 limit 同以保证独占。（3）调度：用 nodeSelector/taint/toleration 把推理或训练任务固定到 GPU 节点。（4）监控：Operator 可选装 DCGM、Prometheus 指标，便于看显存与利用率。（5）多卡与 MIG：多卡节点可配 MIG 或按卡数分片部署；升级与故障时注意 driver 与 CUDA 版本兼容。

### 三、常见问题

镜像需带 CUDA 与对应 cuDNN；K8s 与 driver 版本要匹配；OOM 或 device 未找到时查 device plugin 日志与节点条件。

---

## 面试要点

- GPU Operator 自动化：驱动（可选）、container toolkit、device plugin、监控等，并给节点打 GPU 相关标签。
- 部署：节点满足 OS/驱动要求；Pod 声明 limits.nvidia.com/gpu；用 nodeSelector/taint 调度；可选 DCGM 监控。
- 注意镜像 CUDA 版本、driver 与 K8s 兼容；多卡/MIG 按需配置。

---

## 记忆要点

1. GPU Operator = 自动装驱动/toolkit/device plugin + 节点标签，便于调度。
2. Pod 声明 limits.nvidia.com/gpu；调度靠 nodeSelector/taint。
3. 镜像带 CUDA；版本兼容；多卡/MIG 按需。

[返回模块](./README.md) | [返回总览](../README.md)
