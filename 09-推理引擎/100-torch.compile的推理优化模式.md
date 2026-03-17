# 第 100 题：`torch.compile`的推理优化模式？`reduce-overhead` vs `max-autotune`？

## 题目

`torch.compile`的推理优化模式？`reduce-overhead` vs `max-autotune`？

---

## 完整讲解

### 一、torch.compile 的推理模式

**torch.compile** 对模型做图捕获与优化（TorchDynamo + Inductor 等）。推理时可指定 **mode**：`mode="reduce-overhead"` 侧重降低 **Python 与调度开销**（如减少 Python 调用、融合 kernel）；`mode="max-autotune"` 侧重 **极致性能**，会做更多 kernel 搜索与选型，编译更慢、运行时更快。

### 二、reduce-overhead vs max-autotune

- **reduce-overhead**：优化目标 = 减少 **overhead**（Python、dispatch、小 kernel launch），适合 **batch 不大、推理延迟敏感** 的场景；编译较快，适合迭代与部署平衡。
- **max-autotune**：允许 **更激进的 autotune**（如更多 matmul/cuda 配置），编译时间长，适合 **离线编译、追求峰值吞吐或大 batch**；可能增加显存与编译时间。
- **默认**（无 mode 或 `mode="default"`）：介于两者之间。推理常用 **reduce-overhead** 做延迟优化，或 **max-autotune** 做吞吐优化；训练一般不用 max-autotune（编译与显存成本高）。

### 三、使用建议

- 推理延迟优先：`torch.compile(model, mode="reduce-overhead")`；大 batch 或离线优化：`mode="max-autotune"`。
- 需配合 `fullgraph=True`（若可行）减少 Python 回退；首次运行会编译，可做 warmup。

---

## 面试要点

- reduce-overhead：降 Python/调度开销，适合推理延迟；max-autotune：激进 kernel 搜索，适合吞吐、编译慢。
- 推理常用 reduce-overhead 或 max-autotune；默认介于两者之间。
- 配合 fullgraph、warmup 使用。

---

## 记忆要点

1. reduce-overhead = 低延迟、少 overhead；max-autotune = 高吞吐、慢编译。
2. 推理延迟用 reduce-overhead；吞吐用 max-autotune。
3. 首次运行编译，需 warmup。

[返回模块](./README.md) | [返回总览](../README.md)
