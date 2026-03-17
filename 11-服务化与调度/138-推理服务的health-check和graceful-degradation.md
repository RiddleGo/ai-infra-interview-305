# 第 138 题：推理服务的`health check`和`graceful degradation`？

## 题目

推理服务的`health check`和`graceful degradation`？

---

## 完整讲解

### 一、Health Check

**Health check**：外部或负载均衡定期探测服务是否存活、是否可接受请求。常见：**Liveness**（进程是否在、端口是否监听）：失败则重启实例；**Readiness**（是否就绪接流）：模型是否加载完、是否过载，失败则从 LB 摘除、不再分新流量。实现方式：HTTP 指定 path（如 `/health`、`/ready`）返回 200 或 503；或 gRPC health 协议。探测频率与超时要合理，避免误判；GPU 推理可在 ready 中加「模型加载完成」与可选「显存可用」检查。

### 二、Graceful Degradation

**Graceful degradation**：在部分故障或过载时**降级**而非直接挂掉。策略包括：**限流**：超 QPS 时返回 429 或排队；**降级响应**：超时或错误时返回缓存、默认回复或简化模型结果；**关闭部分功能**：如关闭重排序、只用检索结果；**实例级**：单实例异常时由 LB 摘除，其他实例继续服务。目标是在部分失败下尽量保证可用性与用户体验，并配合告警与自动恢复。

### 三、工程要点

Health 与 LB、K8s readiness/liveness 配合；降级策略可配置（开关、阈值）；监控记录 5xx、超时、降级次数，便于定位与容量规划。

---

## 面试要点

- Health check：Liveness（存活/重启）、Readiness（就绪/摘流）；HTTP 或 gRPC health；可含模型加载与显存检查。
- Graceful degradation：限流、超时降级（缓存/默认/简化）、关部分功能、实例摘除；保证部分故障时仍可用。
- 与 LB、K8s 配合；降级策略可配置；监控 5xx、超时、降级次数。

---

## 记忆要点

1. Health = liveness（重启）+ readiness（摘流）；就绪可含模型与显存。
2. 降级 = 限流、超时降级、关功能、摘实例；目标部分故障仍可用。
3. 配合 LB/K8s；可配置；监控必备。

[返回模块](./README.md) | [返回总览](../README.md)
