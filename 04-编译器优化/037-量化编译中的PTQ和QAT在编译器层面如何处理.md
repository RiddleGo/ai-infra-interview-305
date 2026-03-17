# 第 37 题：量化编译中的`PTQ`和`QAT`在编译器层面如何处理？

## 题目

量化编译中的`PTQ`和`QAT`在编译器层面如何处理？

---

## 完整讲解

### 一、PTQ 与 QAT 在编译器视角

**PTQ**（Post-Training Quantization）：训练完后 **一次性** 用校准数据统计 scale/zero_point（或分布），把权与激活量化；**QAT**（Quantization-Aware Training）：训练时 **前向用量化、反向用直通估计**，权重按量化格式更新。编译器不负责「怎么定 scale」，但负责：**把浮点图转成量化图**（插入/改写 quantize/dequantize、整数 op）、**融合 Q/DQ 与相邻 op**、**选择后端支持的量化 op**（如 int8 conv、per-channel 等）。

### 二、PTQ 在编译层的处理

- **图改写**：根据 **已定的 scale/zero_point**（由校准阶段产生，存在模型或配置里），把 Float op 换成 **Quantized op**（权与激活用 int8/uint8），并在合适位置插 **QuantizeLinear / DequantizeLinear**（或等价节点）。
- **融合**：**Q → Op → DQ** 常融合成「量化 op」一个 kernel（如 int8 conv），减少往返整数与浮点的转换。
- **常量折叠**：权重量化后的常量可 fold 进引擎或 kernel，不占运行时计算。

### 三、QAT 在编译层的处理

- **训练时**：编译器/框架把「假量化」（fake quantize：前向量化再反量化、梯度直通）当成普通 op 建图；通常不在此阶段做激进融合，以便梯度正确。
- **导出/部署时**：QAT 导出的图往往 **已带 Q/DQ 或量化参数**；编译器同样做 **图改写与 Q-Op-DQ 融合**，与 PTQ 导出后的处理类似；区别是 scale 来自训练过程而非事后校准。
- **统一点**：无论 PTQ 还是 QAT，**部署侧** 都是「量化图 + 融合 + 后端 int8 实现」；编译器不区分 scale 来源，只按图上 Q/DQ 与 op 做融合与 lowering。

### 四、小结

- **PTQ**：校准得到 scale → 图改写为量化 op + Q/DQ → 融合 Q-Op-DQ。
- **QAT**：训练时假量化，导出带 Q/DQ 的图 → 部署时同样改写与融合。
- 编译器重点：图级量化 op 插入/替换、Q-DQ 与 op 融合、对接到后端 int8 kernel。

---

## 面试要点

- 编译器不决定 scale，只做：量化图改写（Q/DQ、整数 op）、Q-Op-DQ 融合、对后端 int8 实现。
- PTQ：校准后图改写 + 融合；QAT：导出图已带 Q/DQ，部署时同样改写与融合。
- 融合减少 Q/DQ 往返；训练时假量化一般不做激进融合以保梯度。

---

## 记忆要点

1. PTQ/QAT 的 scale 由校准或训练定；编译器做图改写与融合。
2. 共同处理：插入/替换量化 op、融合 Q-Op-DQ、对接 int8 后端。
3. QAT 导出图带 Q/DQ；部署侧与 PTQ 一样做融合与 lowering。

[返回模块](./README.md) | [返回总览](../README.md)
