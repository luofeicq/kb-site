# -*- coding: utf-8 -*-
"""页面自检：渲染各页并回传关键指标"""
import subprocess, os, re, itertools

CH = r'C:/Program Files/Google/Chrome/Application/chrome.exe'
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(D)
BS = chr(92)
pre = '<script>window.__e=[];window.onerror=function(m,u,l){window.__e.push(m+"@L"+l);};</script>'
seq = itertools.count(1)
made = []


def run(f, js, budget=5000):
    s = open(os.path.join(D, f), encoding='utf-8').read()
    wrap = ('<script>window.addEventListener("load",function(){setTimeout(function(){try{%s}'
            'catch(x){window.__e.push("THROW:"+x.message);}'
            'var d=document.createElement("pre");d.id="R";d.textContent=JSON.stringify(window.__o);'
            'document.body.appendChild(d);},900);});</script>') % js
    page = s.replace('</head>', pre + '</head>').replace('</body>', wrap + '</body>')
    name = '_chk%d.html' % next(seq)
    p = os.path.join(D, name)
    open(p, 'w', encoding='utf-8').write(page)
    made.append(p)
    url = 'file:///' + p.replace(BS, '/')
    r = subprocess.run([CH, '--headless=new', '--disable-gpu', '--window-size=1280,1000',
                        '--virtual-time-budget=%d' % budget, '--dump-dom', url],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    m = re.search(r'id="R">([^<]*)', r.stdout)
    return m.group(1) if m else '未取到'


MIS_JS = '''
var o={};o.err=window.__e.length?window.__e.join(' | '):'none';
o.cards=document.querySelectorAll('.mcard').length;
o.total=document.getElementById('mTotal').textContent;
o.chips=document.querySelectorAll('#mChips .chip').length;
document.querySelectorAll('#mChips .chip')[1].click();
o.afterChip=document.querySelectorAll('.mcard').length;
document.querySelector('.mcard button[data-act="toggle"]').click();
o.ansOpen=!!document.querySelector('.mans.on');
document.querySelector('.mcard button[data-act="mark"]').click();
o.doneCnt=document.getElementById('mDone').textContent;
window.__o=o;
'''

KN_JS = '''
var o={};o.err=window.__e.length?window.__e.join(' | '):'none';
o.tab=!!document.querySelector('.subjtab');
o.onTab=(document.querySelector('.subjtab a.on')||{}).textContent;
o.h2=document.querySelectorAll('main h2').length;
o.h3id=document.querySelectorAll('main h3[id]').length;
o.nav=document.querySelectorAll('.sb-nav a').length;
window.__kbOpen();
var i=document.getElementById('kbsIn');
i.value='函数';i.dispatchEvent(new Event('input'));
o.hits=document.querySelectorAll('.kbs-item').length;
window.__o=o;
'''

HOME_JS = '''
var o={};o.err=window.__e.length?window.__e.join(' | '):'none';
o.idx=(window.KB_INDEX||[]).length;
o.cards=document.querySelectorAll('.subj').length;
window.__kbOpen();
var i=document.getElementById('kbsIn');
['动量','减数分裂','电解','三角函数','文言','勒夏特列','定语从句'].forEach(function(q){
  i.value=q;i.dispatchEvent(new Event('input'));
  var its=document.querySelectorAll('.kbs-item');
  o[q]= its.length ? its[0].getAttribute('href') : 0;
});
window.__o=o;
'''

KS = ['math', 'physics', 'bio', 'chem', 'chinese', 'english']
try:
    for k in KS:
        print('%-9s' % k, run('%s-mistakes.html' % k, MIS_JS))
    for k in KS:
        print('%-9s' % (k + '知'), run('%s-knowledge.html' % k, KN_JS))
    print('%-9s' % '首页', run('index.html', HOME_JS))
finally:
    for p in made:
        try:
            os.remove(p)
        except Exception:
            pass
