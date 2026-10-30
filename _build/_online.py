# -*- coding: utf-8 -*-
"""线上验证：13 个页面 + 静态资源"""
import urllib.request, ssl, re, time, os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
BASE = 'https://luofeicq.github.io/kb-site/'
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAGES = ['', 'math-knowledge.html', 'math-mistakes.html',
         'physics-knowledge.html', 'physics-mistakes.html',
         'bio-knowledge.html', 'bio-mistakes.html',
         'chem-knowledge.html', 'chem-mistakes.html',
         'chinese-knowledge.html', 'chinese-mistakes.html',
         'english-knowledge.html', 'english-mistakes.html']
ASSETS = ['assets/base.css', 'assets/mistakes.css', 'assets/site.js',
          'assets/search.js', 'assets/mistakes.js', 'assets/index.js',
          'data/mistakes-physics.js']

ok = bad = 0
for path in PAGES + ASSETS:
    url = BASE + path
    name = path or 'index.html'
    for a in range(4):
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache'})
            with urllib.request.urlopen(req, timeout=45, context=ctx) as r:
                body = r.read()
                code = r.status
            txt = body.decode('utf-8', 'replace')
            extra = ''
            if path.endswith('.html') or path == '':
                t = re.search(r'<title>(.*?)</title>', txt, re.S)
                loc = open(os.path.join(D, name), 'rb').read()
                same = body.replace(b'\r\n', b'\n') == loc.replace(b'\r\n', b'\n')
                extra = 'canvas=%-2d details=%-3d 一致=%s' % (
                    txt.count('<canvas'), txt.count('<details>'), same)
                print('%-24s %d %7.1f KB  %-34s %s' % (
                    name, code, len(body) / 1024,
                    (t.group(1).strip() if t else '')[:30], extra))
            else:
                print('%-24s %d %7.1f KB' % (name, code, len(body) / 1024))
            ok += 1
            break
        except Exception as e:
            if a == 3:
                print('%-24s 失败 %s' % (name, str(e)[:90]))
                bad += 1
            else:
                time.sleep(5)
print('\n成功 %d，失败 %d' % (ok, bad))
