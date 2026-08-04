#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""逐味对比：维基版(上传) vs 电子版 玉楸药解草部药物正文（简繁归一）"""
import re
from zhconv import convert

def norm(s):
    """繁体转简体 + 去符号空白"""
    return convert(s, 'zh-cn').replace(' ', '').replace('\n', '')

# ── 解析维基版：药名 + 正文 ──
with open('/tmp/yujie_wiki.txt', encoding='utf-8') as f:
    wlines = f.read().split('\n')

wiki_drugs = []  # [(药名, 正文)]
cur = None
buf = []
for i, l in enumerate(wlines):
    s = l.strip()
    if s == '编辑' and i > 0:
        if cur:
            wiki_drugs.append((cur, '\n'.join(buf)))
        # 找药名
        for j in range(i-1, max(0, i-5), -1):
            if wlines[j].strip():
                cur = wlines[j].strip()
                buf = []
                break
    elif cur and s and not s.startswith(('From:','Snapshot','Subject','Date','MIME','Content-','boundary','------')):
        if '编辑' not in s and not s.startswith('[') and '玉楸藥解' not in s[:10]:
            buf.append(s)
if cur:
    wiki_drugs.append((cur, '\n'.join(buf)))
# 去掉卷二~卷八的卷标
wiki_drugs = [(n, t) for n, t in wiki_drugs if not re.match(r'^卷[一二三四五六七八]$', n)]

# ── 解析电子版 ──
with open('/sandbox/workspace/skills/黄元御中医辩证skill/modules/06_yishu_11zhong.md', encoding='utf-8') as f:
    elines = f.readlines()

# 草部范围 36376-37147
edrugs = []  # [(药名, 行号, 正文)]
cur_name = None
cur_ln = None
cur_body = []
for i in range(36375, 37147):
    l = elines[i].rstrip('\n')
    s = l.strip()
    m = re.match(r'^#{2,4} (.+)$', s)
    if m:
        if cur_name:
            edrugs.append((cur_name, cur_ln, '\n'.join(cur_body)))
        title = m.group(1).strip()
        # 过滤页眉
        if title in ('玉楸药解','草部') or re.match(r'^\d+$|^\d+·$', title):
            cur_name = None
            continue
        cur_name = re.sub(r'^[■☑☐]+\s*', '', title)
        cur_ln = i + 1
        cur_body = []
    elif cur_name and s:
        if re.match(r'^【.*第\d+页】$', s) or re.match(r'^[一二三四五六七八九]+$', s) or '医书十一种' in s:
            continue
        cur_body.append(s)
if cur_name:
    edrugs.append((cur_name, cur_ln, '\n'.join(cur_body)))

print(f'维基版药物: {len(wiki_drugs)}')
print(f'电子版药物: {len(edrugs)}')

# ── 对比：按维基版药名找电子版对应（简繁归一） ──
print('\n=== 电子版缺失的药物（维基有而电子版无） ===')
missing = []
for wn, wt in wiki_drugs:
    wn_n = norm(wn)
    hit = None
    for en, eln, eb in edrugs:
        en_n = norm(en)
        if wn_n == en_n or (len(wn_n) >= 2 and wn_n in en_n) or (len(en_n) >= 2 and en_n in wn_n):
            hit = (en, eln, eb)
            break
    if not hit:
        missing.append(wn)
        print(f'  ✗ {wn}')
if not missing:
    print('  无 ✓（电子版覆盖维基版全部药物）')

# ── 对比：性味归经首句 ──
print('\n=== 首句(性味归经)不一致的药物 ===')
def first_sentence(body):
    m = re.search(r'味[^。\n]+。', body)
    return m.group(0) if m else body[:40]

diff_cnt = 0
for wn, wt in wiki_drugs:
    wn_n = norm(wn)
    for en, eln, eb in edrugs:
        en_n = norm(en)
        if wn_n == en_n or (len(wn_n) >= 2 and wn_n in en_n) or (len(en_n) >= 2 and en_n in wn_n):
            wf = norm(first_sentence(wt))
            ef = norm(first_sentence(eb))
            if wf != ef:
                diff_cnt += 1
                print(f'  L{eln} {en}:')
                print(f'    维基: {wf}')
                print(f'    电子: {ef}')
            break
print(f'首句差异: {diff_cnt} 处')

# ── 对比：正文长度（可能截断） ──
print('\n=== 正文长度差异大的药物（>35%差） ===')
for wn, wt in wiki_drugs:
    wn_n = norm(wn)
    for en, eln, eb in edrugs:
        en_n = norm(en)
        if wn_n == en_n or (len(wn_n) >= 2 and wn_n in en_n) or (len(en_n) >= 2 and en_n in wn_n):
            wlen = len(norm(wt))
            elen = len(norm(eb))
            if wlen > 40 and elen > 0 and abs(wlen - elen) / max(wlen, elen) > 0.35:
                print(f'  L{eln} {en}: 维基{wlen}字 vs 电子{elen}字')
            break
