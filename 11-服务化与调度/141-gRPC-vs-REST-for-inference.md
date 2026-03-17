# 第 141 题：`gRPC` vs `REST` for inference？性能差异和适用场景？

## 题目

`gRPC` vs `REST` for inference？性能差异和适用场景？

---

## 完整讲解

### 一、gRPC vs REST 概览

**REST**：HTTP/JSON（或其它序列化），无状态、易调试、浏览器与 curl 直接支持，生态广。**gRPC**：基于 HTTP/2、默认 Protobuf 二进制，支持流、多路复用、强类型接口，延迟与序列化开销通常更小，但需要 client 库与 IDL 定义。

### 二、性能差异与推理场景

**延迟与吞吐**：gRPC 二进制序列化更小、HTTP/2 多路复用减少连接开销，高 QPS 下通常**延迟更低、吞吐更高**；REST/JSON 序列化与解析成本大，大 payload 时差异明显。**流式**：gRPC 原生双向流，适合长上下文、流式生成（token 级推流）；REST 需 SSE 或 chunked 等，实现与生态略逊。**调试与兼容**：REST 用 curl/Postman 即可；gRPC 需工具或代码，对开放 API、多语言轻量调用更友好的是 REST。

### 三、适用场景

**选 gRPC**：内部推理服务、高 QPS、低延迟、流式生成、多语言强类型契约。**选 REST**：对外 API、需要简单调试、浏览器或脚本直接调用、对延迟不极端敏感。实践中内部多 gRPC，对外或简单调用用 REST；也有网关将 REST 转 gRPC 后端。

---

## 面试要点

- gRPC：HTTP/2 + Protobuf，低延迟、高吞吐、原生流；REST：HTTP/JSON，易调试、兼容好。
- 推理高 QPS、流式生成倾向 gRPC；对外、简单调用、调试友好用 REST。
- 可组合：内部 gRPC、网关对外 REST。

---

## 记忆要点

1. gRPC = 二进制+多路复用+流，性能好；REST = 易调试、兼容广。
2. 推理内部、流式、高 QPS 用 gRPC；对外、简单用 REST。
3. 内部 gRPC + 网关 REST 常见。

[返回模块](./README.md) | [返回总览](../README.md)
