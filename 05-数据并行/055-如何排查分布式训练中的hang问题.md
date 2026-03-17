# 第 55 题：如何排查分布式训练中的hang问题？`NCCL_DEBUG=INFO`的输出如何解读？

## 题目

如何排查分布式训练中的hang问题？`NCCL_DEBUG=INFO`的输出如何解读？

---

## 完整讲解

### 一、分布式 hang 的常见原因

- **集体通信不同步**：某卡没参与某次 all-reduce/all-gather，或参与顺序/次数不一致，其他卡会一直等 → hang。
- **死锁**：例如某卡在等数据、另一卡在等梯度；或 DDP 里 find_unused_parameters 与梯度不同步导致某卡多/少一次通信。
- **网络/驱动**：丢包、超时、NCCL 与网络配置不匹配（如 IB 未正确配置），某次 collective 永远不返回。
- **资源**：某进程 OOM 或被 kill，其他进程一直等其参与 collective。

---

### 二、NCCL_DEBUG=INFO 能看什么？

设置 **NCCL_DEBUG=INFO**（或 WARN）后，NCCL 会打印**每次 collective 的参与信息、transport 选择、超时等**。典型输出包括：

- **各 rank 的 transport**：用 TCP 还是 IB、RoCE；若部分卡走 TCP、部分走 IB，可能慢或异常。
- **Collective 的 op 与 size**：哪次 all-reduce、多少字节；可对照代码看「应该是第几次、多大」。
- **超时 / 错误**：若某卡没发或没收，会看到 timeout 或 peer 不可达；**最后一行**往往指向「谁在等谁」。
- **Rank 与 world_size**：确认每卡认为的 rank 和 world_size 一致，避免漏进程或重复 rank。

---

### 三、如何用这些信息排查？

- **先看最后几行**：hang 时哪几个 rank 在等、等什么 op；若只有部分 rank 打印，说明有的进程已卡死或没进到该 collective。
- **对照代码**：确认 backward、optimizer.step、SyncBN、自定义 collective 的**次数和顺序**在所有 rank 上一致；不一致就会在某次 collective 上 hang。
- **结合 PyTorch**：用 **TORCH_DISTRIBUTED_DEBUG=DETAIL** 可打印每次 collective 的调用栈，看是 DDP、FSDP 还是用户代码里哪一步；再配合 NCCL_DEBUG 看是哪个 op 卡住。
- **网络**：看 transport 是否一致、是否有 IB 未 up、防火墙/端口问题；可先 **NCCL_IB_DISABLE=1** 强制 TCP 试是否能跑通。

---

### 四、小结

- Hang 多为 collective 不同步或网络/进程异常；NCCL_DEBUG=INFO 看 transport、op、超时、rank。
- 排查：最后输出看「谁在等」→ 对照代码找「谁多/少调了 collective」→ 结合 TORCH_DISTRIBUTED_DEBUG 定位调用点；网络问题可试关 IB 或查端口/防火墙。

---

## 面试要点

- Hang 常见：collective 不同步、死锁、网络/进程异常。
- NCCL_DEBUG=INFO：看 transport、collective op/size、超时、rank；最后几行指向「谁在等」。
- 排查：对照代码保证每 rank 调用 collective 次数顺序一致；用 TORCH_DISTRIBUTED_DEBUG 看调用栈；网络可试 NCCL_IB_DISABLE=1。

---

## 记忆要点

1. Hang ≈ collective 不同步或网络/进程挂；NCCL_DEBUG 看 op、transport、超时。
2. 最后输出看谁在等；对照代码找多/少调用的 rank。
3. TORCH_DISTRIBUTED_DEBUG=DETAIL + NCCL_DEBUG 组合定位；网络问题试 TCP-only。

[返回模块](./README.md) | [返回总览](../README.md)
