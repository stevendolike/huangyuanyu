#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""素灵微蕴 + 长沙药解 OCR 讹字修正（对比维基文库版确认，不改变行数）"""
SRC = "/sandbox/workspace/skills/黄元御中医辩证skill/modules/06_yishu_11zhong.md"

with open(SRC, encoding="utf-8") as f:
    lines = f.readlines()

orig = len(lines)

fixes = [
    # ── 素灵微蕴 ──
    ("### 齁嘂解", "### 齁喘解"),        # L30799 篇名
    ("### 噎腷解", "### 噎膈解"),        # L31099 篇名
    ("爱生五气", "爰生五气"),            # L30437 胎化解
    ("时或自到", "时或自刭"),            # L30897 悲恐解
    ("故时欲自到", "故时欲自刭"),        # L30899 悲恐解
    ("肌色鼾", "肌色皯黣"),              # L31139 中风解
    ("若晚饭杯洒", "若晚饮杯洒"),        # L30996 脾胃解
    ("上自膈内", "上自腨内"),            # L31028 火逆解
    ("雾气埋淤", "雾气堙淤"),            # L31085 气鼓解
    ("<金匮》", "《金匮》"),            # L30899 书名号缺
    # ── 长沙药解 ──
    ("痃疟", "痎疟"),                    # L35472 猪苓【本经】
    ("恶创，瘘瘤", "恶创，瘿瘤"),        # L35566 连翘【本经】
    ("热气诸痛，除邪", "热气诸痈，除邪"),# L35606 防己【本经】
    ("化瘀消症", "化癖消症"),            # L35768 赤硝
]

total = 0
for old, new in fixes:
    cnt = 0
    for i, l in enumerate(lines):
        if old in l:
            lines[i] = l.replace(old, new)
            cnt += l.count(old)
    total += cnt
    print(f"{old} → {new}: {cnt} 处")

print(f"\n总计 {total} 处，行数 {orig} → {len(lines)} {'✓' if orig == len(lines) else '✗'}")

with open(SRC, "w", encoding="utf-8") as f:
    f.writelines(lines)

with open(SRC, encoding="utf-8") as f:
    t = f.read()
residual = [old for old, _ in fixes if old in t]
print(f"残留: {residual if residual else '无 ✓'}")
