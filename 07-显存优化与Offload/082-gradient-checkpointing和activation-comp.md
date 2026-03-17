# 第 82 题：`gradient checkpointing`和`activation compression`的结合？

## 题目

`gradient checkpointing`和`activation compression`的结合？

---

## 完整讲解

### 一、Gradient checkpointing 与 activation compression

**Gradient checkpointing**（即 activation checkpointing）：少存激活、backward 时重算，用算力换显存。**Activation compression**：对激活做量化、稀疏或低秩近似再存，用精度/算力换显存。两者都可降低「激活占用」的显存，可叠加使用。

### 二、结合的方式与注意点

- **先 checkpoint 再压缩**：checkpoint 处只存「压缩后」的激活（如 int8 或稀疏），重算时解压再算梯度；显存进一步降，但解压与重算有额外算力，且压缩误差可能影响梯度。
- **选择性组合**：大激活层用 checkpoint，部分层再对存下来的激活做压缩（如只对非 checkpoint 的中间层做轻量压缩），平衡显存、算力与精度。
- **误差与收敛**：压缩会引入误差，需做误差分析或小规模实验验证收敛；通常先单独用 checkpoint 稳定，再谨慎加压缩（如 8bit 激活）并监控 loss。

### 三、工程实践

- 多数框架先支持 checkpoint；activation compression 多在研究或特定场景（如超长序列、显存极紧）使用。
- 结合时：checkpoint 的「存点」存压缩版本，backward 时解压→重算→反传；或对非 checkpoint 的激活做在线压缩再写回，需注意与 autograd 的兼容性（如自定义 backward）。

---

## 面试要点

- Checkpoint 用算力换显存；compression 用精度/算力换显存；可叠加。
- 结合时：存压缩激活、重算时解压；或部分层 checkpoint、部分层压缩；注意误差与收敛。
- 工程上先 checkpoint 稳，再视需要加压缩并验证。

---

## 记忆要点

1. Checkpoint = 重算换显存；compression = 量化/稀疏换显存；可一起用。
2. 存压缩版激活、backward 解压重算；注意精度与收敛。
3. 先上 checkpoint，再谨慎加 compression。

[返回模块](./README.md) | [返回总览](../README.md)
