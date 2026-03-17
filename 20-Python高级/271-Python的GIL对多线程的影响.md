# 第 271 题：Python的`GIL`对多线程的影响？`multiprocessing` vs `threading`？

## 题目

Python的`GIL`对多线程的影响？`multiprocessing` vs `threading`？

---

## 完整讲解

### 一、GIL 是什么

**GIL**（Global Interpreter Lock）是 CPython 中一把进程级互斥锁，同一时刻只允许一个线程执行 Python 字节码。目的是保护解释器内部状态（如引用计数）一致，但导致**多线程无法并行执行 Python 代码**，多核 CPU 上多线程只能交替执行。

### 二、对多线程的影响

**CPU 密集型**：多线程几乎无法提速，甚至因切换与锁竞争变慢；应改用 **multiprocessing** 多进程，每进程独立解释器、各自有 GIL。**IO 密集型**：线程在等待 IO 时会释放 GIL，多线程可重叠 IO 与计算，threading 仍有价值；也可用 **asyncio** 单线程并发 IO。

### 三、multiprocessing vs threading

**threading**：共享内存、轻量，受 GIL 限制，适合 IO 密集或需共享状态的场景。**multiprocessing**：多进程、无 GIL 限制、可真并行，适合 CPU 密集；进程间通信用 Queue、Pipe 等，数据需可序列化。选型：CPU 密集用 multiprocessing；IO 密集用 threading 或 asyncio。

---

## 面试要点

- GIL：CPython 进程级锁，同一时刻仅一线程执行字节码；多线程无法并行执行 Python。
- CPU 密集：多线程几乎不加速，用 multiprocessing；IO 密集：线程在 IO 时释放 GIL，threading 有用。
- multiprocessing = 多进程、无 GIL、真并行；threading = 轻量、共享内存、受 GIL 限制。
- 选型：CPU 密集用进程；IO 密集用线程或 asyncio。

---

## 记忆要点

1. GIL 导致多线程不能并行执行 Python 字节码。
2. CPU 密集用 multiprocessing；IO 密集用 threading 或 asyncio。
3. 进程间不共享内存、需序列化；线程共享内存、受 GIL 限制。

[返回模块](./README.md) | [返回总览](../README.md)
