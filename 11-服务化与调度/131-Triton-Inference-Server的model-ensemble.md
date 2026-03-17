# 第 131 题：Triton Inference Server的`model ensemble`如何使用？

## 题目

Triton Inference Server的`model ensemble`如何使用？

---

## 完整讲解

### 一、Model Ensemble 是什么

Triton 的 **model ensemble** 把多个模型（或同一模型不同阶段）组成一个**推理流水线**：请求依次经过 A→B→C，前一个模型的输出作为后一个的输入，在 server 内部完成多步推理，对客户端暴露为**一个**模型接口。典型用途：预处理模型 + 主模型、主模型 + 后处理/重排序、多阶段检索+生成等。

### 二、如何使用

在 **config.pbtxt** 中定义 `ensemble_scheduling` 类型的模型，在 `ensemble_scheduling` 里声明 `step` 列表：每个 step 指定用哪个模型、输入来自上一 step 的哪几个输出、输出名到下一 step 的映射。输入/输出名需与各子模型的 config 一致。部署时各子模型需先单独加载（或作为 dependency 声明）；请求发往 ensemble 模型名，Triton 按 step 顺序调度、在 GPU/CPU 间传递中间 tensor。

### 三、注意点

Step 间数据在进程内传递，避免网络往返；可配置各 step 的 instance 数与设备。调试时先确保各子模型单独可调通，再组 ensemble；版本更新时需保证各子模型版本兼容（输入输出 shape/名一致）。

---

## 面试要点

- Ensemble = 多模型组成流水线 A→B→C，对客户端暴露为一个模型；用于预处理+主模型、多阶段生成等。
- 使用：config 里定义 ensemble 模型、声明 step 与各 step 的 model、输入输出映射；子模型先部署，请求发往 ensemble 名。
- 数据在进程内传递；注意子模型输入输出名与 shape 一致、版本兼容。

---

## 记忆要点

1. Ensemble = 多模型流水线，一步推理多阶段，对外一个接口。
2. 配置 = ensemble 类型 + step 列表（model、输入输出映射）；子模型先加载。
3. 进程内传中间结果；部署时保证各子模型 config 与版本兼容。

[返回模块](./README.md) | [返回总览](../README.md)
