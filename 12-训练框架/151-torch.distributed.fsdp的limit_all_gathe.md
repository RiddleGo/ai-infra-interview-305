# 第 151 题：`torch.distributed.fsdp`的`limit_all_gathers`参数作用？

## 题目

`torch.distributed.fsdp`的`limit_all_gathers`参数作用？

---

## 完整讲解

### 一、FSDP 中的 All-Gather

FSDP 在前向与反向时需要对当前层的参数做 **all-gather**，把各 rank 持有的分片拼成完整参数再计算。若多个层或多次 all-gather 同时进行，会**并发占用大量显存**（多份完整参数临时存在），容易 OOM；且 all-gather 是集体通信，过多并发也会增加调度与同步开销。

### 二、limit_all_gathers 的作用

**limit_all_gathers**（或等价选项）：限制**同一时刻**处于「已 all-gather、未释放」状态的参数量，即对并发 all-gather 做**限流**。实现上通常通过调度：只有当前「未释放的 all-gathered 参数」占用的显存低于某阈值或数量时，才允许下一层执行 all-gather；否则等待前面某层释放后再进行。这样用少量额外同步换显存峰值下降，避免因多段同时全量参数而 OOM，特别在层数多、参数大的模型上有效。

### 三、使用建议

显存紧张或大模型时建议开启；会略微增加通信与调度序列化，但能显著提高可训模型规模或 batch 上限。具体参数名与默认值以当前 PyTorch FSDP 文档为准（如 `limit_all_gathers=True` 或带数值的配置）。

---

## 面试要点

- FSDP 按层 all-gather 参数，多段同时 all-gather 会拉高显存峰值、易 OOM。
- limit_all_gathers：限制同一时刻「已 gather 未释放」的 all-gather 数量/显存，用限流换峰值降低。
- 显存紧张时建议开；会略增调度与序列化，但能训更大模型或更大 batch。

---

## 记忆要点

1. 多段同时 all-gather → 显存峰值高、易 OOM。
2. limit_all_gathers = 限流 all-gather，控制并发 gather 数量/显存。
3. 开后可训更大模型或 batch；以 PyTorch 文档为准。

[返回模块](./README.md) | [返回总览](../README.md)
