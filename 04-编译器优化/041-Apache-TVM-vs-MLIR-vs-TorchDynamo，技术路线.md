# 第 41 题：Apache TVM vs MLIR vs TorchDynamo，技术路线差异？

## 题目

Apache TVM vs MLIR vs TorchDynamo，技术路线差异？

---

## 完整讲解

### 一、Apache TVM

**TVM** 是 **端到端深度学习编译器**：从 **Relay（高层计算图）或 TensorIR** 经 **调度与优化**（auto-schedule 如 MetaSchedule、手写 schedule）到 **TIR**，再 **codegen** 到 LLVM/CUDA/Metal 等。特点：**以性能为导向**、**搜索/模板** 做算子级优化、**多后端**（CPU/GPU/NPU）；偏「从图到可执行」的完整栈，IR 自成一系（Relay、TIR），与 PyTorch/TF 通过 **前端导入**（ONNX、TorchScript 等）连接。

### 二、MLIR

**MLIR** 是 **多级 IR 与基础设施**：不绑死某一前端或后端，提供 **Dialect、Operation、Pass** 抽象，让不同项目定义自己的 dialect 并 **渐进 lowering**。TensorFlow、IREE、TPU 等都用 MLIR；PyTorch 的 LTC 也可用 MLIR。特点：**可扩展、可复用**、强调「层与层之间的接口」；偏 **编译器基础设施**，具体「怎么从 PyTorch 到 GPU」由上层项目（如 Torch-MLIR、IREE）完成。

### 三、TorchDynamo

**TorchDynamo** 是 PyTorch 2 的 **图捕获机制**：通过 **CPython 帧的 bytecode 与 guard**，在 **运行时** 追踪执行、重建计算图（FX graph），再交给 **后端**（如 Inductor、ONNX、或自定义）编译。特点：**不改用户代码**（装饰器或默认开启）、**按需编译、guard 失效则重捕获**；偏 **捕获与兼容**，与 **Inductor** 组合成「Dynamo 捕获 → Inductor 编译」的 PyTorch 2 默认路径。

### 四、技术路线差异简表

| 维度     | TVM           | MLIR              | TorchDynamo      |
|----------|----------------|-------------------|------------------|
| 定位     | 端到端编译器   | 多级 IR 基础设施  | 图捕获与分发     |
| 前端     | Relay/TensorIR、ONNX 等 | 各项目自定     | PyTorch 运行时   |
| 优化     | Schedule、AutoTVM/MetaSchedule | Pass、各 dialect | 交给后端（如 Inductor） |
| 后端     | LLVM/CUDA 等   | 多后端、可接 LLVM | Inductor/ONNX 等 |

---

## 面试要点

- TVM：端到端编译器，Relay/TensorIR → schedule → TIR → codegen；多后端、重搜索与性能。
- MLIR：多级 IR 框架，dialect/pass 可扩展；各项目在其上建前端与后端；偏基础设施。
- TorchDynamo：PyTorch 图捕获（bytecode+guard），不绑死后端；常与 Inductor 搭配。

---

## 记忆要点

1. TVM = 端到端编译栈，自研 IR + schedule + codegen；MLIR = 多级 IR 基础设施，可扩展。
2. Dynamo = 捕获图，后端可换；TVM/MLIR 偏「编译与优化」本身。
3. 组合关系：Dynamo 可把图交给 ONNX/Torch-MLIR 等；TVM 可接 ONNX；MLIR 可作 TVM 或 PyTorch 的中间层。

[返回模块](./README.md) | [返回总览](../README.md)
