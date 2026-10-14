/* 選字問 AI（規格 docs/superpowers/specs/2026-10-14-ask-ai-design.md）。
   上半是純函式（node 測試用得到）；下半是瀏覽器部分，只有 build 放了 ASKAI_CONFIG 才跑。 */
var NotesAsk = {
  /* 選取範圍複製出來的 HTML → 純文字。日文的讀音（rt）與括號（rp）整個拿掉，
     不然「私」會變成「私わたし」送出去。選取切在讀音中間時只剩半個標籤，一樣拿掉。 */
  stripReadings: function (html) {
    var s = String(html || '')
      .replace(/<(rt|rp)\b[^>]*>[\s\S]*?<\/\1>/gi, '')
      .replace(/^[\s\S]*?<\/rt>/i, function (m) { return /<rt\b/i.test(m) ? m : ''; })   // 開頭半截：…</rt>
      .replace(/<rt\b[^>]*>[\s\S]*$/i, '')                                               // 結尾半截：<rt>…
      .replace(/<br\s*\/?>/gi, '\n')
      .replace(/<[^>]*>/g, '');
    s = s.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'")
      .replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&');
    return s.split('\n').map(function (l) { return l.replace(/[ \t　]+/g, ' ').trim(); })
      .join('\n').replace(/\n{3,}/g, '\n\n').trim();
  },
  clip: function (s, n) {
    s = String(s || '');
    return s.length > n ? { text: s.slice(0, n) + '…', cut: true } : { text: s, cut: false };
  },
  systemText: function (lang) {
    var lines = [
      '你是幫台灣學生解釋文法的老師，用繁體中文、台灣用語回答。',
      '先一句話講結論，再條列說明；不寫長段落。',
      '日文漢字後面用全形括號附讀音，例：私（わたし）。不用羅馬拼音。',
      '有不確定的地方直接說不確定，不要編。'
    ];
    if (lang === 'ja') lines.push('讀者程度：剛學完日檢 N5 文法。');
    else if (lang === 'en') lines.push('讀者在準備多益。');
    return lines.join('\n');
  },
  buildPrompt: function (c) {
    var out = [];
    if (c.module) out.push('模組：' + c.module);
    if (c.lesson) out.push('課：' + c.lesson);
    if (c.section) out.push('小節：' + c.section);
    if (c.context) out.push('前後文：' + c.context);
    out.push('我選的字：「' + (c.selected || '') + '」');
    out.push('問題：' + (c.question || ''));
    return out.join('\n');
  },
  /* AI 回的 Markdown → HTML。先把整段跳脫，AI 回什麼都不會變成標籤；只轉粗體、條列、行內程式碼、換行。 */
  renderAnswer: function (md) {
    function esc(s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
    function inline(s) {
      s = esc(s)
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        .replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>');
      /* 日文包 lang="ja"：連續假名，或後面帶（讀音）的漢字 */
      return s.replace(/(?:[一-鿿々]+（[぀-ヿー]+）|[぀-ヿー])+/g, '<span lang="ja">$&</span>');
    }
    var html = [], list = null, para = [];
    function flushPara() { if (para.length) { html.push('<p>' + para.join('<br>') + '</p>'); para = []; } }
    function flushList() { if (list) { html.push('<' + list.tag + '>' + list.items.join('') + '</' + list.tag + '>'); list = null; } }
    String(md || '').split('\n').forEach(function (line) {
      var m = line.match(/^\s*(?:([-*])|(\d+)\.)\s+(.*)$/);
      if (m) {
        flushPara();
        var tag = m[1] ? 'ul' : 'ol';
        if (!list || list.tag !== tag) { flushList(); list = { tag: tag, items: [] }; }
        list.items.push('<li>' + inline(m[3]) + '</li>');
      } else if (!line.trim()) {
        flushPara(); flushList();
      } else {
        flushList(); para.push(inline(line.trim()));
      }
    });
    flushPara(); flushList();
    return html.join('');
  },
  classifyError: function (err) {
    if (!err) return 'other';
    var d = err.customErrorData || {};
    var status = d.status || 0;
    var text = (err.message || '') + ' ' + JSON.stringify(d.errorDetails || '');
    if (err.code === 'response-error') return 'blocked';
    if (status === 429) return /PerDay|per day/i.test(text) ? 'quota-day' : 'quota-minute';
    if (status === 401 || status === 403 || /app ?check/i.test(text)) return 'appcheck';
    if (err.name === 'TypeError' || err.name === 'AbortError' || (err.code === 'error' && !status) ||
        (err.code === 'fetch-error' && !status)) return 'network';
    return 'other';
  },
  /* 一段對話的狀態。getModel() 回傳 Promise<模型>；ask 回傳 Promise：'done'、'stale'（中途 reset 了），失敗就 reject。
     - 第一題還沒成功前，每次都送完整問題（含選的字、前後文）；SDK 只在成功時把這輪記進對話紀錄，
       所以失敗後要丟掉 chat 重開，不然下一題只剩「問題」那一句、沒有前後文。
     - reset（關對話框、換題）之後立刻不算忙碌，晚到的回答片段也不再交給 onChunk。 */
  session: function (getModel) {
    var chat = null, turns = 0, gen = 0, busy = false;
    return {
      busy: function () { return busy; },
      reset: function () { gen++; chat = null; turns = 0; busy = false; },
      ask: function (q, ctx, onChunk) {
        var my = gen;
        busy = true;
        var text = turns ? q : NotesAsk.buildPrompt({ module: ctx.module, lesson: ctx.lesson, section: ctx.section,
          context: ctx.context, selected: ctx.selected, question: q });
        return Promise.resolve(getModel()).then(function (model) {
          if (my !== gen) return 'stale';
          if (!chat) chat = model.startChat();
          return chat.sendMessageStream(text).then(async function (res) {
            var acc = '';
            for await (var c of res.stream) {
              if (my !== gen) return 'stale';
              acc += c.text();
              onChunk(acc);
            }
            if (my !== gen) return 'stale';
            if (!acc) throw { code: 'response-error' };
            turns++;
            return 'done';
          });
        }).then(function (r) {
          if (my === gen) busy = false;
          return r;
        }, function (err) {
          if (my !== gen) return 'stale';
          busy = false;
          if (!turns) chat = null;
          throw err;
        });
      }
    };
  },
  MESSAGES: {
    'quota-day': '今天的免費額度用完了，明天再試。',
    'quota-minute': '問太快了，等一分鐘再問。',
    'appcheck': '驗證沒通過，重新整理頁面再試。',
    'network': '連不上 AI，檢查網路後按「再試一次」。',
    'blocked': 'AI 沒有回答這題，換個問法試試。',
    'other': 'AI 暫時沒有回應，按「再試一次」。'
  }
};
if (typeof module !== 'undefined' && module.exports) { module.exports = NotesAsk; }

/* 瀏覽器部分：build 只在「有登入、有 askai.json、模組開了 ask_ai」時放 ASKAI_CONFIG */
if (typeof document !== 'undefined' && typeof ASKAI_CONFIG !== 'undefined') (function () {
  var CFG = ASKAI_CONFIG;
  var local = /^(localhost|127\.0\.0\.1)$/.test(location.hostname);
  var mockMode = local ? ((location.search.match(/[?&]askai=(mock[\w-]*)/) || [])[1] || '') : '';
  var DEFAULT_Q = '這段的文法是什麼意思？';
  var NOTE = '免費版：問題與回答會被 Google 用來改進產品，不要貼個人資料。';
  var main = document.getElementById('main');
  var btn = null, panel = null, lastRange = null, ctx = null, modelP = null;
  var sess = NotesAsk.session(function () { return loadModel(); });

  function allowed() { return mockMode || document.documentElement.getAttribute('data-sync') === 'ok'; }
  function icon(n) { return '<svg class="ic" aria-hidden="true"><use href="#ic-' + n + '"/></svg>'; }
  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  /* ---- 載入 Gemini：第一次問才載，平常不多載任何東西 ---- */
  function loadModel() {
    if (mockMode) return Promise.resolve(mockModel());
    if (modelP) return modelP;
    modelP = Promise.all(['app', 'app-check', 'ai'].map(function (n) { return import(CFG.sdk + 'firebase-' + n + '.js'); }))
      .then(function (m) {
        var app = m[0].initializeApp(Object.assign({}, FIREBASE_CONFIG, { appId: CFG.app_id }), 'askai');
        if (local) self.FIREBASE_APPCHECK_DEBUG_TOKEN = true;   // 本機用除錯碼，步驟在 docs/ask-ai-setup.md
        m[1].initializeAppCheck(app, { provider: new m[1].ReCaptchaEnterpriseProvider(CFG.recaptcha_site_key), isTokenAutoRefreshEnabled: true });
        var ai = m[2].getAI(app, { backend: new m[2].GoogleAIBackend(), useLimitedUseAppCheckTokens: true });
        return m[2].getGenerativeModel(ai, { model: CFG.model, systemInstruction: NotesAsk.systemText(CFG.lang) });
      });
    modelP['catch'](function () { modelP = null; });   // 載入失敗下次重載
    return modelP;
  }
  /* 本機測畫面用：不連 Firebase，回答一段一段吐出來；mock-xxx 模擬錯誤 */
  function mockModel() {
    var errs = {
      'mock-quota-day': { code: 'fetch-error', customErrorData: { status: 429, errorDetails: [{ violations: [{ quotaId: 'GenerateRequestsPerDayPerProjectPerModel-FreeTier' }] }] } },
      'mock-quota-minute': { code: 'fetch-error', customErrorData: { status: 429, errorDetails: [] } },
      'mock-appcheck': { code: 'fetch-error', customErrorData: { status: 403, errorDetails: [] }, message: 'App Check' },
      'mock-network': { name: 'TypeError', message: 'Failed to fetch' },
      'mock-blocked': { code: 'response-error' }
    };
    var answer = '**が表示主語**，強調「是誰」。\n- 私（わたし）が行きます：去的是我\n- 用は的話是在講話題\n\n<img src=x onerror=alert(1)> 這行要顯示成純文字';
    return { startChat: function () { return { sendMessageStream: function () {
      if (errs[mockMode]) return Promise.reject(errs[mockMode]);
      var parts = answer.match(/[\s\S]{1,6}/g);
      return Promise.resolve({ stream: (async function* () {
        for (var i = 0; i < parts.length; i++) { await new Promise(function (r) { setTimeout(r, 60); }); yield { text: function () { return parts[i]; } }; }
      })() });
    } }; } };
  }

  /* ---- 選字按鈕 ---- */
  function inMain(node) {
    var e = node && (node.nodeType === 1 ? node : node.parentElement);
    return !!(e && main && main.contains(e) && !(panel && panel.contains(e)));
  }
  function selectedText(range) {
    /* 整段選取都在讀音裡（例如只選到「わたし」）：複製出來只剩文字、沒有 rt 標籤可濾，直接當沒選 */
    var c = range.commonAncestorContainer, ce = c.nodeType === 1 ? c : c.parentElement;
    if (ce && ce.closest('rt,rp')) return '';
    var box = document.createElement('div');
    box.appendChild(range.cloneContents());
    return NotesAsk.stripReadings(box.innerHTML);
  }
  function hideBtn() { if (btn) btn.hidden = true; }
  function onSelection() {
    var sel = window.getSelection();
    if (!allowed() || !sel || sel.isCollapsed || !sel.rangeCount) { return; }   // 選取消失時不馬上藏：手機點按鈕的瞬間選取會先被清掉
    var r = sel.getRangeAt(0);
    if (!inMain(r.commonAncestorContainer) || !selectedText(r)) { hideBtn(); return; }
    lastRange = r.cloneRange();
    if (!btn) {
      btn = el('button', 'askbtn', icon('ask') + '問 AI'); btn.type = 'button'; btn.hidden = true;
      btn.addEventListener('pointerdown', function (e) { e.preventDefault(); });   // 電腦上按下時保留選取
      btn.addEventListener('click', function () { if (lastRange) openPanel(lastRange); });
      document.body.appendChild(btn);
    }
    var rect = r.getBoundingClientRect();
    btn.hidden = false;
    var w = btn.offsetWidth || 90;
    /* 放在選取範圍下方：手機的系統選單（拷貝／查詢）在上方 */
    btn.style.top = (rect.bottom + window.scrollY + 10) + 'px';
    btn.style.left = Math.max(8, Math.min(rect.left + window.scrollX, window.scrollX + document.documentElement.clientWidth - w - 8)) + 'px';
  }
  var selTimer = null;
  document.addEventListener('selectionchange', function () { clearTimeout(selTimer); selTimer = setTimeout(onSelection, 250); });
  document.addEventListener('pointerdown', function (e) { if (btn && !btn.contains(e.target)) { hideBtn(); } });
  window.addEventListener('hashchange', function () { hideBtn(); closePanel(); });

  /* ---- 位置與前後文 ---- */
  function contextOf(range) {
    var node = range.commonAncestorContainer;
    var e = node.nodeType === 1 ? node : node.parentElement;
    var art = e.closest('article');
    var slug = art && art.id ? art.id.replace(/^pg-/, '') : '';
    var lesson = slug === 'ov' ? '總覽' : slug === 'wrong' ? '錯題區' : ((typeof TITLES !== 'undefined' && TITLES[slug]) || '');
    var section = '';
    if (art) art.querySelectorAll('h3.head').forEach(function (h) {
      if (h.compareDocumentPosition(e) & Node.DOCUMENT_POSITION_FOLLOWING || h.contains(e)) section = NotesAsk.stripReadings(h.innerHTML);
    });
    var block = e.closest('.qq') || e.closest('.drill') || e.closest('p,li,td,th,h3');
    var context = block ? NotesAsk.clip(NotesAsk.stripReadings(block.innerHTML), 800).text : '';
    var sel = NotesAsk.clip(selectedText(range), 500);
    return { module: document.title, lesson: lesson, section: section, context: context, selected: sel.text, cut: sel.cut };
  }

  /* ---- 對話框 ---- */
  function build() {
    panel = el('aside', 'askai'); panel.setAttribute('role', 'dialog'); panel.setAttribute('aria-label', '問 AI'); panel.hidden = true;
    panel.innerHTML = '<div class="aa-head"><span>問 AI</span><button class="aa-x" type="button" aria-label="關閉">' + icon('close') + '</button></div>'
      + '<div class="aa-sel"></div><p class="aa-cut" hidden>選的字超過 500 字，只送出前 500 字。</p>'
      + '<div class="aa-log" aria-live="polite"></div>'
      + '<form class="aa-form"><textarea rows="2" aria-label="你的問題"></textarea><button class="aa-send" type="submit">送出</button></form>'
      + '<p class="aa-note">' + NOTE + '</p>';
    document.body.appendChild(panel);
    panel.querySelector('.aa-x').addEventListener('click', closePanel);
    panel.querySelector('.aa-form').addEventListener('submit', function (e) { e.preventDefault(); send(); });
    panel.querySelector('textarea').addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) { e.preventDefault(); send(); }   // 輸入法選字中的 Enter 不送出
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !panel.hidden) closePanel(); });
  }
  function openPanel(range) {
    if (!panel) build();
    ctx = contextOf(range);
    sess.reset();
    panel.querySelector('.aa-send').disabled = false;   // 上一題還在回答時就換題，送出鈕要恢復
    var selBox = panel.querySelector('.aa-sel');
    selBox.textContent = ctx.selected;
    if (CFG.lang === 'ja') selBox.setAttribute('lang', 'ja'); else selBox.removeAttribute('lang');
    panel.querySelector('.aa-cut').hidden = !ctx.cut;
    panel.querySelector('.aa-log').innerHTML = '';
    var ta = panel.querySelector('textarea'); ta.value = DEFAULT_Q;
    panel.hidden = false; hideBtn();
    ta.focus(); ta.select();
  }
  function closePanel() { if (!panel) return; panel.hidden = true; sess.reset(); ctx = null; }

  function send(retryText) {
    var ta = panel.querySelector('textarea'), log = panel.querySelector('.aa-log'), sendBtn = panel.querySelector('.aa-send');
    var q = retryText || ta.value.trim();
    if (!q || !ctx) return;
    if (!retryText) { log.appendChild(el('div', 'aa-q', esc(q))); ta.value = ''; }
    var ans = el('div', 'aa-a', '<p>…</p>'); log.appendChild(ans); log.scrollTop = log.scrollHeight;
    sendBtn.disabled = true;
    sess.ask(q, ctx, function (acc) {
      ans.innerHTML = NotesAsk.renderAnswer(acc);
      log.scrollTop = log.scrollHeight;
    }).then(function (r) {
      if (r !== 'stale') sendBtn.disabled = false;
    }, function (err) {
      var k = NotesAsk.classifyError(err);
      ans.className = 'aa-err';
      ans.innerHTML = esc(NotesAsk.MESSAGES[k]) + ((k === 'network' || k === 'other') ? '<button type="button">再試一次</button>' : '');
      var rb = ans.querySelector('button');
      if (rb) rb.addEventListener('click', function () { ans.remove(); send(q); });   // 失敗的那輪沒進對話紀錄，直接重送同一題
      sendBtn.disabled = false;
      if (window.console) console.warn('askai', err);
    });
  }
})();
