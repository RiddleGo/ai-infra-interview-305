# 第 209 题：混合精度训练的`numerical stability`问题？

## 题目

混合精度训练的`numerical stability`问题？

---

## 完整讲解

### 一、混合精度的数值风险

**FP16/BF16** 范围与精度低于 FP32：**溢出**（大数变 inf）、**下溢**（小数变 0）、**舍入误差累积**。在 **loss scaling、梯度、某些层** 上可能表现为 **loss NaN、梯度爆炸/消失、训练不稳**。

### 二、常见问题与对策

**Loss scaling**：梯度在 FP16 下容易下溢；用 **动态或静态 scale** 放大梯度再做 backward，还原后再 **unscale** 更新；可避免梯度变 0。**敏感层**：**LayerNorm、Softmax、loss** 等保持 **FP32**（或 BF16）计算，仅部分 linear/matmul 用 FP16，即 **混合精度** 而非全 FP16。**BF16**：指数域与 FP32 同，范围大，**不易溢出**，可减少 scaling 与 cast；精度略逊 FP16，通常训练更稳。**检查**：训练中监控 **梯度 norm、loss**；若出现 NaN 可先关混合精度做 baseline，再逐层或逐 op 放宽精度定位。

### 三、工程实践

PyTorch **AMP**（autocast + GradScaler）：autocast 自动选 op 精度，GradScaler 做 loss scale 与 unscale；一般够用。**自定义**：对已知敏感 op 用 `torch.amp.autocast(..., enabled=False)` 包一层保持 FP32。**数值稳定性** 与 **速度** 需权衡；BF16 在 A100 等上推荐为首选。
---

## 面试要点

- 混合精度有溢出/下溢/舍入风险；loss scaling、敏感层 FP32、BF16 可缓解。
- Loss scaling（GradScaler）；LayerNorm/Softmax/loss 等保持 FP32；BF16 范围大更稳。
- AMP：autocast + GradScaler；敏感 op 可局部关 autocast。

---

## 记忆要点

1. 风险：溢出、下溢、舍入；loss scaling + 敏感层 FP32。
2. BF16 范围大、不易溢出；AMP 常用 GradScaler。
3. 监控梯度/loss；NaN 时先关 AMP 再逐层排查。

[返回模块](./README.md) | [返回总览](../README.md)
