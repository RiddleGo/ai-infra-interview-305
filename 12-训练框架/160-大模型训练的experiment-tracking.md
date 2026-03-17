# 第 160 题：大模型训练的`experiment tracking`？`Weights & Biases`、`MLflow`？

## 题目

大模型训练的`experiment tracking`？`Weights & Biases`、`MLflow`？

---

## 完整讲解

### 一、Experiment Tracking 做什么

大模型训练实验多、超参与配置复杂，**实验追踪**记录：每个 run 的 **config**（模型、lr、batch、并行度等）、**metrics**（loss、accuracy、 throughput 等随时间或 step）、**artifacts**（checkpoint、日志、生成样例）、**代码与环境**（git commit、依赖版本），便于对比、复现与选型。

### 二、Weights & Biases（W&B）

**W&B**：云端实验管理，与 PyTorch/TF 等集成简单，`wandb.init()`、`wandb.log(metrics)`、`wandb.save()` 即可上报 config、曲线与文件。支持多 run 对比、表格与可视化、报告与协作；可自建 server 或用其云。适合大规模实验、团队协作与可视化；注意数据与 checkpoint 上传带宽与存储成本。

### 三、MLflow

**MLflow**：开源实验与模型管理，含 **Tracking**（metrics、params、artifacts）、**Projects**（可复现运行）、**Models**（模型注册与部署）。可本地或自建 server，与主流框架集成；适合自托管、合规要求高的场景。与 W&B 相比更偏自建与模型全生命周期；W&B 在可视化与协作上更丰富。

---

## 面试要点

- 实验追踪 = config + metrics + artifacts + 代码/环境；便于对比、复现与选型。
- W&B：云端、集成简单、可视化与协作强；wandb.init/log/save；注意带宽与存储。
- MLflow：开源、Tracking+Projects+Models；可自建、偏模型全生命周期；W&B 偏实验与协作。

---

## 记忆要点

1. 追踪 = config + metrics + artifacts + 可复现；大模型实验必备。
2. W&B = 云端、易集成、可视化好；MLflow = 开源、自建、模型全周期。
3. 选型：要协作与云端用 W&B；要自建与模型注册用 MLflow。

[返回模块](./README.md) | [返回总览](../README.md)
