# 第 35 题：TensorRT的plugin开发流程？如何支持dynamic shape？

## 题目

TensorRT的plugin开发流程？如何支持dynamic shape？

---

## 完整讲解

### 一、TensorRT Plugin 开发流程

**Plugin** 用于在 TensorRT 中实现 **不支持的 op** 或 **自定义融合**。流程要点：

- **定义 Plugin 类**：继承 `IPluginV2DynamicExt`（或 V2 的静态 shape 版本），实现 `getOutputDimensions`、`enqueue`、`configurePlugin`、`clone`、`serialize/deserialize` 等；**Dynamic** 版本支持运行时 shape。
- **注册**：通过 `REGISTER_TENSORRT_PLUGIN(MyPluginCreator)` 把 plugin 注册到 TensorRT，parser（ONNX 等）通过 **op 类型名** 或 **plugin 名** 找到并实例化。
- **与 ONNX 对接**：在 ONNX 里把自定义 op 的 **op_type** 写成 TRT 注册的 plugin 名，或使用 `trt.OnnxParser` 的 custom op 映射；必要时写 **ONNX 到 TRT 的转换**（把 ONNX 节点转成 Plugin 层）。
- **构建与运行**：`builder` 构建 engine 时会把对应节点建为 Plugin 层；`enqueue` 在推理时被调用，里层写 CUDA kernel 或调库。

### 二、如何支持 dynamic shape？

- **用 Dynamic 接口**：实现 `IPluginV2DynamicExt`，在 `getOutputDimensions` 里根据输入维度 **推导** 输出维度（可含 -1 或符号）；在 `configurePlugin` 里根据 min/max/opt profile 做准备（如选 kernel、分配 workspace）。
- **enqueue**：接收实际 `inputDims`、`outputDims`，根据 **当前 shape** 启动对应 kernel 或分支；若不同 shape 需不同实现，可在 plugin 内按 shape 分派。
- **Profile**：builder 阶段要设 **min/max/opt shape**，TRT 会为 dynamic 维度做优化或选 kernel；plugin 的 `configurePlugin` 会收到这些范围，可据此预分配或选策略。

### 三、注意点

- **序列化**：plugin 参数、类型要在 serialize 里写全，deserialize 时还原，否则 engine 跨进程/版本会失败。
- **线程安全**：clone 与多 context 并发要按 TRT 文档保证正确。
- **性能**：dynamic shape 下 TRT 可能为多 shape 生成多 kernel 或通用 kernel，plugin 内也可自己按 shape 选最优实现。

---

## 面试要点

- Plugin 流程：实现 IPluginV2DynamicExt（或 V2）、实现 getOutputDimensions/enqueue/configurePlugin/serialize；注册并和 ONNX op 对应。
- Dynamic shape：用 Dynamic 接口，getOutputDimensions 推导输出维；enqueue 按实际 shape 派发；设 min/max/opt profile。
- 序列化要完整；多 context 注意线程安全；dynamic 下可按 shape 选 kernel。

---

## 记忆要点

1. Plugin = 继承 IPluginV2DynamicExt，实现 getOutputDimensions、enqueue、configure、serialize；注册后 parser 可挂到图上。
2. Dynamic：输出维由输入维推导；enqueue 看实际 dims；builder 设 profile。
3. 序列化完整、线程安全；dynamic 时可按 shape 多分支实现。

[返回模块](./README.md) | [返回总览](../README.md)
