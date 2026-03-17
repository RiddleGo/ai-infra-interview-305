# 第 99 题：ONNX Runtime的`execution provider`有哪些？`CUDA`、`TensorRT`、`Dire…

## 题目

ONNX Runtime的`execution provider`有哪些？`CUDA`、`TensorRT`、`DirectML`？

---

## 完整讲解

### 一、Execution Provider（EP）的作用

ONNX Runtime 的 **Execution Provider** 把算子在**不同后端**上执行：CPU、CUDA、TensorRT、DirectML 等。同一 ONNX 模型可切换 EP，在 GPU/CPU/不同框架间选择，无需改模型。

### 二、常见 EP

- **CPU**：默认，跨平台，无 GPU 依赖；适合小模型或无 GPU 环境。
- **CUDA**：NVIDIA GPU，用 cuDNN/cuBLAS；延迟与吞吐优于 CPU，需 CUDA 环境。
- **TensorRT**：将子图或整图交给 TensorRT 优化执行，在 NVIDIA 上往往比纯 CUDA EP 更快；需 TensorRT 库，build 可能较慢。
- **DirectML**：Windows 上利用 DirectX 12 与多种 GPU（NVIDIA/AMD/Intel），跨厂商；适合 Windows 部署。
- **CoreML**（Apple）、**OpenVINO**（Intel）、**NNAPI**（Android）等：针对特定平台。选择时按部署环境与性能需求选；多 EP 可组合（如 CUDA + TensorRT，部分 op  fallback）。

### 三、使用方式

创建 session 时指定 provider 列表：`ort.InferenceSession(model_path, providers=['TensorRTExecutionProvider', 'CUDAExecutionProvider', 'CPUExecutionProvider'])`；按序 fallback：先试 TensorRT，再 CUDA，再 CPU。可传 EP 专属选项（如 TensorRT 的 fp16、cache 路径）。

---

## 面试要点

- EP = 执行后端；常见有 CPU、CUDA、TensorRT、DirectML、CoreML、OpenVINO 等。
- GPU 上常用 CUDA 或 TensorRT；Windows 多 GPU 可用 DirectML；按平台与性能选。
- Session 指定 providers 列表，按序 fallback；可传各 EP 的选项。

---

## 记忆要点

1. EP = 后端；CPU/CUDA/TensorRT/DirectML 等。
2. GPU 首选 CUDA 或 TensorRT；TensorRT 更优但依赖重。
3. providers 列表决定优先级与 fallback。

[返回模块](./README.md) | [返回总览](../README.md)
