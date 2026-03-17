# 第 8 题：解释PyTorch的`torch.distributed`中的`DDP`和`FSDP`的区别

## 题目

解释PyTorch的`torch.distributed`中的`DDP`和`FSDP`的区别

---

## 完整讲解

### 一、DDP（DistributedDataParallel）在做什么？

**DDP** 是**数据并行**：每张卡上有一份**完整模型**，每轮各卡用**不同数据**算 forward 和 backward；backward 结束后，各卡上的梯度要**同步**（通常 all-reduce），再在本卡用同一份梯度更新参数，所以每卡参数始终保持一致。显存占用 ≈ **单卡模型 + 单卡激活 + 梯度**，模型必须能放进单卡。

---

### 二、FSDP（Fully Sharded Data Parallel）在做什么？

**FSDP** 是**分片数据并行**：把**模型参数、梯度、有时还有优化器状态**按卡**分片**，每张卡只存 1/N（N=卡数）；forward 时用 all-gather 把当前层所需参数临时拼起来算，算完丢掉；backward 同样 all-gather → 算梯度 → reduce-scatter 把梯度按片回写。这样**单卡显存 ≈ 1/N 模型 + 当前层激活**，可以训「单卡放不下」的大模型。

---

### 三、核心区别对比

| 维度           | DDP                          | FSDP                                  |
|----------------|------------------------------|----------------------------------------|
| 参数存储       | 每卡一份完整模型              | 每卡 1/N 参数（分片）                  |
| 梯度           | 每卡一份完整梯度，all-reduce | 分片，reduce-scatter 写回               |
| 优化器状态     | 每卡一份完整                 | 可只存本卡分片（显存再省）             |
| 单卡显存       | 约 1× 模型 + 激活 + 梯度     | 约 1/N 模型 + 激活（可训大模型）       |
| 通信           | backward 后梯度 all-reduce   | 每层 forward/backward 的 all-gather/reduce-scatter |
| 典型场景       | 模型能放进单卡、多卡加速     | 模型太大单卡放不下、大模型训练         |

---

### 四、为什么需要 FSDP？

当模型参数量大（如数十 B、上百 B），即使用上梯度 checkpoint，单卡也存不下「完整参数 + 梯度 + 优化器」。FSDP 用**分片**换通信：每次只 all-gather 当前层需要的参数，算完就丢，所以**显存从「整模型」变成「1/N 模型 + 当前层激活」**，能显著扩大可训模型规模；代价是每层多一次 all-gather/reduce-scatter，通信量比 DDP 的「一次梯度 all-reduce」大，需要好的通信和 overlap 设计。

---

### 五、面试可怎么说？

- **DDP**：每卡完整模型、不同数据、梯度 all-reduce 后一致更新；适合模型能塞进单卡、追求训练速度。
- **FSDP**：参数（及可选梯度/优化器）分片，按层 all-gather 算、reduce-scatter 回写；显存约 1/N，能训大模型；通信更复杂、每层有集合通信。
- **选型**：单卡能放下用 DDP；放不下或要省显存用 FSDP（或与 ZeRO 等结合）。

---

## 面试要点

- DDP：完整模型每卡、数据并行、梯度 all-reduce；显存 ≈ 单卡模型+激活+梯度。
- FSDP：参数（及可选梯度和优化器）分片，forward/backward 时 all-gather 用、reduce-scatter 回；显存约 1/N，可训大模型；通信为每层 all-gather + reduce-scatter。
- 区别：存储方式（完整 vs 分片）、显存规模、通信模式与量。

---

## 记忆要点

1. DDP = 数据并行 + 每卡完整模型 + 梯度 all-reduce；单卡能放下模型时用。
2. FSDP = 参数分片 + 按层 all-gather/reduce-scatter；单卡放不下或要省显存时用。
3. FSDP 显存约 1/N，通信量和次数比 DDP 多；两者可和 ZeRO、混合精度等组合用。

[返回模块](./README.md) | [返回总览](../README.md)
