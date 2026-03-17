# 第 6 题：`torch.jit.trace`和`torch.jit.script`的区别？什么情况下会失败？

## 题目

`torch.jit.trace`和`torch.jit.script`的区别？什么情况下会失败？

---

## 完整讲解

### 一、Trace 和 Script 各自在干什么？

- **`torch.jit.trace`**：用**一组具体输入**跑一遍你的 `model.forward`，把实际执行到的算子序列**录成一张静态图**；控制流（if/for）会按「这一轮输入」走的分支被固化成图，不会出现「另一条分支」。输出是 TorchScript 图，可序列化、在 C++ 里跑、做算子融合等。
- **`torch.jit.script`**：**不跑**模型，而是把 Python 源码（函数或 Module）**解析、编译**成 TorchScript 的 IR；if/for 会变成图里的控制流节点，运行时按条件走不同分支。适合控制流多、依赖输入动态变化的逻辑。

一句话：**trace = 用一次运行「拍快照」；script = 把代码「翻译」成图。**

---

### 二、主要区别

| 维度       | trace                          | script                           |
|------------|--------------------------------|----------------------------------|
| 输入       | 需要示例输入，跑一遍            | 不需要运行，解析源码              |
| 控制流     | 固化为当时走的那条分支         | 保留 if/for，图中有控制流        |
| 数据相关   | 与示例输入绑死（如 shape 固定） | 可写动态 shape、动态分支         |
| Python 特性| 只保留执行到的代码             | 受限支持（见下），部分不支持     |

---

### 三、Trace 什么时候会失败或不对？

- **控制流依赖数据**：如 `if x.sum() > 0: ... else: ...`，trace 只录当前输入走的那条分支，换输入可能逻辑错。
- **动态 shape**：trace 时若 shape 固定，图里会写死；换 batch/seq 长可能错或要重新 trace。
- **未执行到的代码**：某分支没被示例输入走到，就不会出现在图里，部署时若走到该分支会缺算子或行为不符。
- **非 Tensor 或复杂 Python**：部分 Python 对象、反射、eval 等无法被记录进图。

---

### 四、Script 什么时候会失败？

- **不支持的 Python 语法**：如部分动态类型、任意 list/dict 操作、字符串操作、反射、open/文件等，TorchScript 的 Python 子集不支持就会报错。
- **类型推断失败**：Script 需要能推断 tensor 类型和 shape；若推断不出或类型不一致会失败。
- **调用了非 script 的代码**：若函数里调了没被 `@torch.jit.script` 的 Python 函数或第三方库，通常无法 script。

---

### 五、实践建议

- 控制流少、shape 较固定、想快速得到一张图：用 **trace**；注意用**有代表性的输入**，并检查不同输入是否仍符合预期。
- 控制流多、依赖输入动态分支：用 **script** 或 **trace + script 混合**（如部分子模块 script，再 trace 整体）；script 不通过时再考虑重写为 TorchScript 支持的写法。
- PyTorch 2.0 后很多场景用 **torch.compile** 替代 JIT，但 trace/script 仍用于导出 ONNX、LibTorch 部署等，面试可提「trace 适合静态、script 适合动态控制流」。

---

## 面试要点

- trace = 用示例输入跑一遍，录成静态图；控制流和 shape 易被固化为那一轮；script = 解析源码成图，保留 if/for。
- trace 失败/不对：数据相关分支、动态 shape、未执行到的代码；script 失败：不支持的 Python 语法、类型推断失败、调了非 script 代码。
- 选型：静态/少分支用 trace；多控制流用 script 或混合。

---

## 记忆要点

1. trace：跑一次录图，控制流和 shape 绑死示例输入；script：解析源码，图里带控制流。
2. trace 坑：数据相关 if、动态 shape、未走到分支；script 坑：语法/类型/非 script 调用。
3. 静态场景 trace，动态分支 script；部署/ONNX 仍常用 trace。

[返回模块](./README.md) | [返回总览](../README.md)
