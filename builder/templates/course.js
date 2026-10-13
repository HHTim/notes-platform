/* ── 純邏輯：題目指紋與錯題紀錄的進出（node 測試也會載入這段，所以不碰 document）──
   錯題鍵 = 課slug|題目序號|題目文字指紋。題目文字改過，指紋就對不上，舊紀錄自動視為不存在。
   紀錄形狀 {streak: 連對次數, removed: 移除時間（0＝還在）, at: 最後更動時間}，時間都是秒。 */
var NotesQuiz = {
  /* FNV-1a 32 位元雜湊（把任意文字算成固定長度代碼的簡單算法），轉 36 進位取 6 碼 */
  fingerprint: function (text) {
    var h = 0x811c9dc5;
    for (var i = 0; i < text.length; i++) {
      h ^= text.charCodeAt(i);
      h = Math.imul(h, 0x01000193) >>> 0;
    }
    return ('000000' + h.toString(36)).slice(-6);
  },
  wrongKey: function (slug, qi, qtext) { return slug + '|' + qi + '|' + NotesQuiz.fingerprint(qtext); },
  _copy: function (wrong) {
    var out = {};
    Object.keys(wrong || {}).forEach(function (k) {
      var r = wrong[k] || {};
      out[k] = { streak: r.streak || 0, removed: r.removed || 0, at: r.at || 0 };
    });
    return out;
  },
  /* 隨堂測驗對完：答錯的進錯題區（連對歸零、移除取消）；答對的不動 */
  afterQuiz: function (wrong, results, now) {
    var out = NotesQuiz._copy(wrong);
    results.forEach(function (r) {
      if (r.right) return;
      out[NotesQuiz.wrongKey(r.slug, r.qi, r.q)] = { streak: 0, removed: 0, at: now };
    });
    return out;
  },
  /* 錯題區練習對完：答對連對加一，到兩次就記移除時間；答錯歸零 */
  afterPractice: function (wrong, results, now) {
    var out = NotesQuiz._copy(wrong);
    results.forEach(function (r) {
      var k = NotesQuiz.wrongKey(r.slug, r.qi, r.q);
      var cur = out[k] || { streak: 0, removed: 0, at: 0 };
      if (r.right) {
        var s = cur.streak + 1;
        out[k] = { streak: s, removed: s >= 2 ? now : 0, at: now };
      } else {
        out[k] = { streak: 0, removed: 0, at: now };
      }
    });
    return out;
  },
  /* 手動移除：留著當記號（避免舊裝置同步時加回來），只記移除時間 */
  remove: function (wrong, key, now) {
    var out = NotesQuiz._copy(wrong);
    var cur = out[key] || { streak: 0, removed: 0, at: 0 };
    out[key] = { streak: cur.streak, removed: now, at: now };
    return out;
  },
  /* 目前還在錯題區的題目，依課序、題序排 */
  active: function (wrong, quiz, slugs) {
    var out = [];
    if (!wrong) return out;
    slugs.forEach(function (slug) {
      (quiz[slug] || []).forEach(function (q, qi) {
        var k = NotesQuiz.wrongKey(slug, qi, q.q);
        var r = wrong[k];
        if (r && !r.removed && (r.streak || 0) < 2) out.push({ key: k, slug: slug, qi: qi, q: q, streak: r.streak || 0 });
      });
    });
    return out;
  }
};
if (typeof module !== 'undefined' && module.exports) { module.exports = NotesQuiz; }

/* ── 以下是頁面行為，只在瀏覽器裡跑 ── */
if (typeof document !== 'undefined') (function(){
var KEY='notes-progress:'+MODULE;
function loadDone(){try{return JSON.parse(localStorage.getItem(KEY))||{};}catch(e){return {};}}
function saveDone(d){
  try{localStorage.setItem(KEY,JSON.stringify(d));}catch(e){}
  try{document.dispatchEvent(new CustomEvent('notes:progress-saved',{detail:{module:MODULE,data:d}}));}catch(e){}
}
function refreshTicks(){
  var d=loadDone(),n=0;
  SLUGS.forEach(function(s){ if(d[s]&&d[s].done)n++; });
  document.querySelectorAll('[data-tick]').forEach(function(el){
    var slug=el.closest('a').getAttribute('data-nav');
    el.hidden=!(d[slug]&&d[slug].done);
  });
  document.querySelectorAll('[data-ovtick]').forEach(function(el){
    var k=el.getAttribute('data-ovtick');el.hidden=!(d[k]&&d[k].done);
  });
  var p=document.getElementById('ovProgress');
  if(p) p.innerHTML='已完成 <b>'+n+'</b> / '+SLUGS.length+' 課'+(n===SLUGS.length?'——全部打勾了 🎉':'');
  var sp=document.getElementById('sideProg');
  if(sp) sp.innerHTML='已完成 <b>'+n+'</b> / '+SLUGS.length+' 課';
}
function shuffle(a){
  for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=a[i];a[i]=a[j];a[j]=t;}
  return a;
}
function renderQuiz(slug){
  var host=document.querySelector('[data-quiz="'+slug+'"]');
  if(!host||!QUIZ[slug])return;
  var qs=QUIZ[slug];
  host.innerHTML='';
  var head=document.createElement('div');
  head.innerHTML='<div class="qhead"><span class="qtag">QUIZ · 隨堂測驗</span><span class="qtitle">檢查你學會了沒</span></div>'
    +'<p class="qnote">共 '+qs.length+' 題，選項順序每次都會重排。全部選好後按「對答案」；全對就在側邊欄打勾。</p>';
  host.appendChild(head);
  var picks=qs.map(function(){return null;});
  var graded=false;
  qs.forEach(function(q,qi){
    var wrap=document.createElement('div');wrap.className='qq';
    var qt=document.createElement('p');qt.className='qt';
    qt.innerHTML='<span class="qn">Q'+(qi+1)+'</span>'+q.q;
    wrap.appendChild(qt);
    var opts=document.createElement('div');opts.className='opts';
    var order=shuffle(q.opts.map(function(_,k){return k;}));
    order.forEach(function(oi){
      var b=document.createElement('button');b.type='button';b.className='opt';
      b.setAttribute('data-oi',oi);
      b.innerHTML='<span class="dot"></span><span>'+q.opts[oi]+'</span>';
      b.addEventListener('click',function(){
        if(graded)return;
        picks[qi]=oi;
        opts.querySelectorAll('.opt').forEach(function(x){x.classList.remove('sel');});
        b.classList.add('sel');
        btn.disabled=picks.some(function(p){return p===null;});
        msg.textContent=btn.disabled?'請先回答全部 '+qs.length+' 題':'都選好了，按「對答案」';
        msg.className='qmsg';
      });
      opts.appendChild(b);
    });
    wrap.appendChild(opts);
    var exp=document.createElement('p');exp.className='exp';exp.hidden=true;
    exp.setAttribute('data-exp',qi);
    wrap.appendChild(exp);
    host.appendChild(wrap);
  });
  var act=document.createElement('div');act.className='qact';
  var btn=document.createElement('button');btn.className='qbtn';btn.textContent='對答案';btn.disabled=true;
  var msg=document.createElement('span');msg.className='qmsg';msg.textContent='請先回答全部 '+qs.length+' 題';
  act.appendChild(btn);act.appendChild(msg);host.appendChild(act);
  btn.addEventListener('click',function(){
    if(graded){renderQuiz(slug);return;}
    graded=true;var allRight=true;
    qs.forEach(function(q,qi){
      var opts=host.querySelectorAll('.qq')[qi].querySelectorAll('.opt');
      opts.forEach(function(b){
        b.disabled=true;
        var oi=+b.getAttribute('data-oi');
        if(oi===0)b.classList.add('right');
        else if(picks[qi]===oi)b.classList.add('wrongpick');
      });
      var exp=host.querySelector('[data-exp="'+qi+'"]');
      var right=picks[qi]===0;
      if(!right)allRight=false;
      exp.hidden=false;
      exp.className='exp'+(right?'':' bad');
      exp.innerHTML=(right?'✓ 答對。':'✗ 正確答案是打勾那一個。')+' '+q.exp;
    });
    btn.textContent='再測一次';btn.disabled=false;
    var rightCount=0;
    qs.forEach(function(q,qi){if(picks[qi]===0)rightCount++;});
    var d=loadDone();
    var rec=d[slug]||{best:0,total:qs.length,done:false};
    rec.total=qs.length;
    if(rightCount>rec.best)rec.best=rightCount;
    if(allRight)rec.done=true;
    d[slug]=rec;saveDone(d);refreshTicks();
    if(allRight){
      msg.textContent='✓ 全對！已在側邊欄打勾';msg.className='qmsg pass';
    }else{
      msg.textContent='有幾題再想想——看完解析可以「再測一次」';msg.className='qmsg fail';
    }
  });
}
/* 課中練習：點一個選項就公布對錯與解析，不計分、不記錄 */
function initDrills(){
  document.querySelectorAll('.drill').forEach(function(d){
    var exp=d.querySelector('.dexp');if(exp)exp.hidden=true;
    var lis=d.querySelectorAll('.dopts li');
    lis.forEach(function(li){
      li.setAttribute('role','button');li.setAttribute('tabindex','0');
      li.insertAdjacentHTML('afterbegin','<span class="dot"></span>');
      function pick(){
        if(d.classList.contains('answered'))return;
        d.classList.add('answered');
        var ok=li.hasAttribute('data-ok');
        lis.forEach(function(x){
          x.setAttribute('aria-disabled','true');x.removeAttribute('tabindex');
          if(x.hasAttribute('data-ok'))x.classList.add('right');
        });
        if(!ok)li.classList.add('wrongpick');
        if(exp){exp.hidden=false;exp.className='dexp'+(ok?'':' bad');
          exp.insertAdjacentHTML('afterbegin',ok?'✓ 答對。':'✗ 正確答案是綠色那個。');}
      }
      li.addEventListener('click',pick);
      li.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();pick();}});
    });
  });
}
initDrills();
/* 路由 */
var sidebar=document.getElementById('sidebar'),scrim=document.getElementById('scrim');
document.getElementById('burger').addEventListener('click',function(){
  sidebar.classList.toggle('open');scrim.classList.toggle('show');
});
scrim.addEventListener('click',function(){sidebar.classList.remove('open');scrim.classList.remove('show');});
sidebar.addEventListener('click',function(e){
  if(e.target.closest('a')){sidebar.classList.remove('open');scrim.classList.remove('show');}
});
function route(){
  var h=location.hash||'#/';
  var m=h.match(/^#\/lesson\/([a-z0-9-]+)$/);
  var slug=m&&SLUGS.indexOf(m[1])>=0?m[1]:null;
  document.querySelectorAll('main > article').forEach(function(a){a.hidden=true;});
  var pg=document.getElementById(slug?('pg-'+slug):'pg-ov');
  if(!pg){pg=document.getElementById('pg-ov');slug=null;}
  pg.hidden=false;
  document.querySelectorAll('.sidebar a').forEach(function(a){
    a.classList.toggle('active',a.getAttribute('data-nav')===(slug||'ov'));
  });
  if(slug)renderQuiz(slug);
  refreshTicks();
  window.scrollTo(0,0);
  try{localStorage.setItem('notes-last:'+MODULE,h);}catch(e){}
}
window.addEventListener('hashchange',route);
/* 回到上次看的課 */
if(!location.hash){
  var last=null;try{last=localStorage.getItem('notes-last:'+MODULE);}catch(e){}
  if(last&&last!=='#/')location.hash=last;
}
route();
var modsel=document.getElementById('modsel');
if(modsel)modsel.addEventListener('change',function(){location.href='../'+this.value+'/';});
window.NotesCourse={module:MODULE,slugs:SLUGS,loadDone:loadDone,saveDone:saveDone,refreshTicks:refreshTicks};
})();
