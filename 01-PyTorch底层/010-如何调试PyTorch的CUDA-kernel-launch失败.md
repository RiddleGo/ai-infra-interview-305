# 第 10 题：如何调试PyTorch的CUDA kernel launch失败？`CUDA_LAUNCH_BLOCKING=1`的原理？

## 题目

如何调试PyTorch的CUDA kernel launch失败？`CUDA_LAUNCH_BLOCKING=1`的原理？

---

## 完整讲解

### 一、CUDA kernel「launch 失败」常见原因

- **显存不足**：分配失败或碎片导致大块分配不到。
- **参数错误**：grid/block 维度不合法（如 0、超过硬件限制）、shared memory 超限。
- **异步性**：默认 kernel 是**异步发射**的，报错可能出现在**后面某次 sync** 时，堆栈指向 sync 而不是真正出错的 kernel，难以定位。
- **设备不匹配**：在错误 device 上 launch 或 pointer 指向错误设备内存。

---

### 二、CUDA_LAUNCH_BLOCKING=1 在干什么？

设置环境变量 **`CUDA_LAUNCH_BLOCKING=1`** 后，**每次 kernel launch 都会变成同步**：driver 会等这个 kernel 执行完再返回，且一旦 kernel 内部出错，报错会**立刻**发生在对应的 launch 调用处，而不是等到后面的 `cudaDeviceSynchronize()` 或下一次同步点。这样：

- **堆栈**会指向真正触发错误的那个 API 调用（如某次 `tensor.add_` 或自定义 kernel）。
- **顺序**与代码顺序一致，不会因为异步执行而「错位」。

代价是 **GPU 和 CPU 无法并行**，整体变慢，所以**只用于调试**，生产环境不要开。

---

### 三、调试步骤建议

1. **先开 CUDA_LAUNCH_BLOCKING=1**：`export CUDA_LAUNCH_BLOCKING=1`（或 Windows 下在环境变量里设），再跑，看报错堆栈指向哪一行、哪个 op。
2. **看完整错误信息**：CUDA 会报 error code（如 invalid configuration、out of memory）；对照文档判断是显存、配置还是设备问题。
3. **缩小范围**：若报错指向某一大段，可注释掉部分代码或减小 batch/shape，确认是哪个 tensor 或哪次 launch 导致。
4. **显存**：用 `torch.cuda.memory_summary()`、`nvidia-smi` 看是否 OOM 或碎片；可先减小模型/ batch 验证。
5. **自定义 kernel**：检查 grid/block、shared memory、是否在正确 device；用 cuda-memcheck 或 compute-sanitizer 查越界和非法访问。

---

### 四、其他常用手段

- **CUDA_LAUNCH_BLOCKING=1**：同步 launch，精确定位出错 kernel（如上）。
- **TORCH_SHOW_CPP_STACKTRACES=1**：让 PyTorch 打印 C++ 堆栈，便于看到是哪个 ATen op。
- **cuda-gdb / Nsight Compute**：单步调试或 profile 某个 kernel，看寄存器、shared memory、越界。
- **compute-sanitizer**：查内存越界、未初始化等。

---

## 面试要点

- CUDA 默认异步 launch，错误可能延迟到后面 sync 才报，堆栈不对应真正出错的 kernel。
- CUDA_LAUNCH_BLOCKING=1：每次 launch 同步执行，错误立刻报在对应 launch 处，便于定位；会丧失 CPU-GPU 并行，仅调试用。
- 调试流程：开 blocking → 看堆栈和 error code → 缩范围、查显存/配置/自定义 kernel 参数。

---

## 记忆要点

1. launch 失败常见：OOM、grid/block 非法、异步导致报错位置滞后。
2. CUDA_LAUNCH_BLOCKING=1 = 同步 launch，错误立刻落在正确调用点；仅调试用。
3. 配合 TORCH_SHOW_CPP_STACKTRACES、memory_summary、cuda-gdb 等缩小范围。

[返回模块](./README.md) | [返回总览](../README.md)
