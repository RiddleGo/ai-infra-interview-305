# 第 276 题：`context manager`的`__enter__`和`__exit__`？

## 题目

`context manager`的`__enter__`和`__exit__`？

---

## 完整讲解

### 一、Context Manager 协议

**Context manager** 支持 `with` 语句，保证「进入时设、退出时清」。协议：实现 `__enter__(self)` 和 `__exit__(self, exc_type, exc_val, exc_tb)`。`with obj:` 时先调 `__enter__`，其返回值赋给 `as` 目标；离开 with 块时调 `__exit__`（含异常时三个参数非 None）。

### 二、__enter__ 与 __exit__ 语义

`__enter__`：做资源申请或状态设置，返回给 `as` 的可为 self 或其它对象。`__exit__`：做清理（关文件、释锁、回滚等）；若返回 **True** 表示「已处理异常」，解释器不再传播；返回 False 或 None 则异常继续向上抛。若 with 块内无异常，`__exit__` 的三个异常参数均为 None。

### 三、实现方式

类实现上述两方法即可；或用 **contextlib.contextmanager** 写生成器：`yield` 前为 enter、后为 exit，用 `try/finally` 保证清理。常用于文件、锁、连接、临时状态等。

---

## 面试要点

- Context manager 协议：__enter__（进入时调，返回值给 as）、__exit__（退出时调，异常信息传入）。
- __exit__ 返回 True 表示吞掉异常；False/None 则异常继续传播。
- 可用类实现两方法，或用 contextlib.contextmanager + 生成器（yield 前后即 enter/exit）。
- 用于文件、锁、连接等「进设退清」场景。

---

## 记忆要点

1. __enter__ = 进入时调；__exit__ = 退出时调，可接收异常。
2. __exit__ 返回 True 吞异常；用 try/finally 保证清理。
3. 类实现协议或 contextmanager + 生成器。

[返回模块](./README.md) | [返回总览](../README.md)
