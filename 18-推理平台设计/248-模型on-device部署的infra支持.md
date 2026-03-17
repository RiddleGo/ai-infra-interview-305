# 第 248 题：模型`on-device`部署的infra支持？`Core ML`、`TFLite`？

## 题目

模型`on-device`部署的infra支持？`Core ML`、`TFLite`？

---

## 完整讲解

### 一、On-device 部署场景

**On-device**：模型在 **端侧**（手机、IoT、边缘盒子）运行，**低延迟、隐私、离线**。**Infra 支持**：**模型转换与下发**、**版本与兼容**、**监控与更新**；与 **云端推理** 形成「云+端」协同。

### 二、Core ML、TFLite

**Core ML**（Apple）：**iOS/macOS** 上推理框架；模型需 **转换为 Core ML 格式**（.mlmodel）；支持 **Neural Engine、GPU、CPU**。**工具链**：从 PyTorch/ONNX 等 **导出 → 转 Core ML**；平台可提供 **转换流水线**（如 ONNX → Core ML）、**量化与优化**、**版本与下发**（通过 App 更新或 MDM）。**TFLite**（TensorFlow Lite）：**Android、嵌入式** 常用；模型为 **.tflite**；支持 **GPU delegate、NNAPI、Hexagon** 等。**转换**：TF/Keras 或 **TF 兼容** 模型 → TFLite；**量化、剪枝** 在转换时可选。**平台**：**模型仓库** 存 **多端格式**（ONNX、TFLite、Core ML）；**CI** 在训练/导出后 **自动转** 各端格式并做 **兼容与性能测试**；**OTA/MDM** 或 **应用市场** 下发。

### 三、统一与迭代

**一次训练、多端部署**：**统一** 导出 **ONNX** 或 **IR**，再 **分别转** Core ML、TFLite、MNN 等；**平台** 管理「一模型多格式」的 **版本与血缘**。**迭代**：端侧 **上报** 性能与崩溃；**A/B 与灰度** 控制新模型下发比例。
---

## 面试要点

- On-device：端侧推理；infra 支持 = 转换、下发、版本、监控。
- Core ML：iOS/macOS、.mlmodel、从 ONNX 等转；TFLite：Android/嵌入式、.tflite、delegate。
- 平台：多端格式、转换流水线、版本与下发；一次训练多端部署。

---

## 记忆要点

1. On-device = 端侧；Core ML = Apple；TFLite = Android/嵌入式。
2. 转换流水线、多端格式、版本管理。
3. 一次训练多端；OTA/MDM 下发。

[返回模块](./README.md) | [返回总览](../README.md)
