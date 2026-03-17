# 第 287 题：实现一个`rate limiter`？`token bucket` vs `leaky bucket`？

## 题目

实现一个`rate limiter`？`token bucket` vs `leaky bucket`？

---

## 完整讲解

### 一、Rate limiter 目的

限制请求速率，防止过载、保证公平或满足上游配额。常见策略：**固定窗口**、**滑动窗口**、**token bucket**、**leaky bucket**。实现时需考虑并发、分布式下多实例的协同（如用 Redis 做共享计数）。

### 二、Token bucket vs Leaky bucket

**Token bucket**：桶里放「令牌」，以固定速率补充；请求消耗若干令牌，无令牌则拒绝或等待。允许**突发**（桶满时一段时间可高吞吐），适合「平均速率限制、允许短时突发」的场景。**Leaky bucket**：请求进桶，以固定速率「漏出」被处理；超出桶容量则拒绝或排队。**平滑输出**、不允许多余突发，适合「输出速率严格恒定」的场景。二者可互相近似（如 leaky 的「漏率」对应 token 的「补充率」），侧重点不同。

### 三、实现要点

Token bucket：记录 last_time、tokens；每次请求时按时间差补令牌、扣减；需加锁或原子操作。Leaky bucket：记录 last_time、水位；按漏率更新水位再判断是否接受。分布式时用 Redis 的计数器 + 时间窗口或 Lua 脚本保证原子性。

---

## 面试要点

- Rate limiter 限制请求速率；策略有固定/滑动窗口、token bucket、leaky bucket。
- Token bucket：令牌按速率补充、请求消耗；允许突发；适合平均限速。
- Leaky bucket：请求入桶、按固定速率漏出；输出平滑、限制突发。
- 实现：记录时间与容量/令牌；并发用锁或原子；分布式用 Redis 等。

---

## 记忆要点

1. Token bucket = 令牌补充 + 消耗；允突发。Leaky bucket = 入桶 + 固定漏率；平滑输出。
2. 实现：last_time + tokens/水位；按时间更新再判断。
3. 分布式用共享存储（如 Redis）做计数与原子性。

[返回模块](./README.md) | [返回总览](../README.md)
