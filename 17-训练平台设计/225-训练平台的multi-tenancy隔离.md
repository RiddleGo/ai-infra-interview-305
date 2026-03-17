# 第 225 题：训练平台的`multi-tenancy`隔离？`namespace`、`cgroup`？

## 题目

训练平台的`multi-tenancy`隔离？`namespace`、`cgroup`？

---

## 完整讲解

### 一、多租户隔离需求

**多租户**：多团队/多项目**共享**同一集群；需 **资源隔离**（某租户不能占满）、**故障与噪声隔离**（某任务异常不影响他人）、**安全与权限**（只能看/用自己资源）。

### 二、Namespace 与 cgroup

**Namespace**（K8s）：**逻辑隔离**；每个租户一个 **namespace**，Pod、PVC、ConfigMap 等归属其下；**RBAC** 限制谁只能操作哪些 namespace。**ResourceQuota** 在 namespace 级限 **CPU/内存/GPU 总量**；**LimitRange** 限单 Pod 上下界。**Cgroup**：**内核级** 资源限制；K8s 通过 **requests/limits** 落到 **CPU/memory cgroup**；可扩展 **GPU、IO** 等。**隔离效果**：CPU/内存/GPU 硬限、避免某 Pod 吃满节点；**网络** 可配 **NetworkPolicy**；**存储** 可按 namespace 或 PVC 隔离。

### 三、与调度、计费配合

**队列**：租户对应 **queue** 或 **namespace**；调度器按 queue 做 **fair share 或 cap**。**计费**：按 namespace/queue 统计 **GPU 小时** 等，做 chargeback。**噪声**：多租户同节点时可能 **CPU/内存/网络** 争抢；**GPU 独占** 或 **MIG** 可做更细 GPU 隔离；**优先级与抢占** 保证高优租户不受低优拖累。
---

## 面试要点

- 多租户：资源隔离、故障隔离、权限；Namespace 做逻辑隔离 + Quota/LimitRange。
- Cgroup 做 CPU/内存等硬限；K8s 通过 requests/limits 落 cgroup。
- 队列 + 计费按 namespace；GPU 独占/MIG 做细粒度隔离。

---

## 记忆要点

1. Namespace = 逻辑隔离 + Quota；cgroup = 内核资源限。
2. ResourceQuota、LimitRange、RBAC 配合。
3. 队列、计费、GPU 隔离（MIG/独占）。

[返回模块](./README.md) | [返回总览](../README.md)
