# 第 242 题：长文本生成的`streaming`实现？`Server-Sent Events`？

## 题目

长文本生成的`streaming`实现？`Server-Sent Events`？

---

## 完整讲解

### 一、长文本生成的流式需求

**长文本生成**（如大模型对话、摘要）：**逐 token 输出**，若等**全部生成完再返回**，**首包延迟** 高、用户体验差。**流式**：每生成若干 token 就 **立即推给客户端**，降低 **TTFT**（Time To First Token）感知、提升体验。

### 二、Server-Sent Events（SSE）

**SSE**：**HTTP 长连接**，服务端 **单向** 向客户端 **持续推送** 文本事件（event stream）。**格式**：`Content-Type: text/event-stream`；每条为 `data: ...\n\n`。**优点**：**简单、基于 HTTP**，易与现有网关与前端集成；**自动重连**（浏览器 EventSource）。**适用**：**流式生成**— 每生成一段就 `data: chunk` 推送；客户端边收边展示。**与 WebSocket**：SSE 单向、HTTP；WebSocket 双向、独立协议；若只需「服务端推生成结果」SSE 足够。

### 三、实现要点

**后端**：推理引擎 **流式输出**（如 vLLM 的 streaming、OpenAI 兼容的 stream=True）；**每 token 或每 N token** 通过 **SSE** 写回。**超时与断开**：长连接需设 **keepalive、超时**；客户端断线时服务端应 **停止生成** 或做清理。**网关**：需支持 **流式透传**（不缓冲整响应）；**负载均衡** 在流式场景下通常 **sticky** 到同一实例。
---

## 面试要点

- 长文本生成流式：边生成边返回，降低 TTFT、提升体验；常用 SSE。
- SSE：HTTP 长连接、服务端单向推送；Content-Type: text/event-stream；简单易集成。
- 后端流式输出 + SSE 写回；超时与断开清理；网关流式透传、sticky。

---

## 记忆要点

1. 流式 = 边生成边返回；SSE = HTTP 单向推送。
2. text/event-stream；data: chunk。
3. 超时、断开清理；网关透传、sticky。

[返回模块](./README.md) | [返回总览](../README.md)
