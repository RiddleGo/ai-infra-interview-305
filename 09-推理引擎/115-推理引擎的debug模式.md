# 第 115 题：推理引擎的`debug`模式？如何定位精度下降问题？

## 题目

推理引擎的`debug`模式？如何定位精度下降问题？

---

## 完整讲解

### 一、推理引擎的 Debug 模式

- **精度/数值**：以 **FP32 或高精度** 跑同一输入，与「优化/量化版本」逐层或逐 tensor 对比（**diff**），定位从哪一层开始误差变大；TensorRT/ONNX 等可关掉部分优化（如 fp16、int8）做 baseline。
- **Dump 与比对**：在关键层 **dump 输入输出**（FP32 与优化版），用脚本算 max/mean abs diff、相对误差；或导出 **ONNX** 用 ONNX Runtime 的 reference 实现对比。
- **逐层/逐 op**：在引擎中 **禁用融合** 或 **单 op 执行**，缩小范围；或用 **torch/ONNX 的逐层执行** 与引擎结果对比，找到第一个不一致的 op。
- **环境**：设置 **CUDA_LAUNCH_BLOCKING=1** 保证同步执行，便于复现与断点；或用 **cuda-gdb / Nsight** 做 GPU 侧调试。

### 二、精度下降的常见原因

- **FP16/INT8**：舍入与溢出；检查 **scale/calibration**、**clip 范围**；对比 FP32 baseline。
- **图优化/融合**：融合或改写导致等价性破坏（如 reassociation）；逐层关优化或对比中间结果。
- **Plugin 或自定义 op**：实现错误或与框架约定不一致；单独测 plugin、对比参考实现。
- **量化**：per-tensor vs per-channel、symmetric vs asymmetric；校准数据与真实分布不一致会掉点；用代表性数据重新 calibration 或提高精度档位。

### 三、定位流程

1. **确定 golden**：FP32 或 PyTorch/ONNX 高精度结果作为标准。  
2. **同输入** 跑优化引擎，逐层或按 block dump 对比，找到 **首次显著偏差** 的层/op。  
3. 对该层 **关优化、提精度、或替换为参考实现** 再测，确认是否该点导致。  
4. 若为量化，检查 **scale、校准集、量化配置**；若为融合，检查该融合的数学等价性。  
5. 修复后做 **回归测试**（多输入、多 shape），避免再次退化。

---

## 面试要点

- Debug 模式：高精度 baseline、dump 对比、逐层/逐 op 缩小范围、必要时 CUDA_LAUNCH_BLOCKING。
- 精度下降常见：FP16/INT8、图融合、plugin、量化配置与校准。
- 定位流程：golden → 同输入对比 → 找首次偏差层 → 单点修复 → 回归。

---

## 记忆要点

1. 用 FP32/高精度做 golden；dump 对比找首次偏差层。
2. 关优化、提精度、单 op 测试缩小范围。
3. 量化问题查 scale 与 calibration；融合问题查等价性。

[返回模块](./README.md) | [返回总览](../README.md)
