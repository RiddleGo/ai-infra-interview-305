# 第 17 题：TF的`tf.function`和PyTorch的`torch.jit`设计理念差异？

## 题目

TF的`tf.function`和PyTorch的`torch.jit`设计理念差异？

---

## 完整讲解

### 一、tf.function 的设计

**tf.function** 把 Python 函数**按执行轨迹 trace 成 TF 图**，之后用**图 + 缓存**执行：相同输入「签名」（如 shape、dtype）走缓存，不同则重新 trace 并缓存。设计偏向「**默认用、透明加速**」：用户加个装饰器，TF 负责 trace、retrace、concrete function 管理；控制流用 **tf.cond/tf.while** 或 **AutoGraph** 转成图内节点，尽量不落回 Python。理念是：**一次定义、多签名缓存、图执行为主。**

---

### 二、torch.jit 的设计

**torch.jit** 提供 **trace** 和 **script** 两种路径：**trace** 用示例输入跑一遍，录成静态图（控制流被固化为当时分支）；**script** 解析 Python 源码编译成 TorchScript IR，保留 if/for。用户通常要**显式**选 trace 或 script，并处理「不支持的语法」「动态 shape」等问题。理念是：**提供两种捕获方式，部署/导出时用，eager 仍是默认开发体验。**

---

### 三、主要差异

| 维度       | tf.function                    | torch.jit                          |
|------------|--------------------------------|-------------------------------------|
| 默认体验   | 装饰即用，图执行透明           | 开发多为 eager，JIT 用于部署/导出   |
| 控制流     | AutoGraph 转图内 cond/while    | trace 固化为单分支；script 保留控制流 |
| 多 signature | 多 concrete function 缓存     | trace 绑死示例 shape；script 更灵活 |
| 与 eager 关系 | 与 eager 互转，可关图执行   | 两套路径，trace/script 与 eager 分离 |
| 生态       | TF 全栈围绕图与 SavedModel    | PyTorch 2.0 更多用 torch.compile   |

---

### 四、一句话概括

**tf.function**：以图为中心，装饰器即可、多签名缓存、控制流进图，透明加速。**torch.jit**：eager 为主，trace/script 两条路显式选，用于导出和部署；PyTorch 2.0 后很多场景用 **torch.compile** 替代 JIT 做训练侧加速。

---

## 面试要点

- tf.function：trace 成图、多 signature 缓存、AutoGraph 处理控制流；透明图执行。
- torch.jit：trace（绑死分支）或 script（保留控制流）；显式、多用于部署/导出。
- 差异：图是否「默认」、控制流进图方式、多 shape 处理；PyTorch 2.0 推 compile 多于 jit。

---

## 记忆要点

1. tf.function = 图为主、透明、多签名；torch.jit = trace/script 二选一、偏部署。
2. 控制流：TF AutoGraph 进图；JIT trace 固化为单分支、script 保留。
3. 当前 PyTorch 训练加速更多用 torch.compile，JIT 仍用于 ONNX/LibTorch 等导出。

[返回模块](./README.md) | [返回总览](../README.md)
