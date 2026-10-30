/* ============================================================
   全站通用脚本：阅读进度条 / 返回顶部 / 平滑锚点
   ============================================================ */
(function(){
  "use strict";

  /* 阅读进度 */
  var pg = document.createElement('div');
  pg.className = 'pgbar';
  document.body.appendChild(pg);

  /* 返回顶部 */
  var tt = document.createElement('button');
  tt.className = 'totop';
  tt.setAttribute('aria-label', '返回顶部');
  tt.title = '返回顶部';
  tt.innerHTML = '<svg viewBox="0 0 24 24"><path d="M12 19V5M5 12l7-7 7 7"/></svg>';
  tt.addEventListener('click', function(){ window.scrollTo({top:0, behavior:'smooth'}); });
  document.body.appendChild(tt);

  function onScroll(){
    var h = document.documentElement.scrollHeight - window.innerHeight;
    pg.style.width = (h > 0 ? Math.min(100, Math.max(0, window.scrollY / h * 100)) : 0) + '%';
    tt.classList.toggle('on', window.scrollY > 600);
  }
  window.addEventListener('scroll', onScroll, {passive:true});
  onScroll();

  /* 锚点闪烁 */
  function flash(){
    if(!location.hash) return;
    var t = null;
    try { t = document.querySelector(decodeURIComponent(location.hash)); } catch(e){}
    if(!t) return;
    setTimeout(function(){
      t.classList.add('hit-flash');
      setTimeout(function(){ t.classList.remove('hit-flash'); }, 2000);
    }, 240);
  }
  window.addEventListener('hashchange', flash);
  flash();
})();
