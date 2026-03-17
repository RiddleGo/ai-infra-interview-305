# 第 273 题：Python的`memory profiler`使用？`tracemalloc`？

## 题目

Python的`memory profiler`使用？`tracemalloc`？

---

## 完整讲解

### 一、内存分析需求

Python 动态分配、引用计数与 GC，内存泄漏或大对象常需定位「谁在占用」。**memory profiler** 用于统计各函数/行分配量、追踪对象增长，便于发现泄漏与优化大结构。

### 二、tracemalloc 使用

**tracemalloc**（标准库，Python 3.4+）可追踪**分配来源**（文件名、行号）。`tracemalloc.start()` 开启；`tracemalloc.get_traced_memory()` 得当前 traced 内存；`tracemalloc.get_tracemalloc_memory()` 得 tracemalloc 自身开销；`tracemalloc.get_object_traceback(obj)` 可查某对象分配处。`snapshot = tracemalloc.take_snapshot()` 后对 `snapshot.statistics('lineno')` 排序可看分配最多的行。

### 三、其他工具与注意

**memory_profiler** 包：`@profile` 装饰器或 `mprof run` 做逐行内存占用；与 tracemalloc 互补（一个看行级、一个看调用栈/对象）。生产环境 tracemalloc 有开销，可按需开启或采样。

---

## 面试要点

- 内存分析：定位泄漏、大对象；常用 tracemalloc（标准库）与 memory_profiler。
- tracemalloc：start → take_snapshot → statistics('lineno') 看分配最多的行；get_object_traceback 查对象分配处。
- memory_profiler：@profile 或 mprof 做逐行内存；可和 tracemalloc 配合。
- tracemalloc 有运行时开销，生产可按需或采样开启。

---

## 记忆要点

1. tracemalloc = 标准库、追踪分配来源（文件/行）；snapshot + statistics。
2. memory_profiler = 逐行内存；@profile / mprof。
3. 分析泄漏看增长与引用；注意 tracemalloc 开销。

[返回模块](./README.md) | [返回总览](../README.md)
