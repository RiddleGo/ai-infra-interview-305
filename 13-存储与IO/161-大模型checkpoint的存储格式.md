# 第 161 题：大模型checkpoint的存储格式？`safetensors` vs `pytorch.bin`？

## 题目

大模型checkpoint的存储格式？`safetensors` vs `pytorch.bin`？

---

## 完整讲解

### 一、常见 Checkpoint 存储格式

**PyTorch 原生**（`.pt`/`.pth`/`.bin`）：`torch.save(state_dict, path)`，内部为 pickle + 张量二进制，**不安全**——反序列化可执行任意代码，且无校验，易损坏。**safetensors**：Hugging Face 推动的格式，**仅存张量**（无代码）、内存映射友好、带简单校验，**安全**且多语言可读；文件为头信息（shape、dtype、offset）+ 裸张量数据，便于 mmap 与按 key 懒加载。

### 二、safetensors vs pytorch.bin

**安全**：safetensors 不执行代码，适合不可信来源；.bin 反序列化有风险。**加载方式**：safetensors 支持 **mmap**，大文件可映射不一次性读入内存；.bin 通常整文件读入再反序列化。**跨语言**：safetensors 有 Rust/Python 等实现，易被其它栈读取；.bin 强依赖 PyTorch。**体积与速度**：二者张量存储类似；safetensors 头信息紧凑，多 key 时按 key 加载更省内存。生产与开源分发更推荐 safetensors；需兼容旧脚本或仅 PyTorch 时可保留 .bin。

### 三、使用建议

新项目与模型分发用 safetensors；加载大模型时用 `safetensors.torch.load_file(..., device_map="cpu")` 等做懒加载或 mmap，控制内存峰值。

---

## 面试要点

- .bin/.pt：torch.save、pickle+张量，反序列化不安全、无校验；safetensors：仅张量、安全、可 mmap、多语言。
- safetensors 适合不可信来源、大文件 mmap、按 key 加载；.bin 兼容旧脚本。
- 新项目与分发推荐 safetensors；大模型加载用 mmap/懒加载控内存。

---

## 记忆要点

1. .bin = pickle 不安全；safetensors = 安全、mmap、多语言。
2. 大模型加载：safetensors 可 mmap/按 key；.bin 常整文件读入。
3. 推荐 safetensors；兼容时保留 .bin。

[返回模块](./README.md) | [返回总览](../README.md)
