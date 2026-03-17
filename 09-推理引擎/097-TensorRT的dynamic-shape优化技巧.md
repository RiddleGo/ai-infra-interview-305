# 第 97 题：TensorRT的`dynamic shape`优化技巧？`optimization profile`？

## 题目

TensorRT的`dynamic shape`优化技巧？`optimization profile`？

---

## 完整讲解

### 一、Dynamic Shape 的挑战

输入 shape 在运行时变化（如 batch、seq_len 可变）时，TensorRT 需在 **build 时** 知道范围或若干典型值，才能选 kernel、做融合与显存分配。若完全动态，需用 **dynamic shape API** 与 **optimization profile**。

### 二、Optimization Profile

**Optimization profile**：为 dynamic 维度指定 **min / opt / max**（如 batch=1,8,32；seq=16,128,512）。Builder 会针对 **opt** 做主要优化，并保证 min～max 内均可执行；Runtime 执行时若在范围内则用同一 engine，超出则需多 profile 或重 build。多个 profile 可并存（如不同 batch 段），运行时按当前 shape 选 profile。

### 三、优化技巧

- **opt 选常见/热点 shape**：让 opt 接近线上 P50/P90 的 shape，延迟与吞吐更稳。
- **min/max 不要过宽**：过宽会增大显存与 kernel 通用性，可能牺牲 opt 点性能；按业务上下界设即可。
- **避免不必要的动态维**：能固定的维度（如 feature 维）尽量固定，只对 batch、seq 等必要维开 dynamic。
- **多 profile**：若 min～max 跨度大，可建多个 profile（如小 batch 一个、大 batch 一个），运行时按 shape 选，比单一大 range 更高效。

---

## 面试要点

- Dynamic shape 需在 build 时给 min/opt/max；optimization profile 指定各 dynamic 维范围。
- opt 决定主要优化点，选常见 shape；min/max 不过宽，必要时多 profile。
- 能固定的维尽量固定，减少动态维数量。

---

## 记忆要点

1. Optimization profile = min/opt/max；opt 为主优化目标。
2. 范围不过宽；多 profile 可覆盖大跨度。
3. 固定维尽量固定。

[返回模块](./README.md) | [返回总览](../README.md)
