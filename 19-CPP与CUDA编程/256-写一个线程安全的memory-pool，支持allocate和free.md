# 第 256 题：写一个线程安全的`memory pool`，支持`allocate`和`free`

## 题目

写一个线程安全的`memory pool`，支持`allocate`和`free`

---

## 完整讲解

### 一、目的与接口

内存池预分配大块内存、按块或按 size-class 分配/释放，减少 malloc/free 次数与碎片。接口通常为 `allocate(size)`、`free(ptr)`，多线程并发调用需保证线程安全。

### 二、实现要点

用 **mutex** 或 **spinlock** 保护空闲链表（free list）；按固定块大小或多种 size-class 管理；allocate 从链表取块，free 将块归还。高并发时可做 **per-thread 子池** + 全局 fallback，减少锁竞争与假共享。

### 三、工程经验

大块预分配用 `malloc` 或 `mmap` 一次；注意对齐与元数据开销；生产环境可选用 tcmalloc、jemalloc 等成熟实现。

---

## 面试要点

- 内存池目的：减少 malloc/free 调用与碎片，接口 allocate/free 需线程安全。
- 用 mutex/spinlock 保护 free list；按块或 size-class 管理。
- 高并发可做 per-thread 子池 + 全局 fallback。
- 预分配大块、控制元数据与对齐；可引用 tcmalloc/jemalloc。

---

## 记忆要点

1. 内存池 = 预分配 + free list + 线程安全（锁或 per-thread 子池）。
2. allocate 从链表取、free 归还；注意锁粒度与假共享。
3. 工程上大块预分配、控制开销；复杂场景用现成分配器。

[返回模块](./README.md) | [返回总览](../README.md)
