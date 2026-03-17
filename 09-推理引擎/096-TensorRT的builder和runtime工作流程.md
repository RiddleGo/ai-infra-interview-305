# 第 96 题：TensorRT的`builder`和`runtime`工作流程？`plan`文件包含什么？

## 题目

TensorRT的`builder`和`runtime`工作流程？`plan`文件包含什么？

---

## 完整讲解

### 一、Builder 阶段

**Builder**：读入模型（ONNX、Caffe、或 TensorRT API 构建），做**图优化**（层融合、精度校准、kernel 选择、显存规划等），输出 **Engine**（即优化后的可执行计划）。Builder 通常离线、较慢，会尝试多种 kernel 与精度组合（如 fp16、int8），生成针对目标 GPU 的最优执行计划。

### 二、Runtime 阶段

**Runtime**：加载已构建好的 **Engine**（或从 plan 反序列化），在目标设备上**执行** inference。Runtime 轻量、无优化开销，适合部署时反复执行；可多线程/多 stream 并发执行同一 engine。

### 三、Plan 文件

**Plan**：序列化后的 Engine，包含 **优化后的网络结构**、**kernel 选择**、**显存分配**、**精度与 calibration 信息**（若 int8）等；不含原始权重路径，权重通常单独存或在 engine 内嵌。同一 plan 可在**同架构同 GPU** 上直接加载；换 GPU 或驱动大版本升级建议重 build。流程：Builder 生成 Engine → 序列化写 plan → 部署时 Runtime 读 plan → 反序列化执行。

---

## 面试要点

- Builder：图优化、kernel 选择、生成 Engine；Runtime：加载 Engine 执行。
- Plan = 序列化 Engine，含结构、kernel、显存与精度信息；部署用 Runtime + plan。
- Builder 离线、Runtime 在线；同架构可复用 plan，换 GPU 建议重 build。

---

## 记忆要点

1. Builder 建 Engine，Runtime 跑 Engine；plan = 序列化 Engine。
2. Plan 含结构、kernel、显存；权重可内嵌或单独。
3. 同卡复用 plan；换卡/换驱动重 build。

[返回模块](./README.md) | [返回总览](../README.md)
