# 第 98 题：TensorRT的`plugin`开发中，`IPluginV2DynamicExt`和`IPluginV2IOExt`区…

## 题目

TensorRT的`plugin`开发中，`IPluginV2DynamicExt`和`IPluginV2IOExt`区别？

---

## 完整讲解

### 一、IPluginV2 系列

TensorRT **plugin** 用于不支持或需自定义的算子。**IPluginV2** 为固定 shape；**IPluginV2Ext** 扩展了类型与 format；**IPluginV2DynamicExt** 与 **IPluginV2IOExt** 用于动态与 IO 扩展。

### 二、IPluginV2DynamicExt

**IPluginV2DynamicExt**：支持 **dynamic shape** 的 plugin。关键方法：`getOutputDimensions`、`configurePlugin` 根据输入维度推导输出维度与内部配置；`enqueue` 接收 runtime 的 actual shape，执行计算。用于 **输入/输出维在运行时变化** 的算子（如变长 seq、dynamic batch），需在 build 时通过 optimization profile 给范围。

### 三、IPluginV2IOExt

**IPluginV2IOExt**：扩展 **输入输出类型与 layout**（如 FP32/FP16/INT8、NCHW/NHWC），不强调 dynamic shape。用于需要**多精度或多 layout** 的 plugin，或与 IO 格式转换配合。若只需 dynamic shape，用 **IPluginV2DynamicExt**；若需丰富 IO 类型/layout，用 **IPluginV2IOExt** 或与 DynamicExt 组合（视 TensorRT 版本 API）。

### 四、对比小结

- **DynamicExt**：核心是 **动态维**；getOutputDimensions/configurePlugin 按输入维推导，enqueue 用 actual shape。
- **IOExt**：核心是 **类型与 layout**；支持多精度与格式。两者可同时继承（若 API 允许）或按需求二选一。

---

## 面试要点

- IPluginV2DynamicExt：支持 dynamic shape；getOutputDimensions/configurePlugin/enqueue 与运行时 shape 相关。
- IPluginV2IOExt：扩展 IO 类型与 layout（精度、NCHW 等），不强调动态维。
- 需要变长/变 batch 用 DynamicExt；需要多精度/格式用 IOExt。

---

## 记忆要点

1. DynamicExt = 动态 shape；IOExt = 多类型/layout。
2. Dynamic 需实现维度推导与 enqueue(actual shape)。
3. 按需求选或组合（视版本）。

[返回模块](./README.md) | [返回总览](../README.md)
