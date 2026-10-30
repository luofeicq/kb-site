# -*- coding: utf-8 -*-
"""把物理页重组为「全册 18 章 + 深化专题 6 个」：
- 保留原有 head/style/script（含 7 张交互图的绘图代码）
- 替换 aside 目录、pagehead
- 在原 6 专题前插入新写的全册内容
"""
import os
import re

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(D)
P = 'physics-knowledge.html'
s = open(P, encoding='utf-8').read()

# ---------- 1. 切分原文件 ----------
i_aside = s.find('<aside class="side">')
i_main = s.find('<main>')
i_head_end = s.rfind('</header>', 0, i_aside) + len('</header>')
i_h2 = [m.start() for m in re.finditer(r'<h2 class="topic"', s)][0]
i_footer = s.find('<footer', i_h2)

head_part = s[:i_head_end]          # <!DOCTYPE>…</header>
topic_part = s[i_h2:i_footer]       # 原 6 专题 + 附录
tail_part = s[i_footer:]            # footer + 关闭标签 + scripts

print('head %d / topics %d / tail %d' % (len(head_part), len(topic_part), len(tail_part)))

# ---------- 2. 新目录 ----------
CHAPTERS = [
    ('m1',  '必修一', '运动的描述'),
    ('m2',  '必修一', '匀变速直线运动'),
    ('m3',  '必修一', '相互作用——力'),
    ('m4',  '必修一', '牛顿运动定律'),
    ('m5',  '必修二', '抛体运动'),
    ('m6',  '必修二', '圆周运动'),
    ('m7',  '必修二', '万有引力与航天'),
    ('m8',  '必修二', '机械能守恒'),
    ('m9',  '必修三', '静电场'),
    ('m10', '必修三', '恒定电流与电路'),
    ('m11', '必修三/选必二', '电磁感应与交变电流'),
    ('m12', '选必一', '动量守恒定律'),
    ('m13', '选必一', '机械振动'),
    ('m14', '选必一', '机械波'),
    ('m15', '选必一', '光'),
    ('m16', '选必二', '磁场'),
    ('m17', '选必三', '热学'),
    ('m18', '选必三', '近代物理'),
]

nav = ['<nav>', '  <div class="grp">全 册 知 识 点</div>']
for hid, book, name in CHAPTERS:
    nav.append(f'    <a href="#{hid}">{book}　{name}</a>')
nav.append('  <div class="grp">深 化 专 题</div>')
for hid, label in [('t1', '波的图像与多解'), ('t2', '两个等量点电荷'),
                   ('t3', '库仑力 + 圆弧'), ('t4', '单摆'),
                   ('t5', '弹簧振子'), ('t6', '静电概念')]:
    nav.append(f'    <a href="#{hid}">{label}</a>')
nav.append('  <div class="grp">附　录</div>')
nav.append('    <a href="#apx1">通用解题检查清单</a>')
nav.append('    <a href="#apx2">两周学习计划</a>')
nav.append('</nav>')
nav_html = '\n'.join(nav)

aside = (
    '<aside class="side">\n'
    '  <div class="brand">高中物理 · 全册 + 专题</div>\n'
    '  <div class="sub">按人教版教材顺序 · 交互版</div>\n'
    + nav_html + '\n'
    '</aside>\n'
)

# ---------- 3. 新页头 ----------
quick = ''.join(f'<a href="#{h}">{n}</a>' for h, _, n in CHAPTERS)
pagehead = f'''<main>

<div class="pagehead">
  <div class="crumb"><a href="index.html">首页</a><span>/</span><a href="physics-knowledge.html">物理</a><span>/</span>知识点学习</div>
  
    <div class="subjtab"><a href="physics-knowledge.html" class="on">知识点学习</a><a href="physics-mistakes.html">错题练习</a></div>
    <h1>物理知识点 · 全册精讲<span class="badge">18 章 + 6 专题</span></h1>
  <p class="lead">前半部分按人教版必修一、二、三与选择性必修一、二、三的顺序排，覆&#30422;力学、电磁学、振动与波、光学、热学、近代物理；后半部分是六个由真实错题反推出来的深化专题，配 7 张可拖动的交互图。</p>
  <div class="inline-search" data-search-open>
    <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
    <div class="ph">在本页搜索物理知识点</div><kbd>/</kbd>
  </div>
  <div class="quick" style="margin-top:14px">{quick}<a href="#t1">深化专题</a><a href="physics-mistakes.html">→ 错题练习</a></div>
</div>

'''

# ---------- 4. 拼接新内容 ----------
parts = []
for f in ['phy_b1.html', 'phy_b2.html', 'phy_b3.html', 'phy_b4.html', 'phy_b5.html']:
    parts.append(open(os.path.join('_build', f), encoding='utf-8').read())
new_body = '\n'.join(parts)

# 原专题加一个分隔标题
sep = ('<h2 class="topic" id="topics-start" style="margin-top:56px">'
       '<span class="no">第 二 部 分</span>深化专题（错题驱动）</h2>\n'
       '<p class="topic-meta">这六个专题来自错题本里的真实错误，'
       '每个都从"这题在考什么"起步，用大白话讲透原理，配可操作的交互图。'
       '如果上面某一章看完还是心里没底，多半要来这里再走一遍。</p>\n\n')

new = head_part + '\n\n<div class="layout">\n\n' + aside + pagehead + new_body + '\n' + sep + topic_part + tail_part

# 修正 footer 文案
new = new.replace(
    '<footer class="sitefoot" style="max-width:1240px"><div>六个专题由错题诊断结果排序而来，不是全册覆盖。交互图全部本地绘制，不联网也能用。</div></footer>',
    '<footer class="sitefoot" style="max-width:1240px"><div>全册 18 章按人教版 2019 版教材顺序编排，'
    '覆盖必修一、二、三与选择性必修一、二、三；六个深化专题由错题诊断结果排序而来。'
    '章节编排以通行版本为准，不同地区教材顺序可能略有差异。交互图全部本地绘制，不联网也能用。</div></footer>')

open(P, 'w', encoding='utf-8').write(new)
print('新文件 %.1f KB' % (len(new.encode()) / 1024))
print('h2 数:', len(re.findall(r'<h2 class="topic"', new)))
print('h3 数:', len(re.findall(r'<h3', new)))
