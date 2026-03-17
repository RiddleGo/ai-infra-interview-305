# 第 44 题：`operator decomposing`和`operator fusion`的边界在哪里？

## 题目

`operator decomposing`和`operator fusion`的边界在哪里？

---

## 完整讲解

### 一、Decomposing 与 fusion 在做什么？

**算子分解（decomposing）**：把 **大/复杂 op** 拆成 **多个小 op** 或更基础的 op，以便：后端有实现、便于做更多 **图级优化**（如和相邻 op 再融合）、或 **简化语义**（如把自定义 op 用标准 op 表示）。**算子融合（fusion）**：把 **多个小 op** 合并成 **一个或少个 kernel**，减少 launch、中间读写与调度开销。二者方向 **相反**：一个「拆」、一个「合」。

### 二、边界在哪里？

- **何时先 decompose**：**一、** 某 op 在某后端 **没有实现**，需拆成该后端有的 op；**二、** 某 op **过于复杂**，拆开后能匹配到更多 **融合 pattern**（例如拆成 A+B+C 再与前后 op 融成 A'+B'）；**三、** 做 **等价替换** 以便用更优的融合子图（如某库的融合 Conv+BN+Relu 要求先有单独的 Conv/BN/Relu 再被识别）。
- **何时不拆、直接融合**：**一、** 后端已有 **高效融合实现**（如 CuDNN 的 fused op），保留大 op 更优；**二、** 拆开会导致 **无法再融合**（如硬件只认「一整块」才给加速）；**三、** 拆开 **增加调度与 launch 开销**、且无更好融合机会时，不拆更划算。
- **边界**：取决于 **后端能力**（有无单 op、有无融合 pattern）、**图上下文**（拆开后能否和邻居融得更好）、**性能实测**（拆+融 vs 保留大 op 谁快）。没有绝对规则，一般是 **先 legalize（必要时 decompose）再 fusion**，用 cost 或 heuristics 决定某处是否拆。

### 三、在 pipeline 中的顺序

常见顺序：**前端图** → **legalize**（复杂/不支持的 op 做 decompose）→ **融合 pass**（pattern 匹配，多 op 合一）→ **lowering**。有时 **多轮**：融合后再 legalize（新 op 可能需再拆），再融合。边界由 **pass 顺序与每条规则的条件** 共同决定。

---

## 面试要点

- Decomposing = 拆成小 op，便于后端实现或后续融合；fusion = 多 op 合一 kernel，减 launch 与访存。
- 边界：后端有无实现、拆开能否带来更好融合、实测谁快；先 legalize（含 decompose）再 fusion 常见。
- 无绝对规则；多轮 legalize + fusion 时，每条规则的条件与顺序决定最终形态。

---

## 记忆要点

1. 分解 = 拆（为后端或更好融合）；融合 = 合（减 launch 与中间读写）；方向相反。
2. 先 decompose 当后端无实现或拆开能更好融合；不拆当有现成融合实现或拆了融不回来。
3. Pipeline 常为 legalize（含 decompose）→ fusion；可多轮，边界由规则与顺序定。

[返回模块](./README.md) | [返回总览](../README.md)
