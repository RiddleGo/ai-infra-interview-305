# 第 52 题：梯度累积（gradient accumulation）在DDP中的正确实现方式？

## 题目

梯度累积（gradient accumulation）在DDP中的正确实现方式？

---

## 完整讲解

### 一、梯度累积的目的

想用 **大 effective batch size**，但单次 forward/backward 显存放不下那么大 batch，就**分多步**算：每步小 batch forward+backward，**不立刻 step**，梯度**累加**在 `.grad` 里；累加够 K 步后**再 optimizer.step()** 并 **zero_grad()**。Effective batch = 单步 batch × K。

---

### 二、DDP 下的正确方式

- **每步**：`loss = model(x) / K`（或 loss 不除 K、step 前对梯度除 K），`loss.backward()`。DDP 会对**当前步**的梯度做 all-reduce，所以**每步 backward 后每卡的梯度已经是「当前步的全局梯度」**。
- **累积**：**不要**在梯度累积的中间步调 `optimizer.zero_grad()`；只在**第 1 步前** zero_grad，然后 K 步内只 backward，梯度会**自动累加**（PyTorch 默认 `grad += 新梯度`）。
- **Step**：第 K 步 backward 后，若 loss 没除 K，要对梯度 **÷K**（或 optimizer 的 lr 等价成 lr/K），再 `optimizer.step()`，然后 `optimizer.zero_grad()` 为下一轮累积做准备。
- **No_sync**：DDP 默认每次 backward 结束都会 all-reduce。梯度累积时**前 K-1 步不需要同步**（只累加本地梯度），可在这几步用 **model.no_sync()** 包住 forward/backward，**最后一步**不用 no_sync，让最后一步 backward 做 all-reduce，此时每卡上的梯度是「K 步累积后的全局梯度」。这样通信量从「K 次 all-reduce」变成「1 次」，正确且更高效。

---

### 三、小结

- 前 K-1 步：`with model.no_sync(): loss.backward()`，不 all-reduce，梯度只在本卡累加。
- 第 K 步：正常 `loss.backward()`，DDP all-reduce；若未对 loss 除 K，则 step 前 `scaler.unscale_()` 后对梯度除 K（或等价方式）。
- 然后 `optimizer.step()`、`zero_grad()`（若用 AMP 还有 `scaler.update()`）。

---

## 面试要点

- 累积 K 步再 step；中间步不 zero_grad；梯度自动累加。
- 前 K-1 步用 **no_sync()** 关掉 all-reduce，最后一步再 all-reduce，通信从 K 次变 1 次。
- Step 前若 loss 未除 K，需对梯度除 K（或调 lr）保证 effective batch 语义。

---

## 记忆要点

1. 前 K-1 步 no_sync()，最后一步正常 backward 做 all-reduce。
2. 中间不 zero_grad；step 后 zero_grad；梯度除 K 或 loss 除 K 二选一。
3. 正确 + 高效 = no_sync 减通信。

[返回模块](./README.md) | [返回总览](../README.md)
