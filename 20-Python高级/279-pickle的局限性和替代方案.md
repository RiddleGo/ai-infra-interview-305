# 第 279 题：`pickle`的局限性和替代方案？`cloudpickle`、`dill`？

## 题目

`pickle`的局限性和替代方案？`cloudpickle`、`dill`？

---

## 完整讲解

### 一、pickle 的局限性

**pickle** 是 Python 原生序列化，仅适合 Python 间传对象。局限：**不安全**，反序列化会执行任意代码，不可反序列化不可信数据；**仅 Python**，其它语言无法读；**版本/类路径依赖**，类定义变更或移动可能导致无法反序列化；**不能序列化** 函数、lambda、某些 C 扩展、含不可序列化引用的对象等。

### 二、cloudpickle、dill 等替代

**cloudpickle**：可序列化更多对象（如 lambda、嵌套函数、某些类），常用于分布式计算（如 Dask、Ray）在 worker 间传任务。**dill**：扩展更多类型（含更多函数、模块状态等），适合持久化复杂状态。二者 API 与 pickle 类似（dump/load、协议版本）；仍**仅限 Python 且需同环境**，安全性与 pickle 类似，不可信数据勿用。

### 三、跨语言与安全场景

跨语言用 **JSON、MessagePack、Protobuf** 等；需安全反序列化则避免 pickle，用白名单结构或专用格式。

---

## 面试要点

- pickle 局限：不安全（反序列化可执行代码）、仅 Python、版本/类路径敏感、不能序列化函数等。
- cloudpickle：支持 lambda、嵌套函数等，常用于 Dask/Ray 等分布式传任务。
- dill：支持更多类型与状态；仍仅 Python、不安全。
- 跨语言用 JSON/Protobuf；不可信数据不用 pickle。

---

## 记忆要点

1. pickle 不安全、仅 Python、不能序列化函数/lambda 等。
2. cloudpickle/dill 扩展可序列化类型；分布式与持久化常用。
3. 跨语言与安全场景用 JSON/Protobuf 等。

[返回模块](./README.md) | [返回总览](../README.md)
