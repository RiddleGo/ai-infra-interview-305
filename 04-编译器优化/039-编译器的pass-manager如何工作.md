# 第 39 题：编译器的pass manager如何工作？`top-down` vs `bottom-up`遍历？

## 题目

编译器的pass manager如何工作？`top-down` vs `bottom-up`遍历？

---

## 完整讲解

### 一、Pass manager 在做什么？

**Pass manager** 负责 **按顺序或条件执行一系列 pass**（每个 pass 对 IR 做分析或变换）：保证 **依赖关系**（如 A pass 在 B 之前）、**失效信息的维护**（某 pass 改了 IR，后续可能依赖的分析要重算或标记失效）、**可选并行**（无依赖的 pass 可并行）。用户或编译器把 pass 注册成 **pipeline**，run 时依次执行，直到得到目标 IR 或完成优化。

### 二、Top-down 与 bottom-up 遍历

- **Top-down**：从 **根/入口** 往 **子节点/后继** 遍历（如从函数到 block 到 op 到 operand）。适合：先处理「外层结构」再处理内层；例如先决定「这个 loop 要不要展开」再处理内部 op。某些分析（如 dominance、CFG）也常从入口向下。
- **Bottom-up**：从 **叶子/无后继** 往 **根** 遍历（如从 use 到 def、从子 region 到父）。适合：先知道「子节点/子区域」的结果再决定父节点；例如 **常量折叠** 要先知道 operand 是否常量（子已算完），再决定当前 op 能否 fold；**指令调度** 有时从 def-use 链底往上排。
- **在 pass 中的应用**：不同 pass 按需求选遍历顺序；有的 pass 内部用 top-down（如 legalization 从外到内），有的用 bottom-up（如 fold、CSE）；PassManager 只保证 pass 之间的顺序，每个 pass 内部可自定遍历。

### 三、与 MLIR/LLVM 的对应

- **MLIR**：PassManager 跑 pass pipeline；遍历 IR 时可按 **region 块**、**op 列表** 做 top-down 或 bottom-up；`walk` 可指定顺序。
- **LLVM**：FunctionPass、ModulePass 等；分析/变换的遍历顺序由各 pass 实现（如 dom tree 先算再 top-down 用）。

---

## 面试要点

- Pass manager：按序/条件执行 pass，管依赖与失效；用户组 pipeline，run 时依次执行。
- Top-down：根→子，先外后内；bottom-up：叶子→根，先子后父（如 fold 需先知道 operand）。
- 不同 pass 按需选遍历；PassManager 管 pass 顺序，单 pass 内可自定 top-down/bottom-up。

---

## 记忆要点

1. Pass manager = 顺序执行 pass、管依赖与失效；pipeline 由用户/编译器注册。
2. Top-down = 根到子；bottom-up = 子到根；fold 等常用 bottom-up。
3. 遍历顺序由各 pass 自定；PassManager 不强制单 pass 内顺序。

[返回模块](./README.md) | [返回总览](../README.md)
