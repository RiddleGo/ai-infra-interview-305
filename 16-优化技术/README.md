# 16-优化技术（第 196–215 题）

| 题号 | 主题 | 文章 |
|------|------|------|
| 196 | `FlashAttention`的`IO-aware`优化原理？`til… | [196-FlashAttention的IO-aware优化原理.md](./196-FlashAttention的IO-aware优化原理.md) |
| 197 | `FlashAttention-2`和`FlashAttention`的… | [197-FlashAttention-2和FlashAttention的改进点.md](./197-FlashAttention-2和FlashAttention的改进点.md) |
| 198 | `xFormers`的`memory_efficient_attenti… | [198-xFormers的memory_efficient_attention使用.md](./198-xFormers的memory_efficient_attention使用.md) |
| 199 | `cuDNN`的`fused attention`如何调用？ | [199-cuDNN的fused-attention如何调用.md](./199-cuDNN的fused-attention如何调用.md) |
| 200 | 算子融合的边界判断？融合后register pressure过高？ | [200-算子融合的边界判断.md](./200-算子融合的边界判断.md) |
| 201 | 内存带宽bound vs 计算bound的判断？`arithmetic … | [201-内存带宽bound-vs-计算bound的判断.md](./201-内存带宽bound-vs-计算bound的判断.md) |
| 202 | `kernel fusion`的手动实现 vs 编译器自动生成？ | [202-kernel-fusion的手动实现-vs-编译器自动生成.md](./202-kernel-fusion的手动实现-vs-编译器自动生成.md) |
| 203 | `CUDA Graph`的捕获和重放？`torch.cuda.make_… | [203-CUDA-Graph的捕获和重放.md](./203-CUDA-Graph的捕获和重放.md) |
| 204 | 动态shape的优化困境？`torch.compile`的`dynami… | [204-动态shape的优化困境.md](./204-动态shape的优化困境.md) |
| 205 | `torch.backends.cudnn.benchmark`的作用和… | [205-torch.backends.cudnn.benchmark的作用和副作用.md](./205-torch.backends.cudnn.benchmark的作用和副作用.md) |
| 206 | CPU offload的`pin_memory`和`non_blocki… | [206-CPU-offload的pin_memory和non_blocking.md](./206-CPU-offload的pin_memory和non_blocking.md) |
| 207 | 数据预处理的`multi-processing`优化？`num_work… | [207-数据预处理的multi-processing优化.md](./207-数据预处理的multi-processing优化.md) |
| 208 | `DALI`的`GPU decoding`和`augmentation`… | [208-DALI的GPU-decoding和augmentation.md](./208-DALI的GPU-decoding和augmentation.md) |
| 209 | 混合精度训练的`numerical stability`问题？ | [209-混合精度训练的numerical-stability问题.md](./209-混合精度训练的numerical-stability问题.md) |
| 210 | `gradient accumulation`的`effective b… | [210-gradient-accumulation的effective-batch-.md](./210-gradient-accumulation的effective-batch-.md) |
| 211 | 大batch训练的`learning rate scaling`规则？ | [211-大batch训练的learning-rate-scaling规则.md](./211-大batch训练的learning-rate-scaling规则.md) |
| 212 | `LARS`、`LAMB`优化器在大batch场景的应用？ | [212-LARS、LAMB优化器在大batch场景的应用.md](./212-LARS、LAMB优化器在大batch场景的应用.md) |
| 213 | 模型并行的`communication hiding`技术？ | [213-模型并行的communication-hiding技术.md](./213-模型并行的communication-hiding技术.md) |
| 214 | `pipeline bubble`的数学分析和优化？ | [214-pipeline-bubble的数学分析和优化.md](./214-pipeline-bubble的数学分析和优化.md) |
| 215 | 稀疏attention的优化？`Sparse Transformer`、… | [215-稀疏attention的优化.md](./215-稀疏attention的优化.md) |

[返回总览](../README.md)
