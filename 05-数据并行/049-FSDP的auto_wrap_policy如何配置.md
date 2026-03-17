# 第 49 题：FSDP的`auto_wrap_policy`如何配置？`size_based` vs `module_based`？

## 题目

FSDP的`auto_wrap_policy`如何配置？`size_based` vs `module_based`？

---

## 完整讲解

### 一、为什么需要 wrap policy？

FSDP 不是「整模型一个大块」做分片，而是把模型切成多个**子模块**，每个子模块是一个 **FSDP 单元**：单元内做 all-gather → 算 → 丢，单元间顺序执行。**Wrap policy** 决定「**哪些子模块**被包成 FSDP 单元」：包得太粗（如整模型一块）显存峰值高、重叠少；包得太细（每层一个）通信次数多、开销大。**auto_wrap_policy** 用规则**自动**决定包装边界。

---

### 二、size_based

- **思路**：按**参数量**划界；子树的**参数总量**超过某阈值（如 1e8）就包成一个 FSDP 单元，否则继续往子节点看。
- **效果**：大块（如一大坨 Linear）会单独成单元，小块会合并到父节点或相邻；单元大小相对均匀、易控显存峰值。
- **配置**：如 `size_based_auto_wrap_policy(min_params=1e8)`，min_params 可调；调大则单元更大、通信次数少但单次 all-gather 大、显存峰值高。

---

### 三、module_based

- **思路**：按**模块类型**划界；指定「哪些类」的实例要包成 FSDP 单元（如 `TransformerBlock`、`ResBlock`），其他层和它们一起按层级包装。
- **效果**：与模型结构对齐，如每个 Transformer block 一个单元，便于理解和调优；对已知结构（如 Megatron 风格）很合适。
- **配置**：如 `module_based_auto_wrap_policy(module_classes={TransformerBlock})`，只对这些类做「切分点」。

---

### 四、如何选？

- **结构清晰、有明确 block**（如 Transformer、ResNet block）：用 **module_based**，按 block 包，易控且符合直觉。
- **结构杂、或想按参数量均衡**：用 **size_based**，按 min_params 调到一个合适单元大小，平衡显存与通信。
- 也可**组合**：先按 module 切几刀，再对剩余部分用 size_based；或手写 policy 函数，混合两种逻辑。

---

## 面试要点

- Wrap policy 决定哪些子模块被包成 FSDP 单元；太粗显存高、太细通信多。
- size_based：按参数量阈值（如 min_params）划单元；均衡、易控。
- module_based：按模块类型（如 TransformerBlock）划单元；与结构对齐，易理解。

---

## 记忆要点

1. 单元太粗→显存高；太细→通信多；policy 自动划界。
2. size_based = 按参数量阈值；module_based = 按指定类（如 Block）。
3. 有明确 block 用 module_based；否则或混合用 size_based。

[返回模块](./README.md) | [返回总览](../README.md)
