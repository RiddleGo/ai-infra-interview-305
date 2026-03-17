# AI Infra 工程师面经（305 题版）

本专栏为 **AI 基础设施 / 机器学习系统** 方向面试与知识体系整理，覆盖：PyTorch 底层、TensorFlow/XLA、自定义算子、编译器、数据/模型/流水线并行、显存与通信、推理引擎、量化、服务化与调度、训练/推理平台设计、C++/CUDA、Python、算法与网络、存储与虚拟化等。

每篇文章包含：**完整讲解** + **面试要点** + **记忆要点**。

---

## 先读导读（推荐）

- **[305 题漫游指南：从 PyTorch 底层到集群调度的一天](./305题漫游指南.md)** — 按「一天搞懂 AI Infra」的主线串起 305 题，文中链接可点击跳转到对应题目。

---

## 目录结构

| 模块 | 题号 | 说明 |
|------|------|------|
| [PyTorch 底层](./01-PyTorch底层) | 1–15 | Autograd、Module、Dispatch、CUDA 算子、内存池、JIT、DDP/FSDP、torch.compile、hook、QAT、checkpoint、AMP、profiler |
| [TensorFlow/XLA](./02-TensorFlow与XLA) | 16–20 | XLA 优化、tf.function、HLO IR、SavedModel、TF Serving |
| [自定义算子开发](./03-自定义算子开发) | 21–30 | CUDA vector add、Triton、融合算子、CUTLASS、memory coalescing、Nsight、warp divergence、PagedAttention |
| [编译器优化](./04-编译器优化) | 31–45 | TVM、MLIR、Inductor、ONNX、TensorRT、loop tiling、PTQ/QAT、sparsity、pass manager、control flow |
| [数据并行](./05-数据并行) | 46–60 | DDP、FSDP、ZeRO、梯度累积、SyncBatchNorm、NCCL、梯度压缩 |
| [模型并行与流水线](./06-模型并行与流水线) | 61–75 | TP、PP、bubble、1F1B、3D 并行、序列并行、MoE、Zero Bubble |
| [显存优化与 Offload](./07-显存优化与Offload) | 76–85 | ZeRO-Offload、DeepSpeed-Infinity、checkpoint、碎片、显存估算 |
| [通信优化](./08-通信优化) | 86–95 | NCCL Tree/Ring、all-reduce、NVLink/IB、overlap、RDMA |
| [推理引擎](./09-推理引擎) | 96–115 | TensorRT、vLLM、TGI、llama.cpp、batching、延迟、多 stream |
| [量化与压缩](./10-量化与压缩) | 116–130 | INT8、SmoothQuant、AWQ、GPTQ、GGUF、FP8、校准、剪枝 |
| [服务化与调度](./11-服务化与调度) | 131–145 | Triton、K8s、MIG、priority、health check、gRPC、多租户 |
| [训练框架](./12-训练框架) | 146–160 | Megatron、DeepSpeed、Colossal、FSDP、Accelerate、checkpoint、RLHF、MoE |
| [存储与 IO](./13-存储与IO) | 161–170 | checkpoint 格式、Lustre、caching、DALI、S3 |
| [集群调度](./14-集群调度) | 171–180 | Slurm、Volcano、gang scheduling、preemption、utilization |
| [性能分析工具](./15-性能分析工具) | 181–195 | nvidia-smi、Nsight、PyTorch Profiler、Chrome Trace、perf、scaling efficiency |
| [优化技术](./16-优化技术) | 196–215 | FlashAttention、xFormers、CUDA Graph、arithmetic intensity、LARS/LAMB |
| [训练平台设计](./17-训练平台设计) | 216–235 | 1000 卡平台、scheduler、存储、网络、fault tolerance、CI/CD |
| [推理平台设计](./18-推理平台设计) | 236–255 | 10 万 QPS、auto-scaling、routing、streaming、A/B、latency SLO |
| [C++/CUDA 编程](./19-CPP与CUDA编程) | 256–270 | memory pool、shared memory、ring buffer、stream、CUTLASS、NCCL、CUDA Graph |
| [Python 高级](./20-Python高级) | 271–280 | GIL、asyncio、Cython、pybind11、descriptor、metaclass |
| [算法与数据结构](./21-算法与数据结构) | 281–290 | LRU、external sort、consistent hashing、bloom filter、rate limiter |
| [网络](./22-网络) | 291–300 | TCP/RDMA、InfiniBand、RoCE、NCCL、fat-tree、DPDK |
| [存储与虚拟化](./23-存储与虚拟化) | 301–305 | containerd、CNI、GPU 虚拟化、CSI、etcd |

---

## 使用方式

- 按题号在对应模块下查找文章（文件名 `001.md`～`305.md`）。
- 每篇文章含 **完整讲解 + 面试要点 + 记忆要点**。
- 建议搭配 [305 题漫游指南](./305题漫游指南.md) 按主题线通读后再精刷。

---

*共 305 题，覆盖 AI Infra 全栈。*
