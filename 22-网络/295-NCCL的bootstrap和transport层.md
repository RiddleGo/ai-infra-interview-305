# 第 295 题：`NCCL`的`bootstrap`和`transport`层？

## 题目

`NCCL`的`bootstrap`和`transport`层？

---

## 完整讲解

### 一、NCCL 分层

NCCL 提供多 GPU/多机集合通信（all-reduce、all-gather、reduce-scatter 等），内部大致分 **bootstrap** 与 **transport** 等层。**Bootstrap**：负责**发现与组网**——哪些 rank、如何找到彼此（如通过环境变量、socket、共享存储等），建立控制面。**Transport**：负责**实际数据传输**——选择网络路径（如 Net/Socket、IB、RoCE）、选择算法（ring、tree 等）、执行 send/recv 与同步。

### 二、Bootstrap 层

启动时各 rank 需知道「总 rank 数、本 rank id、其它 rank 的地址」等。NCCL 支持多种 **bootstrap**：如 **env**（NCCL_SOCKET_IFNAME、master 地址等环境变量）、**file**（共享文件里写地址）、**tcp**（指定 master 与 port）等。Bootstrap 完成后，各 rank 拥有一致的 group 与拓扑信息，供 transport 建连与选算法。

### 三、Transport 层

根据**检测到的网络**（IB、RoCE、TCP 等）创建 channel、QP 或 socket；根据 **topology**（单机多卡、多机）选择 **ring、tree、collnet** 等算法；执行实际的 reduce、all-gather 等步骤。调优常涉及 NCCL_DEBUG、NCCL_IB_DISABLE、NCCL_ALGO 等环境变量。

---

## 面试要点

- Bootstrap = 发现与组网：rank 发现、地址交换、建控制面；支持 env/file/tcp 等。
- Transport = 实际传输：选网（IB/RoCE/TCP）、选算法（ring/tree）、执行通信。
- Bootstrap 决定「谁和谁通信」；Transport 决定「怎么传、走哪条路」。
- 调优：NCCL_DEBUG、NCCL_ALGO、NCCL_IB 等环境变量。

---

## 记忆要点

1. Bootstrap = 组网与发现；Transport = 传输与算法选择。
2. Bootstrap 有 env/file/tcp 等；Transport 有 ring/tree、IB/Socket。
3. 排障与调优看 bootstrap 是否成功、transport 选用的网络与算法。

[返回模块](./README.md) | [返回总览](../README.md)
