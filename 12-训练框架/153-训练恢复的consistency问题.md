# 第 153 题：训练恢复的`consistency`问题？如何确保resume后的loss一致？

## 题目

训练恢复的`consistency`问题？如何确保resume后的loss一致？

---

## 完整讲解

### 一、Resume 的 Consistency 问题

**训练恢复**（resume）需恢复：模型参数、优化器状态、随机数状态、**当前 step/epoch**、以及可选的学习率调度、dataloader 位置等。若漏掉或错恢复某一项，**恢复后的 loss 曲线与未中断时不一致**：例如优化器动量未恢复会导致下一步更新方向不同；RNG 未恢复会导致 dropout/data shuffle 不同；step 未恢复会导致 lr schedule 错位；分布式时各 rank 的 dataloader 需从同一逻辑位置恢复，否则数据顺序错乱。

### 二、如何确保 Loss 一致

（1）**Checkpoint 内容完整**：至少包含 model state、optimizer state、step（或 epoch）、RNG states（torch、numpy、random）；分布式时还有 rank0 的 step 与 dataloader 的 sampler 状态。（2）**加载顺序与设备**：按相同设备与 key 加载，避免 half/full 或 key 不匹配。（3）**Dataloader**：用 `sampler.set_epoch(epoch)` 或保存/恢复 sampler 状态，保证各 rank 恢复后读到同一顺序的数据。（4）**验证**：恢复后跑若干 step 与「未中断时同 step」的 loss 对比（或与上次 checkpoint 的 loss 衔接），不一致则排查漏项。

### 三、工程要点

Checkpoint 设计时就把 step、optimizer、RNG、dataloader 状态纳入；恢复脚本与保存脚本对称；大规模训练建议定期验证 resume 后的 loss 衔接。

---

## 面试要点

- Consistency 指 resume 后 loss 与未中断时一致；漏恢复 optimizer、step、RNG、dataloader 任一都会导致不一致。
- 做法：checkpoint 含 model、optimizer、step、RNG、dataloader/sampler 状态；加载顺序与设备一致；恢复后验证 loss 衔接。
- 分布式时各 rank 的 step 与 sampler 状态一致；验证用若干 step 对比或看曲线衔接。

---

## 记忆要点

1. 一致 = 恢复后 loss 曲线衔接；漏 optimizer/step/RNG/dataloader 会错。
2. Checkpoint 要全：model、optimizer、step、RNG、sampler；加载对称。
3. 恢复后做验证；分布式注意各 rank 的 step 与 sampler。

[返回模块](./README.md) | [返回总览](../README.md)
