# 第 267 题：`RAII`模式管理CUDA资源？`unique_ptr` with custom deleter？

## 题目

`RAII`模式管理CUDA资源？`unique_ptr` with custom deleter？

---

## 完整讲解

### 一、RAII 与 CUDA 资源

**RAII**（Resource Acquisition Is Initialization）：构造时获取资源、析构时释放，避免泄漏与重复释放。CUDA 资源如 device 指针、stream、event、context 等都应「谁创建谁释放」，用 RAII 封装可防止异常路径泄漏。

### 二、unique_ptr with custom deleter

`std::unique_ptr<T, Deleter>` 在析构时调用 `Deleter`。对 device 指针：`Deleter` 里调用 `cudaFree(ptr.get())`；对 stream：`cudaStreamDestroy`；对 event：`cudaEventDestroy`。定义 `using CudaPtr = std::unique_ptr<float, decltype(&cudaFree)>` 或写一个 functor 封装 cudaFree，即可 `CudaPtr p(ptr, cudaFree)`，出作用域自动释放。

### 三、工程经验

可封装成 `CudaDevicePtr<T>`、`CudaStream`、`CudaEvent` 等类，拷贝禁用、移动允许；与 STL 容器配合时注意 deleter 类型一致。避免 raw new/delete 与 cudaMalloc/cudaFree 混用导致的双重释放。

---

## 面试要点

- RAII：构造获取、析构释放；CUDA 指针/stream/event 都适合 RAII。
- unique_ptr + custom deleter：deleter 里 cudaFree/cudaStreamDestroy/cudaEventDestroy。
- 封装成 CudaDevicePtr/CudaStream 等，禁用拷贝、允许移动。
- 避免 raw 分配与手动 free 混用导致泄漏或双释。

---

## 记忆要点

1. RAII = 构造拿资源、析构放资源；CUDA 资源用 RAII 防泄漏。
2. unique_ptr<T, Deleter>，Deleter 里 cudaFree/StreamDestroy/EventDestroy。
3. 封装成类、禁用拷贝；与 STL 配合注意 deleter 类型。

[返回模块](./README.md) | [返回总览](../README.md)
