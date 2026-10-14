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
