# 05-数据并行（第 46–60 题）

| 题号 | 主题 | 文章 |
|------|------|------|
| 46 | DDP的`gradient bucketing`机制是什么？bucket… | [046-DDP的gradient-bucketing机制是什么.md](./046-DDP的gradient-bucketing机制是什么.md) |
| 47 | DDP的`find_unused_parameters`参数什么时候需要… | [047-DDP的find_unused_parameters参数什么时候需要设置.md](./047-DDP的find_unused_parameters参数什么时候需要设置.md) |
| 48 | FSDP的`sharding strategy`有哪些？`FULL_SH… | [048-FSDP的sharding-strategy有哪些.md](./048-FSDP的sharding-strategy有哪些.md) |
| 49 | FSDP的`auto_wrap_policy`如何配置？`size_ba… | [049-FSDP的auto_wrap_policy如何配置.md](./049-FSDP的auto_wrap_policy如何配置.md) |
| 50 | DeepSpeed的ZeRO-1/2/3分别offload了什么？显存节… | [050-DeepSpeed的ZeRO-1-2-3分别offload了什么.md](./050-DeepSpeed的ZeRO-1-2-3分别offload了什么.md) |
| 51 | 混合精度训练中的`loss scaling`在分布式场景下如何处理？ | [051-混合精度训练中的loss-scaling在分布式场景下如何处理.md](./051-混合精度训练中的loss-scaling在分布式场景下如何处理.md) |
| 52 | 梯度累积（gradient accumulation）在DDP中的正确实… | [052-梯度累积（gradient-accumulation）在DDP中的正确实现方.md](./052-梯度累积（gradient-accumulation）在DDP中的正确实现方.md) |
| 53 | 分布式sampler如何保证每个epoch的数据不重复？ | [053-分布式sampler如何保证每个epoch的数据不重复.md](./053-分布式sampler如何保证每个epoch的数据不重复.md) |
| 54 | DDP的`SyncBatchNorm`原理？什么时候必须用？ | [054-DDP的SyncBatchNorm原理.md](./054-DDP的SyncBatchNorm原理.md) |
| 55 | 如何排查分布式训练中的hang问题？`NCCL_DEBUG=INFO`的… | [055-如何排查分布式训练中的hang问题.md](./055-如何排查分布式训练中的hang问题.md) |
| 56 | DDP的`torchrun`和`mp.spawn`启动方式的区别？ | [056-DDP的torchrun和mp.spawn启动方式的区别.md](./056-DDP的torchrun和mp.spawn启动方式的区别.md) |
| 57 | 多机多卡训练时，如何设置`NCCL_SOCKET_IFNAME`和`NC… | [057-多机多卡训练时，如何设置NCCL_SOCKET_IFNAME和NCCL_IB.md](./057-多机多卡训练时，如何设置NCCL_SOCKET_IFNAME和NCCL_IB.md) |
| 58 | 梯度压缩（gradient compression）的方法有哪些？`fp… | [058-梯度压缩（gradient-compression）的方法有哪些.md](./058-梯度压缩（gradient-compression）的方法有哪些.md) |
| 59 | 异步训练（如`Hogwild!`）在工业界为什么很少用？ | [059-异步训练（如Hogwild!）在工业界为什么很少用.md](./059-异步训练（如Hogwild!）在工业界为什么很少用.md) |
| 60 | 如何实现自定义的分布式优化器？继承`torch.optim.Optimi… | [060-如何实现自定义的分布式优化器.md](./060-如何实现自定义的分布式优化器.md) |

[返回总览](../README.md)
