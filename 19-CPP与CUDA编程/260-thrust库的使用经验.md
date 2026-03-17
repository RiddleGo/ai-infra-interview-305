# 第 260 题：`thrust`库的使用经验？`transform_reduce`？

## 题目

`thrust`库的使用经验？`transform_reduce`？

---

## 完整讲解

### 一、Thrust 简介

Thrust 是 CUDA 自带的 C++ 模板库，提供类似 STL 的接口（vector、transform、reduce、sort 等），在 GPU 上执行。可减少手写 kernel 的工作，适合规则化的数据并行。

### 二、transform_reduce

`thrust::transform_reduce` 先对每个元素做一元/二元 **transform**（如平方、乘权），再对结果做 **reduce**（如 sum）。一次调用完成「映射+归约」，减少 kernel 启动与全局读写。用法：`transform_reduce(itr_begin, itr_end, unary_op, init, binary_reduce_op)`。

### 三、使用经验

用 `thrust::device_vector` 管理显存；迭代器与 host/device 指针配合；复杂算子可自定义 functor。注意 thrust 会占用一定显存与编译时间，简单 kernel 手写有时更可控。

---

## 面试要点

- Thrust = GPU 上的 STL 风格库；vector、transform、reduce、sort 等。
- transform_reduce = 先 transform 再 reduce，一次完成映射+归约。
- device_vector 管理显存；自定义 functor 做复杂逻辑；简单场景可手写 kernel。

---

## 记忆要点

1. Thrust = GPU STL；transform_reduce = transform + reduce 一次完成。
2. 用 device_vector、迭代器；复杂逻辑用 functor。
3. 规则数据并行用 thrust 省事；极简 kernel 可手写。

[返回模块](./README.md) | [返回总览](../README.md)
