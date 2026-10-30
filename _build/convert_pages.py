# -*- coding: utf-8 -*-
"""把物理/化学/生物三份单页改造成六科站点下的知识点页：
   换顶栏、换页头、接入新搜索、去掉旧外壳。"""
import os, re, sys, io

D = r'H:/kb-site'

SUBJ = {
    'physics': dict(
        src='physics.html', out='physics-knowledge.html',
        name='物理', accent='#7c3aed', accent_s='#f3ecfd',
        cssvar='--blue:#7c3aed;',
        title='物理知识点 · 专题精讲',
        lead='按错题诊断排出的六个专题。每个专题都从「这题在考什么」起步，用大白话讲原理，再给出题套路与解题固定动作，最后重做原题。带标记的图可以直接拖动、点击。',
        badge='6 专题',
        sibling='physics-mistakes.html',
    ),
    'chem': dict(
        src='chem.html', out='chem-knowledge.html',
        name='化学', accent='#2563eb', accent_s='#eaf1fe',
        cssvar=None,
        title='化学知识点 · 章节精讲',
        lead='必修一、二与选择性必修 1–3，共 13 章，按教材顺序排。每章固定结构：知识主线 → 高频考点 → 易错辨析 → 口诀 → 例题精解 → 分层练习。',
        badge='13 章',
        sibling='chem-mistakes.html',
    ),
    'bio': dict(
        src='bio.html', out='bio-knowledge.html',
        name='生物', accent='#15803d', accent_s='#e9f6ed',
        cssvar=None,
        title='生物知识点 · 章节精讲',
        lead='必修 1、2 与选择性必修 1–3，共 12 章，按教材顺序排。每章固定结构：知识主线 → 高频考点 → 易错辨析 → 口诀 → 例题精解 → 分层练习。',
        badge='12 章',
        sibling='bio-mistakes.html',
    ),
}

SUBJ_ORDER = [('math', '数学', 'math-knowledge.html'),
              ('physics', '物理', 'physics-knowledge.html'),
              ('bio', '生物', 'bio-knowledge.html'),
              ('chem', '化学', 'chem-knowledge.html'),
              ('chinese', '语文', 'chinese-knowledge.html'),
              ('english', '英语', 'english-knowledge.html')]


def topbar(active_name):
    links = []
    for k, nm, url in SUBJ_ORDER:
        on = ' class="on"' if nm == active_name else ''
        links.append('<a href="%s"%s>%s</a>' % (url, on, nm))
    return (
        '<header class="sitebar"><div class="sb-inner">\n'
        '  <a class="sb-brand" href="index.html"><span class="mk">学</span><span class="tx">高中学习台</span></a>\n'
        '  <nav class="sb-nav">' + ''.join(links) + '</nav>\n'
        '  <div class="sb-right">\n'
        '    <button class="sb-btn" data-search-open type="button" aria-label="搜索">\n'
        '      <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>\n'
        '      <span class="bt">搜索</span><kbd>/</kbd>\n'
        '    </button>\n'
        '  </div>\n'
        '</div></header>\n'
    )


def pagehead(cfg, chapters):
    quick = ''.join('<a href="#%s">%s</a>' % (cid, nm) for cid, nm in chapters[:8])
    return (
        '<div class="pagehead">\n'
        '  <div class="crumb"><a href="index.html">首页</a><span>/</span>'
        '<a href="%s">%s</a><span>/</span>知识点学习</div>\n'
        '  <h1>%s<span class="badge">%s</span></h1>\n'
        '  <p class="lead">%s</p>\n'
        '  <div class="inline-search" data-search-open>\n'
        '    <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>\n'
        '    <div class="ph">在本页搜索%s知识点</div><kbd>/</kbd>\n'
        '  </div>\n'
        '  <div class="quick" style="margin-top:14px">%s<a href="%s">→ 本科错题练习</a></div>\n'
        '</div>\n'
    ) % (cfg['sibling'].replace('-mistakes.html', '-knowledge.html'), cfg['name'],
         cfg['title'], cfg['badge'], cfg['lead'], cfg['name'], quick, cfg['sibling'])


def patch(key, cfg):
    p = os.path.join(D, cfg['src'])
    s = open(p, encoding='utf-8').read()

    # 1) 去掉旧外壳样式（从标记到 </style>）
    a = s.find('/* ===== 站点外壳 ===== */')
    if a > 0:
        b = s.find('</style>', a)
        s = s[:a] + s[b:]
        print('  %-8s 移除旧外壳样式 %d 字符' % (key, b - a))

    # 2) 引入 base.css（放在自带样式之前）
    i = s.index('<style>')
    s = s[:i] + '<link rel="stylesheet" href="assets/base.css">\n' + s[i:]

    # 3) 主题色覆盖（放在自带样式之后，保证生效）
    j = s.index('</style>') + len('</style>')
    extra = '\n<style>\n:root{--accent:%s;--accent-s:%s;%s}\n' \
            '.side{top:var(--bar-h);max-height:calc(100vh - var(--bar-h))}\n' \
            'h2.topic{scroll-margin-top:calc(var(--bar-h) + 18px)}\n' \
            '.layout{max-width:1240px}\n' \
            '</style>' % (cfg['accent'], cfg['accent_s'], cfg['cssvar'] or '')
    s = s[:j] + extra + s[j:]

    # 4) 换顶栏
    m = re.search(r'<header class="sitebar">.*?</header>\n?', s, re.S)
    if m:
        s = s[:m.start()] + topbar(cfg['name']) + s[m.end():]
        print('  %-8s 替换顶栏' % key)

    # 5) 提取章目录，替换 hero
    chapters = []
    for mm in re.finditer(r'<h2 class="topic" id="([^"]+)">(.*?)</h2>', s, re.S):
        cid, raw = mm.group(1), mm.group(2)
        nm = re.sub(r'<span class="no">.*?</span>', '', raw)
        nm = re.sub(r'<[^>]+>', '', nm).strip()
        nm = re.sub(r'\s+', ' ', nm)
        chapters.append((cid, nm[:26]))
    hm = re.search(r'<div class="hero">.*?\n</div>\n', s, re.S)
    if hm:
        s = s[:hm.start()] + pagehead(cfg, chapters) + s[hm.end():]
        print('  %-8s 替换页头（%d 章）' % (key, len(chapters)))

    # 6) 换尾部脚本
    t = s.rfind('<script>window.__KBPAGE')
    if t > 0:
        e = s.index('</body>', t)
        tail = ('<script src="assets/site.js"></script>\n'
                '<script src="assets/search.js"></script>\n'
                '<script>\n'
                '(function(){\n'
                '  var items = KB.search.buildFromDoc();\n'
                "  KB.search.init({items:items, scope:'%s', placeholder:'在本页搜索%s知识点'});\n"
                '})();\n'
                '</script>\n') % (cfg['name'], cfg['name'])
        s = s[:t] + tail + s[e:]
        print('  %-8s 接入新搜索' % key)

    open(os.path.join(D, cfg['out']), 'w', encoding='utf-8').write(s)
    print('  %-8s 输出 %s  %.1f KB' % (key, cfg['out'], len(s.encode()) / 1024))


if __name__ == '__main__':
    for k, c in SUBJ.items():
        print('---', k)
        patch(k, c)
    print('完成')
