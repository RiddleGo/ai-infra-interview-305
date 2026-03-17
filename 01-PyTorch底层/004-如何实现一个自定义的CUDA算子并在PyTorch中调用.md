# 第 4 题：如何实现一个自定义的CUDA算子并在PyTorch中调用？详细步骤是什么？

## 题目

如何实现一个自定义的CUDA算子并在PyTorch中调用？详细步骤是什么？

---

## 完整讲解

### 一、整体流程概览

要在 PyTorch 里用上自定义 CUDA 算子，通常需要：**① 写 CUDA kernel** → **② 用 C++/pybind11 或 torch.library 做绑定并注册** → **③ 可选：实现 autograd 的 backward**。下面按「手写 C++ 扩展 + pybind11」和「torch.library」两条路说。

---

### 二、路线 A：C++ 扩展 + pybind11 + setuptools

1. **写 CUDA kernel**（`.cu`）：实现 `__global__` kernel，例如 `my_kernel<<<grid, block>>>(...)`。
2. **写 C++ 桥接**（`.cpp`）：用 ATen API 取 tensor 的 `data_ptr`、shape，分配输出，调 CUDA kernel（通过 `cudaLaunchKernel` 或把 kernel 包成函数指针）；处理 stream、device。
3. **pybind11 绑定**：在 C++ 里 `m.def("my_op", &my_op_impl, "my op");`，把函数暴露给 Python。
4. **setuptools 编译**：用 `torch.utils.cpp_extension.load` 或 `load_inline`，或写 `setup.py` 里 `CUDAExtension`，编译生成 `.so`。
5. **Python 调用**：`import torch; from my_extension import my_op; y = my_op(x)`。
6. **若要参与训练**：在 Python 侧用 `torch.autograd.Function` 包一层，`forward` 里调 `my_op`，`backward` 里写梯度公式并再调梯度 kernel 或 ATen 算子。

---

### 三、路线 B：torch.library（PyTorch 官方推荐方式）

1. **写 CUDA kernel**：同上，或先用 Triton 写再在 C++ 里调。
2. **在 C++ 里用 torch.library 注册**（或纯 Python 用 `torch.library.define` + `impl`）：
   - 定义算子名：`TORCH_LIBRARY_IMPL(..., CUDA, m) { m.impl("my_op", my_op_cuda_impl); }`
   - 实现 `my_op_cuda_impl`：取 tensor、调你的 kernel、返回结果。
3. **Python 侧**：`torch.ops.xxx.my_op(...)` 或先 `load_library("lib.so")` 再调；若需 autograd，用 `torch.library.autograd` 或自定义 `autograd.Function` 包一层。
4. **编译**：用 `torch.utils.cpp_extension.load` 或 CMake 生成带 CUDA 的 so，在 Python 里 `load_library` 加载。

这样算子会走 PyTorch 的 dispatch，和内置 op 一样参与设备选择、torch.compile 等。

---

### 四、关键注意点

- **设备与 stream**：在实现里用 `tensor.device()`、`at::cuda::getCurrentCUDAStream()` 等，保证在正确的 GPU 上、正确的 stream 上执行。
- **梯度**：若只做推理，可不实现 backward；若训练，必须提供梯度（自定义 backward kernel 或用 ATen 组合）。
- **数据类型与 shape**：C++ 里用 `tensor.scalar_type()`、`tensor.sizes()` 做校验与分支；支持多 dtype 时可模板化或按 dtype 分派。

---

## 面试要点

- 步骤概括：CUDA kernel → C++ 桥接（ATen 取指针、调 kernel）→ pybind11 或 torch.library 暴露 → 编译成 so → Python 调用；要训练再包一层 autograd.Function。
- torch.library 是官方推荐的扩展方式，算子会进 dispatch 体系；C++ 扩展 + pybind11 是传统方式，灵活但需自己管设备/stream。
- 能说清「forward 调我的 kernel、backward 写梯度并调梯度 kernel 或 ATen」即可。

---

## 记忆要点

1. 自定义 CUDA 算子 = CUDA kernel + C++ 桥接（ATen）+ 暴露（pybind11 或 torch.library）+ 编译 so；要 autograd 则用 Function 包装。
2. torch.library 注册后走 dispatch，和内置 op 一致；传统方式用 cpp_extension + pybind11。
3. 注意 device、stream、dtype/shape 与梯度实现。

[返回模块](./README.md) | [返回总览](../README.md)
