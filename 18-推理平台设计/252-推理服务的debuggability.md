# 第 252 题：推理服务的`debuggability`？`request tracing`、`model versioning`？

## 题目

推理服务的`debuggability`？`request tracing`、`model versioning`？

---

## 完整讲解

### 一、Debuggability 需求

**可调试性**：**请求失败或延迟异常** 时，能 **快速定位** 是模型、数据、实例还是网络问题；**模型版本与配置** 可追溯；**单请求** 的 **完整路径** 可复现与分析。

### 二、Request tracing

**Tracing**：为每个请求分配 **trace_id**（或沿用上游），在 **网关、推理服务、下游** 间 **透传**；各环节 **打 span**（开始、结束、标签）。**排查**：按 **trace_id** 查 **整条链路**— 排队、调度、哪台实例、模型加载、推理各阶段耗时、是否超时或错误。**实现**：**OpenTelemetry** 等标准；**日志** 与 **指标** 带 trace_id，便于关联。**与 SLO**：P99 差时，**取 P99 对应 trace** 看瓶颈在排队、某层、还是网络。

### 三、Model versioning

**版本管理**：每次部署带 **模型版本**（如 digest、tag）；**请求** 可带「期望版本」或 **路由到指定版本**。**排查**：**错误或掉点** 时确认 **实际调用的版本**；**回滚** 到上一版本对比；**血缘** 记录版本对应的训练 job、数据与配置。**平台**：**模型仓库** 存版本与元数据；**推理** 上报「请求 → 模型版本」；**debug 界面** 支持按版本查指标与 trace。
---

## 面试要点

- Debuggability：请求失败/延迟异常可定位；request tracing + model versioning。
- Tracing：trace_id 透传、span 打点；按 trace_id 查链路、定位瓶颈与错误。
- Model versioning：请求与版本关联、回滚与血缘；平台存版本、推理上报版本。

---

## 记忆要点

1. Debug = tracing + versioning。
2. trace_id、span、整条链路可查。
3. 版本与请求关联、回滚、血缘。

[返回模块](./README.md) | [返回总览](../README.md)
