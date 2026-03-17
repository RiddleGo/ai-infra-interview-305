# -*- coding: utf-8 -*-
"""Generate 23 module READMEs and 305 question .md files for AI Infra 面经 305 题."""
import os

BASE = os.path.dirname(os.path.abspath(__file__))

MODULES = [
    ("01-PyTorch底层", 1, 15),
    ("02-TensorFlow与XLA", 16, 20),
    ("03-自定义算子开发", 21, 30),
    ("04-编译器优化", 31, 45),
    ("05-数据并行", 46, 60),
    ("06-模型并行与流水线", 61, 75),
    ("07-显存优化与Offload", 76, 85),
    ("08-通信优化", 86, 95),
    ("09-推理引擎", 96, 115),
    ("10-量化与压缩", 116, 130),
    ("11-服务化与调度", 131, 145),
    ("12-训练框架", 146, 160),
    ("13-存储与IO", 161, 170),
    ("14-集群调度", 171, 180),
    ("15-性能分析工具", 181, 195),
    ("16-优化技术", 196, 215),
    ("17-训练平台设计", 216, 235),
    ("18-推理平台设计", 236, 255),
    ("19-CPP与CUDA编程", 256, 270),
    ("20-Python高级", 271, 280),
    ("21-算法与数据结构", 281, 290),
    ("22-网络", 291, 300),
    ("23-存储与虚拟化", 301, 305),
]

def get_module_for_num(n):
    for folder, low, high in MODULES:
        if low <= n <= high:
            return folder
    return None

def write_md(mod_dir, num, q, slug):
    path = os.path.join(BASE, mod_dir, f"{num:03d}-{slug}.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    title_short = (q[:60] + "…") if len(q) > 60 else q
    content = f"""# 第 {num} 题：{title_short}

## 题目

{q}

---

## 完整讲解

（待补充：本题的完整原理、实现要点与工程经验。）

---

## 面试要点

- 

---

## 记忆要点

- 

[返回模块](./README.md) | [返回总览](../README.md)
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    from questions_data import QUESTIONS
    from slug_titles import get_slugs
    slugs = get_slugs()
    assert len(slugs) == len(QUESTIONS)
    for folder, low, high in MODULES:
        mod_path = os.path.join(BASE, folder)
        os.makedirs(mod_path, exist_ok=True)
        rows = []
        for n in range(low, high + 1):
            if n <= len(QUESTIONS):
                title = QUESTIONS[n - 1]
                short = (title[:36] + "…") if len(title) > 36 else title
                fn = f"{n:03d}-{slugs[n-1]}.md"
                rows.append(f"| {n} | {short} | [{fn}](./{fn}) |")
        table = "\n".join(rows)
        readme = f"""# {folder}（第 {low}–{high} 题）

| 题号 | 主题 | 文章 |
|------|------|------|
{table}

[返回总览](../README.md)
"""
        with open(os.path.join(mod_path, "README.md"), "w", encoding="utf-8") as f:
            f.write(readme)
    for num in range(1, len(QUESTIONS) + 1):
        mod_dir = get_module_for_num(num)
        if mod_dir:
            write_md(mod_dir, num, QUESTIONS[num - 1], slugs[num - 1])
    print("Done: 23 READMEs + 305 .md files (NNN-题目简称.md)")

if __name__ == "__main__":
    main()
