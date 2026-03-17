# 第 110 题：多stream推理的实现？`CUDA stream`的同步机制？

## 题目

多stream推理的实现？`CUDA stream`的同步机制？

---

## 完整讲解

### 一、多 Stream 推理的目的

**多 stream**：用多条 **CUDA stream** 并行执行多路推理（如多 batch、多请求），使 **kernel 与拷贝** 在时间上重叠，提高 GPU 利用率与吞吐。单 stream 时推理串行；多 stream 时不同 stream 上的 kernel 可被调度器交错执行，**隐藏延迟、填满 GPU**。

### 二、实现要点

- **Stream 分配**：为每个「逻辑并发单元」（如每路 batch、每 worker）分配独立 stream；或维护 stream 池，请求到来时取空闲 stream、执行完归还。
- **依赖与同步**：同一 stream 内顺序执行；**跨 stream** 用 **cudaEventRecord** + **cudaStreamWaitEvent** 表达「A 在 stream1 完成后，stream2 再继续」；避免多 stream 同时写同一显存（需加锁或分 buffer）。
- **与推理引擎结合**：TensorRT/ONNX Runtime 等支持 **enqueue 时传入 stream**；多请求分别 enqueue 到不同 stream，由 CUDA 调度器并行；需保证每个请求的输入/输出 buffer 独立，避免数据竞争。

### 三、同步机制小结

- **cudaStreamSynchronize(stream)**：当前 host 等该 stream 全部完成；会 stall，少用。
- **cudaEventRecord(event, stream)**：在该 stream 上打点；**cudaStreamWaitEvent(other_stream, event)**：另一 stream 等到该 event 再执行。用 event 做 **流间依赖** 即可实现「A 算完再算 B」或「拷贝完再算」，而不必全局 sync。
- **多 stream 推理**：每路请求绑定 stream，用 event 保证「输入就绪→推理→输出就绪」的依赖；host 侧可用 callback 或轮询 event 得知完成。

---

## 面试要点

- 多 stream = 多路推理并行，提高 GPU 利用率；每路独立 stream，buffer 独立。
- 同步：同 stream 内顺序；跨 stream 用 event（Record + WaitEvent），避免全局 sync。
- 推理引擎 enqueue 时传 stream；用 event 表达输入/输出依赖。

---

## 记忆要点

1. 多 stream 并行填满 GPU；每路一线程/stream，buffer 独立。
2. 跨 stream 依赖用 Event（Record + WaitEvent）。
3. 少用 StreamSynchronize，多用 event 精细同步。

[返回模块](./README.md) | [返回总览](../README.md)
