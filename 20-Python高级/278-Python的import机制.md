# 第 278 题：Python的`import`机制？`sys.path`、`PYTHONPATH`？

## 题目

Python的`import`机制？`sys.path`、`PYTHONPATH`？

---

## 完整讲解

### 一、import 机制简述

`import foo` 或 `from foo import bar` 时，解释器在 **sys.modules** 查是否已加载；若无则按 **查找路径** 找 foo 对应模块（包或 .py），加载并执行、将结果放入 sys.modules，再绑定到当前命名空间。查找路径来自 **sys.path**：脚本所在目录、PYTHONPATH、标准库、site-packages 等。

### 二、sys.path 与 PYTHONPATH

**sys.path** 是字符串列表，为模块搜索路径的先后顺序。默认包含：当前脚本目录、环境变量 **PYTHONPATH**（若设）、安装的 prefix 下的 lib 等。修改 sys.path（如 append 项目根）可临时加入搜索路径；**PYTHONPATH** 在进程启动前设置，影响所有 import。包内相对 import 用 `from . import xxx`，依赖包结构。

### 三、工程注意

虚拟环境会改 sys.path 的 prefix；打包/部署需保证 PYTHONPATH 或 sys.path 含项目与依赖。避免在代码里随意改 sys.path，优先用包结构或安装为包。

---

## 面试要点

- import 先查 sys.modules；未则按 sys.path 找模块文件，加载后放入 sys.modules。
- sys.path：脚本目录、PYTHONPATH、标准库、site-packages 等；顺序即查找顺序。
- PYTHONPATH 在启动前设，影响全局；可临时 append sys.path 但不推荐滥用。
- 包内用相对 import（. 表示当前包）；虚拟环境会改 path prefix。

---

## 记忆要点

1. 查找顺序：sys.modules → sys.path 列表。
2. sys.path 含当前目录、PYTHONPATH、标准库、site-packages。
3. 改路径优先用包结构与安装；少改 sys.path。

[返回模块](./README.md) | [返回总览](../README.md)
