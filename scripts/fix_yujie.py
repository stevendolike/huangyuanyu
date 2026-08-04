#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""玉楸药解 OCR 讹字修正：萆薢/槟榔/楝子/萹蓄/茹 + 清理页眉残留（不改变行数）"""
SRC = "/sandbox/workspace/skills/黄元御中医辩证skill/modules/06_yishu_11zhong.md"

with open(SRC, encoding="utf-8") as f:
    lines = f.readlines()

orig = len(lines)
fixes = [
    ("### 草\n", "### 萆薢\n"),          # L37002 草→萆薢
    ("### 楧榔\n", "### 槟榔\n"),        # L37190 楧榔→槟榔
    ("### 棟子\n", "### 楝子\n"),        # L37336 棟子→楝子
    ("### ■ 篇蓄\n", "### ■ 萹蓄\n"),    # L36976 篇蓄→萹蓄
    ("### ■藺茹\n", "### ■茹\n"),        # L36618 藺茹→茹
    ("### 20·\n", "\n"),                 # L37230 页眉残留
    ("### 24 ·\n", "\n"),                # L37414 页眉残留
]

report = []
for old, new in fixes:
    cnt = 0
    for i, l in enumerate(lines):
        if l == old:
            lines[i] = new
            cnt += 1
            report.append((i + 1, old.strip(), new.strip() or "<清空>"))
    print(f"{old.strip()!r} → {new.strip()!r}: {cnt} 处")

print(f"行数: {orig} → {len(lines)} {'✓' if orig == len(lines) else '✗'}")

with open(SRC, "w", encoding="utf-8") as f:
    f.writelines(lines)

# 验证
with open(SRC, encoding="utf-8") as f:
    t = f.read()
for k in ["### 草\n", "楧榔", "棟子", "篇蓄", "藺茹", "20·", "24 ·"]:
    if k in t:
        print(f"⚠️ 残留: {k!r}")
print("验证完成 ✓")
