# 第 272 题：`asyncio`在IO密集型任务中的应用？`aiohttp`？

## 题目

`asyncio`在IO密集型任务中的应用？`aiohttp`？

---

## 完整讲解

### 一、asyncio 与 IO 密集型

**asyncio** 是 Python 的异步 IO 框架，单线程内通过**协程 + 事件循环**并发执行多个「可挂起」任务。在等待 IO（网络、磁盘）时挂起当前协程、执行其他协程，从而在**单线程**下实现高并发 IO，无 GIL 并行执行问题（因为主要在等 IO）。

### 二、基本用法

用 `async def` 定义协程，`await` 挂起等待 IO 或其它协程；`asyncio.run(main())` 运行入口。与 aiohttp 结合：`async with aiohttp.ClientSession() as session:` 内用 `session.get(url)` 等异步请求，多任务用 `asyncio.gather()` 并发执行，大量 HTTP 请求时比多线程更轻量、连接数可控。

### 三、aiohttp 与注意

**aiohttp** 提供异步 HTTP client/server；client 侧与 asyncio 配合做高并发爬虫、API 调用等。注意：标准库部分模块仍为同步，在 async 里调用会阻塞事件循环，需用 `run_in_executor` 或选异步库（如 aiofiles）。

---

## 面试要点

- asyncio：单线程协程 + 事件循环，IO 等待时挂起、执行其他协程，适合 IO 密集。
- async/await、asyncio.run、asyncio.gather 为常用写法。
- aiohttp：异步 HTTP；与 asyncio 配合做高并发请求；注意同步调用会阻塞事件循环。
- IO 密集用 asyncio 可省线程、高并发；CPU 密集仍需多进程。

---

## 记忆要点

1. asyncio = 单线程协程 + 事件循环；await 挂起、不占线程。
2. aiohttp = 异步 HTTP；与 asyncio 配合做高并发 client。
3. 同步代码在 async 里会阻塞事件循环；用 run_in_executor 或异步库。

[返回模块](./README.md) | [返回总览](../README.md)
