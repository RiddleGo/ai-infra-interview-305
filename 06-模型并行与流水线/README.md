# 06-模型并行与流水线（第 61–75 题）

| 题号 | 主题 | 文章 |
|------|------|------|
| 61 | Tensor Parallelism（TP）的`fused attent… | [061-Tensor-Parallelism（TP）的fused-attention.md](./061-Tensor-Parallelism（TP）的fused-attention.md) |
| 62 | Megatron-LM的`column parallel`和`row p… | [062-Megatron-LM的column-parallel和row-parall.md](./062-Megatron-LM的column-parallel和row-parall.md) |
| 63 | Pipeline Parallelism（PP）的`bubble`问题如… | [063-Pipeline-Parallelism（PP）的bubble问题如何量化.md](./063-Pipeline-Parallelism（PP）的bubble问题如何量化.md) |
| 64 | `interleaved pipeline`（如Megatron的1F1… | [064-interleaved-pipeline（如Megatron的1F1B）如何.md](./064-interleaved-pipeline（如Megatron的1F1B）如何.md) |
| 65 | 激活重计算（activation checkpointing）在PP中的… | [065-激活重计算（activation-checkpointing）在PP中的特殊.md](./065-激活重计算（activation-checkpointing）在PP中的特殊.md) |
| 66 | 如何平衡TP、PP、DP的维度划分？以175B模型为例 | [066-如何平衡TP、PP、DP的维度划分.md](./066-如何平衡TP、PP、DP的维度划分.md) |
| 67 | `torch.distributed.pipeline.sync.Pip… | [067-torch.distributed.pipeline.sync.Pipe的使.md](./067-torch.distributed.pipeline.sync.Pipe的使.md) |
| 68 | 模型并行中的`all-gather`和`reduce-scatter`通… | [068-模型并行中的all-gather和reduce-scatter通信模式.md](./068-模型并行中的all-gather和reduce-scatter通信模式.md) |
| 69 | 流水线并行中的`micro-batch`大小如何影响吞吐？ | [069-流水线并行中的micro-batch大小如何影响吞吐.md](./069-流水线并行中的micro-batch大小如何影响吞吐.md) |
| 70 | 如何处理PP中的负载不均衡？`recompute`和`no-recomp… | [070-如何处理PP中的负载不均衡.md](./070-如何处理PP中的负载不均衡.md) |
| 71 | 3D并行（3D parallelism）的通信复杂度分析？ | [071-3D并行（3D-parallelism）的通信复杂度分析.md](./071-3D并行（3D-parallelism）的通信复杂度分析.md) |
| 72 | 序列并行（Sequence Parallelism）在长文本训练中的应用… | [072-序列并行（Sequence-Parallelism）在长文本训练中的应用.md](./072-序列并行（Sequence-Parallelism）在长文本训练中的应用.md) |
| 73 | Expert Parallelism在MoE模型中的all-to-all… | [073-Expert-Parallelism在MoE模型中的all-to-all通信.md](./073-Expert-Parallelism在MoE模型中的all-to-all通信.md) |
| 74 | 零气泡流水线（Zero Bubble）的最新进展？ | [074-零气泡流水线（Zero-Bubble）的最新进展.md](./074-零气泡流水线（Zero-Bubble）的最新进展.md) |
| 75 | 如何profile分布式训练的通信开销？`torch.profiler`… | [075-如何profile分布式训练的通信开销.md](./075-如何profile分布式训练的通信开销.md) |

[返回总览](../README.md)
