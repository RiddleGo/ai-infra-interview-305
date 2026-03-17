# 第 227 题：训练任务的`dry-run`和`profiling`模式？

## 题目

训练任务的`dry-run`和`profiling`模式？

---

## 完整讲解

### 一、Dry-run 模式

**Dry-run**：**不真正跑训练**，只做 **资源配置校验、依赖检查、启动命令与环境模拟**。例如：检查 **GPU/节点数** 是否满足、**镜像与数据路径** 是否存在、**启动脚本** 能否解析 rank/world_size；可 **打印** 将要执行的命令与 env，便于用户确认。用于 **提交前自检**、**CI 校验**、避免占资源却因配置错误秒挂。

### 二、Profiling 模式

**Profiling 模式**：以 **少量 step 或短时间** 跑训练，**打开 profiler**（PyTorch Profiler、Nsight）采集 **耗时、通信、显存** 等，**不追求收敛**。目的：**性能基线**、**瓶颈定位**、**资源预估**（如显存峰值、建议 GPU 数）。平台可提供「**profiling job 类型**」：自动注入 profiler、限制 step 数、产出 trace 或报告；与正式长训共享同一镜像与配置，仅运行时参数不同。

### 三、与正式任务的衔接

Dry-run 通过后可 **一键转正式**（同一配置、去掉 dry-run 标志）。Profiling 结果可 **回填到 job 模板**（如建议 batch、GPU 数）、或供 **cost model** 做耗时预测；正式任务可引用「某次 profiling job」的配置与建议。
---

## 面试要点

- Dry-run：不跑训练，只校验资源、依赖、命令与环境；提交前自检、CI。
- Profiling 模式：短时/少 step + profiler，采性能数据；做基线、瓶颈分析、资源预估。
- 与正式任务衔接：dry-run 通过转正式；profiling 结果驱动配置与 cost model。

---

## 记忆要点

1. Dry-run = 校验不执行；Profiling = 短跑 + profiler。
2. Dry-run 查资源、依赖、命令；Profiling 出 trace、显存、建议。
3. 衔接：转正式、配置建议、cost model。

[返回模块](./README.md) | [返回总览](../README.md)
