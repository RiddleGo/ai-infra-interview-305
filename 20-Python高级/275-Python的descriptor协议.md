# 第 275 题：Python的`descriptor`协议？`property`的实现？

## 题目

Python的`descriptor`协议？`property`的实现？

---

## 完整讲解

### 一、Descriptor 协议

**Descriptor** 是实现了 `__get__`、`__set__`、`__delete__` 中至少一个的对象。当作为**类属性**被访问时，解释器会调用这些方法：`a.x` 触发 `type(a).__dict__['x'].__get__(a, type(a))`。用于实现 **property、方法绑定、staticmethod、classmethod** 等。

### 二、property 的实现

`property(fget, fset, fdel, doc)` 返回一个 **descriptor**：其 `__get__` 调 fget(instance)、`__set__` 调 fset(instance, value)。即「属性访问」被转成函数调用，从而可做计算、校验、懒加载等。等价于在类里放一个实现 `__get__`/`__set__` 的 descriptor 对象。

### 三、常见用法

用 `@property` 装饰器定义只读或读写「属性」；只读可只写 `__get__`；只写需同时有 `__set__`（少见）。自定义 descriptor 可做类型检查、缓存、懒加载；注意区分**数据 descriptor**（有 `__set__`）与**非数据 descriptor**（仅 `__get__`），前者在实例字典之前参与查找。

---

## 面试要点

- Descriptor：实现 __get__/__set__/__delete__ 的对象；作为类属性时访问会调这些方法。
- property 本质是 descriptor；__get__ 调 getter、__set__ 调 setter。
- 用于计算属性、校验、懒加载；数据 descriptor（有 __set__）优先于实例字典。
- 方法绑定、staticmethod、classmethod 也由 descriptor 实现。

---

## 记忆要点

1. Descriptor = __get__/__set__/__delete__；作为类属性时被调用。
2. property = descriptor，把属性访问转成 getter/setter 调用。
3. 数据 descriptor 优先实例 dict；可做校验、缓存、懒加载。

[返回模块](./README.md) | [返回总览](../README.md)
