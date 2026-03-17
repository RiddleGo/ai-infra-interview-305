# 第 280 题：Python代码的性能优化？`cProfile`、`line_profiler`？

## 题目

Python代码的性能优化？`cProfile`、`line_profiler`？

---

## 完整讲解

### 一、性能优化思路

先**定位热点**再优化：用 profiler 找耗时函数与调用关系，避免盲目改。常见瓶颈：循环内重复计算、过多小对象分配、IO、算法复杂度。优化手段：算法与数据结构、减少分配、局部用 C 扩展（Cython/pybind11）、并发/异步等。

### 二、cProfile 使用

**cProfile**（标准库）：`cProfile.run('func()')` 或 `python -m cProfile script.py`，输出各函数调用次数与累计时间。按 `cumulative` 看「含子调用」总时间、按 `tottime` 看「不含子调用」自身时间；可 `pstats.Stats` 做排序、过滤。适合找「谁在耗时间」。

### 三、line_profiler 使用

**line_profiler**：逐**行**统计耗时，需对目标函数加 `@profile` 装饰器，用 `kernprof -l -v script.py` 运行，得到每行命中次数与耗时。适合在已知热点函数内进一步定位到具体行。二者结合：cProfile 定函数、line_profiler 定行。

---

## 面试要点

- 先 profiling 再优化；cProfile 看函数级、line_profiler 看行级。
- cProfile：run() 或 -m cProfile；看 cumtime/tottime；pstats 排序过滤。
- line_profiler：@profile + kernprof -l -v；得每行命中与耗时。
- 结合使用：cProfile 找热点函数，line_profiler 找热点行。

---

## 记忆要点

1. cProfile = 函数级统计；cumtime/tottime；找热点函数。
2. line_profiler = 行级；@profile + kernprof；找热点行。
3. 先测再优；算法与数据结构优先，再考虑 C 扩展与并发。

[返回模块](./README.md) | [返回总览](../README.md)
