# 第 274 题：`Cython`和`pybind11`的区别？什么时候用？

## 题目

`Cython`和`pybind11`的区别？什么时候用？

---

## 完整讲解

### 一、Cython 与 pybind11 定位

二者都用于 **Python 调用 C/C++**，提升性能或复用现有 C++ 库。**Cython**：写「类 Python」或带类型的 .pyx，编译成 C 再编成扩展模块；偏「用 Python 语法写扩展」。**pybind11**：在 **C++ 侧**用声明式 API 暴露类型与函数给 Python；偏「在 C++ 项目里加 Python 绑定」。

### 二、区别概览

**Cython**：可只改类型注解、逐步优化；与 NumPy 集成好（typed memoryview）；适合重写热点或包装 C 库。**pybind11**：头文件库、C++11、绑定写法简洁；适合大型 C++ 项目暴露 API、与 STL/自定义类型映射；需写 C++。**性能**：二者都能达到 C/C++ 级；Cython 更易从纯 Python 渐进迁移。

### 三、何时用

已有 C++ 库、主要在 C++ 侧维护 → **pybind11**。从 Python 项目出发、热点循环或需要 NumPy 深度集成 → **Cython**。两者也可混用（如 Cython 调 pybind11 暴露的模块）。

---

## 面试要点

- Cython：写 .pyx、编译成扩展；类 Python 语法、易从 Python 渐进优化；NumPy 友好。
- pybind11：C++ 侧写绑定、声明式 API；适合已有 C++ 项目暴露给 Python。
- 从 Python 出发、热点/NumPy 多用 Cython；从 C++ 出发、大库绑定用 pybind11。
- 性能都可到 C/C++ 级；可按项目主导语言与维护成本选。

---

## 记忆要点

1. Cython = Python 风格写扩展、.pyx；pybind11 = C++ 侧写绑定。
2. 渐进优化、NumPy 多用 Cython；大 C++ 库暴露用 pybind11。
3. 二者可混用；选型看主导语言与维护成本。

[返回模块](./README.md) | [返回总览](../README.md)
