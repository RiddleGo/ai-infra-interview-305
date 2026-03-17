# 第 171 题：Slurm的`sbatch`脚本编写？`gres`资源申请？

## 题目

Slurm的`sbatch`脚本编写？`gres`资源申请？

---

## 完整讲解

### 一、sbatch 脚本结构

**sbatch** 是 Slurm 的批处理提交命令，脚本中通过 `#SBATCH`  directive 指定资源与行为。常用项：`--job-name`、`--partition`、`--nodes`/`--ntasks-per-node`、`--cpus-per-task`、`--time`、`--output`/`--error`；GPU 通过 **gres** 申请。脚本体为实际要执行的命令（如 `srun` 启动 MPI、或直接跑 Python）。

### 二、gres 资源申请

**gres**（Generic Resource）：在 Slurm 中表示 GPU、FPGA 等设备。典型写法：`#SBATCH --gres=gpu:2`（2 块任意 GPU）、`#SBATCH --gres=gpu:a100:4`（4 块 A100）。需集群配置 `GresTypes=gpu` 及每节点 `Gres=gpu:8` 等。申请后任务内通过 `CUDA_VISIBLE_DEVICES`（由 Slurm 自动设置）使用对应 GPU。

### 三、工程要点

脚本内用 `srun` 做多进程/多节点时，通常每个 task 对应一进程；配合 `--gres` 保证每进程可见的 GPU 与 task 绑定。超时用 `--time` 避免长占；大作业用 `--exclusive` 独占节点时可减少干扰。生产环境常把 partition、account、qos 等写进脚本或通过环境/模板注入。
---

## 面试要点

- sbatch 用 `#SBATCH` 指定 partition、nodes、cpus、time、output；GPU 用 `--gres=gpu[:type]:数量`。
- gres 需集群配置 GresTypes 与节点 Gres；任务内通过 CUDA_VISIBLE_DEVICES 使用 GPU。
- 多任务时 srun 与 gres 配合；可结合 --exclusive、--account、--qos 做资源与计费控制。

---

## 记忆要点

1. sbatch = 批处理脚本；#SBATCH 写资源，脚本体写执行命令。
2. gres=gpu:2 或 gres=gpu:a100:4；集群需配置 Gres。
3. 任务内用 CUDA_VISIBLE_DEVICES；srun 多任务时注意 GPU 与 task 绑定。

[返回模块](./README.md) | [返回总览](../README.md)
