# 第 305 题：`etcd`在K8s中的作用？性能调优？

## 题目

`etcd`在K8s中的作用？性能调优？

---

## 完整讲解

### 一、etcd 在 K8s 中的作用

**etcd** 是 Kubernetes 的**后端存储**：存**集群状态**（Pod、Node、Service、ConfigMap 等所有 API 对象）、**元数据与 lease**。API Server 是唯一写 etcd 的组件；Controller、Scheduler、kubelet 等通过 API Server 读/写。etcd 提供 **watch**，使各组件能**增量感知**变更，实现协调与声明式逻辑。**高可用**部署通常 3 或 5 节点，用 Raft 共识保证一致性与容错。

### 二、性能瓶颈与调优

**写入**：大量 Pod 创建/删除、频繁更新（如 status、annotation）会推高 QPS 与 compaction 压力。**大 key/value**：单对象过大（如 ConfigMap 几 MB）会拉长单次请求与 compaction。**历史版本**：etcd 保留多版本，**compaction** 不及时会占磁盘与内存。**调优**：**--auto-compaction** 与 **--compact-interval** 控制压缩周期；**--quota-backend-bytes** 限制 DB 大小防爆盘；**SSD、足够内存**；**分离 watch 与读写**（可读副本）；**控制单对象大小与更新频率**（如 status 与主对象分离、限流）。

### 三、运维要点

监控 **etcd 延迟、QPS、db size、compaction**；避免单对象过大与全量 list；升级与备份按官方建议做；生产至少 3 节点、定期备份与恢复演练。

---

## 面试要点

- etcd = K8s 集群状态存储；API Server 唯写；watch 供各组件增量感知。
- 性能：写 QPS、大对象、历史版本与 compaction；调优：auto-compaction、quota、SSD/内存。
- 控制单对象大小与更新频率；监控延迟、db size、compaction。
- 高可用 3/5 节点；备份与恢复演练。

---

## 记忆要点

1. etcd 存全集群 API 对象；API Server 写、各组件通过 watch 感知。
2. 调优：compaction、quota、SSD；控制大对象与频繁更新。
3. 监控延迟与 db size；生产多节点、定期备份。

[返回模块](./README.md) | [返回总览](../README.md)
