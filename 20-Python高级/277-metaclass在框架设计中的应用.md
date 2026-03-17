# 第 277 题：`metaclass`在框架设计中的应用？`abc.ABCMeta`？

## 题目

`metaclass`在框架设计中的应用？`abc.ABCMeta`？

---

## 完整讲解

### 一、Metaclass 是什么

**Metaclass** 是「类的类」：类由 type 或其子类实例化得到，该子类即 metaclass。定义类时指定 `metaclass=MyMeta`，则类对象的创建由 `MyMeta.__new__`/`__init__` 控制，可在**类创建时**注册、校验、注入属性或改继承关系，实现框架级行为。

### 二、在框架设计中的应用

**插件/注册**：metaclass 在类定义时把类注册到全局表。**接口约束**：要求子类实现某些方法，未实现则在类创建时报错。**abc.ABCMeta**：抽象基类用 ABCMeta 作为 metaclass，配合 `@abstractmethod`，子类未实现抽象方法则无法实例化。**ORM/声明式 API**：类属性（如列名）在 metaclass 里被收集成 schema。

### 三、abc.ABCMeta

`from abc import ABC, abstractmethod`；继承 ABC（其 metaclass 为 ABCMeta）并给方法加 `@abstractmethod`，则子类必须实现这些方法否则不能实例化。ABCMeta 还支持 `register` 做结构性子类型（duck typing 注册）。

---

## 面试要点

- Metaclass = 类的类；控制类的创建（__new__/__init__），在「定义时」执行逻辑。
- 应用：插件注册、接口校验、抽象基类、ORM 声明式收集属性。
- abc.ABCMeta：抽象基类；@abstractmethod 强制子类实现；register 做结构性子类型。
- 框架里少而精地用，避免过度魔法。

---

## 记忆要点

1. Metaclass 控制类对象的创建；用于注册、校验、抽象基类。
2. ABCMeta + @abstractmethod = 抽象方法、子类必须实现。
3. 框架中用于声明式行为；不宜滥用。

[返回模块](./README.md) | [返回总览](../README.md)
