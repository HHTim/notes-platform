# 網站改版與錯題區 實作計畫

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 內容檔一個字不改，把網站換成「白底配色塊」新外觀，測驗回饋改成圈叉加成績卡，每個模組加一個錯題區，首頁加「繼續上次」。

**Architecture:** 網站是 `builder/build.py` 用 `builder/templates/` 的樣板組出來的靜態站。改版全部落在樣板（CSS、JS、兩個 HTML、新的圖示檔）和建置工具（產小節目錄、內嵌圖示、錯題區頁殼）。錯題與「最後看的課」存在既有的進度物件裡，用底線開頭的保留鍵，跟著現有的本機儲存與 Firestore 同步一起走。

**Tech Stack:** Python 3（無第三方套件）、原生 JavaScript（無框架）、Firebase compat SDK（已在用）、`python3 -m unittest` 與 node 腳本測試、gstack `browse`（無頭瀏覽器）做截圖驗收。

**Spec:** `docs/superpowers/specs/2026-10-13-redesign-and-wrong-bank-design.md`

## Global Constraints

- 不改 `content/<模組>/` 底下任何檔案；`content/modules.json` 只改 `icon` 欄位的值。
- 不改 `firebase/firestore.rules`、`.github/workflows/`。
- 色號照規格第 2.1 節：白 #FFFFFF、墨 #233831、次要文字 #5A6B65、底塊 #DEE5DD、薄荷 #C5E0D7／#A9D9C7、桃 #F2CEAE／#F29F80、標記 #FBC580、綠圈 #1F8A5B、紅叉 #D9603A。舊色號 #F7F0E3、#B5730F、#5E7A9B 不得殘留在樣板。
- 字體只用 Noto Sans TC 與 JetBrains Mono；拿掉 Chivo。
- 樣板、建置工具與產出的首頁不得含任何 emoji 或 ✓ ✗ ☰ 這類符號字元；全部用 `icons.svg` 的 SVG 圖示。
- 手機斷點維持 960px。
- 進度物件的保留鍵只有 `_last` 與 `_wrong`；課的 slug 只含小寫英數與連字號，永遠不會以底線開頭。
- 給 Tim 看的文字（程式註解、網站文案、commit 訊息）照 `~/.claude/tim-style/RULES.md`：不發明編號代號、台灣用語、不造字。
- commit 訊息結尾加 `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`。

## Review Focus

1. **舊格式進度**（只有 `{best,total,done}`，沒有 `_last`／`_wrong`）打開新版：側欄、首頁、錯題區都要正常，且不丟任何一課的成績。→ Task 1 的合併測試「沒有錯題就不出現 `_wrong` 鍵」、Task 2 的 `active` 對空物件測試。
2. **題目文字被改過**：舊的錯題紀錄指紋對不上，清單不列、題數不算，不能讓頁面壞掉。→ Task 2 的 `active` 測試含對不上的鍵。
3. **兩台裝置一邊手動移除、一邊還留著舊紀錄**：合併後必須是「已移除」，不能復活。→ Task 1 的合併測試。
4. **沒有課中練習的課**：目錄不列「課中練習」，不能出現對不到的連結。→ Task 4 的 `toc_entries` 測試。
5. **`modules.json` 的圖示名稱打錯**：建置要停下來講是哪個模組、哪個名稱，不能靜靜產出空圖示。→ Task 3 的建置中止測試。

---

## 檔案總表

| 檔案 | 動作 | 負責 |
|---|---|---|
| `builder/templates/sync.js` | 修改 | 合併規則加 `_last`、`_wrong` |
| `builder/tests/test_merge.js` | 修改 | 合併規則新案例 |
| `builder/templates/course.js` | 重寫 | 頂部純邏輯 `NotesQuiz`（node 可載入）＋頁面行為 |
| `builder/tests/test_quiz.js` | 新增 | `NotesQuiz` 測試 |
| `builder/tests/test_sync.py` | 修改 | 跑 `test_quiz.js` |
| `builder/templates/icons.svg` | 新增 | 全部圖示 |
| `builder/build.py` | 修改 | 圖示檢查與內嵌、小節目錄、側欄小節、錯題區頁殼、首頁卡片 |
| `content/modules.json` | 修改 | `icon` 改成名稱 |
| `builder/tests/test_checks.py` | 修改 | 小節目錄、圖示名稱檢查 |
| `builder/tests/test_build.py` | 修改 | 新版面元素、無 emoji、無舊色 |
| `builder/templates/module.html`、`home.html` | 重寫 | 新骨架 |
| `builder/templates/style.css` | 重寫 | 新色系與元件 |
| `builder/templates/favicon.svg` | 重寫 | 新色 |
| `CLAUDE.md` | 修改 | 色系那行、現況段 |

---

### Task 1: 合併規則加 `_last` 與 `_wrong`

**Files:**
- Modify: `builder/templates/sync.js:1-23`
- Test: `builder/tests/test_merge.js`

**Interfaces:**
- Consumes: 無
- Produces: `NotesSync.merge(local, cloud)` 回傳的物件可含 `_last: {slug, at}` 與 `_wrong: { key: {streak, removed, at} }`；課的紀錄形狀不變。

- [ ] **Step 1: 在 `builder/tests/test_merge.js` 的 `console.log` 之前加新案例**

```js
// ── 改版規格第 5.5 節：_last 時間新的贏、_wrong 同鍵時間新的整筆贏 ──

// _last：時間新的贏；只有一邊有就用那邊
assert.deepStrictEqual(
  NotesSync.merge({_last:{slug:'a',at:10}}, {_last:{slug:'b',at:20}})._last, {slug:'b',at:20});
assert.deepStrictEqual(NotesSync.merge({_last:{slug:'a',at:30}}, {})._last, {slug:'a',at:30});

// 保留鍵不會被當成課的紀錄
assert.deepStrictEqual(
  Object.keys(NotesSync.merge({_last:{slug:'a',at:1}, a:{best:1,total:5,done:false}}, {})).sort(),
  ['_last', 'a']);

// _wrong：兩邊各有不同的題，取聯集
var m = NotesSync.merge({_wrong:{k1:{streak:0,removed:0,at:5}}}, {_wrong:{k2:{streak:1,removed:0,at:6}}});
assert.deepStrictEqual(m._wrong, {k1:{streak:0,removed:0,at:5}, k2:{streak:1,removed:0,at:6}});

// 同一題：時間新的整筆贏（雲端那筆是手動移除、時間較新 → 移除保留）
m = NotesSync.merge({_wrong:{k1:{streak:1,removed:0,at:5}}}, {_wrong:{k1:{streak:0,removed:9,at:9}}});
assert.deepStrictEqual(m._wrong.k1, {streak:0,removed:9,at:9});

// 反向：舊裝置上「還在錯題區」的舊紀錄，不能讓已移除的題復活
m = NotesSync.merge({_wrong:{k1:{streak:0,removed:9,at:9}}}, {_wrong:{k1:{streak:0,removed:0,at:3}}});
assert.deepStrictEqual(m._wrong.k1, {streak:0,removed:9,at:9});

// 缺欄位的錯題紀錄要補成完整形狀
assert.deepStrictEqual(NotesSync.merge({_wrong:{k1:{}}}, {})._wrong.k1, {streak:0,removed:0,at:0});

// 沒有錯題、沒有最後看的課，就不多長保留鍵（舊格式進新版不變形）
assert.deepStrictEqual(NotesSync.merge({a:{best:1,total:5,done:false}}, {}), {a:{best:1,total:5,done:false}});
```

- [ ] **Step 2: 跑測試確認失敗**

Run: `node builder/tests/test_merge.js`
Expected: `AssertionError` 在第一個新案例（`_last` 是 `undefined`）。

- [ ] **Step 3: 把 `builder/templates/sync.js` 第 1〜23 行的 `NotesSync` 換成**

```js
/* 進度跨裝置同步：Google 登入＋Firestore。
   只有 builder 在 content/firebase.json 存在時才把本檔放進頁面；
   頁面會先宣告 FIREBASE_CONFIG，並已載入 firebase compat SDK（app/auth/firestore）。 */
var NotesSync = {
  /* 合併規則（總規格第 7 節＋改版規格第 5.5 節）：
     課的紀錄：勾過就算勾過、成績取較好那次，絕不以單邊蓋掉另一邊。
     _last（最後看的課）：時間新的一邊贏。
     _wrong（錯題）：以鍵取聯集；同一鍵兩邊都有時，時間新的那筆整筆贏。
     保留鍵以底線開頭；課的 slug 只有小寫英數與連字號，不會撞到。 */
  merge: function (local, cloud) {
    var out = {};
    function addLessons(src) {
      if (!src) return;
      Object.keys(src).forEach(function (k) {
        if (k.charAt(0) === '_') return;
        var b = src[k] || {};
        var a = out[k];
        if (!a) { out[k] = { best: b.best || 0, total: b.total || 0, done: !!b.done }; return; }
        a.best = Math.max(a.best || 0, b.best || 0);
        a.total = Math.max(a.total || 0, b.total || 0);
        a.done = !!(a.done || b.done);
      });
    }
    addLessons(local); addLessons(cloud);

    var last = null;
    [local && local._last, cloud && cloud._last].forEach(function (x) {
      if (x && x.slug && (!last || (x.at || 0) > (last.at || 0))) last = x;
    });
    if (last) out._last = { slug: last.slug, at: last.at || 0 };

    var wrong = {};
    [local, cloud].forEach(function (src) {
      var m = src && src._wrong;
      if (!m) return;
      Object.keys(m).forEach(function (k) {
        var r = m[k] || {};
        if (!wrong[k] || (r.at || 0) > (wrong[k].at || 0)) {
          wrong[k] = { streak: r.streak || 0, removed: r.removed || 0, at: r.at || 0 };
        }
      });
    });
    if (Object.keys(wrong).length) out._wrong = wrong;
    return out;
  }
};
if (typeof module !== 'undefined' && module.exports) { module.exports = NotesSync; }
```

（第 24 行起的瀏覽器部分先不動，Task 7 再改。）

- [ ] **Step 4: 跑測試確認通過**

Run: `node builder/tests/test_merge.js && python3 -m unittest builder.tests.test_sync -v`
Expected: `merge 規則測試全部通過`，unittest 三條 OK。

- [ ] **Step 5: Commit**

```bash
git add builder/templates/sync.js builder/tests/test_merge.js
git commit -m "feat(sync): 合併規則加最後看的課與錯題紀錄

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 2: 題目指紋與錯題進出的純邏輯 `NotesQuiz`

**Files:**
- Modify: `builder/templates/course.js`（檔案最前面加一段；原本的 IIFE 先包進 `if (typeof document !== 'undefined')`）
- Create: `builder/tests/test_quiz.js`
- Modify: `builder/tests/test_sync.py`

**Interfaces:**
- Produces（Task 6、7 用）：
  - `NotesQuiz.fingerprint(text) → 6 碼字串`
  - `NotesQuiz.wrongKey(slug, qi, qtext) → "slug|qi|指紋"`
  - `NotesQuiz.afterQuiz(wrong, results, now) → 新的 wrong 物件`（不改原物件）；`results` 是 `[{slug, qi, q, right}]`，`q` 是題目文字，`now` 是秒
  - `NotesQuiz.afterPractice(wrong, results, now) → 新的 wrong 物件`
  - `NotesQuiz.remove(wrong, key, now) → 新的 wrong 物件`
  - `NotesQuiz.active(wrong, quiz, slugs) → [{key, slug, qi, q, streak}]`，依課序再依題序；`quiz` 是 `{slug: [題目物件]}`，題目物件至少有 `q`

- [ ] **Step 1: 建 `builder/tests/test_quiz.js`**

```js
// 錯題區的純邏輯（改版規格第 5 節）：指紋、進出規則、清單順序
var assert = require('assert');
var Q = require('../templates/course.js');

// 指紋：固定 6 碼、同文同碼、改一個字就不同
assert.strictEqual(Q.fingerprint('She spoke ___ about it.').length, 6);
assert.strictEqual(Q.fingerprint('abc'), Q.fingerprint('abc'));
assert.notStrictEqual(Q.fingerprint('abc'), Q.fingerprint('abd'));
assert.strictEqual(Q.wrongKey('l1', 2, 'abc'), 'l1|2|' + Q.fingerprint('abc'));

var k = Q.wrongKey('l1', 0, 'q0');
var bank;

// 隨堂測驗：答錯進去（連對 0）、答對不動
bank = Q.afterQuiz({}, [{slug:'l1',qi:0,q:'q0',right:false}, {slug:'l1',qi:1,q:'q1',right:true}], 100);
assert.deepStrictEqual(Object.keys(bank), [k]);
assert.deepStrictEqual(bank[k], {streak:0,removed:0,at:100});

// 已在裡面、連對 1，再答錯 → 歸零
bank = Q.afterQuiz({[k]:{streak:1,removed:0,at:50}}, [{slug:'l1',qi:0,q:'q0',right:false}], 100);
assert.deepStrictEqual(bank[k], {streak:0,removed:0,at:100});

// 移除過的題再答錯 → 復活
bank = Q.afterQuiz({[k]:{streak:2,removed:80,at:80}}, [{slug:'l1',qi:0,q:'q0',right:false}], 100);
assert.deepStrictEqual(bank[k], {streak:0,removed:0,at:100});

// 隨堂測驗裡答對不算（規格 5.1：只有錯題區練習才算連對）
bank = Q.afterQuiz({[k]:{streak:0,removed:0,at:50}}, [{slug:'l1',qi:0,q:'q0',right:true}], 100);
assert.deepStrictEqual(bank[k], {streak:0,removed:0,at:50});

// 練習：對一次連對 1；再對一次 → 連對 2 並記移除時間；錯一次歸零
bank = Q.afterPractice({[k]:{streak:0,removed:0,at:50}}, [{slug:'l1',qi:0,q:'q0',right:true}], 101);
assert.deepStrictEqual(bank[k], {streak:1,removed:0,at:101});
bank = Q.afterPractice(bank, [{slug:'l1',qi:0,q:'q0',right:true}], 102);
assert.deepStrictEqual(bank[k], {streak:2,removed:102,at:102});
bank = Q.afterPractice({[k]:{streak:1,removed:0,at:50}}, [{slug:'l1',qi:0,q:'q0',right:false}], 103);
assert.deepStrictEqual(bank[k], {streak:0,removed:0,at:103});

// 手動移除：保留連對數，記移除時間
bank = Q.remove({[k]:{streak:1,removed:0,at:50}}, k, 104);
assert.deepStrictEqual(bank[k], {streak:1,removed:104,at:104});

// 原物件不被改動
var orig = {}; orig[k] = {streak:0,removed:0,at:1};
Q.remove(orig, k, 9);
Q.afterPractice(orig, [{slug:'l1',qi:0,q:'q0',right:true}], 9);
assert.deepStrictEqual(orig[k], {streak:0,removed:0,at:1});

// active：依課序再依題序；已移除、連對兩次、指紋對不上（題目改過）的都不列；空物件也能用
var quiz = {l1:[{q:'q0'},{q:'q1'}], l2:[{q:'q2'}]};
var k1 = Q.wrongKey('l1', 1, 'q1'), k2 = Q.wrongKey('l2', 0, 'q2');
bank = {};
bank[k2] = {streak:0,removed:0,at:1};
bank[k1] = {streak:1,removed:0,at:1};
bank[k] = {streak:2,removed:5,at:5};
bank['l1|0|zzzzzz'] = {streak:0,removed:0,at:1};
var act = Q.active(bank, quiz, ['l1', 'l2']);
assert.deepStrictEqual(act.map(function (x) { return x.key; }), [k1, k2]);
assert.deepStrictEqual(act[0], {key:k1, slug:'l1', qi:1, q:quiz.l1[1], streak:1});
assert.deepStrictEqual(Q.active({}, quiz, ['l1', 'l2']), []);
assert.deepStrictEqual(Q.active(undefined, quiz, ['l1']), []);

console.log('錯題區純邏輯測試全部通過');
```

- [ ] **Step 2: 跑測試確認失敗**

Run: `node builder/tests/test_quiz.js`
Expected: `TypeError: Q.fingerprint is not a function`（目前 `course.js` 沒有匯出任何東西）。

- [ ] **Step 3: 在 `builder/templates/course.js` 最前面加純邏輯，並把原本整個 `(function(){ … })();` 包進 `if (typeof document !== 'undefined')`**

檔案開頭變成：

```js
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
```

檔案最後一行 `})();` 保持不變（它現在收掉的是 `if (…) (function(){`）。

- [ ] **Step 4: 跑測試確認通過**

Run: `node builder/tests/test_quiz.js && node --check builder/templates/course.js`
Expected: `錯題區純邏輯測試全部通過`，`--check` 無輸出。

- [ ] **Step 5: 在 `builder/tests/test_sync.py` 的 `TestSyncJs` 加一條**

```python
    def test_quiz_rules(self):
        r = subprocess.run(['node', str(ROOT / 'builder' / 'tests' / 'test_quiz.js')],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
```

Run: `python3 -m unittest builder.tests.test_sync -v`
Expected: 四條 OK。

- [ ] **Step 6: Commit**

```bash
git add builder/templates/course.js builder/tests/test_quiz.js builder/tests/test_sync.py
git commit -m "feat(quiz): 題目指紋與錯題進出的純邏輯，附 node 測試

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 3: 圖示檔、圖示名稱檢查、內嵌到每一頁

**Files:**
- Create: `builder/templates/icons.svg`
- Modify: `builder/build.py`（`load_templates`、新函式 `icon_names`／`check_icons`／`icon_html`、`modsel_html`、`build`）
- Modify: `content/modules.json`
- Test: `builder/tests/test_checks.py`、`builder/tests/test_build.py`

**Interfaces:**
- Produces：`build.icon_html(name, cls='ic') → '<svg class="ic" aria-hidden="true"><use href="#ic-名稱"/></svg>'`；樣板裡的 `__ICONS__` 佔位會被整個 `icons.svg` 內容取代（Task 5 的樣板會放這個佔位）；`tpl['icons.svg']` 可用。
- 圖示名稱集合：模組用 `java spring k8s interview algo database cloud english web angular ai-tools`；版面用 `menu home book flag check ok no half empty`。

- [ ] **Step 1: 建 `builder/templates/icons.svg`**

```svg
<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true">
<!-- 全站圖示，畫法「粗線加色」：線寬 2.4、圓端、顏色跟文字一樣（currentColor）；
     每顆挑一塊面填桃 #FBC580 或薄荷 #A9D9C7，填色那段 stroke="none"。
     用法：<svg class="ic"><use href="#ic-名稱"/></svg>。新模組要加圖示就在這裡加一個 <symbol id="ic-名稱">。 -->
<symbol id="ic-java" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path fill="#FBC580" stroke="none" d="M5 10h11v6a4 4 0 0 1-4 4H9a4 4 0 0 1-4-4z"/><path d="M5 10h11v6a4 4 0 0 1-4 4H9a4 4 0 0 1-4-4z"/><path d="M16 12h2a2 2 0 0 1 0 4h-2M8 6c0-1.5 1.5-1.5 1.5-3M12 6c0-1.5 1.5-1.5 1.5-3"/></symbol>
<symbol id="ic-spring" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path fill="#A9D9C7" stroke="none" d="M12 11c0-4 3-7 8-7 0 5-3 7-8 7z"/><path d="M12 21V11"/><path d="M12 11c0-4 3-7 8-7 0 5-3 7-8 7z"/><path d="M12 15c0-3-2-5-6-5 0 4 2 5 6 5z"/></symbol>
<symbol id="ic-k8s" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path fill="#FBC580" stroke="none" d="M12 12l8-4.5v9L12 21z"/><path d="M12 3l8 4.5v9L12 21l-8-4.5v-9z"/><path d="M12 12l8-4.5M12 12v9M12 12L4 7.5"/></symbol>
<symbol id="ic-interview" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><rect fill="#FBC580" stroke="none" x="9" y="3" width="6" height="11" rx="3"/><rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/></symbol>
<symbol id="ic-algo" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><circle fill="#A9D9C7" stroke="none" cx="12" cy="5" r="2.5"/><circle cx="12" cy="5" r="2.5"/><circle cx="6" cy="18" r="2.5"/><circle cx="18" cy="18" r="2.5"/><path d="M12 7.5v4M12 11.5l-5 4M12 11.5l5 4"/></symbol>
<symbol id="ic-database" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><ellipse fill="#FBC580" stroke="none" cx="12" cy="6" rx="7" ry="3"/><ellipse cx="12" cy="6" rx="7" ry="3"/><path d="M5 6v12c0 1.7 3.1 3 7 3s7-1.3 7-3V6M5 12c0 1.7 3.1 3 7 3s7-1.3 7-3"/></symbol>
<symbol id="ic-cloud" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path fill="#A9D9C7" stroke="none" d="M7 18a4 4 0 0 1-.5-8A6 6 0 0 1 18 9.5 3.5 3.5 0 0 1 17.5 18z"/><path d="M7 18a4 4 0 0 1-.5-8A6 6 0 0 1 18 9.5 3.5 3.5 0 0 1 17.5 18z"/></symbol>
<symbol id="ic-english" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path fill="#FBC580" stroke="none" d="M14 19l3-8 3 8z"/><path d="M4 5h9M8.5 5v14M4 19h9"/><path d="M14 19l3-8 3 8M15 16h4"/></symbol>
<symbol id="ic-web" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><circle fill="#A9D9C7" stroke="none" cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/></symbol>
<symbol id="ic-angular" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path fill="#FBC580" stroke="none" d="M12 3l8 3-1.5 12L12 21z"/><path d="M12 3l8 3-1.5 12L12 21l-6.5-3L4 6z"/><path d="M12 7l-3.5 9M12 7l3.5 9M9.8 13h4.4"/></symbol>
<symbol id="ic-ai-tools" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><rect fill="#A9D9C7" stroke="none" x="5" y="8" width="14" height="11" rx="3"/><rect x="5" y="8" width="14" height="11" rx="3"/><path d="M12 8V4M9 13h.01M15 13h.01M9 16h6"/></symbol>
<!-- 版面用 -->
<symbol id="ic-menu" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M4 6h16M4 12h16M4 18h16"/></symbol>
<symbol id="ic-home" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path fill="#FBC580" stroke="none" d="M5 11l7-6 7 6v9H5z"/><path d="M5 11l7-6 7 6v9H5z"/><path d="M10 20v-6h4v6"/></symbol>
<symbol id="ic-book" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path fill="#A9D9C7" stroke="none" d="M12 6c-2-1.5-5-1.5-8-1v13c3-.5 6-.5 8 1z"/><path d="M12 6c-2-1.5-5-1.5-8-1v13c3-.5 6-.5 8 1zM12 6c2-1.5 5-1.5 8-1v13c-3-.5-6-.5-8 1z"/></symbol>
<symbol id="ic-flag" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path fill="#F29F80" stroke="none" d="M5 4h12l-3 4 3 4H5z"/><path d="M5 4h12l-3 4 3 4H5M5 4v17"/></symbol>
<symbol id="ic-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></symbol>
<symbol id="ic-ok" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6"><circle cx="12" cy="12" r="8"/></symbol>
<symbol id="ic-no" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></symbol>
<symbol id="ic-empty" viewBox="0 0 24 24" fill="none" stroke="#A9D9C7" stroke-width="2.4"><circle cx="12" cy="12" r="8"/></symbol>
<symbol id="ic-half" viewBox="0 0 24 24" fill="none" stroke="#A9D9C7" stroke-width="2.4"><circle cx="12" cy="12" r="8"/><path fill="#A9D9C7" stroke="none" d="M12 4a8 8 0 0 1 0 16z"/></symbol>
</svg>
```

- [ ] **Step 2: 在 `builder/tests/test_checks.py` 加測試（放在 `TestDrills` 之後）**

```python
class TestIcons(unittest.TestCase):
    """圖示名稱要對得到 icons.svg 的 <symbol id="ic-名稱">；對不到建置要停，並講是哪個模組"""

    def test_icon_names_from_svg(self):
        names = builder.icon_names('<svg><symbol id="ic-java"></symbol><symbol id="ic-ai-tools"></symbol></svg>')
        self.assertEqual(names, {'java', 'ai-tools'})

    def test_icon_html(self):
        self.assertEqual(builder.icon_html('java'),
                         '<svg class="ic" aria-hidden="true"><use href="#ic-java"/></svg>')
        self.assertIn('class="ic big"', builder.icon_html('java', 'ic big'))

    def test_unknown_icon_stops_build(self):
        content, out = fake_site([('01-one', 'one', LESSON_OK)])
        mj = content / 'modules.json'
        mj.write_text(mj.read_text(encoding='utf-8').replace('"icon": "java"', '"icon": "javaa"'), encoding='utf-8')
        with self.assertRaises(SystemExit) as cm:
            builder.build(content_dir=content, out_dir=out)
        msg = str(cm.exception)
        self.assertIn('demo', msg)
        self.assertIn('javaa', msg)

    def test_icons_inlined_once_per_page(self):
        content, out = fake_site([('01-one', 'one', LESSON_OK)])
        builder.build(content_dir=content, out_dir=out)
        for page in ('index.html', 'demo/index.html'):
            html = (out / page).read_text(encoding='utf-8')
            self.assertEqual(html.count('<symbol id="ic-java"'), 1, page)
            self.assertNotIn('__ICONS__', html, page)
```

並把 `fake_site` 裡的 `'modules': [{'id': 'demo', 'icon': '🧪'}]` 改成 `'modules': [{'id': 'demo', 'icon': 'java'}]`。

- [ ] **Step 3: 跑測試確認失敗**

Run: `python3 -m unittest builder.tests.test_checks.TestIcons -v`
Expected: 四條都 FAIL／ERROR（`AttributeError: module 'build' has no attribute 'icon_names'`）。

- [ ] **Step 4: 改 `builder/build.py`**

`load_templates` 的名單加 `'icons.svg'`：

```python
def load_templates(tpl_dir):
    names = ('style.css', 'course.js', 'sync.js', 'module.html', 'home.html', 'favicon.svg', 'icons.svg')
    return {n: (tpl_dir / n).read_text(encoding='utf-8') for n in names if (tpl_dir / n).exists()}
```

在 `SLUG_RE` 那行後面加：

```python
ICON_ID_RE = re.compile(r'<symbol id="ic-([a-z0-9-]+)"')


def icon_names(icons_svg):
    """icons.svg 裡所有 <symbol id="ic-名稱"> 的名稱集合"""
    return set(ICON_ID_RE.findall(icons_svg))


def check_icons(mods, names):
    """modules.json 的 icon 要是 icons.svg 裡有的名稱；對不到就中止建置並說是哪個模組"""
    bad = ['%s 的 icon「%s」' % (m['id'], m['icon']) for m in mods if m['icon'] not in names]
    if bad:
        raise SystemExit('建置中止：modules.json 的圖示名稱對不到 builder/templates/icons.svg\n  ' + '\n  '.join(bad))


def icon_html(name, cls='ic'):
    return '<svg class="%s" aria-hidden="true"><use href="#ic-%s"/></svg>' % (cls, name)
```

`modsel_html` 拿掉 emoji：

```python
def modsel_html(mods, current_id):
    return ''.join('<option value="%s"%s>%s</option>'
                   % (m['id'], ' selected' if m['id'] == current_id else '', m['title'])
                   for m in mods)
```

`render_module_page` 與 `render_home_page` 的取代清單各加一組 `('__ICONS__', tpl['icons.svg'])`：

```python
    for key, val in (('__TITLE__', mod['title']), ('__MODSEL__', modsel_html(mods, mod['id'])),
                     ('__SIDEBAR__', sidebar_html(mod)), ('__ARTICLES__', ''.join(arts)),
                     ('__DATA__', data), ('__SYNC__', sync), ('__ICONS__', tpl['icons.svg'])):
```

```python
    for key, val in (('__SITE_TITLE__', site['site_title']), ('__SITE_INTRO__', site['site_intro']),
                     ('__SIDEBAR__', side), ('__CARDS__', cards), ('__MODS__', mods_js),
                     ('__SYNC__', sync_html(firebase, '')), ('__ICONS__', tpl['icons.svg'])):
```

`build()` 在 `tpl = load_templates(tpl_dir)` 後面加一行：

```python
    check_icons(mods, icon_names(tpl['icons.svg']))
```

- [ ] **Step 5: 改 `content/modules.json` 的 icon 欄位**

| id | icon |
|---|---|
| java | `"java"` |
| spring | `"spring"` |
| k8s | `"k8s"` |
| interview | `"interview"` |
| algo | `"algo"` |
| database | `"database"` |
| cloud | `"cloud"` |
| english | `"english"` |
| web | `"web"` |
| angular | `"angular"` |
| ai-tools | `"ai-tools"` |

只改值，其餘不動。

- [ ] **Step 6: 先在舊樣板放佔位，讓 `test_icons_inlined_once_per_page` 能過**

`builder/templates/module.html` 與 `home.html` 的 `<body>` 下一行各加一行 `__ICONS__`（Task 5 重寫樣板時會保留）。

- [ ] **Step 7: 跑測試**

Run: `python3 -m unittest builder.tests.test_checks -v`
Expected: 全部 OK。

Run: `python3 -m unittest builder.tests.test_build -v`
Expected: `test_home_page` 會 FAIL（它用 `assertIn(mod['icon'], html)`，現在 icon 是名稱「java」，首頁還沒內嵌 `<use href="#ic-java">`，不一定找得到）。下一步改它。

- [ ] **Step 8: 改 `builder/tests/test_build.py` 的 `test_home_page`**

把 `self.assertIn(mod['icon'], html)` 換成：

```python
            self.assertIn('<use href="#ic-%s"/>' % mod['icon'], html)
```

然後改 `render_home_page`，側欄與卡片用 `icon_html`：

```python
def render_home_page(site, mods, tpl, firebase=None):
    side = ''.join('  <a href="%s/">%s<span>%s</span></a>\n'
                   % (m['id'], icon_html(m['icon']), m['title']) for m in mods)
    cards = ''.join(
        '<a class="mod-card" href="%s/" data-card="%s">%s<b>%s</b>'
        '<span class="bar"><i data-bar="%s"></i></span>'
        '<span class="stats" data-stat="%s">共 %d 課</span></a>\n'
        % (m['id'], m['id'], icon_html(m['icon'], 'ic big'), m['title'], m['id'], m['id'], len(m['lessons']))
        for m in mods)
    mods_js = json.dumps([{'id': m['id'], 'title': m['title'], 'icon': m['icon'], 'count': len(m['lessons']),
                           'lessons': {L['slug']: L['title'] for L in m['lessons']}} for m in mods],
                         ensure_ascii=False).replace('</', '<\\/')
    page = tpl['home.html']
    for key, val in (('__SITE_TITLE__', site['site_title']), ('__SITE_INTRO__', site['site_intro']),
                     ('__SIDEBAR__', side), ('__CARDS__', cards), ('__MODS__', mods_js),
                     ('__SYNC__', sync_html(firebase, '')), ('__ICONS__', tpl['icons.svg'])):
        page = page.replace(key, val)
    return page
```

Run: `python3 -m unittest discover -s builder/tests -v`
Expected: 全部 OK（`test_home_page` 檢查的 `data-stat` 與「共 N 課」仍在）。

- [ ] **Step 9: Commit**

```bash
git add builder/templates/icons.svg builder/build.py content/modules.json builder/templates/module.html builder/templates/home.html builder/tests/test_checks.py builder/tests/test_build.py
git commit -m "feat(icons): 自繪 SVG 圖示檔，建置時檢查名稱並內嵌每一頁；modules.json 改用圖示名稱

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 4: 小節目錄、側欄小節與成績、錯題區頁殼

**Files:**
- Modify: `builder/build.py`（`load_site`、新函式 `section_titles`／`toc_entries`／`toc_html`／`subs_html`／`wrong_html`、`sidebar_html`、`overview_html`、`article_html`、`render_module_page`）
- Test: `builder/tests/test_checks.py`、`builder/tests/test_build.py`

**Interfaces:**
- Produces（Task 6 的 JavaScript 靠這些 id 與屬性）：
  - 每個 `<h3 class="head">` 有 `id="<slug>-sec-N"`（N 從 1 起）
  - 第一個 `<div class="drill">` 有 `id="<slug>-drill"`
  - 測驗容器 `<div class="quiz" id="<slug>-quiz" data-quiz="<slug>">`
  - 課首目錄 `<details class="toc" open><summary>本課小節</summary><ol><li><a href="#" data-goto="<id>">文字</a></li>…</ol></details>`
  - 側欄每課後面 `<div class="subs" data-subs="<slug>" hidden><a href="#" data-goto="<id>">文字</a>…</div>`
  - 側欄每課右邊 `<span class="st" data-st="<slug>"></span>`；側欄第二項 `<a href="#/wrong" data-nav="wrong" class="wrong">…<span class="cnt" data-wrongcnt hidden></span></a>`
  - 錯題區頁殼 `<article id="pg-wrong" hidden>` 內有 `<span class="cnt" id="wrongCount" hidden>` 與 `<div id="wrongBody">`
  - 頁面資料多一個 `var TITLES={slug: 課名}`

- [ ] **Step 1: 在 `builder/tests/test_checks.py` 加測試**

```python
class TestSections(unittest.TestCase):
    """本課小節目錄：從 <h3 class="head"> 自動產生，建置時補 id；有課中練習才列「課中練習」"""

    def test_heads_get_ids_and_titles(self):
        html, titles = builder.section_titles(
            '<h3 class="head">甲 <code>x</code></h3><p>a</p><h3 class="head">乙\n丙</h3>', 'l1')
        self.assertEqual(titles, ['甲 x', '乙 丙'])
        self.assertIn('<h3 class="head" id="l1-sec-1">甲 <code>x</code></h3>', html)
        self.assertIn('<h3 class="head" id="l1-sec-2">', html)

    def test_toc_entries(self):
        L = {'slug': 'l1', 'sections': ['甲', '乙'], 'has_drill': True}
        self.assertEqual(builder.toc_entries(L),
                         [('l1-sec-1', '甲'), ('l1-sec-2', '乙'), ('l1-drill', '課中練習'), ('l1-quiz', '隨堂測驗')])
        L['has_drill'] = False
        self.assertEqual([t for _, t in builder.toc_entries(L)], ['甲', '乙', '隨堂測驗'])

    def test_built_page_has_toc_subs_scores_and_wrong_page(self):
        with_drill = LESSON_OK + DRILL_OK
        content, out = fake_site([('01-one', 'one', with_drill), ('02-two', 'two', LESSON_OK)])
        builder.build(content_dir=content, out_dir=out)
        html = (out / 'demo' / 'index.html').read_text(encoding='utf-8')
        # 課文裡的小節 id、課中練習 id、測驗 id
        self.assertIn('<h3 class="head" id="one-sec-1">標題</h3>', html)
        self.assertIn('<div class="drill" id="one-drill"', html)
        self.assertNotIn('id="two-drill"', html)
        self.assertIn('<div class="quiz" id="one-quiz" data-quiz="one">', html)
        # 課首目錄：第一課有課中練習、第二課沒有
        self.assertIn('<details class="toc" open><summary>本課小節</summary><ol>'
                      '<li><a href="#" data-goto="one-sec-1">標題</a></li>'
                      '<li><a href="#" data-goto="one-drill">課中練習</a></li>'
                      '<li><a href="#" data-goto="one-quiz">隨堂測驗</a></li></ol></details>', html)
        self.assertIn('<li><a href="#" data-goto="two-sec-1">標題</a></li><li><a href="#" data-goto="two-quiz">隨堂測驗</a></li>', html)
        # 側欄：錯題區項目、每課的成績欄、每課的小節
        self.assertIn('href="#/wrong" data-nav="wrong"', html)
        self.assertIn('data-wrongcnt', html)
        self.assertIn('<span class="st" data-st="one"></span>', html)
        self.assertIn('<div class="subs" data-subs="one" hidden><a href="#" data-goto="one-sec-1">標題</a>', html)
        # 錯題區頁殼與課名表
        self.assertIn('<article id="pg-wrong" hidden>', html)
        self.assertIn('id="wrongBody"', html)
        self.assertIn('var TITLES={"one": "第 01-one 課", "two": "第 02-two 課"}', html)
```

（`DRILL_OK` 是 `test_checks.py` 裡既有的常數。）

- [ ] **Step 2: 跑測試確認失敗**

Run: `python3 -m unittest builder.tests.test_checks.TestSections -v`
Expected: 三條 FAIL／ERROR。

- [ ] **Step 3: 改 `builder/build.py`**

在 `icon_html` 後面加：

```python
HEAD_RE = re.compile(r'<h3 class="head">(.*?)</h3>', re.S)
TAG_RE = re.compile(r'<[^>]+>')


def section_titles(html, slug):
    """把每個 <h3 class="head"> 補上 id="<slug>-sec-N"，回傳 (新 html, [標題純文字])。
    所有課的標題都寫成 <h3 class="head">，沒有別的屬性（test_content 守著）。"""
    titles = []

    def rep(m):
        titles.append(re.sub(r'\s+', ' ', TAG_RE.sub('', m.group(1))).strip())
        return '<h3 class="head" id="%s-sec-%d">%s</h3>' % (slug, len(titles), m.group(1))
    return HEAD_RE.sub(rep, html), titles


def toc_entries(L):
    """本課小節：(目標 id, 顯示文字)。小節、課中練習（有才列）、隨堂測驗。"""
    items = [('%s-sec-%d' % (L['slug'], i + 1), t) for i, t in enumerate(L['sections'])]
    if L['has_drill']:
        items.append(('%s-drill' % L['slug'], '課中練習'))
    items.append(('%s-quiz' % L['slug'], '隨堂測驗'))
    return items


def toc_html(L):
    """課首的目錄（手機用；電腦寬度 CSS 會藏起來改看側欄的小節）。
    連結不用 #id（會被路由當成換頁），用 data-goto 交給 course.js 捲動。"""
    lis = ''.join('<li><a href="#" data-goto="%s">%s</a></li>' % (i, t) for i, t in toc_entries(L))
    return '<details class="toc" open><summary>本課小節</summary><ol>%s</ol></details>\n' % lis


def subs_html(L):
    """側欄裡該課底下的小節（電腦用；只有目前這課會被 course.js 打開）"""
    links = ''.join('<a href="#" data-goto="%s">%s</a>' % (i, t) for i, t in toc_entries(L))
    return '  <div class="subs" data-subs="%s" hidden>%s</div>\n' % (L['slug'], links)


def wrong_html():
    """錯題區的頁殼；內容由 course.js 依本機紀錄畫出來"""
    return ('<article id="pg-wrong" hidden>\n'
            '<p class="crumb"><a href="#/">課綱總覽</a> › 錯題區</p>\n'
            '<h1 class="lt">錯題區 <span class="cnt" id="wrongCount" hidden></span></h1>\n'
            '<div id="wrongBody"></div>\n'
            '</article>\n')
```

`load_site` 讀完 `lesson.html` 並檢查後（`L['quiz'] = …` 那行之前）加：

```python
            L['html'], L['sections'] = section_titles(L['html'], L['slug'])
            L['has_drill'] = '<div class="drill"' in L['html']
            if L['has_drill']:
                L['html'] = L['html'].replace('<div class="drill"', '<div class="drill" id="%s-drill"' % L['slug'], 1)
```

`sidebar_html` 整個換成：

```python
def sidebar_html(mod):
    out = ['  <a href="#/" data-nav="ov" class="ov">%s<span>課綱總覽</span></a>\n' % icon_html('book'),
           '  <a href="#/wrong" data-nav="wrong" class="wrong">%s<span>錯題區</span>'
           '<span class="cnt" data-wrongcnt hidden></span></a>\n' % icon_html('flag')]
    group = None
    for i, L in enumerate(mod['lessons']):
        if L.get('group') and L['group'] != group:
            group = L['group']
            out.append('  <div class="group">%s</div>\n' % group)
        out.append('  <a href="#/lesson/%s" data-nav="%s"><span class="n">%d.</span>'
                   '<span>%s</span><span class="st" data-st="%s"></span></a>\n'
                   % (L['slug'], L['slug'], i + 1, L['title'], L['slug']))
        out.append(subs_html(L))
    return ''.join(out)
```

`overview_html` 整個換成（課程列表的打勾改成 SVG 圖示；注意原本是一長串 `%` 格式字串，不要只改一段，`%` 的優先序會把字串切錯）：

```python
def overview_html(mod):
    o = ['<article id="pg-ov">\n<div class="ov-hero">\n<p class="kick">%s</p>\n<h1>%s</h1>\n'
         % (mod['kick'], mod['title'])]
    o.append(intro_html(mod['overview_intro']))
    o.append('<p class="ov-progress" id="ovProgress"></p>\n</div>\n<div class="lesson-list">\n')
    tick = icon_html('check', 'ic ok')
    for i, L in enumerate(mod['lessons']):
        o.append('<a href="#/lesson/%s"><span class="n">%d</span><span class="tt"><b>%s</b>'
                 '<span>%s</span></span><span class="done" data-ovtick="%s" hidden>%s</span>'
                 '<span class="mins">%d 分</span></a>\n'
                 % (L['slug'], i + 1, L['title'], L['desc'], L['slug'], tick, L['mins']))
    o.append('</div>\n<footer class="site">%s</footer>\n</article>\n' % mod['footer_note'])
    return ''.join(o)
```

`article_html`：`p.sub` 那行後面加目錄，測驗容器加 id：

```python
    a.append('<p class="sub">%s</p>\n' % L['desc'])
    a.append(toc_html(L))
    a.append(L['html'] + '\n')   # 「讀完這課你會」框、內文、「重點整理」框都在 lesson.html 裡
    a.append('<div class="quiz" id="%s-quiz" data-quiz="%s"></div>\n' % (L['slug'], L['slug']))
```

`render_module_page`：資料加課名表，文章加錯題區頁殼：

```python
    titles = {L['slug']: L['title'] for L in mod['lessons']}
    data = ('var MODULE=%s;\nvar QUIZ=%s;\nvar SLUGS=%s;\nvar TITLES=%s;'
            % (json.dumps(mod['id']), json.dumps(quiz, ensure_ascii=False),
               json.dumps(slugs, ensure_ascii=False), json.dumps(titles, ensure_ascii=False)))
    data = data.replace('</', '<\\/')
    sync = sync_html(firebase, '../')
    arts = [overview_html(mod), wrong_html()] + [article_html(mod, i, L) for i, L in enumerate(mod['lessons'])]
```

- [ ] **Step 4: 跑測試**

Run: `python3 -m unittest builder.tests.test_checks -v`
Expected: 全部 OK。

Run: `python3 -m unittest builder.tests.test_build -v`
Expected: `test_module_page_k8s` FAIL：`data-nav=` 的數量現在是課數 + 2（總覽、錯題區）。

- [ ] **Step 5: 改 `builder/tests/test_build.py` 的 `test_module_page_k8s`**

```python
        # 側邊欄：總覽 + 錯題區 + 每課
        self.assertEqual(html.count('data-nav='), len(k8s['lessons']) + 2)
```

並在同一個測試最後加：

```python
        # 每課的小節目錄與側欄小節都在；錯題區頁殼在
        for L in k8s['lessons']:
            self.assertIn('data-subs="%s"' % L['slug'], html)
            self.assertIn('data-goto="%s-quiz"' % L['slug'], html)
        self.assertIn('<article id="pg-wrong" hidden>', html)
```

Run: `python3 -m unittest discover -s builder/tests -v`
Expected: 全部 OK。

- [ ] **Step 6: Commit**

```bash
git add builder/build.py builder/tests/test_checks.py builder/tests/test_build.py
git commit -m "feat(build): 自動產生本課小節目錄與側欄小節，側欄加錯題區與每課成績欄

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 5: 新版面骨架、樣式與網站圖示

**Files:**
- Rewrite: `builder/templates/module.html`、`builder/templates/home.html`、`builder/templates/style.css`、`builder/templates/favicon.svg`
- Test: `builder/tests/test_build.py`

**Interfaces:**
- Consumes：Task 3 的 `__ICONS__`、Task 4 的 id 與屬性。
- Produces（Task 6、7 的 JavaScript 靠這些 id）：模組頁 `#burger #scrim #sidebar #main #modsel #sideProg #syncHint`（不變）；首頁 `#burger #scrim #sidebar #syncHint #resume #resumeIcon #resumeMod #resumeLesson`，卡片 `[data-card] [data-bar] [data-stat]`。
- CSS 類別（Task 6 會產生這些元素）：`.quiz .qhead .qtitle .qnote .score .big .t .mono .tr .qact .qact.bottom .qq .qq.ok .qq.ng .qtop .qn .src .mk .qt .opts .opt .opt .l .opt .tx .opt.sel .opt.right .opt.wrongpick .exp .qbtn .qbtn.sec .qmsg .legend .wgroup .witem .wq .wrm .ic .ic.ok .ic.no .ic.big .subs a.on .toc`。

- [ ] **Step 1: 在 `builder/tests/test_build.py` 的 `TestBuild` 加測試**

```python
    EMOJI = re.compile('[\U0001F300-\U0001FAFF☀-➿\U0001F1E6-\U0001F1FF]')

    def test_no_emoji_in_templates_and_chrome(self):
        """樣板、建置工具、首頁、模組頁的外殼（去掉課文）都不能有 emoji 或 ✓ ✗ ☰ 這類符號"""
        for f in (ROOT / 'builder' / 'templates').iterdir():
            self.assertIsNone(self.EMOJI.search(f.read_text(encoding='utf-8')), f.name)
        self.assertIsNone(self.EMOJI.search((ROOT / 'builder' / 'build.py').read_text(encoding='utf-8')))
        self.assertIsNone(self.EMOJI.search((self.out / 'index.html').read_text(encoding='utf-8')))
        shell = re.sub(r'<article id="pg-[a-z0-9-]+".*?</article>', '', (self.out / 'english' / 'index.html').read_text(encoding='utf-8'), flags=re.S)
        self.assertIsNone(self.EMOJI.search(shell))

    def test_new_palette_only(self):
        css = (self.out / 'style.css').read_text(encoding='utf-8')
        for old in ('#F7F0E3', '#B5730F', '#5E7A9B', 'Chivo'):
            self.assertNotIn(old, css, old)
        for new in ('#233831', '#DEE5DD', '#A9D9C7', '#C5E0D7', '#F29F80', '#F2CEAE', '#FBC580'):
            self.assertIn(new, css, new)
        for page in ('index.html', 'english/index.html'):
            self.assertNotIn('Chivo', (self.out / page).read_text(encoding='utf-8'), page)

    def test_home_resume_and_cards(self):
        html = (self.out / 'index.html').read_text(encoding='utf-8')
        for i in ('id="resume"', 'id="resumeIcon"', 'id="resumeMod"', 'id="resumeLesson"'):
            self.assertIn(i, html, i)
        for mod in self.mods:
            self.assertIn('data-card="%s"' % mod['id'], html)
            self.assertIn('data-bar="%s"' % mod['id'], html)
        self.assertNotIn(self.site['site_intro'], html)   # 長介紹不再放首頁
```

- [ ] **Step 2: 跑測試確認失敗**

Run: `python3 -m unittest builder.tests.test_build.TestBuild.test_no_emoji_in_templates_and_chrome builder.tests.test_build.TestBuild.test_new_palette_only builder.tests.test_build.TestBuild.test_home_resume_and_cards -v`
Expected: 三條 FAIL。

- [ ] **Step 3: 重寫 `builder/templates/module.html`**

```html
<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Noto+Sans+TC:wght@400;500;700;900&display=swap">
<link rel="icon" type="image/svg+xml" href="../favicon.svg">
<link rel="apple-touch-icon" href="../favicon.svg">
<link rel="stylesheet" href="../style.css">
</head>
<body>
__ICONS__
<header class="topbar">
  <button class="burger" id="burger" aria-label="開關章節選單"><svg class="ic" aria-hidden="true"><use href="#ic-menu"/></svg></button>
  <a class="home" href="../"><svg class="ic" aria-hidden="true"><use href="#ic-home"/></svg><span>筆記平台</span></a>
  <span class="sep">›</span>
  <select class="modsel" id="modsel" aria-label="切換模組">__MODSEL__</select>
</header>
<div class="scrim" id="scrim"></div>
<nav class="sidebar" id="sidebar" aria-label="章節選單">
__SIDEBAR__
  <div class="sidefoot">
    <p class="sideprog" id="sideProg"></p>
    <p class="synchint" id="syncHint">進度只存在這台裝置</p>
  </div>
</nav>
<main class="main" id="main">
__ARTICLES__
</main>
<script>__DATA__</script>
<script src="../course.js"></script>
__SYNC__
</body>
</html>
```

- [ ] **Step 4: 重寫 `builder/templates/home.html`**

```html
<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__SITE_TITLE__</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Noto+Sans+TC:wght@400;500;700;900&display=swap">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<link rel="apple-touch-icon" href="favicon.svg">
<link rel="stylesheet" href="style.css">
</head>
<body>
__ICONS__
<header class="topbar">
  <button class="burger" id="burger" aria-label="開關模組選單"><svg class="ic" aria-hidden="true"><use href="#ic-menu"/></svg></button>
  <a class="brand" href="./">Tim 的<b>筆記平台</b></a>
  <p class="synchint" id="syncHint"><span class="st">進度只存在這台裝置</span></p>
</header>
<div class="scrim" id="scrim"></div>
<nav class="sidebar" id="sidebar" aria-label="模組選單">
  <div class="group">模組</div>
__SIDEBAR__
</nav>
<main class="main" id="main">
  <div class="ov-hero">
    <h1>__SITE_TITLE__</h1>
    <p>每個模組是一個課程站：側欄選課、課末測驗、全對打勾。</p>
  </div>
  <a class="resume" id="resume" href="./" hidden>
    <svg class="ic big" id="resumeIcon" aria-hidden="true"></svg>
    <span class="rt"><b id="resumeMod"></b><span id="resumeLesson"></span></span>
    <span class="go">接著讀</span>
  </a>
  <div class="mod-cards">
__CARDS__
  </div>
  <footer class="site">內容公開；完成度以這台裝置的紀錄為準，右上角登入後會跟雲端同步。</footer>
</main>
<script>
(function(){
var MODS=__MODS__;
var sidebar=document.getElementById('sidebar'),scrim=document.getElementById('scrim');
document.getElementById('burger').addEventListener('click',function(){
  sidebar.classList.toggle('open');scrim.classList.toggle('show');
});
scrim.addEventListener('click',function(){sidebar.classList.remove('open');scrim.classList.remove('show');});
function load(mid){try{return JSON.parse(localStorage.getItem('notes-progress:'+mid))||{};}catch(e){return {};}}
function refresh(){
  var latest=null;
  MODS.forEach(function(m){
    var d=load(m.id),done=0;
    Object.keys(d).forEach(function(k){if(k.charAt(0)!=='_'&&d[k]&&d[k].done)done++;});
    var st=document.querySelector('[data-stat="'+m.id+'"]');
    if(st)st.textContent='完成 '+done+' / '+m.count+' 課';
    var bar=document.querySelector('[data-bar="'+m.id+'"]');
    if(bar)bar.style.width=Math.round(done*100/m.count)+'%';
    var card=document.querySelector('[data-card="'+m.id+'"]');
    if(card)card.classList.toggle('done',done===m.count);
    var l=d._last;
    if(l&&l.slug&&m.lessons[l.slug]&&(!latest||(l.at||0)>latest.at))latest={at:l.at||0,mod:m,slug:l.slug};
  });
  /* 繼續上次：各模組「最後看的課」裡時間最新的一筆；一筆都沒有就不顯示這張卡 */
  var r=document.getElementById('resume');
  r.hidden=!latest;
  if(latest){
    r.href=latest.mod.id+'/#/lesson/'+latest.slug;
    document.getElementById('resumeMod').textContent='繼續上次：'+latest.mod.title;
    document.getElementById('resumeLesson').textContent=latest.mod.lessons[latest.slug];
    document.getElementById('resumeIcon').innerHTML='<use href="#ic-'+latest.mod.icon+'"/>';
  }
}
refresh();
/* 同步程式開的掛勾：登入後雲端進度合併回本機，卡片與「繼續上次」要重算 */
window.NotesHome={modules:MODS.map(function(m){return m.id;}),refresh:refresh};
})();
</script>
__SYNC__
</body>
</html>
```

（`test_on_with_config` 要求 `window.NotesHome=` 出現在 `<script src="sync.js">` 之前，上面照舊。）

- [ ] **Step 5: 重寫 `builder/templates/favicon.svg`**

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="14" fill="#233831"/>
  <path d="M18 14c6-4 14-4 20 0v36c-6-4-14-4-20 0z" fill="#C5E0D7"/>
  <path d="M38 14c4-3 8-3 12 0v36c-4-3-8-3-12 0" fill="none" stroke="#A9D9C7" stroke-width="4" stroke-linejoin="round"/>
  <path d="M22 40l6 6 12-14" fill="none" stroke="#F29F80" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

- [ ] **Step 6: 重寫 `builder/templates/style.css`**

```css
/* 改版規格 docs/superpowers/specs/2026-10-13-redesign-and-wrong-bank-design.md 第 2 節：
   白底配色塊。顏色只當記號，內容區永遠白底；不做深色模式。 */
:root{
  --paper:#FFFFFF; --surface:#FFFFFF; --sunk:#F7F9F6;
  --ink:#233831; --ink2:#5A6B65; --mut:#8A9792; --line:#DEE5DD;
  --mint:#A9D9C7; --mint-soft:#C5E0D7;
  --peach:#F29F80; --peach-soft:#F2CEAE;
  --amber:#FBC580;
  --ok:#1F8A5B; --no:#D9603A;
  --code:#EEF3EF; --code-ink:#233831; --code-text:#DEE5DD;
  --mono:"JetBrains Mono",ui-monospace,Menlo,monospace;
  --r:12px; --r-sm:10px; --top:54px;
}
*{box-sizing:border-box}
html{scroll-padding-top:calc(var(--top) + 14px)}
body{margin:0;background:var(--paper);color:var(--ink);
  font-family:"Noto Sans TC","PingFang TC","Microsoft JhengHei",sans-serif;
  font-size:16.5px;line-height:1.85;-webkit-font-smoothing:antialiased}
a{color:var(--ink)}
*:focus-visible{outline:2px solid var(--peach);outline-offset:2px}
button{font-family:inherit}

/* ── 圖示 ── */
.ic{width:1.15em;height:1.15em;vertical-align:-.22em;flex:none;display:inline-block}
.ic.big{width:34px;height:34px;vertical-align:middle}
.ic.ok{color:var(--ok)}
.ic.no{color:var(--no)}

/* ── 頂欄 ── */
.topbar{position:fixed;top:0;left:0;right:0;height:var(--top);z-index:40;
  background:var(--paper);border-bottom:3px solid var(--mint);
  display:flex;align-items:center;gap:12px;padding:0 16px}
.topbar .burger{display:none;background:none;border:1.5px solid var(--line);border-radius:8px;
  width:40px;height:40px;color:var(--ink);cursor:pointer;align-items:center;justify-content:center;font-size:18px}
.topbar .brand{font-weight:900;font-size:16.5px;text-decoration:none;color:var(--ink);white-space:nowrap}
.topbar .brand b{color:var(--ink);border-bottom:3px solid var(--amber)}
.topbar .home{display:flex;align-items:center;gap:6px;text-decoration:none;color:var(--ink);font-weight:700;font-size:14.5px;white-space:nowrap}
.topbar .sep{color:var(--mut)}
.topbar .modsel{font-family:inherit;font-size:14px;font-weight:700;color:var(--ink);
  background:var(--surface);border:1.5px solid var(--line);border-radius:8px;padding:5px 8px;
  max-width:min(52vw,320px)}

/* ── 側欄 ── */
.sidebar{position:fixed;top:var(--top);left:0;bottom:0;width:272px;z-index:30;
  background:var(--paper);border-right:1.5px solid var(--line);
  overflow-y:auto;padding:12px 0 30px}
.sidebar a{display:flex;align-items:center;gap:9px;padding:8px 16px 8px 13px;min-height:40px;
  color:var(--ink);text-decoration:none;font-size:14.5px;line-height:1.5;
  border-left:3px solid transparent}
.sidebar a:hover{background:var(--sunk)}
.sidebar a.active{background:var(--line);border-left-color:var(--peach);font-weight:700}
.sidebar a .n{font-family:var(--mono);font-size:12px;color:var(--ink2);min-width:22px;text-align:right;flex:none}
.sidebar a .st{margin-left:auto;flex:none;font-family:var(--mono);font-size:11.5px;color:var(--ink2)}
.sidebar a .cnt{margin-left:auto;flex:none;font-family:var(--mono);font-size:11px;font-weight:600;
  background:var(--peach-soft);border-radius:99px;padding:1px 8px}
.sidebar .group{font-family:var(--mono);font-size:10.5px;letter-spacing:.18em;color:var(--ink2);padding:14px 16px 4px}
.sidebar .ov,.sidebar .wrong{font-weight:700}
.sidebar .subs{display:none;padding:2px 0 6px 44px}
.sidebar .subs a{display:block;padding:3px 10px;min-height:0;font-size:12.5px;color:var(--ink2);
  border-left:2px solid var(--line);margin-left:-2px}
.sidebar .subs a:hover{background:none;color:var(--ink)}
.sidebar .subs a.on{color:var(--ink);font-weight:700;border-left-color:var(--peach)}
.scrim{display:none;position:fixed;inset:var(--top) 0 0 0;background:rgba(35,56,49,.45);z-index:25}
.sidefoot{margin:14px 16px 0;padding-top:12px;border-top:1.5px solid var(--line)}
.sideprog{margin:0;font-size:13px;color:var(--ink2)}
.sideprog b{color:var(--ink)}
.synchint{margin:4px 0 0;font-size:12px;color:var(--ink2);line-height:1.7}
.synchint a{color:var(--ink)}
.sidefoot a{display:inline;padding:0;border-left:0;font-size:inherit;min-height:0}
.sidefoot a:hover{background:none;text-decoration:underline}

/* ── 主內容與斷點 ── */
.main{margin-left:272px;padding:calc(var(--top) + 24px) clamp(18px,4.5vw,56px) 90px;max-width:848px}
.toc{display:none}
@media (min-width:961px){
  .sidebar .subs:not([hidden]){display:block}
}
@media (max-width:960px){
  .topbar .burger{display:flex}
  .sidebar{transform:translateX(-105%);transition:transform .2s ease;box-shadow:4px 0 18px rgba(0,0,0,.15)}
  @media (prefers-reduced-motion:reduce){.sidebar{transition:none}}
  .sidebar.open{transform:none}
  .scrim.show{display:block}
  .main{margin-left:0;padding-left:16px;padding-right:16px}
  .toc{display:block}
}
article[hidden]{display:none}
h3.head,.drill,.quiz{scroll-margin-top:calc(var(--top) + 14px)}

/* ── 課首 ── */
.crumb{font-size:13px;color:var(--ink2);margin:0 0 10px}
.crumb a{color:var(--ink2);text-decoration:none}
.crumb a:hover{text-decoration:underline}
h1.lt{font-weight:900;font-size:clamp(26px,5vw,36px);line-height:1.25;margin:0 0 10px;letter-spacing:-.01em;text-wrap:balance}
h1.lt .cnt{font-family:var(--mono);font-size:13px;font-weight:600;background:var(--peach-soft);border-radius:99px;padding:2px 10px;vertical-align:middle}
.meta{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:0 0 8px}
.meta .chip{font-family:var(--mono);font-size:11.5px;font-weight:600;padding:3px 10px;border-radius:99px;background:var(--line);color:var(--ink)}
p.sub{color:var(--ink2);font-size:16.5px;margin:0 0 18px}
.toc{background:var(--line);border-radius:var(--r-sm);padding:8px 14px;margin:0 0 22px;font-size:14px}
.toc summary{cursor:pointer;font-size:11.5px;letter-spacing:.08em;font-weight:700;padding:4px 0}
.toc ol{margin:4px 0 6px;padding-left:1.3em;display:flex;flex-direction:column;gap:2px}
.toc a{text-decoration:none}
.toc a:hover{text-decoration:underline}

/* ── 內文元件（內容檔裡的 class 不變，只換色） ── */
.learn{background:var(--surface);border:1.5px solid var(--line);border-left:4px solid var(--amber);
  border-radius:var(--r-sm);padding:14px 20px;margin:0 0 30px}
.learn .lbl,.keys .lbl{font-family:var(--mono);font-size:11px;letter-spacing:.16em;color:var(--ink2);margin:0 0 4px;font-weight:600}
.learn ul{margin:0;padding-left:1.2em;display:flex;flex-direction:column;gap:4px}
.learn li{font-size:15px}
section{display:flex;flex-direction:column;gap:16px;margin:0 0 44px}
.era{font-family:var(--mono);font-size:11.5px;letter-spacing:.16em;color:var(--ink2);margin:0}
h3.head{font-weight:900;font-size:clamp(21px,3.6vw,26px);line-height:1.35;margin:0;letter-spacing:-.005em;text-wrap:balance;
  display:flex;align-items:center;gap:10px}
h3.head::before{content:"";flex:none;width:11px;height:11px;border-radius:3px;background:var(--peach)}
h4{font-weight:700;font-size:17.5px;margin:8px 0 0}
h5{margin:0;font-size:12.5px;font-family:var(--mono);letter-spacing:.1em;font-weight:600}
p{margin:0}
.muted{color:var(--ink2)}
.hot{color:var(--no);font-weight:700}
.win{color:var(--ok);font-weight:700}
.good{color:var(--ok);font-weight:700}
code{font-family:var(--mono);font-variant-ligatures:none;font-feature-settings:"liga" 0,"calt" 0;font-size:.85em;background:var(--code);padding:2px 6px;border-radius:4px}
p.q{font-size:17px;font-weight:700;background:var(--sunk);border-left:4px solid var(--amber);border-radius:0 6px 6px 0;padding:11px 17px;margin-top:6px}
p.formula{font-size:clamp(15px,2.3vw,18px);font-weight:700;background:var(--line);border-radius:var(--r-sm);padding:13px 20px;text-align:center;max-width:none;font-family:var(--mono)}
ul.plainlist{margin:0;padding-left:1.2em;display:flex;flex-direction:column;gap:8px}
ul.plainlist li{line-height:1.8}
.orig{display:block;color:var(--mut);font-size:.86em;line-height:1.6;margin-top:2px}
.ledger{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:15px}
.box{border:1.5px solid var(--line);border-radius:var(--r-sm);background:var(--surface);padding:16px 19px;display:flex;flex-direction:column;gap:8px}
.box.solved{border-top:4px solid var(--mint)}
.box.left{border-top:4px solid var(--peach)}
.box ul{margin:0;padding-left:1.1em;display:flex;flex-direction:column;gap:6px}
.box li{font-size:14.5px;line-height:1.7}
figure{margin:0;display:flex;flex-direction:column;gap:10px}
figure svg{display:block;width:100%;height:auto;background:var(--surface);border:1.5px solid var(--line);border-radius:var(--r-sm);padding:10px}
svg text{font-family:"Noto Sans TC","PingFang TC",sans-serif}
svg text:not([fill]){fill:currentColor}
svg .mono{font-family:var(--mono);font-variant-ligatures:none;font-feature-settings:"liga" 0,"calt" 0}
figcaption{font-size:13.5px;color:var(--ink2);line-height:1.7;border-left:2px solid var(--line);padding-left:12px}
.terms{display:grid;grid-template-columns:repeat(auto-fit,minmax(225px,1fr));gap:13px}
.term{background:var(--surface);border:1.5px solid var(--line);border-left:4px solid var(--mint);border-radius:var(--r-sm);padding:13px 15px;display:flex;flex-direction:column;gap:3px}
.term b{font-size:15.5px}
.term span{font-size:14px;line-height:1.65;color:var(--ink2)}
.tablewrap{overflow-x:auto;border:1.5px solid var(--line);border-radius:var(--r-sm);background:var(--surface)}
table{border-collapse:collapse;width:100%;min-width:620px;font-size:14px}
th,td{text-align:left;padding:11px 15px;border-bottom:1px solid var(--line);vertical-align:top}
thead th{font-family:var(--mono);font-size:11px;letter-spacing:.1em;color:var(--ink2);font-weight:600;white-space:nowrap;background:var(--sunk)}
tbody th{font-weight:700;min-width:6.5em;max-width:15em}
td.num{font-family:var(--mono);font-variant-numeric:tabular-nums}
tbody tr:last-child th,tbody tr:last-child td{border-bottom:0}
.keys{background:var(--surface);border:1.5px solid var(--line);border-top:4px solid var(--mint);border-radius:var(--r-sm);padding:18px 22px;margin:8px 0 36px}
.keys ul{margin:0;padding-left:1.2em;display:flex;flex-direction:column;gap:7px}
.keys li{font-size:15px}
.card{background:var(--surface);border:1.5px solid var(--line);border-radius:var(--r-sm);padding:20px;display:flex;flex-direction:column;gap:10px}
.card p{font-size:15px;line-height:1.75}
.card .badge{font-family:var(--mono);font-size:11px;letter-spacing:.12em;color:var(--ink);background:var(--peach-soft);align-self:flex-start;padding:2px 8px;border-radius:99px}
.pits{display:flex;flex-direction:column;gap:14px}
.pit{display:grid;grid-template-columns:auto 1fr;gap:14px;align-items:start;background:var(--surface);border:1.5px solid var(--line);border-left:4px solid var(--peach);border-radius:var(--r-sm);padding:14px 18px}
.pit .n{font-family:var(--mono);color:var(--no);font-weight:600;font-size:15px;line-height:1.85}
.pit p{font-size:15px;line-height:1.75}
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:26px}
mark.fixnote{background:var(--line);color:inherit;padding:1px 4px;border-radius:3px;border-bottom:2px solid var(--mint);cursor:help;position:relative}
mark.fixnote:hover::after,mark.fixnote:focus::after{
  content:attr(data-note);position:absolute;left:0;top:calc(100% + 6px);z-index:20;
  background:var(--ink);color:#FFFFFF;font-size:12.5px;line-height:1.6;font-weight:400;
  padding:8px 12px;border-radius:8px;width:max-content;max-width:min(320px,72vw);white-space:normal}
mark.fixnote:focus{outline:2px solid var(--mint);outline-offset:1px}
a.fixsrc{font-size:11.5px;font-family:var(--mono);color:var(--ink2);text-decoration:none;vertical-align:super;margin-left:2px}
a.fixsrc:hover{text-decoration:underline}
pre{background:var(--code-ink);border-radius:var(--r-sm);padding:14px 18px;margin:0;overflow-x:auto;line-height:1.75}
pre code{background:none;padding:0;border-radius:0;display:block;color:var(--code-text);font-size:13.5px;white-space:pre}
blockquote{background:var(--sunk);border-left:3px solid var(--amber);border-radius:0 var(--r-sm) var(--r-sm) 0;margin:14px 0 4px;padding:14px 20px;font-size:15.5px;line-height:1.9;color:var(--ink)}
blockquote p{margin:0}
blockquote p+p{margin-top:10px}
@media (max-width:640px){figure{overflow-x:auto}figure > svg{min-width:600px}}

/* ── 選項（隨堂測驗、錯題練習、課中練習共用） ── */
.opts,.dopts{display:flex;flex-direction:column;gap:7px;list-style:none;margin:0;padding:0}
.opt,.dopts li{display:flex;gap:10px;align-items:center;border:1.5px solid var(--line);border-radius:var(--r-sm);
  padding:8px 12px;min-height:42px;background:var(--surface);cursor:pointer;font-size:14.5px;line-height:1.6;
  color:var(--ink);text-align:left;width:100%;font-family:inherit}
.opt:hover,.dopts li:hover,.dopts li:focus{border-color:var(--ink2);outline:none}
.opt .l,.dopts li .l{flex:none;width:22px;height:22px;border-radius:50%;background:var(--line);
  display:inline-flex;align-items:center;justify-content:center;font-family:var(--mono);font-size:11.5px;font-weight:600}
.opt .tx{flex:1;min-width:0}
.opt .mk,.dopts li .mk{margin-left:auto;flex:none;display:inline-flex}
.opt.sel{border-color:var(--ink);border-width:2px}
.opt.sel .l{background:var(--ink);color:#FFFFFF}
.opt:disabled,.drill.answered .dopts li{cursor:default}
.drill.answered .dopts li:hover{border-color:var(--line)}
.opt.right,.dopts li.right{background:var(--mint-soft);border-color:var(--mint)}
.opt.right .l,.dopts li.right .l{background:var(--mint)}
.opt.wrongpick,.dopts li.wrongpick{background:var(--peach-soft);border-color:var(--peach)}
.opt.wrongpick .l,.dopts li.wrongpick .l{background:var(--peach)}
.exp,.dexp{font-size:13.5px;color:var(--ink);background:var(--sunk);border-left:3px solid var(--amber);
  padding:7px 12px;margin:8px 0 0;border-radius:0 8px 8px 0}
.dexp .dtr{display:block;color:var(--mut);margin-bottom:4px}

/* ── 課中練習 ── */
article{counter-reset:drill}
.drill{margin:14px 0 18px}
.drill .dq{font-weight:700;margin:0 0 8px}
.drill pre{margin:0 0 8px}
.drill .dq::before{counter-increment:drill;content:"練習 " counter(drill);font-family:var(--mono);font-size:12.5px;color:var(--ink2);margin-right:8px}

/* ── 隨堂測驗、錯題練習 ── */
.quiz{border:1.5px solid var(--line);border-radius:var(--r);padding:clamp(16px,3vw,24px);margin:0 0 34px;background:var(--surface)}
.qhead{display:flex;flex-direction:column;gap:2px;margin:0 0 12px}
.qtitle{font-weight:900;font-size:19px}
.qnote{font-size:13.5px;color:var(--ink2)}
.score{display:flex;align-items:center;gap:16px;background:var(--line);border-radius:var(--r);padding:14px 18px;margin:0 0 12px}
.score .big{font-size:34px;font-weight:900;line-height:1;font-family:var(--mono)}
.score .big small{font-size:15px;font-weight:600}
.score .t{flex:1;min-width:0}
.score .mono{font-family:var(--mono);font-size:12px;color:var(--ink2)}
.tr{height:8px;border-radius:99px;background:var(--surface);overflow:hidden;margin-top:6px}
.tr i{display:block;height:100%;border-radius:99px;background:var(--mint);transition:width .3s ease}
.qact{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:0 0 16px}
.qact.bottom{margin:8px 0 0}
.qbtn{font-size:14.5px;font-weight:700;padding:9px 20px;min-height:40px;border-radius:99px;border:1.5px solid var(--ink);background:var(--ink);color:#FFFFFF;cursor:pointer;flex:1 1 auto}
.qbtn:hover{filter:brightness(1.15)}
.qbtn:disabled{background:var(--line);border-color:var(--line);color:var(--ink2);cursor:not-allowed}
.qbtn.sec{background:var(--surface);color:var(--ink)}
.qmsg{font-size:13.5px;color:var(--ink2);flex:1 1 100%}
.qq{border:1.5px solid var(--line);border-radius:var(--r);padding:12px 14px 10px;margin:0 0 12px}
.qq.ng{border-color:var(--peach)}
.qtop{display:flex;align-items:center;gap:8px;font-size:11.5px;letter-spacing:.08em;font-weight:700;margin:0 0 4px}
.qtop .src{font-weight:400;letter-spacing:0;color:var(--ink2)}
.qtop .mk{margin-left:auto;display:inline-flex;font-size:18px}
.qq .qt{font-weight:700;font-size:15.5px;margin:0 0 10px}

/* ── 錯題區 ── */
.legend{display:flex;gap:16px;flex-wrap:wrap;align-items:center;background:var(--sunk);border-radius:var(--r-sm);padding:7px 12px;margin:0 0 14px;font-size:12.5px;color:var(--ink2)}
.legend .ic{font-size:18px}
.wgroup{font-size:13px;color:var(--ink2);margin:16px 0 6px;display:flex;align-items:center;gap:7px}
.wgroup::before{content:"";width:9px;height:9px;border-radius:3px;background:var(--amber)}
.witem{display:flex;align-items:center;gap:10px;border:1.5px solid var(--line);border-radius:var(--r-sm);padding:9px 12px;margin:0 0 8px;font-size:14.5px}
.witem .ic{font-size:20px}
.witem .wq{flex:1;min-width:0}
.wrm{flex:none;font-size:12px;color:var(--ink2);background:none;border:1.5px solid var(--line);border-radius:99px;padding:3px 10px;min-height:30px;cursor:pointer}
.wrm:hover{border-color:var(--ink2);color:var(--ink)}

/* ── 上一課／下一課 ── */
.pager{display:flex;justify-content:space-between;gap:12px;border-top:1.5px solid var(--line);padding-top:20px}
.pager a{display:flex;flex-direction:column;gap:2px;text-decoration:none;color:var(--ink);border:1.5px solid var(--line);border-radius:var(--r-sm);padding:12px 18px;max-width:46%;background:var(--surface)}
.pager a:hover{border-color:var(--ink2)}
.pager a .dir{font-size:12px;color:var(--ink2)}
.pager a .t{font-weight:700;font-size:15px}
.pager a.next{margin-left:auto;text-align:right}

/* ── 模組總覽 ── */
.ov-hero{margin:0 0 26px}
.ov-hero .kick{font-family:var(--mono);font-size:11.5px;letter-spacing:.2em;color:var(--ink2);margin:0 0 8px}
.ov-hero h1{font-weight:900;font-size:clamp(28px,6vw,42px);line-height:1.2;margin:0 0 12px;letter-spacing:-.01em}
.ov-hero p{color:var(--ink2)}
.ov-hero p:not(.kick):not(.ov-progress){margin:0 0 10px}
.ov-points{margin:0 0 12px;padding-left:1.3em;color:var(--ink2)}
.ov-points li{margin:0 0 6px;line-height:1.7}
.ov-progress{font-size:14.5px;color:var(--ink2);margin:14px 0 0}
.ov-progress b{color:var(--ink)}
.lesson-list{display:flex;flex-direction:column;border:1.5px solid var(--line);border-radius:var(--r);background:var(--surface);overflow:hidden}
.lesson-list a{display:flex;gap:14px;align-items:center;padding:14px 18px;min-height:44px;text-decoration:none;color:var(--ink);border-bottom:1px solid var(--line)}
.lesson-list a:last-child{border-bottom:0}
.lesson-list a:hover{background:var(--sunk)}
.lesson-list .n{font-family:var(--mono);color:var(--ink2);font-size:14px;min-width:22px;text-align:right;flex:none}
.lesson-list .tt{display:flex;flex-direction:column;gap:1px;min-width:0;flex:1}
.lesson-list .tt b{font-size:16px}
.lesson-list .tt span{font-size:13.5px;color:var(--ink2)}
.lesson-list .mins{flex:none;font-family:var(--mono);font-size:12px;color:var(--ink);background:var(--line);border-radius:99px;padding:3px 10px}
.lesson-list .done{flex:none;display:inline-flex;font-size:18px}
footer.site{margin-top:36px;border-top:1.5px solid var(--line);padding-top:15px;font-size:12.5px;color:var(--ink2)}

/* ── 平台首頁 ── */
.resume{display:flex;align-items:center;gap:12px;background:var(--peach-soft);border-radius:var(--r);padding:12px 16px;margin:0 0 20px;text-decoration:none;color:var(--ink)}
.resume .rt{display:flex;flex-direction:column;min-width:0;flex:1}
.resume .rt b{font-size:15px}
.resume .rt span{font-size:13px;color:var(--ink2);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.resume .go{flex:none;background:var(--ink);color:#FFFFFF;border-radius:99px;padding:6px 14px;font-size:13px;font-weight:700}
.mod-cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px}
.mod-card{display:flex;flex-direction:column;gap:8px;background:var(--surface);border:1.5px solid var(--line);border-radius:var(--r);padding:16px 18px;text-decoration:none;color:var(--ink)}
.mod-card:hover{border-color:var(--ink2)}
.mod-card b{font-size:17px;line-height:1.3}
.mod-card .bar{display:block;height:7px;border-radius:99px;background:var(--line);overflow:hidden}
.mod-card .bar i{display:block;height:100%;width:0;border-radius:99px;background:var(--mint)}
.mod-card .stats{font-family:var(--mono);font-size:12px;color:var(--ink2)}
.mod-card.done{background:var(--mint-soft);border-color:var(--mint)}
.mod-card.done .bar{background:var(--surface)}
.mod-card.done .bar i{background:var(--peach)}
@media (max-width:960px){.mod-cards{grid-template-columns:repeat(2,1fr);gap:10px}.mod-card{padding:12px 12px}.mod-card b{font-size:14.5px}}
.topbar .synchint{margin:0 0 0 auto;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.synchint .sh{display:none}
@media (max-width:640px){.topbar .synchint .st{display:none}.topbar .synchint .sh{display:inline}}
```

- [ ] **Step 7: 建置並跑全部測試**

Run: `python3 builder/build.py && python3 -m unittest discover -s builder/tests -v`
Expected: 全部 OK（含 `test_fixnote_styles`：`mark.fixnote`、`attr(data-note)`、`a.fixsrc` 都還在）。

- [ ] **Step 8: Commit**

```bash
git add builder/templates/module.html builder/templates/home.html builder/templates/style.css builder/templates/favicon.svg builder/tests/test_build.py
git commit -m "feat(ui): 白底配色塊新版面：樣式重寫、首頁加繼續上次與進度條、新網站圖示

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 6: 模組頁行為：測驗回饋與重做、錯題區、側欄成績與目錄捲動

**Files:**
- Rewrite: `builder/templates/course.js` 的瀏覽器部分（`if (typeof document !== 'undefined') (function(){ … })();` 裡面全部）
- Test: `builder/tests/test_build.py`（`test_course_js_hooks`）、node `--check`、手動瀏覽器驗證在 Task 8

**Interfaces:**
- Consumes：Task 2 的 `NotesQuiz`；Task 4 的 `TITLES`、id 與屬性；Task 5 的 CSS 類別。
- Produces：`window.NotesCourse = {module, slugs, loadDone, saveDone, refreshTicks}`（sync.js 用，形狀不變）。進度物件寫入 `_last` 與 `_wrong`。

- [ ] **Step 1: 把 `test_course_js_hooks` 加幾條字串檢查**

```python
    def test_course_js_hooks(self):
        js = (self.out / 'course.js').read_text(encoding='utf-8')
        self.assertIn('window.NotesCourse', js)
        self.assertIn('notes:progress-saved', js)
        self.assertIn('sideProg', js)
        for s in ('NotesQuiz.afterQuiz', 'NotesQuiz.afterPractice', 'NotesQuiz.remove', 'NotesQuiz.active',
                  "'#/wrong'", 'data-goto', 'IntersectionObserver', '_last'):
            self.assertIn(s, js, s)
```

Run: `python3 -m unittest builder.tests.test_build.TestBuild.test_course_js_hooks -v`
Expected: FAIL（`NotesQuiz.afterQuiz` 還沒被用到）。

- [ ] **Step 2: 把 `course.js` 的瀏覽器部分換成下面整段**

（檔案前半的 `NotesQuiz` 與 `module.exports` 那行不動；從 `if (typeof document !== 'undefined') (function(){` 起整段取代到檔尾。）

```js
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
    if(wrongIdx.length){
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
```

- [ ] **Step 3: 語法與測試**

Run: `node --check builder/templates/course.js && node builder/tests/test_quiz.js && python3 builder/build.py && python3 -m unittest discover -s builder/tests -v`
Expected: 全部 OK。

- [ ] **Step 4: 在瀏覽器裡冒煙測試（快速版，完整驗收在 Task 8）**

```bash
cd dist && python3 -m http.server 8765 >/dev/null 2>&1 &
sleep 1
B="$HOME/.claude/skills/gstack/browse/dist/browse"
"$B" goto "http://localhost:8765/english/#/lesson/grammar-sentence"
"$B" js "document.querySelectorAll('#pg-grammar-sentence .qq').length"
"$B" js "document.querySelectorAll('.subs[data-subs=\"grammar-sentence\"]:not([hidden]) a').length"
"$B" console
```

Expected：第一個 `js` 印出該課題數（8 或 10）、第二個印出小節數 + 2（課中練習、隨堂測驗）、`console` 無錯誤。測完 `kill %1`。

- [ ] **Step 5: Commit**

```bash
git add builder/templates/course.js builder/tests/test_build.py
git commit -m "feat(course): 測驗回饋改圈叉與成績卡、只重做錯的、錯題區兩頁、側欄成績與小節捲動

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 7: 同步程式配合首頁與錯題區

**Files:**
- Modify: `builder/templates/sync.js:24-148`（瀏覽器部分）
- Test: 既有 `test_sync.py`、`test_build.py::TestFirebaseInjection`

**Interfaces:**
- Consumes：`window.NotesHome.refresh()`（Task 5）、`window.NotesCourse.refreshTicks()`（Task 6）、`NotesSync.merge`（Task 1）。

- [ ] **Step 1: 確認現況不用改邏輯，只補註解**

`mergeAll` 已經對模組頁呼叫 `course.refreshTicks()`、對首頁呼叫 `home.refresh()`；`NotesSync.merge` 已經會帶著 `_last`、`_wrong`。進度事件 `notes:progress-saved` 帶的 `e.detail.data` 是整個模組物件（含保留鍵），`pushCloud` 用 `set(patch,{merge:true})` 寫上去。所以同步程式本身不需要改邏輯。

把 `sync.js` 第 87 行附近的註解改成：

```js
  /* patch 的形狀是 { 模組id: 該模組的進度 }，可以一次帶多個模組；merge:true 不會蓋掉其他模組。
     模組的進度物件裡除了每課的 {best,total,done}，還有 _last（最後看的課）與 _wrong（錯題），
     一起寫上去；錯題的鍵只會新增或更新，不會刪，所以 merge:true 不會漏掉任何一筆。 */
```

- [ ] **Step 2: 跑測試**

Run: `node --check builder/templates/sync.js && python3 -m unittest discover -s builder/tests -v`
Expected: 全部 OK。

- [ ] **Step 3: Commit**

```bash
git add builder/templates/sync.js
git commit -m "docs(sync): 註明進度物件現在含最後看的課與錯題

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 8: 瀏覽器驗收截圖、文件更新

**Files:**
- Modify: `CLAUDE.md`
- 截圖輸出到 scratchpad（不進 git）

- [ ] **Step 1: 建置並起本機伺服器**

```bash
cd /Users/twinb00597734/Workspace/notes-platform && python3 builder/build.py
cd dist && python3 -m http.server 8765 >/dev/null 2>&1 &
sleep 1
```

- [ ] **Step 2: 用假進度把畫面填滿，電腦寬截圖**

```bash
B="$HOME/.claude/skills/gstack/browse/dist/browse"
OUT=/private/tmp/claude-503/-Users-twinb00597734-Workspace-notes-platform/378410cf-5700-4fcb-8932-5f5323864779/scratchpad
"$B" viewport 1280x900
"$B" goto "http://localhost:8765/english/#/lesson/grammar-sentence"
# 假進度：第 1、2 課（slug daily-english、media-english）全對，第 3 課（grammar-sentence）5/8，最後看第 3 課
"$B" js "localStorage.setItem('notes-progress:english', JSON.stringify({'daily-english':{best:8,total:8,done:true},'media-english':{best:8,total:8,done:true},'grammar-sentence':{best:5,total:8,done:false},_last:{slug:'grammar-sentence',at:Math.floor(Date.now()/1000)}}))"
"$B" reload
"$B" screenshot "$OUT/final-lesson-d.png"
```

（英文模組的課資料夾叫 `03-grammar-sentence`，但網址用的 slug 是 `grammar-sentence`，兩者不同；slug 以 `content/english/module.json` 的 `slug` 欄位為準。）

- [ ] **Step 3: 作答並對答案，截圖對完畫面與「只重做錯的」**

```bash
# 每題點第一個選項（順序是隨機的，所以會有對有錯）
"$B" js "document.querySelectorAll('#pg-grammar-sentence .qq').forEach(function(q){q.querySelector('.opt').click();})"
"$B" click "#pg-grammar-sentence .qact.bottom .qbtn"
"$B" screenshot "$OUT/final-graded-d.png"
"$B" js "var b=document.querySelector('#pg-grammar-sentence .qact:not(.bottom) .qbtn'); b&&b.textContent"
"$B" click "#pg-grammar-sentence .qact:not(.bottom) .qbtn"
"$B" screenshot "$OUT/final-redo-d.png"
```

Expected：`final-graded-d.png` 最上面是成績卡（大數字＋進度條＋「最佳 N/8」）、兩顆按鈕、每題圈叉；按了「只重做錯的」後錯的題目變回白底可選、對的留著。

- [ ] **Step 4: 錯題區清單與練習**

```bash
"$B" goto "http://localhost:8765/english/#/wrong"
"$B" screenshot "$OUT/final-wrong-list-d.png"
"$B" click "#wrongStart"
"$B" screenshot "$OUT/final-wrong-practice-d.png"
"$B" js "document.querySelectorAll('.sidebar [data-wrongcnt]')[0].textContent"
```

Expected：清單有圖例列、「開始練習（N 題）」、依課分組的題目與「移除」；練習頁每題標「第 3 課」；側欄錯題區數字等於 N。

- [ ] **Step 5: 首頁**

```bash
"$B" goto "http://localhost:8765/"
"$B" screenshot "$OUT/final-home-d.png"
"$B" js "document.getElementById('resume').hidden"
```

Expected：`false`（「繼續上次：英文」卡顯示，連到第 3 課）；英文卡進度條約 10%。

- [ ] **Step 6: 手機寬，同一組畫面**

```bash
"$B" viewport 390x844
for u in "/" "/english/#/lesson/grammar-sentence" "/english/#/wrong"; do
  "$B" goto "http://localhost:8765$u"
  n=$(echo "$u" | tr -c 'a-z' '-')
  "$B" screenshot "$OUT/final$n-m.png"
done
"$B" goto "http://localhost:8765/english/#/lesson/grammar-sentence"
"$B" click "#burger"
"$B" screenshot "$OUT/final-sidebar-m.png"
"$B" console
```

Expected：手機上課首有可收合的「本課小節」、側欄抽屜打開時每課右邊有成績、錯題區有數字；`console` 無錯誤。

- [ ] **Step 7: 用 Read 工具逐張看截圖**，對照規格第 2〜7 節。發現不對的地方就改樣板、重建、重截，直到每張都符合。常見要盯的：
  - 成績卡沒有「答對幾題、比上次多幾題」字樣
  - 選項沒有「正解／你的答案」文字
  - 頁面任何地方沒有 emoji
  - 手機上選項整列可點、高度夠

- [ ] **Step 8: 關掉伺服器，改 `CLAUDE.md`**

```bash
kill %1
```

`CLAUDE.md` 工程慣例那段的色系行改成：

```markdown
- 色系定稿：白底配色塊（白底、深綠灰墨色 #233831、薄荷與桃橘六個淡色只當記號；色號表在 `docs/superpowers/specs/2026-10-13-redesign-and-wrong-bank-design.md` 第 2 節），**刻意不做深色模式**。圖示全部是 `builder/templates/icons.svg` 裡自己畫的 SVG，不用 emoji。
```

「現況」段最後加一條：

```markdown
- **2026-10-13 改版與錯題區**：外觀換成白底配色塊、測驗回饋改圈叉加成績卡、每個模組有錯題區（連對兩次或手動移除）、首頁有「繼續上次」。規格在 `docs/superpowers/specs/2026-10-13-redesign-and-wrong-bank-design.md`，計畫在 `docs/superpowers/plans/2026-10-13-redesign-and-wrong-bank.md`。進度物件多了 `_last` 與 `_wrong` 兩個保留鍵，合併規則在 `builder/templates/sync.js`。
```

- [ ] **Step 9: 全部測試最後跑一次，Commit**

```bash
python3 -m unittest discover -s builder/tests -v
git add CLAUDE.md
git commit -m "docs: CLAUDE.md 更新色系定稿與 2026-10-13 改版現況

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

- [ ] **Step 10: 把截圖給 Tim 看，等他說可以再 push**

push 到 `main` 就會發佈（GitHub Actions → GitHub Pages）。push 前要 Tim 點頭；push 時遠端是 `git@github-hhtim:HHTim/notes-platform.git`，不改。
