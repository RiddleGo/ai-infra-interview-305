# 第 56 题：DDP的`torchrun`和`mp.spawn`启动方式的区别？

## 题目

DDP的`torchrun`和`mp.spawn`启动方式的区别？

---

## 完整讲解

### 一、torchrun（推荐）

**torchrun**（原 `torch.distributed.launch`）是**单命令启动多进程**：在一台或多台机器上执行一次 `torchrun --nproc_per_node=4 --nnodes=2 ... train.py`，由 **torchrun 进程** fork 出多个 worker（每 node 4 个，共 8 个），每个 worker 里会设好 `RANK`、`WORLD_SIZE`、`MASTER_ADDR`、`MASTER_PORT` 等环境变量，然后执行 `train.py`。**不需要**在脚本里写 `spawn`，脚本只需在入口处 `init_process_group()` 并拿到 rank；**适合多机**：主节点指定 `--nnodes`、`--node_rank`，从节点用同样命令或通过 job 调度拿到相同 env 即可。

---

### 二、mp.spawn

**torch.multiprocessing.spawn** 在**单机**上由**主进程** spawn 出 N 个子进程，每个子进程跑同一 `train_fn(rank, ...)`；在 `train_fn` 里根据 `rank` 调 `init_process_group(rank=rank, world_size=world_size, ...)`，需**手动**传或设 `MASTER_ADDR`、`MASTER_PORT`（通常用本机 127.0.0.1）。**不需要**单独起多个进程再传 env，一切在一个 Python 进程里写：`mp.spawn(train_fn, nprocs=4, args=(...))`。**多机**时不太方便，因为 spawn 是单进程起子进程，跨机要自己起多个进程并配好 env，不如 torchrun 统一。

---

### 三、区别小结

| 维度     | torchrun                    | mp.spawn                          |
|----------|-----------------------------|-----------------------------------|
| 谁起进程 | torchrun 命令行起多进程     | 脚本里主进程 spawn 子进程         |
| 环境变量 | torchrun 自动设 RANK 等     | 需在 train_fn 里 init 时传 rank   |
| 多机     | 原生支持（--nnodes 等）     | 需自己起进程、配 env              |
| 脚本写法 | 脚本只 init_process_group   | 脚本里写 spawn + train_fn         |
| 推荐     | 生产与多机首选              | 单机快速试验、脚本自包含时可用    |

---

### 四、使用建议

- **多机、生产、统一入口**：用 **torchrun**，由调度器或运维一次启动，env 一致。
- **单机、本地试跑**：两种都行；torchrun 更简单（不用写 spawn），spawn 适合「一个脚本里包圆」的写法。

---

## 面试要点

- torchrun：命令行起多进程、自动设 RANK/WORLD_SIZE/MASTER_*；支持多机；脚本只 init。
- mp.spawn：单脚本里主进程 spawn 子进程，train_fn(rank) 里 init；多机需自配。
- 选型：多机/生产用 torchrun；单机可 torchrun 或 spawn。

---

## 记忆要点

1. torchrun = 外部起进程 + 自动 env；mp.spawn = 脚本内 spawn + 手动传 rank。
2. 多机用 torchrun（--nnodes、--node_rank）；单机两者皆可。
3. 脚本写法：torchrun 下只写 init；spawn 下写 spawn(train_fn, nprocs, args)。

[返回模块](./README.md) | [返回总览](../README.md)
