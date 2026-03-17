# -*- coding: utf-8 -*-
"""Rename NNN.md -> NNN-题目简称.md and update all links in READMEs and 漫游指南."""
import os
import re

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

def main():
    from slug_titles import get_slugs
    slugs = get_slugs()
    assert len(slugs) == 305

    # 1) Rename files
    for num in range(1, 306):
        mod_dir = get_module_for_num(num)
        if not mod_dir:
            continue
        old_name = f"{num:03d}.md"
        slug = slugs[num - 1]
        new_name = f"{num:03d}-{slug}.md"
        dir_path = os.path.join(BASE, mod_dir)
        old_path = os.path.join(dir_path, old_name)
        new_path = os.path.join(dir_path, new_name)
        if os.path.isfile(old_path):
            os.rename(old_path, new_path)
            print(f"Renamed {mod_dir}/{old_name} -> {new_name}")

    # 2) Update each module README: replace ](./NNN.md) and [NNN.md] with slug version
    for folder, low, high in MODULES:
        readme_path = os.path.join(BASE, folder, "README.md")
        with open(readme_path, "r", encoding="utf-8") as f:
            text = f.read()
        for n in range(low, high + 1):
            if n > 305:
                break
            old_fn = f"{n:03d}.md"
            new_fn = f"{n:03d}-{slugs[n-1]}.md"
            text = text.replace(f"](./{old_fn})", f"](./{new_fn})")
            text = text.replace(f"[{old_fn}]", f"[{new_fn}]")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Updated {folder}/README.md")

    # 3) Update 漫游指南: replace MODULE/NNN.md with MODULE/NNN-slug.md
    guide_path = os.path.join(BASE, "305题漫游指南.md")
    with open(guide_path, "r", encoding="utf-8") as f:
        text = f.read()
    for folder, low, high in MODULES:
        for n in range(low, high + 1):
            if n > 305:
                break
            old_fn = f"{n:03d}.md"
            new_fn = f"{n:03d}-{slugs[n-1]}.md"
            old_ref = f"{folder}/{old_fn}"
            new_ref = f"{folder}/{new_fn}"
            text = text.replace(old_ref, new_ref)
    with open(guide_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Updated 305题漫游指南.md")

    # 4) Root README if has links
    root_readme = os.path.join(BASE, "README.md")
    with open(root_readme, "r", encoding="utf-8") as f:
        text = f.read()
    for folder, low, high in MODULES:
        for n in range(low, high + 1):
            if n > 305:
                break
            old_ref = f"{folder}/{n:03d}.md"
            new_ref = f"{folder}/{n:03d}-{slugs[n-1]}.md"
            text = text.replace(old_ref, new_ref)
    with open(root_readme, "w", encoding="utf-8") as f:
        f.write(text)
    print("Updated README.md")

    print("Done: all files renamed to NNN-题目简称.md, all links updated.")

if __name__ == "__main__":
    main()
