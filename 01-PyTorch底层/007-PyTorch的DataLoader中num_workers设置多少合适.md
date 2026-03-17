# 第 7 题：PyTorch的`DataLoader`中`num_workers`设置多少合适？遇到过`too many open files`吗？

## 题目

PyTorch的`DataLoader`中`num_workers`设置多少合适？遇到过`too many open files`吗？

---

## 完整讲解

### 一、num_workers 在干什么？

`num_workers > 0` 时，DataLoader 会起**多个子进程**，每个进程负责从 dataset 里取样本、做 collate、放到队列里；主进程只从队列里取 batch。目的是把**数据加载和预处理**和 **GPU 计算**并行，避免 GPU 等数据（数据瓶颈）。workers 越多，理论上吞吐越高，但进程数多了会占 CPU/内存、增加 IPC 和打开文件数。

---

### 二、设多少合适？

- **经验值**：常用 4、8、16；可先设成 **CPU 物理核数或略小**（如 8 核设 4–8），再根据 GPU 利用率和 dataloader 的 `num_workers` 对吞吐的影响做微调。
- **原则**：若 `nvidia-smi` 里 GPU 利用率长期偏低、且不是模型太小，多半是数据跟不上，可**适当加大 num_workers**；若 CPU 或 I/O 已经打满，再加 workers 收益不大，反而可能因上下文切换或内存变慢。
- **batch 大时**：每个 batch 要准备的数据多，可适当多开几个 workers；但 workers 数 × 每进程打开文件/内存要小于系统限制（见下）。

---

### 三、`too many open files` 从哪来？

每个 worker 进程会打开**数据文件**（如每张图一个 fd、或每个 shard 一个 fd）、可能还有 pipe/socket（和主进程通信）。**打开文件数 = 进程数 × 每进程打开文件数**，超过系统 **ulimit（open files）** 就会报 `too many open files`（或 OSError 类似错误）。

常见场景：`num_workers` 较大 + 每个 sample 打开一个文件（如每张图一个文件）、或 dataset 里没及时 close、或系统默认 ulimit 较小（如 1024）。

---

### 四、怎么解决？

- **临时提高 ulimit**：`ulimit -n 65535`（或更大），只对当前 shell 及子进程有效。
- **永久提高**：在 `/etc/security/limits.conf` 或 systemd 的 service 里设 `nofile`，然后重新登录或重启服务。
- **减少每进程打开数**：数据用**大文件 + 偏移读取**（如 TFRecord、WebDataset 的 tar、数据库）而不是「一个 sample 一个文件」；或在 dataset 的 `__getitem__` 里**用完即 close**，不要长期持有 fd。
- **适当减小 num_workers**：在满足吞吐的前提下减小，使  workers × 每进程 fd 数 < ulimit。

---

## 面试要点

- num_workers：子进程数，用于数据加载与 GPU 并行；建议从 CPU 核数附近起调（如 4–8），看 GPU 利用率与吞吐再调。
- too many open files：进程打开 fd 总数超过 ulimit；多因 num_workers 大 + 每 sample 一文件或未及时 close。
- 解决：提高 ulimit、改用大文件/流式读取、保证用完 close、或适当减 num_workers。

---

## 记忆要点

1. num_workers = 数据加载子进程数；一般 4–8 起步，按 GPU 利用率和 CPU 负载调。
2. too many open files = 打开 fd 数 > ulimit；常为 workers 多 + 每 sample 一文件。
3. 解决：ulimit -n、大文件/流式、及时 close、或减 workers。

[返回模块](./README.md) | [返回总览](../README.md)
