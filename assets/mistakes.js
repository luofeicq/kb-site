/* ============================================================
   错题练习模块
   数据：window.MISTAKES = [{ id, topic, type, source, q, opts, answer, analysis, points, level }]
   功能：专题筛选 / 搜索 / 查看解析 / 重做 / 标记掌握（localStorage）/ 进度
   ============================================================ */
(function(){
  "use strict";
  var DATA = window.MISTAKES || [];
  var SUBJ = window.M_SUBJECT || '本学科';
  var KEY = 'kb-mastered-' + SUBJ;

  var state = { topic: 'all', q: '', onlyTodo: false, solved: {} };

  /* ---------- 本地存储 ---------- */
  function load(){
    try{
      var raw = localStorage.getItem(KEY);
      state.solved = raw ? JSON.parse(raw) : {};
    }catch(e){ state.solved = {}; }
  }
  function save(){
    try{ localStorage.setItem(KEY, JSON.stringify(state.solved)); }catch(e){}
  }

  /* ---------- 工具 ---------- */
  function esc(s){
    return String(s == null ? '' : s).replace(/[&<>"]/g, function(c){
      return ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'})[c];
    });
  }
  function topics(){
    var seen = {}, out = [];
    DATA.forEach(function(d){ if(!seen[d.topic]){ seen[d.topic] = 1; out.push(d.topic); } });
    return out;
  }
  function match(d){
    if(state.topic !== 'all' && d.topic !== state.topic) return false;
    if(state.onlyTodo && state.solved[d.id]) return false;
    if(!state.q) return true;
    var hay = (d.topic + ' ' + d.q + ' ' + (d.points||[]).join(' ') + ' ' + (d.analysis||'')).toLowerCase();
    return hay.indexOf(state.q.toLowerCase()) >= 0;
  }

  /* ---------- 渲染 ---------- */
  function renderStats(){
    var total = DATA.length, done = 0;
    DATA.forEach(function(d){ if(state.solved[d.id]) done++; });
    var pct = total ? Math.round(done / total * 100) : 0;
    document.getElementById('mTotal').textContent = total;
    document.getElementById('mDone').textContent = done;
    document.getElementById('mTodo').textContent = total - done;
    document.getElementById('mPct').textContent = pct + '%';
    document.getElementById('mBar').style.width = pct + '%';
  }

  function renderChips(){
    var box = document.getElementById('mChips');
    var list = topics();
    var html = '<button class="chip' + (state.topic === 'all' ? ' on' : '') + '" data-t="all">全部 ' + DATA.length + '</button>';
    list.forEach(function(t){
      var n = DATA.filter(function(d){ return d.topic === t; }).length;
      html += '<button class="chip' + (state.topic === t ? ' on' : '') + '" data-t="' + esc(t) + '">' +
              esc(t) + ' ' + n + '</button>';
    });
    box.innerHTML = html;
  }

  function renderList(){
    var box = document.getElementById('mList');
    var list = DATA.filter(match);
    if(!list.length){
      box.innerHTML = '<div class="m-empty">没有符合条件的错题。' +
        (state.onlyTodo ? '（可以关掉“只看未掌握”）' : '') + '</div>';
      document.getElementById('mCount').textContent = '0 题';
      return;
    }
    document.getElementById('mCount').textContent = list.length + ' 题';
    var html = '';
    list.forEach(function(d, i){
      var done = !!state.solved[d.id];
      var opts = (d.opts || []).map(function(o){ return '<div class="m-opt">' + esc(o) + '</div>'; }).join('');
      var pts = (d.points || []).map(function(p){ return '<span class="m-pt">' + esc(p) + '</span>'; }).join('');
      html +=
        '<article class="mcard' + (done ? ' done' : '') + '" id="q-' + d.id + '">' +
          '<div class="mcard-h">' +
            '<span class="mno">' + (i+1) + '</span>' +
            '<span class="mtopic">' + esc(d.topic) + '</span>' +
            '<span class="mtype">' + esc(d.type || '') + '</span>' +
            (d.level ? '<span class="mlv">' + '★'.repeat(d.level) + '</span>' : '') +
            '<span class="msrc">' + esc(d.source || '') + '</span>' +
            (done ? '<span class="mdone">已掌握</span>' : '') +
          '</div>' +
          '<div class="mbody">' +
            '<div class="mq">' + esc(d.q).replace(/\n/g, '<br>') + '</div>' +
            opts +
            (pts ? '<div class="mpts">' + pts + '</div>' : '') +
            '<div class="mact">' +
              '<button class="mbtn primary" data-act="toggle" data-id="' + d.id + '">看答案与解析</button>' +
              '<button class="mbtn" data-act="mark" data-id="' + d.id + '">' +
                (done ? '取消已掌握' : '标记为已掌握') + '</button>' +
              '<button class="mbtn ghost" data-act="retry" data-id="' + d.id + '">重做一次</button>' +
            '</div>' +
            '<div class="mans" id="ans-' + d.id + '">' +
              '<div class="mans-in">' +
                '<div class="mrow"><b>答案</b><span class="mkey">' + esc(d.answer) + '</span></div>' +
                '<div class="mrow"><b>解析</b><span>' + esc(d.analysis).replace(/\n/g, '<br>') + '</span></div>' +
              '</div>' +
            '</div>' +
          '</div>' +
        '</article>';
    });
    box.innerHTML = html;
  }

  function refresh(){
    renderStats(); renderChips(); renderList();
    /* 同步给站内搜索 */
    if(window.KB && KB.search && window.__kbSearchItems){
      window.__kbSearchItems(DATA);
    }
  }

  /* ---------- 交互 ---------- */
  function bind(){
    document.getElementById('mChips').addEventListener('click', function(e){
      var b = e.target.closest('button[data-t]');
      if(!b) return;
      state.topic = b.getAttribute('data-t');
      refresh();
    });
    document.getElementById('mSearch').addEventListener('input', function(e){
      state.q = e.target.value.trim();
      renderList();
    });
    document.getElementById('mOnly').addEventListener('change', function(e){
      state.onlyTodo = e.target.checked;
      renderList();
    });
    document.getElementById('mReset').addEventListener('click', function(){
      if(!confirm('确定清空所有「已掌握」标记吗？')) return;
      state.solved = {}; save(); refresh();
    });
    document.getElementById('mList').addEventListener('click', function(e){
      var b = e.target.closest('button[data-act]');
      if(!b) return;
      var id = b.getAttribute('data-id'), act = b.getAttribute('data-act');
      if(act === 'toggle'){
        var box = document.getElementById('ans-' + id);
        var open = box.classList.toggle('on');
        b.textContent = open ? '收起解析' : '看答案与解析';
      } else if(act === 'mark'){
        if(state.solved[id]) delete state.solved[id];
        else state.solved[id] = Date.now();
        save(); refresh();
      } else if(act === 'retry'){
        var card = document.getElementById('q-' + id);
        var ans = document.getElementById('ans-' + id);
        ans.classList.remove('on');
        var tb = card.querySelector('button[data-act="toggle"]');
        if(tb) tb.textContent = '看答案与解析';
        card.classList.add('retrying');
        setTimeout(function(){ card.classList.remove('retrying'); }, 1600);
        card.scrollIntoView({behavior:'smooth', block:'center'});
      }
    });
  }

  /* ---------- 启动 ---------- */
  function start(){
    if(!DATA.length){
      document.getElementById('mList').innerHTML = '<div class="m-empty">本学科暂无错题数据。</div>';
      return;
    }
    load(); bind(); refresh();
  }
  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', start);
  } else { start(); }
})();
