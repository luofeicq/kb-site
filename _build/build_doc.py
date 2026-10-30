# -*- coding: utf-8 -*-
"""把 *_body.html 片段包装成完整页面：顶栏 + 侧栏目录 + 页头 + 搜索 + 页脚。"""
import os, re, sys

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(D, '_build')

ORDER = [('math', '数学', 'math-knowledge.html'),
         ('physics', '物理', 'physics-knowledge.html'),
         ('bio', '生物', 'bio-knowledge.html'),
         ('chem', '化学', 'chem-knowledge.html'),
         ('chinese', '语文', 'chinese-knowledge.html'),
         ('english', '英语', 'english-knowledge.html')]

CFG = {
    'math': dict(
        name='数学', accent='#0d7c74', accent_s='#e6f5f3',
        title='数学知识点 · 章节精讲', badge='7 章',
        lead='按教材章节顺序排的七个板块：集合与逻辑、函数与导数、三角函数、数列、立体几何、解析几何、概率统计。每章含知识主线、高频考点、易错辨析与一道完整例题。',
        mistakes='math-mistakes.html',
        tip='在<b>数学 7 章</b>里查找知识点'),
    'chinese': dict(
        name='语文', accent='#b4232a', accent_s='#fdeced',
        title='语文知识点 · 题型精讲', badge='6 章',
        lead='按高考试卷的题型板块组织：现代文阅读、文学类文本、文言文、古代诗歌、语言文字运用、写作。每章讲清「考什么、怎么答、哪里扣分」。',
        mistakes='chinese-mistakes.html',
        tip='在<b>语文 6 章</b>里查找知识点'),
    'english': dict(
        name='英语', accent='#b45309', accent_s='#fdf3e5',
        title='英语知识点 · 语法与题型', badge='6 章',
        lead='语法三条主线（时态语态、非谓语、从句）加三个题型板块（阅读七选五、完形、写作）。每条规则都配了对比示例和易错点。',
        mistakes='english-mistakes.html',
        tip='在<b>英语 6 章</b>里查找知识点'),
}


def topbar(active):
    links = []
    for k, nm, url in ORDER:
        on = ' class="on"' if nm == active else ''
        links.append('<a href="%s"%s>%s</a>' % (url, on, nm))
    return ('<header class="sitebar"><div class="sb-inner">\n'
            '  <a class="sb-brand" href="index.html"><span class="mk">学</span><span class="tx">高中学习台</span></a>\n'
            '  <nav class="sb-nav">' + ''.join(links) + '</nav>\n'
            '  <div class="sb-right">\n'
            '    <button class="sb-btn" data-search-open type="button" aria-label="搜索">\n'
            '      <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>\n'
            '      <span class="bt">搜索</span><kbd>/</kbd>\n'
            '    </button>\n'
            '  </div>\n'
            '</div></header>\n')


def build(key, cfg):
    body = open(os.path.join(B, key + '_body.html'), encoding='utf-8').read()

    # 章目录
    toc, quick = [], []
    for m in re.finditer(r'<h2 id="([^"]+)">\s*<span class="no">([^<]*)</span>([^<]*)</h2>', body):
        cid, no, nm = m.group(1), m.group(2).strip(), m.group(3).strip()
        short = no.replace('第', '').replace('章', '').strip()
        toc.append('<a href="#%s"><span class="n">%s</span>%s</a>' % (cid, short, nm))
        quick.append('<a href="#%s">%s</a>' % (cid, nm))

    html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s · 高中学习台</title>
<link rel="stylesheet" href="assets/base.css">
<style>:root{--accent:%(accent)s;--accent-s:%(accent_s)s}</style>
</head>
<body>
%(topbar)s
<div class="layout">
<aside class="side">
  <div class="hd">章 节 目 录</div>
  <nav>
    %(toc)s
  </nav>
  <a class="back" href="index.html">← 返回首页</a>
  <a class="back" href="%(mistakes)s">错题练习 →</a>
</aside>
<main>
  <div class="pagehead">
    <div class="crumb"><a href="index.html">首页</a><span>/</span><a href="%(self)s">%(name)s</a><span>/</span>知识点学习</div>
    <h1>%(title)s<span class="badge">%(badge)s</span></h1>
    <p class="lead">%(lead)s</p>
    <div class="inline-search" data-search-open>
      <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
      <div class="ph">在本页搜索%(name)s知识点</div><kbd>/</kbd>
    </div>
    <div class="quick" style="margin-top:14px">%(quick)s<a href="%(mistakes)s">→ 本科错题练习</a></div>
  </div>
  <div class="doc">
%(body)s
  </div>
</main>
</div>
<footer class="sitefoot" style="max-width:1240px">
  <div>内容按人教版教材与高考题型编排，用于复习与查知识点。例句、例文为教学示例，非原卷摘录。</div>
</footer>
<script src="assets/site.js"></script>
<script src="assets/search.js"></script>
<script>
(function(){
  var items = KB.search.buildFromDoc();
  KB.search.init({items:items, scope:'%(name)s', placeholder:'在本页搜索%(name)s知识点', tip:'%(tip)s，共 ' + items.length + ' 个条目。'});
  /* 侧栏高亮 */
  var links = [].slice.call(document.querySelectorAll('.side nav a'));
  var secs = links.map(function(a){ return document.querySelector(a.getAttribute('href')); });
  function onScroll(){
    var pos = window.scrollY + 150, cur = 0;
    for(var i=0;i<secs.length;i++){ if(secs[i] && secs[i].offsetTop <= pos) cur = i; }
    links.forEach(function(a,i){ a.classList.toggle('on', i===cur); });
  }
  window.addEventListener('scroll', onScroll, {passive:true}); onScroll();
})();
</script>
</body>
</html>
''' % dict(title=cfg['title'], name=cfg['name'], accent=cfg['accent'], accent_s=cfg['accent_s'],
           badge=cfg['badge'], lead=cfg['lead'], mistakes=cfg['mistakes'],
           self=key + '-knowledge.html', topbar=topbar(cfg['name']),
           toc='\n    '.join(toc), quick=''.join(quick), body=body, tip=cfg['tip'])

    out = os.path.join(D, key + '-knowledge.html')
    open(out, 'w', encoding='utf-8').write(html)
    print('  %-8s → %-22s %.1f KB（%d 章）' %
          (key, key + '-knowledge.html', len(html.encode()) / 1024, len(toc)))


if __name__ == '__main__':
    keys = sys.argv[1:] or list(CFG.keys())
    for k in keys:
        build(k, CFG[k])
