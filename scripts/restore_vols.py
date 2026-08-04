#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""恢复被误删的卷标：插入18个丢失卷标 + 恢复47个·行前缀 + 清理8个页眉行"""
import re

SRC = "/sandbox/workspace/skills/黄元御中医辩证skill/modules/06_yishu_11zhong.md"
with open(SRC, encoding="utf-8") as f:
    lines = f.readlines()

def find_lines():
    return lines[:]

# ── B. ·行恢复（先做，行号未变） ──
# 金匮悬解 # 级：卷二~二十二（按行号升序对应）
jinkui_vols = [
    (19244, 2), (19434, 3), (19552, 4), (19808, 5), (19887, 6),
    (20058, 7), (20255, 8), (20461, 9), (20519, 10), (20839, 11),
    (20984, 12), (21189, 13), (21664, 14), (22022, 15), (22192, 16),
    (22312, 17), (22565, 18), (22653, 19), (22735, 20), (22873, 21),
    (23005, 22),
]
CN = '一二三四五六七八九十'
def cn_num(n):
    if n <= 10: return CN[n-1]
    if n < 20: return '十' + (CN[n-11] if n > 10 else '')
    if n == 20: return '二十'
    return '二十' + CN[n-21]
# 修正 cn_num（十四=十四，十五=十五...）
def cn(n):
    if n <= 10: return CN[n-1]
    if n < 20: return '十' + CN[n-11]  # 11→十一, 14→十四
    if n < 30: return '二十' + (CN[n-21] if n > 20 else '')
    return str(n)

# 金匮 # 级
fix_count = 0
for ln, v in jinkui_vols:
    i = ln - 1
    if '·' in lines[i]:
        lines[i] = lines[i].replace('·', f'金匮悬解卷{cn(v)}·', 1)
        fix_count += 1
# 伤寒说意 # 级：卷一~十
shanghan_shuoyi = [(24669,1),(24831,2),(25067,3),(25222,4),(25319,5),(25420,6),(25502,7),(25573,8),(25631,9),(25811,10)]
for ln, v in shanghan_shuoyi:
    i = ln - 1
    if '·' in lines[i]:
        lines[i] = lines[i].replace('·', f'伤寒说意卷{cn(v)}·', 1)
        fix_count += 1
# 四圣心源：卷一(26853), 卷二###(27046), 卷三(27232), 卷四(27487), 卷五(27825), 卷六(28111), 卷七(28399), 卷八(28696), 卷九(29009), 卷十(29156)
sisheng = [(26853,1),(27046,2),(27232,3),(27487,4),(27825,5),(28111,6),(28399,7),(28696,8),(29009,9),(29156,10)]
for ln, v in sisheng:
    i = ln - 1
    if '·' in lines[i]:
        lines[i] = lines[i].replace('·', f'四圣心源卷{cn(v)}·', 1)
        fix_count += 1
# 玉楸药解：卷一(35922), 卷二###(36684), 卷三(37070), 卷四(37353), 卷五(37650), 卷八(38152)
yuqiu = [(35922,1),(36684,2),(37070,3),(37353,4),(37650,5),(38152,8)]
for ln, v in yuqiu:
    i = ln - 1
    if '·' in lines[i]:
        lines[i] = lines[i].replace('·', f'玉楸药解卷{cn(v)}·', 1)
        fix_count += 1
print(f'B. 恢复·行前缀: {fix_count} 处')

# ── C. 玉椒→玉楸（卷六/七） ──
c_cnt = 0
for i, l in enumerate(lines):
    if '玉椒药解卷' in l:
        lines[i] = l.replace('玉椒药解卷', '玉楸药解卷')
        c_cnt += l.count('玉椒药解卷')
print(f'C. 玉椒→玉楸: {c_cnt} 处')

# ── D. 删除金匮 #### 页眉·行 ──
del_lines = {19268, 19716, 20453, 21271, 21355, 21588, 22529, 22821}
kept = [l for i, l in enumerate(lines) if (i + 1) not in del_lines]
d_cnt = len(lines) - len(kept)
print(f'D. 删除页眉行: {d_cnt}')
lines = kept

# ── A. 插入丢失卷标（从后往前） ──
inserts = [
    # (插入位置行号, 插入文本)  行号 = 在该行之前插入
    (6533, '# 素问悬解卷十三'),
    (6058, '# 素问悬解卷十二'),
    (5522, '# 素问悬解卷十一'),
    (4935, '# 素问悬解卷十'),
    (4610, '# 素问悬解卷九'),
    (4118, '# 素问悬解卷八'),
    (3612, '# 素问悬解卷七'),
    (2976, '# 素问悬解卷六'),
    (2341, '# 素问悬解卷五'),
    (1848, '# 素问悬解卷四'),
    (1351, '# 素问悬解卷三'),
    (750, '# 素问悬解卷二'),
    (324, '# 素问悬解卷一'),
    (19108, '# 金匮悬解卷一'),
    (34986, '# 长沙药解卷四'),
    (34428, '# 长沙药解卷三'),
    (33703, '# 长沙药解卷二'),
    (32999, '# 长沙药解卷一'),
]
# 注意：D 删除 8 行会影响 A 的行号（被删行都在金匮范围 19000-23000）！
# 素问悬解(55-8106)、长沙药解(32800+) 不受 D 影响；金匮悬解 L19108 受影响（被删行都在19268+，L19108 之前无删除，不受影响）
for pos, text in inserts:
    i = pos - 1
    if 0 <= i <= len(lines):
        lines.insert(i, text + '\n')
    else:
        print(f'  ⚠️ 插入越界: L{pos} {text}')
print(f'A. 插入卷标: {len(inserts)} 个')

with open(SRC, "w", encoding="utf-8") as f:
    f.writelines(lines)
print(f'总行数: {len(lines)}')
