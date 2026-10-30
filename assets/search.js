/* ============================================================
   站内搜索组件
   用法：
     KB.search.init({ items:[...], scope:'化学', placeholder:'…' })
     items: [{ g:分组, n:标题, d:摘要, u:链接 }]
     KB.search.buildFromDoc()  从当前页面标题自动生成 items
   ============================================================ */
(function(){
  "use strict";
  var KB = window.KB = window.KB || {};

  var cfg = { items: [], scope: '', placeholder: '搜索本页内容' };
  var mask, inp, body, cnt, sel = -1, hits = [];

  function esc(s){
    return String(s).replace(/[&<>"]/g, function(c){
      return ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'})[c];
    });
  }
  function hl(text, q){
    if(!q) return esc(text);
    var i = text.toLowerCase().indexOf(q.toLowerCase());
    if(i < 0) return esc(text);
    return esc(text.slice(0,i)) + '<mark>' + esc(text.slice(i, i+q.length)) +
           '</mark>' + esc(text.slice(i+q.length));
  }

  /* ---------- 面板 ---------- */
  function mount(){
    if(mask) return;
    mask = document.createElement('div');
    mask.className = 'kbs';
    mask.innerHTML =
      '<div class="kbs-box">' +
        '<div class="kbs-head">' +
          '<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>' +
          '<input class="kbs-input" id="kbsIn" type="text" autocomplete="off" spellcheck="false">' +
          '<button class="kbs-close" id="kbsClose">ESC</button>' +
        '</div>' +
        '<div class="kbs-body" id="kbsBody"></div>' +
        '<div class="kbs-foot"><span>↑↓ 选择　<b>Enter</b> 打开　<b>Esc</b> 关闭</span>' +
        '<span id="kbsCnt"></span></div>' +
      '</div>';
    document.body.appendChild(mask);
    inp = mask.querySelector('#kbsIn');
    body = mask.querySelector('#kbsBody');
    cnt = mask.querySelector('#kbsCnt');

    inp.addEventListener('input', function(){ render(inp.value); });
    inp.addEventListener('keydown', onKey);
    mask.querySelector('#kbsClose').addEventListener('click', close);
    mask.addEventListener('click', function(e){ if(e.target === mask) close(); });
  }

  /* ---------- 检索 ---------- */
  function query(q){
    q = q.trim();
    if(!q) return [];
    var ql = q.toLowerCase(), out = [];
    cfg.items.forEach(function(it){
      var hay = ((it.n||'') + ' ' + (it.g||'') + ' ' + (it.d||'')).toLowerCase();
      var pos = hay.indexOf(ql), loose = 0, key = ql;
      if(pos < 0){
        if(ql.length < 3) return;
        var grams = [], step = ql.length > 6 ? 2 : 1;
        for(var g=0; g+2<=ql.length; g+=step) grams.push(ql.substr(g,2));
        var hit = 0;
        grams.forEach(function(gm){ if(hay.indexOf(gm) >= 0) hit++; });
        if(!grams.length || hit/grams.length < 0.6) return;
        loose = hit/grams.length; key = grams[0]; pos = hay.indexOf(grams[0]);
      }
      var nl = (it.n||'').toLowerCase(), score = 0;
      if(nl.indexOf(ql) >= 0) score += 1000 - nl.indexOf(ql);
      if((it.g||'').toLowerCase().indexOf(ql) >= 0) score += 300;
      var occ = hay.split(ql).length - 1;
      score += Math.min(occ, 12) * 8;
      if(loose) score *= loose * 0.6;

      /* 摘要：定位到命中词附近 */
      var src = it.d || it.n || '';
      var p2 = src.toLowerCase().indexOf(key);
      var snip = src.slice(0, 78);
      if(p2 >= 0){
        var a = Math.max(0, p2 - 22), b = Math.min(src.length, p2 + key.length + 52);
        snip = (a > 0 ? '…' : '') + src.slice(a, b) + (b < src.length ? '…' : '');
      }
      out.push({ it: it, snip: snip, score: score, pos: pos });
    });
    out.sort(function(x,y){
      if(y.score !== x.score) return y.score - x.score;
      return x.pos - y.pos;
    });
    return out.slice(0, 30);
  }

  function render(q){
    if(!q.trim()){
      body.innerHTML = '<div class="kbs-tip">' + cfg.tip +
        '<br>也可以直接使用浏览器查找（<b>Ctrl/Cmd + F</b>）在<em>当前页</em>里定位文字。</div>';
      cnt.textContent = '';
      hits = []; sel = -1;
      return;
    }
    hits = query(q);
    if(!hits.length){
      body.innerHTML = '<div class="kbs-empty">没有找到「' + esc(q) + '」。<br>' +
        '<span style="font-size:12.5px">试试更短的词，只保留核心名词。</span></div>';
      cnt.textContent = '0 条';
      sel = -1;
      return;
    }
    var cur = null, html = '';
    hits.forEach(function(h){
      if(h.it.g !== cur){ html += '<div class="kbs-grp">' + esc(h.it.g || '') + '</div>'; cur = h.it.g; }
      html += '<a class="kbs-item" href="' + h.it.u + '">' +
        '<div class="r1"><span class="kbs-tag">' + esc(h.it.tag || cfg.scope) + '</span>' +
        '<span class="nm">' + hl(h.it.n, q) + '</span></div>' +
        '<div class="r2">' + hl(h.snip, q) + '</div></a>';
    });
    body.innerHTML = html;
    hits = [].slice.call(body.querySelectorAll('.kbs-item'));
    sel = -1;
    cnt.textContent = hits.length + ' 条';
  }

  /* ---------- 键盘 ---------- */
  function move(d){
    if(!hits.length) return;
    sel = (sel + d + hits.length) % hits.length;
    hits.forEach(function(el,i){ el.classList.toggle('sel', i === sel); });
    hits[sel].scrollIntoView({block:'nearest'});
  }
  function onKey(e){
    if(e.key === 'ArrowDown'){ e.preventDefault(); move(1); }
    else if(e.key === 'ArrowUp'){ e.preventDefault(); move(-1); }
    else if(e.key === 'Enter'){
      e.preventDefault();
      var t = sel >= 0 ? hits[sel] : hits[0];
      if(t) window.location.href = t.getAttribute('href');
    } else if(e.key === 'Escape'){ close(); }
  }

  function open(prefill){
    mount();
    mask.classList.add('on');
    inp.value = prefill || '';
    render(inp.value);
    setTimeout(function(){ inp.focus(); }, 40);
  }
  function close(){
    if(mask) mask.classList.remove('on');
    hits = []; sel = -1;
  }

  /* ---------- 从页面标题自动建索引 ---------- */
  function buildFromDoc(){
    var nodes = [].slice.call(document.querySelectorAll('main h2, main h3, main h4'));
    var items = [], seq = 0, subs = { h2:'章节', h3:'小节', h4:'要点' };
    nodes.forEach(function(h, i){
      if(!h.id){
        h.id = 'sec-' + i;
      }
      var lv = h.tagName.toLowerCase();
      /* 取本节正文：向后收集直到遇到同级或更高级标题 */
      var txt = '', el = h.nextElementSibling, guard = 0;
      while(el && guard < 40){
        if(/^H[2-4]$/.test(el.tagName) && el.tagName.toLowerCase() <= lv) break;
        txt += ' ' + el.textContent;
        el = el.nextElementSibling; guard++;
      }
      txt = txt.replace(/\s+/g, ' ').trim().slice(0, 320);
      var name = h.textContent.replace(/\s+/g, ' ').trim();
      if(!name) return;
      items.push({
        g: subs[lv],
        n: name,
        d: txt,
        u: '#' + h.id,
        tag: lv.toUpperCase()
      });
      seq++;
    });
    return items;
  }

  /* ---------- 对外接口 ---------- */
  KB.search = {
    init: function(o){
      cfg.items = o.items || [];
      cfg.scope = o.scope || '';
      cfg.placeholder = o.placeholder || '搜索本页内容';
      cfg.tip = o.tip || ('在<b>' + (o.scope || '本页') + '</b>里查找知识点，共 ' + cfg.items.length + ' 个条目。');
      mount();
      inp.setAttribute('placeholder', cfg.placeholder);
      /* 页面上的搜索框 */
      [].forEach.call(document.querySelectorAll('[data-search-open]'), function(el){
        el.addEventListener('click', function(){ open(el.getAttribute('data-q') || ''); });
      });
      /* 快捷键 */
      window.addEventListener('keydown', function(e){
        if((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k'){ e.preventDefault(); open(); }
        else if(e.key === '/' ){
          var t = document.activeElement.tagName;
          if(t !== 'INPUT' && t !== 'TEXTAREA'){ e.preventDefault(); open(); }
        }
      });
      window.__kbOpen = open;
    },
    open: open,
    close: close,
    buildFromDoc: buildFromDoc,
    setItems: function(items){ cfg.items = items || []; }
  };
})();
