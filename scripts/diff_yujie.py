#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全量逐字对比维基版 vs 电子版 草部药物正文，列出所有文本差异"""
import re
from zhconv import convert

def norm(s):
    return convert(s, 'zh-cn').replace(' ', '').replace('\n', '')

# 维基版
with open('/tmp/yujie_wiki.txt', encoding='utf-8') as f:
    wlines = f.read().split('\n')
wiki_drugs = []
cur = None; buf = []
for i, l in enumerate(wlines):
    s = l.strip()
    if s == '编辑' and i > 0:
        if cur:
            wiki_drugs.append((cur, '\n'.join(buf)))
        for j in range(i-1, max(0, i-5), -1):
            if wlines[j].strip():
                cur = wlines[j].strip(); buf = []; break
    elif cur and s and not s.startswith(('From:','Snapshot','Subject','Date','MIME','Content-','boundary','------')):
        if '编辑' not in s and not s.startswith('[') and '玉楸藥解' not in s[:10]:
            buf.append(s)
if cur: wiki_drugs.append((cur, '\n'.join(buf)))
wiki_drugs = [(n, t) for n, t in wiki_drugs if not re.match(r'^卷[一二三四五六七八]$', n)]

# 电子版
with open('/sandbox/workspace/skills/黄元御中医辩证skill/modules/06_yishu_11zhong.md', encoding='utf-8') as f:
    elines = f.readlines()
edrugs = []
cur_name = None; cur_ln = None; cur_body = []
for i in range(36375, 37147):
    l = elines[i].rstrip('\n'); s = l.strip()
    m = re.match(r'^#{2,4} (.+)$', s)
    if m:
        if cur_name: edrugs.append((cur_name, cur_ln, '\n'.join(cur_body)))
        title = m.group(1).strip()
        if title in ('玉楸药解','草部') or re.match(r'^\d+$|^\d+·$', title):
            cur_name = None; continue
        cur_name = re.sub(r'^[■☑☐]+\s*', '', title)
        cur_ln = i + 1; cur_body = []
    elif cur_name and s:
        if re.match(r'^【.*第\d+页】$', s) or re.match(r'^[一二三四五六七八九]+$', s) or '医书十一种' in s or re.match(r'^#{1,4} ', s):
            continue
        cur_body.append(s)
if cur_name: edrugs.append((cur_name, cur_ln, '\n'.join(cur_body)))

# 精确匹配（优先全等，其次包含）
def find_edrug(wn):
    wn_n = norm(wn)
    for en, eln, eb in edrugs:
        if norm(en) == wn_n:
            return en, eln, eb
    for en, eln, eb in edrugs:
        if wn_n in norm(en) or norm(en) in wn_n:
            return en, eln, eb
    return None

print("=== 正文差异明细（非繁简差异） ===")
total_diff = 0
for wn, wt in wiki_drugs:
    hit = find_edrug(wn)
    if not hit:
        print(f'[{wn}] 无对应')
        continue
    en, eln, eb = hit
    w_txt = norm(wt)
    e_txt = norm(eb)
    if w_txt == e_txt:
        continue
    total_diff += 1
    # 找第一个差异点上下文
    i = 0
    while i < min(len(w_txt), len(e_txt)) and w_txt[i] == e_txt[i]:
        i += 1
    ctx_w = w_txt[max(0,i-12):i+15]
    ctx_e = e_txt[max(0,i-12):i+15]
    print(f'L{eln} {en}（维基{len(w_txt)}字/电子{len(e_txt)}字）:')
    print(f'  维基…{ctx_w}…')
    print(f'  电子…{ctx_e}…')
print(f'\n共 {total_diff} 味药正文有差异')
