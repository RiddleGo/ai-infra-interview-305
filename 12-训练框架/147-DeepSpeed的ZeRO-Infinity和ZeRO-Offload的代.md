# 第 147 题：DeepSpeed的`ZeRO-Infinity`和`ZeRO-Offload`的代码入口？

## 题目

DeepSpeed的`ZeRO-Infinity`和`ZeRO-Offload`的代码入口？

---

## 完整讲解

### 一、ZeRO-Infinity 与 ZeRO-Offload 简述

**ZeRO-Offload**：把优化器状态与梯度 offload 到 CPU 内存，GPU 只保留参数与激活，用 CPU-GPU 异步拷贝与计算重叠，实现单卡或少量卡训练大模型。**ZeRO-Infinity**：在 Offload 基础上进一步把**参数**也 offload 到 CPU（或 NVMe），仅计算时按需把参数块换入 GPU，突破单机 GPU 显存上限，支持极大模型。

### 二、代码入口与关键模块

**DeepSpeed** 中与 ZeRO 相关的入口与配置：`deepspeed.initialize()` 时传入 `config` 中的 `zero_optimization`；其中 `stage` 3 表示 ZeRO-3（参数分片），`offload_optimizer`、`offload_param` 对应 CPU/NVMe offload。**代码路径**：`deepspeed/runtime/zero/` 下，`stage2.py`、`stage3.py` 等实现分片与通信；offload 逻辑在 `offload_config.py` 与 optimizer/parameter 的 CPU 侧管理；`partition_parameters.py`、`gather_parameters.py` 等实现参数的分片与 all-gather。查「ZeRO-Infinity」时可搜 `offload_param`、`infinity`；查「Offload」时可搜 `offload_optimizer`、`cpu_optimizer`。

### 三、使用方式

用户通过 `ds_config.json` 或 API 开启 `zero_optimization.stage=3`、`offload_optimizer`/`offload_param` 的 device 与 buffer 配置；训练脚本用 `deepspeed.initialize(model=..., config=...)` 即可，无需改模型结构，仅改配置与启动命令。

---

## 面试要点

- ZeRO-Offload = 优化器/梯度 offload 到 CPU；ZeRO-Infinity = 参数也 offload 到 CPU/NVMe，按需换入 GPU。
- 代码：deepspeed.initialize + zero_optimization 配置；deepseed/runtime/zero/ 下 stage2/3、offload 相关；offload_param、partition/gather 等。
- 使用：ds_config 里 stage、offload_optimizer、offload_param；无需改模型。

---

## 记忆要点

1. Offload = 优化器/梯度→CPU；Infinity = 参数→CPU/NVMe，按需换入。
2. 入口 = deepspeed.initialize + config；实现 = runtime/zero/ + offload 与 partition。
3. 配置 stage、offload_optimizer、offload_param 即可启用。

[返回模块](./README.md) | [返回总览](../README.md)
