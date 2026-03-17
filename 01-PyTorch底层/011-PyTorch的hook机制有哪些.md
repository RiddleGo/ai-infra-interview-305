# 第 11 题：PyTorch的`hook`机制有哪些？`forward_pre_hook`和`backward_hook`的应用场景？

## 题目

PyTorch的`hook`机制有哪些？`forward_pre_hook`和`backward_hook`的应用场景？

---

## 完整讲解

### 一、Hook 有哪些？

- **forward_pre_hook**：在某一层的 **forward 被调用之前** 执行；签名 `hook(module, input)`，可修改或查看**输入**，再交给该层 forward。
- **forward_hook**：在该层 **forward 被调用之后** 执行；签名 `hook(module, input, output)`，可查看或替换**输出**。
- **backward_hook**：在该层 **backward 时** 执行（即梯度反传到这一层时）；签名 `hook(module, grad_input, grad_output)`，可查看或修改**梯度**（grad_output 是上一层传下来的，grad_input 是传给再上一层的）。

前两个在 `Module` 上注册（`module.register_forward_pre_hook(...)` 等），backward_hook 同样在 Module 上注册，在反向传播经过该 module 时被调用。

---

### 二、forward_pre_hook 能干什么？

- **改输入**：例如做输入归一化、插入噪声（对抗训练）、把输入转到另一设备。
- **调试与可视化**：打印每层输入的 shape、范围、是否有 NaN；或把中间结果导出做可视化。
- **插层 / 条件计算**：根据输入决定是否执行该层、或插入额外计算（注意返回值格式要符合下一层预期）。

典型场景：**调试时看某一层入口的 tensor 长什么样、是否数值异常**；或在做输入预处理/增强时统一在某一层前做。

---

### 三、forward_hook 能干什么？

- **取中间特征**：做特征可视化、CAM、或把某几层的输出当「特征」喂给下游任务（如蒸馏、多任务头）。
- **改输出**：例如做输出归一化、dropout 式 mask、或替换成自己算的结果（如替换 attention 输出做分析）。
- **记录激活**：为激活重计算、显存分析、或离线分析记录每层输出（注意显存，大模型可只记 shape 或采样）。

典型场景：**可视化某层特征图、做知识蒸馏时取教师中间层输出、或做剪枝/敏感度分析时记录每层输出。**

---

### 四、backward_hook 能干什么？

- **梯度检查与可视化**：看某层收到的梯度（grad_output）和传出的梯度（grad_input），查梯度消失/爆炸、是否某层梯度为 0。
- **梯度修改**：如梯度裁剪（在 hook 里 clamp）、梯度噪声、或自定义的梯度重加权（如某通道乘一个系数）。
- **敏感度与剪枝**：根据梯度大小判断参数/通道重要性，用于剪枝或 NAS。

典型场景：**调试「某层不更新」时看该层梯度是否为空或过小；或实现 per-layer 梯度缩放/裁剪。**

---

### 五、使用注意

- Hook 里**不要**做耗时或阻塞操作，否则会拖慢训练；记录到列表再在别处处理更安全。
- 修改 tensor 时注意 **inplace 与计算图**：若在 forward_hook 里改 output，要保证不破坏 backward 需要的图；backward_hook 里改梯度要保证形状一致。
- 带 `full_backward_hook` 的 API（PyTorch 新版本）在 pack 的输入下行为更一致，旧版 backward_hook 在 pack 时可能有 tuple 拆包问题，需看文档。

---

## 面试要点

- 三种 hook：forward_pre_hook（forward 前，改/看输入）、forward_hook（forward 后，改/看输出）、backward_hook（反向时，改/看梯度）。
- 应用：pre = 输入预处理、调试；forward = 特征可视化、蒸馏、记录激活；backward = 梯度检查、裁剪、敏感度分析。
- 注意：别在 hook 里做重活、改 tensor 别破坏图/形状。

---

## 记忆要点

1. forward_pre_hook：入口，改/看输入；forward_hook：出口，改/看输出；backward_hook：反向，改/看梯度。
2. 应用：调试、可视化、蒸馏、梯度检查与修改、剪枝敏感度。
3. 只做轻量操作；改 tensor 注意图和形状。

[返回模块](./README.md) | [返回总览](../README.md)
