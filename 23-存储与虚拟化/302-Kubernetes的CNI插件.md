# 第 302 题：Kubernetes的`CNI`插件？`Calico`、`Cilium`？

## 题目

Kubernetes的`CNI`插件？`Calico`、`Cilium`？

---

## 完整讲解

### 一、CNI 作用

**CNI**（Container Network Interface）是 Kubernetes 的**网络插件接口**：kubelet 在创建/删除 Pod 时调用配置好的 CNI 插件，为 Pod 配置**网络命名空间**（网卡、IP、路由、与集群/外网互通等）。插件以二进制或脚本形式存在，通过 stdin 接收配置、通过 stdout 返回结果。

### 二、Calico

**Calico**：基于 **BGP** 或 **overlay**（VxLAN 等）的**三层网络**方案，每 Pod 有独立 IP、可做**网络策略**（NetworkPolicy）、支持 eBPF 数据面。适合**大规模、需策略与可观测**的集群；可纯 BGP 与底层网络集成、无 overlay 封装，性能好。常用于生产、混合云与多集群。

### 三、Cilium

**Cilium**：基于 **eBPF** 的 CNI，**内核态**实现转发、负载均衡、策略、可观测（替代 iptables 与部分 kube-proxy）。支持 **Hubble** 观测、**多集群**、**服务网格** 等高级能力。适合**高性能、可观测与安全**需求；对内核版本有要求。与 Calico 相比：都支持 NetworkPolicy 与高性能；Cilium 更偏 eBPF 与可观测、Calico 更成熟于 BGP 与策略。

---

## 面试要点

- CNI = K8s 网络插件接口；Pod 创建/删除时配置网络命名空间。
- Calico：BGP 或 overlay、NetworkPolicy、可 eBPF；适合大规模与策略。
- Cilium：eBPF 驱动、可观测（Hubble）、服务网格；高性能与可观测。
- 选型看规模、策略需求、是否要 eBPF 与可观测。

---

## 记忆要点

1. CNI = 插件接口；为 Pod 配网卡、IP、路由。
2. Calico = BGP/overlay、策略；Cilium = eBPF、可观测。
3. 二者都支持高性能与策略；Cilium 偏 eBPF 与可观测。

[返回模块](./README.md) | [返回总览](../README.md)
