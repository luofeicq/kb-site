/* 站点外壳脚本：注入到三个学科页 */
(function(){
  "use strict";
  var IDX = window.__KBIDX || [];
  var PAGE = window.__KBPAGE || '';   /* 当前页文件名 */

  /* ---------- 进度条 ---------- */
  var pg = document.createElement('div');
  pg.className = 'pgbar';
  document.body.appendChild(pg);
  function onScroll(){
    var h = document.documentElement.scrollHeight - window.innerHeight;
    var p = h > 0 ? (window.scrollY / h) * 100 : 0;
    pg.style.width = Math.min(100, Math.max(0, p)) + '%';
    tt.classList.toggle('on', window.scrollY > 600);
  }

  /* ---------- 返回顶部 ---------- */
  var tt = document.createElement('button');
  tt.className = 'totop';
  tt.setAttribute('aria-label', '返回顶部');
  tt.innerHTML = '<svg viewBox="0 0 24 24"><path d="M12 19V5M5 12l7-7 7 7"/></svg>';
  tt.addEventListener('click', function(){ window.scrollTo({top:0, behavior:'smooth'}); });
  document.body.appendChild(tt);
  window.addEventListener('scroll', onScroll, {passive:true});
  onScroll();

  /* ---------- 搜索 ---------- */
  var SK = [['物理','phy','physics.html'],['化学','chem','chem.html'],['生物','bio','bio.html']];

  var mask = document.createElement('div');
  mask.className = 'kbs';
  mask.innerHTML =
    '<div class="kbs-box">' +
      '<div class="kbs-head">' +
        '<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>' +
        '<input class="kbs-input" id="kbsIn" type="text" placeholder="搜索知识点，例如：勒夏特列、减数分裂、单摆" autocomplete="off" spellcheck="false">' +
        '<button class="kbs-close" id="kbsClose">ESC</button>' +
      '</div>' +
      '<div class="kbs-body" id="kbsBody"></div>' +
      '<div class="kbs-foot">' +
        '<span>↑↓ 选择　<b>Enter</b> 打开　<b>Esc</b> 关闭</span>' +
        '<span id="kbsCnt"></span>' +
      '</div>' +
    '</div>';
  document.body.appendChild(mask);

  var inp = mask.querySelector('#kbsIn');
  var body = mask.querySelector('#kbsBody');
  var cnt = mask.querySelector('#kbsCnt');
  var items = [], sel = -1;

  function esc(s){
    return String(s).replace(/[&<>"]/g, function(c){
      return ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'})[c];
    });
  }
  function hl(text, q){
    if(!q) return esc(text);
    var i = text.toLowerCase().indexOf(q.toLowerCase());
    if(i < 0) return esc(text);
    return esc(text.slice(0,i)) + '<mark>' + esc(text.slice(i, i+q.length)) + '</mark>' + esc(text.slice(i+q.length));
  }

  function search(q){
    q = q.trim();
    if(!q){
      body.innerHTML = '<div class="kbs-tip">' +
        '输入关键词即可跨三科查找。<b>查概念</b>试“勒夏特列”“动作电位”“机械能守恒”；' +
        '<b>查题型</b>试“波的图像”“滴定”“遗传规律”。<br>' +
        '也可以直接点顶部的科目，用左侧目录浏览全部章节。</div>';
      cnt.textContent = '';
      items = []; sel = -1;
      return;
    }
    var ql = q.toLowerCase();
    var hits = [];
    for(var i=0;i<IDX.length;i++){
      var it = IDX[i];
      var hay = (it.n + ' ' + it.c + ' ' + it.k).toLowerCase();
      var pos = hay.indexOf(ql);
      var loose = 0, key = ql;
      if(pos < 0){
        /* 整词没命中时按 2 字片段兜底，命中六成以上算相关 */
        if(ql.length >= 3){
          var grams = [], step = ql.length > 6 ? 2 : 1;
          for(var g=0; g+2<=ql.length; g+=step) grams.push(ql.substr(g,2));
          var hit = 0;
          for(var g2=0; g2<grams.length; g2++){ if(hay.indexOf(grams[g2]) >= 0) hit++; }
          if(grams.length && hit/grams.length >= 0.6){
            loose = hit / grams.length;
            key = grams[0];
            pos = hay.indexOf(grams[0]);
          } else continue;
        } else continue;
      }
      /* 命中位置所在的上下文片段 */
      var src = it.k || it.n;
      var p2 = src.toLowerCase().indexOf(key);
      var snip = '';
      if(p2 >= 0){
        var a = Math.max(0, p2 - 26), b = Math.min(src.length, p2 + key.length + 46);
        snip = (a > 0 ? '…' : '') + src.slice(a, b) + (b < src.length ? '…' : '');
      } else {
        snip = it.k.slice(0, 70);
      }
      var nl = it.n.toLowerCase(), cl = it.c.toLowerCase();
      var score = 0;
      if(nl.indexOf(ql) >= 0) score += 1000 - nl.indexOf(ql);   /* 章名命中最高优先 */
      if(cl.indexOf(ql) >= 0) score += 300;                      /* 章号（如“必修1 · 第1章”）命中 */
      var occ = hay.split(ql).length - 1;                        /* 词频 */
      score += Math.min(occ, 12) * 8;
      if(loose) score = score * loose * 0.6;                     /* 模糊命中降权 */
      hits.push({it: it, snip: snip, score: score, pos: pos});
    }
    hits.sort(function(a,b){
      if(b.score !== a.score) return b.score - a.score;
      return a.pos - b.pos;
    });
    hits = hits.slice(0, 24);

    if(!hits.length){
      body.innerHTML = '<div class="kbs-tip">没有找到「' + esc(q) + '」。<br>' +
        '试试<b>更短的词</b>：把“化学平衡移动”拆成“平衡”，只留核心名词。<br>' +
        '当前收录化学 13 章、生物 12 章、物理 6 个专题，未覆盖的内容自然搜不到。</div>';
      cnt.textContent = '0 条结果';
      items = []; sel = -1;
      return;
    }

    var cur = null, html = '';
    hits.forEach(function(h){
      if(h.it.s !== cur){
        if(cur) html += '';
        html += '<div class="kbs-grp">' + esc(h.it.s) + '</div>';
        cur = h.it.s;
      }
      var cls = SK.filter(function(x){ return x[0] === h.it.s; })[0][1];
      html += '<a class="kbs-item" href="' + h.it.f + '#' + h.it.id + '">' +
        '<div class="r1"><span class="kbs-tag ' + cls + '">' + esc(h.it.s) + '</span>' +
        '<span class="nm">' + hl(h.it.n, q) + '</span></div>' +
        '<div class="r2">' + esc(h.it.c) + '　' + hl(h.snip, q) + '</div></a>';
    });
    body.innerHTML = html;
    items = [].slice.call(body.querySelectorAll('.kbs-item'));
    sel = -1;
    cnt.textContent = hits.length + ' 条结果';
  }

  function open(){
    mask.classList.add('on');
    inp.value = '';
    search('');
    setTimeout(function(){ inp.focus(); }, 40);
  }
  function close(){
    mask.classList.remove('on');
    items = []; sel = -1;
  }
  function move(d){
    if(!items.length) return;
    sel = (sel + d + items.length) % items.length;
    items.forEach(function(el,i){ el.classList.toggle('sel', i === sel); });
    items[sel].scrollIntoView({block:'nearest'});
  }

  inp.addEventListener('input', function(){ search(inp.value); });
  mask.querySelector('#kbsClose').addEventListener('click', close);
  mask.addEventListener('click', function(e){ if(e.target === mask) close(); });
  inp.addEventListener('keydown', function(e){
    if(e.key === 'ArrowDown'){ e.preventDefault(); move(1); }
    else if(e.key === 'ArrowUp'){ e.preventDefault(); move(-1); }
    else if(e.key === 'Enter'){
      e.preventDefault();
      var t = sel >= 0 ? items[sel] : items[0];
      if(t) window.location.href = t.getAttribute('href');
    } else if(e.key === 'Escape'){ close(); }
  });

  var btns = [].slice.call(document.querySelectorAll('[data-kbs-open]'));
  btns.forEach(function(b){ b.addEventListener('click', open); });
  window.addEventListener('keydown', function(e){
    if((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k'){ e.preventDefault(); open(); }
    else if(e.key === '/' && document.activeElement.tagName !== 'INPUT' &&
            document.activeElement.tagName !== 'TEXTAREA'){
      e.preventDefault(); open();
    } else if(e.key === 'Escape' && mask.classList.contains('on')){ close(); }
  });
  window.__kbOpen = open;

  /* ---------- 从首页带 hash 跳进来时，闪一下目标 ---------- */
  if(location.hash){
    var target = document.querySelector(location.hash);
    if(target){
      setTimeout(function(){
        var box = target.closest('section') || target;
        box.classList.add('hit-flash');
        setTimeout(function(){ box.classList.remove('hit-flash'); }, 2000);
      }, 260);
    }
  }

  /* ---------- 侧栏当前章节高亮（沿用页面原有逻辑，只补顶栏偏移） ---------- */
  var side = document.querySelector('.side');
  if(side){ side.style.top = 'var(--bar-h)'; }
})();
