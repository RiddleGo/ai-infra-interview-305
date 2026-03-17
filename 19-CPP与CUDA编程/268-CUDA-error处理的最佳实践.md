# 第 268 题：`CUDA error`处理的最佳实践？`CUDA_CHECK`宏？

## 题目

`CUDA error`处理的最佳实践？`CUDA_CHECK`宏？

---

## 完整讲解

### 一、CUDA 错误返回方式

多数 CUDA API 返回 `cudaError_t`；kernel 启动**不阻塞**，错误在后续同步或下一次 API 调用时才可见。因此需要在**同步点或每次 API 调用后**检查返回值，否则错误可能被忽略或延迟发现。

### 二、CUDA_CHECK 宏

常用写法：`#define CUDA_CHECK(call) do { cudaError_t e = (call); if (e != cudaSuccess) { fprintf(stderr, "CUDA error %s at %s:%d\n", cudaGetErrorString(e), __FILE__, __LINE__); abort(); } } while(0)`。用法：`CUDA_CHECK(cudaMalloc(&p, n));`、`CUDA_CHECK(cudaStreamSynchronize(s));`。这样任意一次调用失败会立刻打印并终止，便于定位。

### 三、最佳实践

在 debug 构建中始终使用 CUDA_CHECK；kernel 后若有 sync，在 sync 处检查（因为 kernel 错误在 sync 时才报出）。可用 `cudaGetLastError()` 清除并获取上一次错误。Release 下可保留关键路径检查、或条件编译关闭以减开销。

---

## 面试要点

- CUDA API 返回 cudaError_t；kernel 异步，错误在同步或后续 API 才暴露。
- CUDA_CHECK 宏：调用 API、检查返回值、失败则打印 cudaGetErrorString 并 abort。
- Debug 下全程 CHECK；kernel 后在 sync 处检查；可用 cudaGetLastError 清除错误。
- Release 可只保留关键路径或条件编译。

---

## 记忆要点

1. 错误在同步/后续 API 暴露；用宏统一检查返回值。
2. CUDA_CHECK：call → 判 e != cudaSuccess → 打印 + abort。
3. kernel 后在 sync 处 CHECK；cudaGetLastError 可清错误。

[返回模块](./README.md) | [返回总览](../README.md)
