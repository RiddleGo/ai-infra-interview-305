# 第 21 题：用CUDA写一个简单的vector add，如何绑定到Python？

## 题目

用CUDA写一个简单的vector add，如何绑定到Python？

---

## 完整讲解

### 一、CUDA vector add 怎么写？

用 CUDA 写 vector add：在 **kernel** 里每个线程负责若干元素（或一对一），从 global memory 读 `a[i]`、`b[i]`，写回 `c[i] = a[i] + b[i]`。注意 **grid/block 维度**：block 内线程数常取 256，grid 大小 = `(n + blockSize - 1) / blockSize`；kernel 内用 `blockIdx.x * blockDim.x + threadIdx.x` 得到全局下标，并加 **bounds check**（`if (i < n)`）防止越界。

### 二、如何暴露给 Python？

常见方式：**PyTorch C++ 扩展**（`torch.utils.cpp_extension`）、**pybind11 + 自己编译**、或 **CuPy/NumPy 的 C 扩展**。

- **PyTorch 扩展**：写 `.cu` 里 `__global__` kernel，在 `.cpp` 里用 `at::Tensor` 取 data ptr、调 CUDA kernel；用 `load_inline` 或 `load` 编译成 so，Python 里 `import torch.utils.cpp_extension; torch.ops.load_library(...)` 或通过 `torch.library.define` 注册，即可 `torch.ops.my_ns.vector_add(a, b)` 调用。
- **pybind11**：CUDA 分配/拷贝自己管，用 `py::array_t` 或 raw pointer 传进 Python；需在 C++ 侧做 host/device 拷贝，或接受已 in GPU 的 buffer（如从 CuPy 传过来）。

### 三、工程要点

- 编译依赖：CUDA toolkit、与当前 PyTorch 一致的 CUDA 版本；Windows 上需配 nvcc、PATH。
- 若要在 **Autograd** 里用，需再包一层 `torch.autograd.Function`，在 backward 里实现梯度（vector add 的梯度就是直传）。
- 小规模可先 CPU 或 `torch` 算子验证正确性，再对比 GPU 结果与性能。

---

## 面试要点

- CUDA kernel：grid/block、全局下标、bounds check；vector add 是 memory-bound，注意 coalesced 访问。
- 绑定 Python：PyTorch C++ 扩展（cpp_extension + at::Tensor）或 pybind11；扩展需正确链接 CUDA、与 PyTorch CUDA 版本一致。
- 要参与训练需用 `autograd.Function` 包装，backward 实现梯度并可选再调 kernel。

---

## 记忆要点

1. CUDA vector add：每线程算下标 `i`，读 a[i]、b[i]，写 c[i]；grid/block 覆盖 n，加 `i < n` 判断。
2. 绑 Python：PyTorch 扩展（.cu + .cpp，load_library）或 pybind11；at::Tensor 取 ptr 调 kernel。
3. 参与 Autograd 需包一层 Function，forward 调 kernel，backward 传梯度。

[返回模块](./README.md) | [返回总览](../README.md)
