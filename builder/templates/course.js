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
function now(){return Math.floor(Date.now()/1000);}
function loadDone(){try{return JSON.parse(localStorage.getItem(KEY))||{};}catch(e){return {};}}
function saveDone(d){
  try{localStorage.setItem(KEY,JSON.stringify(d));}catch(e){}
  try{document.dispatchEvent(new CustomEvent('notes:progress-saved',{detail:{module:MODULE,data:d}}));}catch(e){}
}
function icon(name,cls){return '<svg class="'+(cls||'ic')+'" aria-hidden="true"><use href="#ic-'+name+'"/></svg>';}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function lessonLabel(slug){return '第 '+(SLUGS.indexOf(slug)+1)+' 課';}
function wrongActive(d){return NotesQuiz.active(d._wrong||{},QUIZ,SLUGS);}

/* 側欄與總覽的成績、錯題數；錯題區清單頁開著時一併重畫 */
function refreshTicks(){
  var d=loadDone(),n=0;
  SLUGS.forEach(function(s){ if(d[s]&&d[s].done)n++; });
  document.querySelectorAll('[data-st]').forEach(function(el){
    var r=d[el.getAttribute('data-st')];
    if(r&&r.done)el.innerHTML=icon('check','ic ok');
    else if(r&&r.best>0)el.textContent=r.best+'/'+r.total;
    else el.textContent='–';
  });
  document.querySelectorAll('[data-ovtick]').forEach(function(el){
    var k=el.getAttribute('data-ovtick');el.hidden=!(d[k]&&d[k].done);
  });
  var cnt=wrongActive(d).length;
  document.querySelectorAll('[data-wrongcnt]').forEach(function(el){el.hidden=!cnt;el.textContent=cnt;});
  var wc=document.getElementById('wrongCount');
  if(wc){wc.hidden=!cnt;wc.textContent=cnt+' 題';}
  var p=document.getElementById('ovProgress');
  if(p) p.innerHTML='已完成 <b>'+n+'</b> / '+SLUGS.length+' 課'+(n===SLUGS.length?'，全部打勾了':'');
  var sp=document.getElementById('sideProg');
  if(sp) sp.innerHTML='已完成 <b>'+n+'</b> / '+SLUGS.length+' 課';
  var pw=document.getElementById('pg-wrong');
  if(pw&&!pw.hidden&&!document.getElementById('wrongQuiz'))renderWrongList();
}
function shuffle(a){
  for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=a[i];a[i]=a[j];a[j]=t;}
  return a;
}

/* 題組畫面：隨堂測驗與錯題練習共用（改版規格第 4 節）。
   items：[{slug, qi, q:{q,opts,exp}, title?}]；q.opts[0] 永遠是正解（內容檔的慣例）。
   mode 'lesson'：記成績、答錯進錯題區；'practice'：只記錯題的連對。
   流程：全部選好 → 對答案 → 成績卡＋每題圈叉 → 「只重做錯的」把錯的清空重選、對的鎖住。 */
function renderQuiz(host,items,mode,slug){
  host.innerHTML='';
  var picks=items.map(function(){return null;});
  var locked=items.map(function(){return false;});   // 已答對、重做時不能動
  var graded=false;
  var head=document.createElement('div');head.className='qhead';
  head.innerHTML='<span class="qtitle">'+(mode==='lesson'?'隨堂測驗':'練習中')+'</span>'
    +'<span class="qnote">共 '+items.length+' 題，全部選好後按「對答案」'+(mode==='lesson'?'；全對這課才算完成':'')+'。</span>';
  host.appendChild(head);
  var score=document.createElement('div');score.className='score';score.hidden=true;host.appendChild(score);
  var act=document.createElement('div');act.className='qact';act.hidden=true;host.appendChild(act);
  var body=document.createElement('div');host.appendChild(body);
  var act2=document.createElement('div');act2.className='qact bottom';host.appendChild(act2);
  var btn=document.createElement('button');btn.type='button';btn.className='qbtn';btn.textContent='對答案';btn.disabled=true;
  var msg=document.createElement('span');msg.className='qmsg';
  act2.appendChild(btn);act2.appendChild(msg);

  function pending(){return picks.filter(function(p,i){return p===null&&!locked[i];}).length;}
  function updateBtn(){var n=pending();btn.disabled=n>0;msg.textContent=n>0?'還有 '+n+' 題沒選':'都選好了，按「對答案」';}

  function renderCard(i){
    var it=items[i],q=it.q;
    var wrap=document.createElement('div');wrap.className='qq';wrap.setAttribute('data-qi',i);
    var top=document.createElement('div');top.className='qtop';
    top.innerHTML='<span class="qn">Q'+(i+1)+'</span>'+(it.title?'<span class="src">'+esc(it.title)+'</span>':'')+'<span class="mk"></span>';
    wrap.appendChild(top);
    var qt=document.createElement('p');qt.className='qt';qt.innerHTML=q.q;wrap.appendChild(qt);
    var opts=document.createElement('div');opts.className='opts';
    var order=shuffle(q.opts.map(function(_,k){return k;}));
    order.forEach(function(oi,pos){
      var b=document.createElement('button');b.type='button';b.className='opt';b.setAttribute('data-oi',oi);
      b.innerHTML='<span class="l">'+String.fromCharCode(65+pos)+'</span><span class="tx">'+q.opts[oi]+'</span><span class="mk"></span>';
      b.addEventListener('click',function(){
        if(graded||locked[i])return;
        picks[i]=oi;
        opts.querySelectorAll('.opt').forEach(function(x){x.classList.remove('sel');});
        b.classList.add('sel');
        updateBtn();
      });
      opts.appendChild(b);
    });
    wrap.appendChild(opts);
    var exp=document.createElement('p');exp.className='exp';exp.hidden=true;wrap.appendChild(exp);
    return wrap;
  }
  items.forEach(function(_,i){body.appendChild(renderCard(i));});
  updateBtn();

  /* 批改一題：題目卡標圈叉、正解薄荷底、選錯桃底、顯示解說 */
  function markCard(i){
    var wrap=body.querySelector('[data-qi="'+i+'"]');
    var right=picks[i]===0;
    wrap.querySelector('.qtop .mk').innerHTML=icon(right?'ok':'no','ic '+(right?'ok':'no'));
    wrap.querySelectorAll('.opt').forEach(function(b){
      b.disabled=true;
      var oi=+b.getAttribute('data-oi');
      if(oi===0){b.classList.add('right');b.querySelector('.mk').innerHTML=icon('ok','ic ok');}
      else if(picks[i]===oi){b.classList.add('wrongpick');b.querySelector('.mk').innerHTML=icon('no','ic no');}
    });
    var exp=wrap.querySelector('.exp');exp.hidden=false;exp.innerHTML=items[i].q.exp;
    wrap.classList.add(right?'ok':'ng');
  }

  function grade(){
    graded=true;
    var results=[],rightCount=0,wrongIdx=[];
    items.forEach(function(it,i){
      var fresh=!locked[i];
      var right=picks[i]===0;
      if(fresh){markCard(i);results.push({slug:it.slug,qi:it.qi,q:it.q.q,right:right});}
      if(right){rightCount++;locked[i]=true;}else wrongIdx.push(i);
    });
    var d=loadDone(),best=null;
    if(mode==='lesson'){
      var rec=d[slug]||{best:0,total:items.length,done:false};
      rec.total=items.length;
      if(rightCount>rec.best)rec.best=rightCount;
      if(!wrongIdx.length)rec.done=true;
      d[slug]=rec;best=rec.best;
      d._wrong=NotesQuiz.afterQuiz(d._wrong||{},results,now());
    }else{
      d._wrong=NotesQuiz.afterPractice(d._wrong||{},results,now());
    }
    saveDone(d);refreshTicks();

    var note=best!==null?'最佳 '+best+'/'+items.length:(wrongIdx.length?'錯的題目留在錯題區':'這批全對');
    score.hidden=false;
    score.innerHTML='<div class="big">'+rightCount+'<small> / '+items.length+'</small></div>'
      +'<div class="t"><span class="mono">'+note+'</span><div class="tr"><i style="width:'+Math.round(rightCount*100/items.length)+'%"></i></div></div>';
    act.innerHTML='';act.hidden=false;act2.hidden=true;
    if(wrongIdx.length&&mode==='lesson'){   // 規格 5.3：錯題練習對完只有「回錯題區」，不給重做（重做會讓連對變得太容易）
      var b1=document.createElement('button');b1.type='button';b1.className='qbtn';b1.textContent='只重做錯的 '+wrongIdx.length+' 題';
      b1.addEventListener('click',function(){
        graded=false;
        wrongIdx.forEach(function(i){
          picks[i]=null;
          var old=body.querySelector('[data-qi="'+i+'"]');
          body.replaceChild(renderCard(i),old);
        });
        score.querySelector('.mono').textContent=note+' · 重做 '+wrongIdx.length+' 題中';
        act.hidden=true;act2.hidden=false;updateBtn();
      });
      act.appendChild(b1);
    }
    var b2=document.createElement('button');b2.type='button';b2.className='qbtn sec';
    b2.textContent=mode==='lesson'?'全部重做':'回錯題區';
    b2.addEventListener('click',function(){
      if(mode==='lesson')renderQuiz(host,items,mode,slug);else renderWrongList();
    });
    act.appendChild(b2);
    host.scrollIntoView({block:'start'});
  }
  btn.addEventListener('click',grade);
}

function renderLessonQuiz(slug){
  var host=document.querySelector('[data-quiz="'+slug+'"]');
  if(!host||!QUIZ[slug])return;
  renderQuiz(host,QUIZ[slug].map(function(q,qi){return {slug:slug,qi:qi,q:q};}),'lesson',slug);
}

/* 錯題區清單（改版規格第 5.2 節） */
function renderWrongList(){
  var body=document.getElementById('wrongBody');
  if(!body)return;
  var act=wrongActive(loadDone());
  if(!act.length){body.innerHTML='<p class="sub">目前沒有錯題。</p>';return;}
  var html='<p class="sub">課末測驗答錯的題目會收在這裡。連續答對兩次自動移除，也可以手動移除。</p>'
    +'<div class="legend"><span>'+icon('empty')+' 還沒對過</span><span>'+icon('half')+' 對過一次</span></div>'
    +'<div class="qact"><button type="button" class="qbtn" id="wrongStart">開始練習（'+act.length+' 題）</button></div>';
  var cur=null;
  act.forEach(function(x){
    if(x.slug!==cur){cur=x.slug;html+='<h4 class="wgroup">'+lessonLabel(cur)+' '+esc(TITLES[cur]||cur)+'</h4>';}
    html+='<div class="witem">'+icon(x.streak?'half':'empty')+'<div class="wq">'+x.q.q+'</div>'
      +'<button type="button" class="wrm" data-rm="'+esc(x.key)+'">移除</button></div>';
  });
  body.innerHTML=html;
  document.getElementById('wrongStart').addEventListener('click',function(){renderPractice(act);});
  body.querySelectorAll('[data-rm]').forEach(function(b){
    b.addEventListener('click',function(){
      var d=loadDone();
      d._wrong=NotesQuiz.remove(d._wrong||{},b.getAttribute('data-rm'),now());
      saveDone(d);refreshTicks();
    });
  });
}
/* 錯題區練習（改版規格第 5.3 節）：一次列出全部錯題，作答與對完畫面同隨堂測驗 */
function renderPractice(act){
  var body=document.getElementById('wrongBody');
  body.innerHTML='<div class="quiz" id="wrongQuiz"></div>';
  renderQuiz(document.getElementById('wrongQuiz'),
    act.map(function(x){return {slug:x.slug,qi:x.qi,q:x.q,title:lessonLabel(x.slug)};}),'practice',null);
}

/* 課中練習：點一個選項就公布對錯與解析，不計分、不記錄 */
function initDrills(){
  document.querySelectorAll('.drill').forEach(function(d){
    var exp=d.querySelector('.dexp');if(exp)exp.hidden=true;
    var lis=d.querySelectorAll('.dopts li');
    lis.forEach(function(li,pos){
      li.setAttribute('role','button');li.setAttribute('tabindex','0');
      li.insertAdjacentHTML('afterbegin','<span class="l">'+String.fromCharCode(65+pos)+'</span>');
      li.insertAdjacentHTML('beforeend','<span class="mk"></span>');
      function pick(){
        if(d.classList.contains('answered'))return;
        d.classList.add('answered');
        var ok=li.hasAttribute('data-ok');
        lis.forEach(function(x){
          x.setAttribute('aria-disabled','true');x.removeAttribute('tabindex');
          if(x.hasAttribute('data-ok')){x.classList.add('right');x.querySelector('.mk').innerHTML=icon('ok','ic ok');}
        });
        if(!ok){li.classList.add('wrongpick');li.querySelector('.mk').innerHTML=icon('no','ic no');}
        if(exp)exp.hidden=false;
      }
      li.addEventListener('click',pick);
      li.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();pick();}});
    });
  });
}
initDrills();

/* 本課小節：目錄連結捲到該節（不走網址，免得被路由當成換頁）；側欄小節隨捲動標目前位置 */
var sidebar=document.getElementById('sidebar'),scrim=document.getElementById('scrim');
function closeSidebar(){sidebar.classList.remove('open');scrim.classList.remove('show');}
document.addEventListener('click',function(e){
  var a=e.target.closest('[data-goto]');if(!a)return;
  e.preventDefault();
  var el=document.getElementById(a.getAttribute('data-goto'));
  if(el)el.scrollIntoView({block:'start'});
  closeSidebar();
});
var spy=null;
function watchSections(slug){
  if(spy){spy.disconnect();spy=null;}
  if(!('IntersectionObserver' in window))return;
  var heads=document.querySelectorAll('#pg-'+slug+' h3.head[id]');
  if(!heads.length)return;
  spy=new IntersectionObserver(function(entries){
    entries.forEach(function(en){
      if(!en.isIntersecting)return;
      var id=en.target.id;
      document.querySelectorAll('.subs[data-subs="'+slug+'"] a').forEach(function(a){
        a.classList.toggle('on',a.getAttribute('data-goto')===id);
      });
    });
  },{rootMargin:'-60px 0px -70% 0px'});
  heads.forEach(function(h){spy.observe(h);});
}

/* 路由：#/ 總覽、#/wrong 錯題區、#/lesson/<slug> 某課 */
document.getElementById('burger').addEventListener('click',function(){
  sidebar.classList.toggle('open');scrim.classList.toggle('show');
});
scrim.addEventListener('click',closeSidebar);
sidebar.addEventListener('click',function(e){
  if(e.target.closest('a[data-nav]'))closeSidebar();
});
function route(){
  var h=location.hash||'#/';
  var m=h.match(/^#\/lesson\/([a-z0-9-]+)$/);
  var slug=m&&SLUGS.indexOf(m[1])>=0?m[1]:null;
  var nav=slug||(h==='#/wrong'?'wrong':'ov');
  document.querySelectorAll('main > article').forEach(function(a){a.hidden=true;});
  var pg=document.getElementById(slug?'pg-'+slug:(nav==='wrong'?'pg-wrong':'pg-ov'));
  if(!pg){pg=document.getElementById('pg-ov');slug=null;nav='ov';}
  pg.hidden=false;
  document.querySelectorAll('.sidebar a[data-nav]').forEach(function(a){
    a.classList.toggle('active',a.getAttribute('data-nav')===nav);
  });
  document.querySelectorAll('.sidebar .subs').forEach(function(s){s.hidden=s.getAttribute('data-subs')!==slug;});
  if(slug){
    renderLessonQuiz(slug);
    watchSections(slug);
    var d=loadDone();d._last={slug:slug,at:now()};saveDone(d);   // 首頁「繼續上次」用
  }
  if(nav==='wrong')renderWrongList();
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
