# 第 264 题：多GPU的`peer-to-peer`访问？`cudaDeviceEnablePeerAccess`？

## 题目

多GPU的`peer-to-peer`访问？`cudaDeviceEnablePeerAccess`？

---

## 完整讲解

### 一、P2P 概念

**Peer-to-Peer（P2P）** 指多 GPU 间**直接访问对方显存**，不经过 host。在支持 P2P 的拓扑下（如同一 PCIe 树、NVLink），可降低延迟、提高带宽，用于多卡 kernel 间直接读写。

### 二、cudaDeviceEnablePeerAccess

`cudaDeviceEnablePeerAccess(peerDeviceId, flags)` 使**当前 device** 能访问 **peerDeviceId** 的显存。需在两端都启用（A 能访问 B、B 能访问 A 需各调一次）。返回 cudaErrorPeerAccessAlreadyEnabled 表示已开。配合 `cudaMemcpyPeer(dst, dstDev, src, srcDev, size)` 做 D2D 拷贝。

### 三、条件与注意

拓扑需支持（同机多卡通常支持；跨机不行）。可先 `cudaDeviceCanAccessPeer(&can, dev, peer)` 查询。P2P 打开后，分配在 peer 上的指针可在本 device kernel 中通过统一地址或 Peer 接口使用（视驱动与 UVA 而定）。

---

## 面试要点

- P2P = 多 GPU 直接访问对方显存，不经过 host；同机/同 PCIe 树常支持。
- cudaDeviceEnablePeerAccess(peerId, 0) 使当前 device 能访问 peer；双向需各调一次。
- cudaMemcpyPeer 做 D2D；先 cudaDeviceCanAccessPeer 查询是否支持。
- 用于多卡间低延迟、高带宽数据交换。

---

## 记忆要点

1. P2P = GPU 直接访问 GPU 显存；cudaDeviceEnablePeerAccess 开启。
2. 双向访问需各自 Enable；cudaMemcpyPeer 做 D2D。
3. 需拓扑支持；cudaDeviceCanAccessPeer 查询。

[返回模块](./README.md) | [返回总览](../README.md)
