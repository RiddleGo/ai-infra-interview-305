# 第 177 题：集群的`utilization`监控？`Prometheus` + `Grafana`？

## 题目

集群的`utilization`监控？`Prometheus` + `Grafana`？

---

## 完整讲解

### 一、Utilization 指标

**集群利用率**：GPU/CPU 的**使用率**（如 nvidia-smi 的 GPU-Util、或基于 DCGM 的 SM 利用率）、**显存占用**、**节点/卡在线与空闲比例**等。高利用率表示资源被有效使用；长期低利用率说明空闲多、可做弹性或混部。需区分「分配率」（已分配/总资源）与「使用率」（实际算力/显存占用）。

### 二、Prometheus + Grafana

**Prometheus**：拉取并存储**时序指标**；通过 **exporter**（如 **DCGM Exporter** 暴露 GPU 指标、**node_exporter** 暴露节点 CPU/内存/磁盘）采集各节点与 GPU 的 utilization、memory、temperature 等。**Grafana**：连接 Prometheus 做**看板**：曲线图、单值、表格，按节点/作业/队列聚合，设告警阈值。典型面板：集群总 GPU 利用率、每节点利用率、每作业占用、排队时长、失败率等。

### 三、工程要点

调度器或作业系统可暴露「已分配/已使用」到 Prometheus；结合 **labels**（job_id、user、queue）做多维度查询与公平性分析。告警：利用率长期异常、节点故障、作业大量失败时触发；与工单或自动化恢复联动。
---

## 面试要点

- 利用率包括 GPU 算力利用率、显存占用、分配率；用于评估集群效率与容量。
- Prometheus 拉取 DCGM/node_exporter 等指标；Grafana 做看板与告警。
- 指标带 job/queue/user 等 label，便于按维度分析与做公平性/容量规划。

---

## 记忆要点

1. Utilization = 使用率/分配率；GPU 常用 DCGM、nvidia-smi 采集。
2. Prometheus 存时序；Grafana 画图与告警。
3. 多维度 label + 告警，支撑容量与公平性分析。

[返回模块](./README.md) | [返回总览](../README.md)
