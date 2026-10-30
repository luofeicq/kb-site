# -*- coding: utf-8 -*-
"""
站点构建：
1) 给六个知识点页补齐 h3 的 id，并注入「知识点 / 错题练习」切换条
2) 生成六个错题练习页
3) 由 node 读取 data/*.js，生成 assets/index.js（全站搜索索引）
幂等：重复执行不会重复注入。
"""
import os, re, json, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

SUBJ = [
    # key,    中文,  主色,       浅色,       板块名,                    导航顺序
    ('math',    '数学', '#0d7c74', '#e6f5f3'),
    ('physics', '物理', '#7c3aed', '#f3ecfd'),
    ('bio',     '生物', '#15803d', '#e9f6ed'),
    ('chem',    '化学', '#2563eb', '#eaf1fe'),
    ('chinese', '语文', '#b4232a', '#fdeced'),
    ('english', '英语', '#b45309', '#fdf3e5'),
]
NAME = {k: n for k, n, _, _ in SUBJ}

META = {
    'math': dict(
        scope='8 道典型易错题',
        lead='按高考高频陷阱挑的八道题：集合空集、导数隐零点、解三角形多解、数列求和方法、立体几何建系、解析几何设而不求、概率统计区分度、基本不等式取等条件。'),
    'physics': dict(
        scope='11 道真实错题',
        lead='全部来自错题本里记录的原题，集中在静电场、机械振动、机械波和力电综合四块。每题标了错因要点，先自己重做一遍再看解析。'),
    'bio': dict(
        scope='8 道典型易错题',
        lead='覆盖分子组成、物质运输、光合与呼吸、细胞增殖、遗传规律、基因表达、稳态调节、生态系统八块，重点在概念边界而不是计算。'),
    'chem': dict(
        scope='8 道典型易错题',
        lead='离子反应、氧化还原、物质的量、化学平衡、电化学、离子平衡、沉淀溶解平衡、实验各一题，都是过程分最容易丢的地方。'),
    'chinese': dict(
        scope='6 道典型易错题',
        lead='语言运用、成语、文言文、诗歌鉴赏、现代文阅读、写作各一题，重点看答题的落点意识。'),
    'english': dict(
        scope='6 道典型易错题',
        lead='时态语态、非谓语、定语从句、情态动词、七选五、书面表达各一题，集中处理母语干扰造成的错选。'),
}

NAV_ORDER = ['math', 'physics', 'bio', 'chem', 'chinese', 'english']


def nav(current, mode):
    """顶栏：六个科目，current 高亮；链接指向该科目的同类板块"""
    out = []
    for k in NAV_ORDER:
        href = f'{k}-knowledge.html' if mode == 'knowledge' else f'{k}-mistakes.html'
        cls = ' class="on"' if k == current else ''
        out.append(f'<a href="{href}"{cls}>{NAME[k]}</a>')
    return '<nav class="sb-nav">' + ''.join(out) + '</nav>'


def sitebar(current, mode):
    return (
        '<header class="sitebar"><div class="sb-inner">\n'
        '  <a class="sb-brand" href="index.html"><span class="mk">学</span>'
        '<span class="tx">高中学习台</span></a>\n'
        '  ' + nav(current, mode) + '\n'
        '  <div class="sb-right">\n'
        '    <button class="sb-btn" data-search-open type="button" aria-label="搜索">\n'
        '      <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/>'
        '<path d="M20 20l-3.5-3.5"/></svg>\n'
        '      <span class="bt">搜索</span><kbd>/</kbd>\n'
        '    </button>\n'
        '  </div>\n'
        '</div></header>\n'
    )


def subjtab(k, active):
    a = ' class="on"' if active == 'knowledge' else ''
    b = ' class="on"' if active == 'mistakes' else ''
    return (f'<div class="subjtab"><a href="{k}-knowledge.html"{a}>知识点学习</a>'
            f'<a href="{k}-mistakes.html"{b}>错题练习</a></div>\n    ')


# ---------------------------------------------------------------- 1) 知识点页
def fix_knowledge(k):
    p = f'{k}-knowledge.html'
    s = open(p, encoding='utf-8').read()
    changed = []

    # 1.1 h3 / h4 补 id（都进索引，h4 常是具体考点）
    n = [0, 0]

    def add_id(m):
        tag, attrs, inner = m.group(1), m.group(2), m.group(3)
        if 'id=' in attrs:
            return m.group(0)
        n[0 if tag == 'h3' else 1] += 1
        return f'<{tag} id="{k}-{tag}-{n[0 if tag == "h3" else 1]}"{attrs}>{inner}</{tag}>'

    s2 = re.sub(r'<(h[34])([^>]*)>(.*?)</\1>', add_id, s, flags=re.S)
    if s2 != s:
        changed.append(f'h3 补 id {n[0]} 个 / h4 补 id {n[1]} 个')
        s = s2

    # 1.2 注入切换条（放在面包屑之后）
    if 'class="subjtab"' not in s:
        m = re.search(r'(<div class="crumb">.*?</div>\s*)', s, re.S)
        if m:
            s = s[:m.end()] + '\n    ' + subjtab(k, 'knowledge') + s[m.end():]
            changed.append('注入切换条')

    # 1.3 顶栏统一为本站点导航
    # 替换顶栏时去掉结尾换行，否则每跑一次就多一个空行
    s = re.sub(r'<header class="sitebar">.*?</header>',
               sitebar(k, 'knowledge').rstrip('\n'), s, count=1, flags=re.S)

    open(p, 'w', encoding='utf-8').write(s)
    return changed


# ---------------------------------------------------------------- 2) 错题页
MISTAKE_TPL = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{name}错题练习 · 高中学习台</title>
<link rel="stylesheet" href="assets/base.css">
<link rel="stylesheet" href="assets/mistakes.css">
<style>:root{{--accent:{c};--accent-s:{cs}}}</style>
</head>
<body>
{bar}
<div class="wrap">
  <div class="pagehead">
    <div class="crumb"><a href="index.html">首页</a><span>/</span><a href="{k}-knowledge.html">{name}</a><span>/</span>错题练习</div>
    {tab}
    <h1>{name}错题练习<span class="badge">{count} 道</span></h1>
    <p class="lead">{lead}</p>
    <div class="inline-search" data-search-open>
      <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
      <div class="ph">在本页搜索错题（题干、考点、解析）</div><kbd>/</kbd>
    </div>
  </div>

  <div class="mstats">
    <div class="mstat"><div class="k">错题总数</div><div class="v" id="mTotal">0</div></div>
    <div class="mstat hl"><div class="k">已掌握</div><div class="v" id="mDone">0</div></div>
    <div class="mstat"><div class="k">待攻克</div><div class="v" id="mTodo">0</div></div>
    <div class="mstat"><div class="k">完成度</div><div class="v" id="mPct">0%</div></div>
  </div>

  <div class="mprog">
    <div class="track"><div class="fill" id="mBar"></div></div>
    <div class="txt">「已掌握」状态保存在本机浏览器，换设备不跟随。</div>
  </div>

  <div class="mtools">
    <div class="mrow1">
      <label class="msearch">
        <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
        <input id="mSearch" type="text" placeholder="搜题干、考点或解析里的关键词" autocomplete="off">
      </label>
      <label class="monly"><input type="checkbox" id="mOnly">只看未掌握</label>
      <button class="mreset" id="mReset" type="button">清空记录</button>
      <span class="mcount" id="mCount">0 题</span>
    </div>
    <div class="mchips" id="mChips"></div>
  </div>

  <div class="mnote">
    <b>怎么用：</b>点「重做一次」会收起答案、把卡片滚到屏幕中间，先自己在纸上做一遍；
    做完再点「看答案与解析」对照。<b>判断能不能算掌握，看两点</b>：一是重做时思路是自己想出来的，
    不是回忆起答案；二是同类的变式题也能上手。两条都满足再点「标记为已掌握」。
  </div>

  <div id="mList"></div>
</div>

<footer class="sitefoot" style="max-width:1000px">
  <div>{foot}</div>
</footer>

<script src="assets/site.js"></script>
<script src="assets/search.js"></script>
<script src="data/mistakes-{k}.js"></script>
<script src="assets/mistakes.js"></script>
<script>
(function(){{
  /* 把错题并入本页搜索 */
  window.__kbSearchItems = function(list){{
    KB.search.setItems(list.map(function(d){{
      return {{
        g: d.topic,
        n: (d.q || '').replace(/\\s+/g, ' ').slice(0, 50),
        d: (d.answer || '') + '　' + (d.analysis || '').slice(0, 150),
        u: '#q-' + d.id,
        tag: '错题'
      }};
    }}));
  }};
  KB.search.init({{
    items: [],
    scope: '{name}',
    placeholder: '在本页搜索错题',
    tip: '在<b>{name}错题</b>里查找，可搜题干、考点与解析关键词。'
  }});
}})();
</script>
</body>
</html>
'''


def build_mistakes(k):
    c = dict(SUBJ_D.get(k))
    meta = META[k]
    bar = sitebar(k, 'mistakes').replace('\n', '\n')
    html = MISTAKE_TPL.format(
        k=k, name=NAME[k], c=c['c'], cs=c['cs'],
        bar=bar, tab=subjtab(k, 'mistakes'), lead=meta['lead'],
        count=DATA_COUNT[k], foot=FOOT[k]
    )
    open(f'{k}-mistakes.html', 'w', encoding='utf-8').write(html)
    return len(html.encode())


FOOT = {
    'physics': '本页错题来自错题本原始记录（第五周定时作业 09-27、第七周定时作业 10-11），题干数值按原卷核对过。',
    'math': '题目标注「典型例题」，为按高考常见陷阱自拟的练习题，非原卷摘录；考点与解法贴合现行高考要求。',
    'bio': '题目标注「典型例题」，为按高考常见命题方向自拟的练习题，非原卷摘录。',
    'chem': '题目标注「典型例题」，为按高考常见命题方向自拟的练习题，非原卷摘录。',
    'chinese': '题目标注「典型例题」，为教学示例，非原卷摘录；文言选段与诗句均取自常见篇目。',
    'english': '题目标注「典型例题」，为教学示例，非原卷摘录；单句与短文的语法点对应现行高考考查方式。',
}


# ---------------------------------------------------------------- 3) 全站索引
NODE_DUMP = r'''
const fs=require('fs'), vm=require('vm');
const keys=['math','physics','bio','chem','chinese','english'];
const out={};
for(const k of keys){
  const ctx={window:{}};
  vm.createContext(ctx);
  try{
    vm.runInContext(fs.readFileSync('data/mistakes-'+k+'.js','utf8'), ctx);
    out[k]=(ctx.window.MISTAKES||[]).map(d=>({id:d.id,topic:d.topic,q:d.q,answer:d.answer}));
  }catch(e){ out[k]=[]; }
}
process.stdout.write(JSON.stringify(out));
'''


def dump_mistakes():
    p = '_build/_dump.js'
    open(p, 'w', encoding='utf-8').write(NODE_DUMP)
    r = subprocess.run(['node', p], capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode != 0:
        raise SystemExit('node dump failed: ' + (r.stderr or '')[:400])
    return json.loads(r.stdout)


def strip_tags(x):
    x = re.sub(r'<[^>]+>', '', x)
    x = x.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    return re.sub(r'\s+', ' ', x).strip()


def page_items(k, mode, mis):
    p = f'{k}-{mode}.html'
    s = open(p, encoding='utf-8').read()
    items = []
    if mode == 'knowledge':
        # 收集全部 h2 / h3 / h4 及其正文（到下一个同级或更高级标题为止）
        heads = [(m.start(), m.end(), int(m.group(1)), m.group(2), m.group(3))
                 for m in re.finditer(r'<h([234]) id="([^"]+)"[^>]*>(.*?)</h\1>', s, re.S)]
        raw = []
        for idx, (st, en, lv, hid, inner) in enumerate(heads):
            end = len(s)
            for st2, en2, lv2, hid2, in2 in heads[idx + 1:]:
                if lv2 <= lv:
                    end = st2
                    break
            name = strip_tags(inner)
            if not name:
                continue
            body = strip_tags(s[en:end])
            raw.append({'lv': lv, 'id': hid, 'name': name, 'body': body})

        # 章级条目补上下属小节标题，保证章节粒度也能命中细分考点
        for i, it in enumerate(raw):
            if it['lv'] != 2:
                continue
            subs = []
            for jt in raw[i + 1:]:
                if jt['lv'] == 2:
                    break
                subs.append(jt['name'])
            it['subs'] = subs

        for it in raw:
            d = it['body'][:150]
            if it.get('subs'):
                d = d + '｜' + '·'.join(it['subs'])[:260]
            items.append({
                'g': f'{NAME[k]} · 知识点',
                'n': it['name'],
                'd': d,
                'u': f'{k}-knowledge.html#{it["id"]}',
                'tag': {2: '章', 3: '节', 4: '点'}[it['lv']],
            })
    else:
        for d in mis:
            items.append({
                'g': f'{NAME[k]} · 错题',
                'n': strip_tags(d['q'])[:52],
                'd': (strip_tags(d.get('answer') or '') + '　' + strip_tags(d['q']))[:160],
                'u': f'{k}-mistakes.html#q-{d["id"]}',
                'tag': '错题',
            })
    return items


def build_index(mis):
    allitems = []
    for k, _, _, _ in SUBJ:
        allitems += page_items(k, 'knowledge', [])
        allitems += page_items(k, 'mistakes', mis[k])
    js = '/* 全站搜索索引：由 _build/build_site.py 自动生成，勿手改 */\n'
    js += 'window.KB_INDEX = ' + json.dumps(allitems, ensure_ascii=False, separators=(',', ':')) + ';\n'
    open('assets/index.js', 'w', encoding='utf-8').write(js)
    return len(allitems), len(js.encode())


# ---------------------------------------------------------------- main
SUBJ_D = {k: {'c': c, 'cs': cs} for k, _, c, cs in SUBJ}

if __name__ == '__main__':
    mis = dump_mistakes()
    DATA_COUNT = {k: len(v) for k, v in mis.items()}
    print('错题条数:', DATA_COUNT)

    for k, _, _, _ in SUBJ:
        ch = fix_knowledge(k)
        print(f'  {k}-knowledge.html  {ch or "无变化"}')

    for k, _, _, _ in SUBJ:
        n = build_mistakes(k)
        print(f'  {k}-mistakes.html  {n/1024:.1f} KB')

    n, sz = build_index(mis)
    print(f'assets/index.js  索引 {n} 条  {sz/1024:.1f} KB')
