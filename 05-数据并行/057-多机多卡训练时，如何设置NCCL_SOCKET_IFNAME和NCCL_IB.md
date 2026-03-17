# 第 57 题：多机多卡训练时，如何设置`NCCL_SOCKET_IFNAME`和`NCCL_IB_DISABLE`？

## 题目

多机多卡训练时，如何设置`NCCL_SOCKET_IFNAME`和`NCCL_IB_DISABLE`？

---

## 完整讲解

### 一、NCCL_SOCKET_IFNAME

NCCL 做 **TCP 通信**（bootstrap 或 fallback transport）时要绑定**网卡接口**。多机多网卡时，若用错网卡（如用了管理网、带宽小的网），会慢或连不上。**NCCL_SOCKET_IFNAME** 指定**使用的网络接口名**，如 `eth0`、`ib0`（部分环境里 IB 也走 socket 名）、`bond0` 等。

- **设成什么**：用 `ifconfig` 或 `ip link` 看本机网卡名，选**数据面、高带宽**的那块（如万兆、IB）；设成该名，如 `export NCCL_SOCKET_IFNAME=eth1`。
- **多机一致**：各节点**同一逻辑角色**的网卡名最好一致（都是 eth1），否则要在每台机设对；若名不一致，可每台机单独设或通过调度器传 env。
- **不设**：NCCL 会自选，可能选到 lo 或错误网卡，多机常连不上或很慢，**建议显式设**。

---

### 二、NCCL_IB_DISABLE

**NCCL_IB_DISABLE=1** 表示**禁用 InfiniBand**，NCCL 只用 **TCP**（和可能的 NVLink 等）。用途：

- **没有 IB 或驱动未配好**：机器没有 IB 卡、或驱动/OFED 有问题，开 IB 会报错或 hang；设成 1 强制 TCP，先跑通。
- **排查问题**：多机 hang 或很慢时，先设 `NCCL_IB_DISABLE=1` 看是否 TCP 能正常；若 TCP 正常，再查 IB 配置（子网、MTU、防火墙等）。
- **有 IB 且正常**：不设或设 0，用 IB 获得更高带宽和更低延迟。

---

### 三、典型组合

- **多机、有 IB、已配置**：`NCCL_SOCKET_IFNAME=ib0`（或你数据面网卡名），不设 NCCL_IB_DISABLE（或 =0）。
- **多机、无 IB 或 IB 有问题**：`NCCL_IB_DISABLE=1`，`NCCL_SOCKET_IFNAME=eth1`（选数据面 TCP 网卡）。
- **单机多卡**：常走 NVLink/PCIe，不依赖 TCP/IB，可不必设；若用 TCP（如多机模拟），同上。

---

## 面试要点

- NCCL_SOCKET_IFNAME：指定 TCP 用的网卡（如 eth1、ib0）；多机要选数据面、高带宽，且各节点一致或每机设对。
- NCCL_IB_DISABLE=1：禁用 IB，只用 TCP；用于无 IB、IB 异常或排查时。
- 有 IB 且正常不设 IB_DISABLE；无 IB 或排查时设 1 + 指定 SOCKET_IFNAME。

---

## 记忆要点

1. SOCKET_IFNAME = 选 TCP 网卡；多机选数据面网卡、名一致或每机配好。
2. IB_DISABLE=1 = 只用 TCP；无 IB 或排错时用。
3. 有 IB 用 IB；无/异常时 IB_DISABLE=1 + 正确 IFNAME。

[返回模块](./README.md) | [返回总览](../README.md)
