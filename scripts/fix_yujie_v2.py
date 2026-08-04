#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""玉楸药解 正文 OCR 讹字修正（对比维基文库版确认，不改变行数）"""
SRC = "/sandbox/workspace/skills/黄元御中医辩证skill/modules/06_yishu_11zhong.md"

with open(SRC, encoding="utf-8") as f:
    lines = f.readlines()

orig = len(lines)

# 精确替换（长串优先，避免误伤）
fixes = [
    ("疮疗俱治", "疮疖俱治"),            # 茜草
    ("瘈痰", "瘈疭"),                    # 钩藤钩
    ("治疗疮肿毒", "治疔疮肿毒"),        # 豨莶草
    ("咽斜", "喎斜"),                    # 羌活/乳香
    ("呖斜", "喎斜"),                    # 荆芥/蓖麻子
    ("喝斜", "喎斜"),                    # 浮萍/桑枝
    ("黙斑", "䵟斑"),                    # 木鳖子/山慈菰
    ("脑水胀", "臌水胀"),                # 牛蒡子
    ("凉肝消肿，消肿败毒", "凉肝消肺，消肿败毒"),  # 金银花
    ("奸胞", "皯疱"),                    # 白芨
    ("草薢疏泻水道", "萆薢疏泻水道"),    # 萆薢
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

# 验证残留
with open(SRC, encoding="utf-8") as f:
    t = f.read()
residual = [old for old, _ in fixes if old in t]
print(f"残留: {residual if residual else '无 ✓'}")
