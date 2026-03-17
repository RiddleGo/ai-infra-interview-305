# 第 19 题：TensorFlow的SavedModel格式和PyTorch的TorchScript对比？

## 题目

TensorFlow的SavedModel格式和PyTorch的TorchScript对比？

---

## 完整讲解

### 一、SavedModel 是什么？

**SavedModel** 是 TensorFlow 的**标准部署格式**：一个目录，包含 **pb 图**（或 MLIR）、**变量/权重**（如 variables/）、**签名**（输入/输出名与 shape）、以及 **assets** 等。支持多 signature（如 predict、train_step），TF Serving、TFLite、TF.js 等都能直接加载；图通常是「已优化、可执行」的静态图，控制流已用 tf.cond/while 等固化。

---

### 二、TorchScript 是什么？

**TorchScript** 是 PyTorch 的**可序列化、可部署**的表示：可以是 **trace 得到的图**（与示例输入绑定的静态图），或 **script 得到的图**（带控制流的 IR）。保存成 `.pt`/`.pts` 文件，在 C++ 的 LibTorch 里用 `torch::jit::load()` 加载、无 Python 运行；也可再转 ONNX。和 eager 的「Python + 动态图」是两套：TorchScript 偏部署与跨语言。

---

### 三、对比

| 维度         | SavedModel                    | TorchScript                          |
|--------------|-------------------------------|---------------------------------------|
| 形态         | 目录（图 + 变量 + 签名）      | 文件（.pt/.pts，图 + 权重）           |
| 图来源       | tf.function / 建图 API        | trace 或 script                       |
| 控制流       | 图内 tf.cond/while            | trace 固化为单分支；script 保留       |
| 多签名       | 原生多 signature              | 一般单入口，可多方法                  |
| 加载环境     | TF runtime、TF Serving 等    | LibTorch C++、或再转 ONNX             |
| 生态         | TF 全栈、TFLite、TF.js        | PyTorch 部署、ONNX、移动端需再转      |

---

### 四、使用场景

- **SavedModel**：TF 模型上线、TF Serving、跨平台（TFLite/TF.js）时用；强调「一份格式、多运行时」。
- **TorchScript**：PyTorch 模型要**无 Python 部署**（C++、移动端）或**转 ONNX 前**的中间表示；trace 适合静态、script 适合带控制流的模型。

---

## 面试要点

- SavedModel = 目录、图+变量+签名、多 signature、TF 生态标准部署格式。
- TorchScript = 序列化图+权重、trace/script 两种、LibTorch 加载无 Python、可转 ONNX。
- 差异：形态、图来源、控制流、多签名、加载方与生态。

---

## 记忆要点

1. SavedModel：目录、多签名、TF 部署与 Serving；TorchScript：文件、trace/script、LibTorch/ONNX。
2. 控制流：SavedModel 图内；TorchScript trace 固化为单分支、script 保留。
3. 选型：TF 栈用 SavedModel；PyTorch 无 Python 部署用 TorchScript 或再转 ONNX。

[返回模块](./README.md) | [返回总览](../README.md)
