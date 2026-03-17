# 第 237 题：推理服务的`auto-scaling`策略？`HPA`、`VPA`、`KEDA`？

## 题目

推理服务的`auto-scaling`策略？`HPA`、`VPA`、`KEDA`？

---

## 完整讲解

### 一、Auto-scaling 目标

**自动扩缩容**：根据 **负载**（QPS、队列深度、延迟）**自动增加或减少** 推理实例数，在 **保证 SLA** 前提下 **控制成本**。负载高时扩容减排队与延迟；负载低时缩容省资源。

### 二、HPA、VPA、KEDA

**HPA**（Horizontal Pod Autoscaler）：K8s 原生，按 **CPU/内存** 或 **自定义 metric**（如 QPS、请求数）**水平** 扩缩 **Pod 副本数**。需 **metrics-server** 或 **custom metrics adapter**（如 Prometheus adapter）提供 QPS 等；**target** 设为「平均每 Pod 的 QPS 或利用率」。**VPA**（Vertical Pod Autoscaler）：**垂直** 调整 **单 Pod 的 request/limit**（CPU、内存），适合「单实例规格不固定」；推理场景更常用 **HPA** 做副本数伸缩。**KEDA**：基于 **Kubernetes Event-Driven Autoscaling**，用 **多种 trigger**（队列长度、Prometheus、HTTP 等）驱动扩缩容；**从 0 扩到 N** 支持好，适合 **队列消费、定时或事件触发** 的推理与批处理。

### 三、策略与注意

**指标**：推理常用 **QPS、队列深度、P99 延迟** 作为 scale 依据；**多指标** 可设「满足任一即扩容」。**冷却与预热**：扩容后 **warmup** 再接流量（模型加载、编译）；缩容前 **cooldown** 避免抖动。**最小/最大副本** 与 **资源 quota** 防止过度扩缩。
---

## 面试要点

- Auto-scaling：按负载扩缩实例；HPA 水平扩缩副本、VPA 垂直调单 Pod 资源、KEDA 事件驱动。
- 推理常用 HPA/KEDA；指标：QPS、队列、P99；custom metrics 或 Prometheus adapter。
- 预热与冷却；最小/最大副本与 quota。

---

## 记忆要点

1. HPA = 水平扩副本；VPA = 垂直调资源；KEDA = 事件驱动、可缩到 0。
2. 推理指标：QPS、队列、P99；warmup、cooldown。
3. 多指标、min/max、quota。

[返回模块](./README.md) | [返回总览](../README.md)
