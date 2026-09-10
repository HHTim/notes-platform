# 第二期：進度跨裝置同步 實作計畫

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**目標：** 沒登入一切照舊（進度存瀏覽器）；用 Google 登入且 email 在白名單的人，進度存 Firestore、跨裝置同步；合併規則是「勾過就算勾過、成績取較好那次」。

**做法：** Firebase 只用兩個零件（Google 登入＋Firestore 雲端資料庫），SDK 從 CDN 用傳統 `<script>` 載入（compat 版，配合現有無建置步驟的原生 JavaScript）。設定檔 `content/firebase.json` **可以不存在**——不存在就完全不載 Firebase，網站行為與現在完全相同；因此全部程式先寫完測完，最後才需要 Tim 開 Firebase 專案。同步邏輯集中在新檔 `sync.js`，透過 `course.js` 開出的掛勾（讀寫進度、重畫打勾）運作。

**技術：** 原生 JavaScript、Firebase JS SDK 10.14.1（compat 版，CDN）、Python 3 標準庫（builder 與測試）、node（測 JavaScript 的合併函式與語法）。

**規格：** `docs/superpowers/specs/2026-09-04-notes-platform-design.md` 第 7 節（進度跨裝置同步）與第 9 節第二期驗收。

## 全域限制（每個任務都適用）

- **不用任何框架**；builder 只用 Python 3 標準庫。Firebase SDK 是規格明定的雲端零件，用 CDN compat 版、版本釘死 `10.14.1`，只載 app、auth、firestore 三支。
- **`content/firebase.json` 不存在時，建置產物必須與第一期完全相同的行為**：不載任何 Firebase 程式、`dist/` 沒有 `sync.js`、提示列顯示「進度只存在這台裝置」（沒有登入連結）。
- **三狀態提示文字照規格第 7 節的表格逐字**（固定位置、不跳視窗）：
  - 沒登入：`進度只存在這台裝置 · 登入後跨裝置同步`（後半句是登入連結）
  - 已登入＋白名單：`已同步（<Google 帳號名>）`
  - 已登入但不在白名單：`此帳號未獲授權，進度僅存於本機`
  - 本計畫追加：後兩態尾端附一個小的「登出」連結（規格沒寫，但登入錯帳號時需要退路——這是刻意的補充，不是偏離）。
- **合併規則**（規格逐字）：本機與雲端不一致時取聯集——勾過就算勾過，測驗成績取較好那次。**絕不以單邊蓋掉另一邊。**
- **資料庫規則三條**（規格逐字）：名單只有 Tim 能改；名單上的人只能讀寫自己的進度；其他一律拒絕。
- Firebase 的 `apiKey`/`authDomain`/`projectId` 是公開識別碼，放進公開 repo 是 Firebase 官方設計（安全靠資料庫規則，不靠藏設定）——不要當成祕密處理，也不要把真正的祕密（任何私鑰）放進 repo。
- 亮暖色、不做深色模式；`dist/` 不進 git；整站重建。
- 不做排行榜、不看別人進度；白名單成員彼此完全隔離（規格第 10 節）。
- Git：遠端 SSH 別名不動、repo 身分 commit、直接在 `main` 上做。
- 寫給人看的文字照 Tim 的用詞規則（台灣講法、不發明編號代號、不造字）。

## 檔案結構總覽

```
notes-platform/
├── content/
│   └── firebase.json               （任務 5 由 Tim 的設定值產生；之前不存在）
├── builder/
│   ├── build.py                    （任務 3 改）讀 firebase.json、條件式注入
│   ├── templates/
│   │   ├── module.html             （任務 1 改側欄底部；任務 3 加 __SYNC__ 佔位符）
│   │   ├── style.css               （任務 1 改）側欄底部樣式
│   │   ├── course.js               （任務 1 改）三個掛勾
│   │   └── sync.js                 （任務 2 建）合併函式＋登入＋三狀態＋Firestore 讀寫
│   └── tests/
│       ├── test_build.py           （任務 1、3 擴充）
│       ├── test_merge.js           （任務 2 建）合併規則的 node 測試
│       └── test_sync.py            （任務 2 建）跑 node 測試與語法檢查的包裝
├── firebase/
│   └── firestore.rules             （任務 4 建）資料庫規則（Tim 貼進主控台用）
└── docs/
    └── firebase-setup.md           （任務 4 建）Tim 的一次性設定手冊
```

**責任分工**：`course.js` 依舊是唯一讀寫 localStorage 的地方；`sync.js` 只透過 `course.js` 開的掛勾動進度，自己只管 Firebase。兩檔之間的介面見下節。

## 介面（所有任務共用）

`course.js` 開給 `sync.js` 的掛勾（任務 1 建立）：

```js
window.NotesCourse = {
  module: MODULE,          // 模組 id，字串，例如 "k8s"
  slugs: SLUGS,            // 課的 slug 陣列
  loadDone: loadDone,      // () => {slug: {best, total, done}}
  saveDone: saveDone,      // (d) => 寫進 localStorage 並發出事件
  refreshTicks: refreshTicks  // () => 重畫側邊欄與總覽的打勾、進度數字
};
```

`saveDone` 每次寫入後在 `document` 上發出事件 `notes:progress-saved`，`detail = {module: MODULE, data: <整份進度物件>}`。

Firestore 資料佈局：

- `whitelist/{email}`——白名單，一個 email 一份文件（內容不重要，存在與否才重要）。只有 Tim 從 Firebase 管理網頁增刪。
- `progress/{uid}`——每人一份進度文件，欄位是模組 id：`{k8s: {physical: {best,total,done}, …}, redis: {…}}`。

`content/firebase.json` 格式（三個值都來自 Firebase 主控台的網頁應用程式設定）：

```json
{"apiKey": "…", "authDomain": "<專案>.firebaseapp.com", "projectId": "<專案>"}
```

---

### 任務 1：course.js 掛勾＋側邊欄進度列

**Files:**
- Modify: `builder/templates/course.js`（三處，見下）
- Modify: `builder/templates/module.html`（側邊欄底部加一塊）
- Modify: `builder/templates/style.css`（檔尾追加）
- Modify: `builder/tests/test_build.py`（`TestBuild` 加兩個測試方法）

**Interfaces:**
- Consumes: 現有 `course.js` 的 `loadDone`/`saveDone`/`refreshTicks`/`MODULE`/`SLUGS`
- Produces: `window.NotesCourse` 掛勾與 `notes:progress-saved` 事件（簽名見「介面」節）；`#sideProg`、`#syncHint` 兩個側欄元素

- [ ] **步驟 1：寫失敗的測試**

在 `builder/tests/test_build.py` 的 `TestBuild` 類別里加：

```python
    def test_sidebar_progress_and_hint(self):
        for mid in ('k8s', 'redis'):
            html = (self.out / mid / 'index.html').read_text(encoding='utf-8')
            self.assertIn('id="sideProg"', html, mid)
            self.assertIn('id="syncHint"', html, mid)
            self.assertIn('進度只存在這台裝置', html, mid)

    def test_course_js_hooks(self):
        js = (self.out / 'course.js').read_text(encoding='utf-8')
        self.assertIn('window.NotesCourse', js)
        self.assertIn('notes:progress-saved', js)
        self.assertIn('sideProg', js)
```

- [ ] **步驟 2：跑測試，確認新測試失敗**

```bash
python3 -m unittest discover -s builder/tests -v
```

預期：兩個新測試 FAIL，其餘照舊全綠（含 2 個自動跳過）。

- [ ] **步驟 3：改 `builder/templates/module.html`**

側邊欄那段從：

```html
<nav class="sidebar" id="sidebar" aria-label="章節選單">
__SIDEBAR__
</nav>
```

改成：

```html
<nav class="sidebar" id="sidebar" aria-label="章節選單">
__SIDEBAR__
  <div class="sidefoot">
    <p class="sideprog" id="sideProg"></p>
    <p class="synchint" id="syncHint">進度只存在這台裝置</p>
  </div>
</nav>
```

- [ ] **步驟 4：`builder/templates/style.css` 檔尾追加**

```css
/* ── 側邊欄底部：進度數字與同步狀態 ── */
.sidefoot{margin:14px 18px 0;padding-top:12px;border-top:1px solid var(--line)}
.sideprog{margin:0;font-size:13px;color:var(--ink2)}
.sideprog b{color:var(--gold-deep)}
.synchint{margin:4px 0 0;font-size:12px;color:var(--mut);line-height:1.7}
.synchint a{color:var(--gold)}
```

- [ ] **步驟 5：改 `builder/templates/course.js` 三處**

第一處——`saveDone` 寫完發事件。原：

```js
function saveDone(d){try{localStorage.setItem(KEY,JSON.stringify(d));}catch(e){}}
```

改成：

```js
function saveDone(d){
  try{localStorage.setItem(KEY,JSON.stringify(d));}catch(e){}
  try{document.dispatchEvent(new CustomEvent('notes:progress-saved',{detail:{module:MODULE,data:d}}));}catch(e){}
}
```

第二處——`refreshTicks` 也更新側欄進度數字。在

```js
  var p=document.getElementById('ovProgress');
  if(p) p.innerHTML='已完成 <b>'+n+'</b> / '+SLUGS.length+' 課'+(n===SLUGS.length?'——全部打勾了 🎉':'');
```

之後（同函式內）加：

```js
  var sp=document.getElementById('sideProg');
  if(sp) sp.innerHTML='已完成 <b>'+n+'</b> / '+SLUGS.length+' 課';
```

第三處——檔尾開掛勾。在最後的 `})();` 之前（`modsel` 那兩行之後）加：

```js
window.NotesCourse={module:MODULE,slugs:SLUGS,loadDone:loadDone,saveDone:saveDone,refreshTicks:refreshTicks};
```

- [ ] **步驟 6：跑測試與語法檢查，確認通過**

```bash
python3 -m unittest discover -s builder/tests -v
python3 builder/build.py && node --check dist/course.js
```

預期：全綠；node 無輸出（語法正確）。

- [ ] **步驟 7：commit**

```bash
git add builder/
git commit -m "feat: course.js 開同步掛勾；側邊欄底部顯示進度數字與同步狀態列"
```

---

### 任務 2：sync.js——合併規則、登入、三狀態、Firestore 讀寫

**Files:**
- Create: `builder/templates/sync.js`
- Create: `builder/tests/test_merge.js`
- Create: `builder/tests/test_sync.py`

**Interfaces:**
- Consumes: 任務 1 的 `window.NotesCourse` 與 `notes:progress-saved` 事件；頁面全域變數 `FIREBASE_CONFIG`（任務 3 注入）；CDN 載入的 `firebase` 全域（compat 版）
- Produces: `NotesSync.merge(local, cloud) -> merged`——純函式，兩個 `{slug:{best,total,done}}` 物件合併成一個；node 環境下 `module.exports = NotesSync`

- [ ] **步驟 1：寫失敗的測試**

建 `builder/tests/test_merge.js`：

```js
// 合併規則（規格第 7 節）：勾過就算勾過、成績取較好那次、絕不以單邊蓋掉另一邊
var assert = require('assert');
var NotesSync = require('../templates/sync.js');

// 聯集：兩邊各有對方沒有的課
assert.deepStrictEqual(
  NotesSync.merge({a:{best:2,total:5,done:false}}, {b:{best:5,total:5,done:true}}),
  {a:{best:2,total:5,done:false}, b:{best:5,total:5,done:true}});

// 同一課：done 勾過就算勾過（本機 true 雲端 false）、best 取高（雲端高）
assert.deepStrictEqual(
  NotesSync.merge({a:{best:3,total:5,done:true}}, {a:{best:5,total:5,done:false}}),
  {a:{best:5,total:5,done:true}});

// 反向：雲端勾過、本機成績高
assert.deepStrictEqual(
  NotesSync.merge({a:{best:4,total:5,done:false}}, {a:{best:1,total:5,done:true}}),
  {a:{best:4,total:5,done:true}});

// total 取大（補題後兩邊題數不同）
assert.deepStrictEqual(
  NotesSync.merge({a:{best:3,total:3,done:true}}, {a:{best:4,total:5,done:false}}),
  {a:{best:4,total:5,done:true}});

// 空邊與缺欄位：任一邊空、或紀錄缺 best/total/done，都要能合
assert.deepStrictEqual(NotesSync.merge(null, {a:{best:1,total:5,done:false}}),
  {a:{best:1,total:5,done:false}});
assert.deepStrictEqual(NotesSync.merge({}, {}), {});
assert.deepStrictEqual(NotesSync.merge({a:{done:true}}, {a:{best:2}}),
  {a:{best:2,total:0,done:true}});

console.log('merge 規則測試全部通過');
```

建 `builder/tests/test_sync.py`：

```python
# -*- coding: utf-8 -*-
# sync.js 的檢查：語法正確、合併規則符合規格。用 node 跑；沒裝 node 就跳過。
import shutil, subprocess, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


@unittest.skipUnless(shutil.which('node'), '沒裝 node，跳過 JavaScript 檢查')
class TestSyncJs(unittest.TestCase):
    def test_syntax(self):
        subprocess.run(['node', '--check', str(ROOT / 'builder' / 'templates' / 'sync.js')],
                       check=True)

    def test_merge_rules(self):
        r = subprocess.run(['node', str(ROOT / 'builder' / 'tests' / 'test_merge.js')],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
```

- [ ] **步驟 2：跑測試，確認失敗**

```bash
python3 -m unittest discover -s builder/tests -v
```

預期：`TestSyncJs` 兩個都 FAIL/ERROR（sync.js 不存在）。

- [ ] **步驟 3：建 `builder/templates/sync.js`**

```js
/* 進度跨裝置同步：Google 登入＋Firestore。
   只有 builder 在 content/firebase.json 存在時才把本檔放進頁面；
   頁面會先宣告 FIREBASE_CONFIG，並已載入 firebase compat SDK（app/auth/firestore）。 */
var NotesSync = {
  /* 合併規則（規格第 7 節）：勾過就算勾過、成績取較好那次，絕不以單邊蓋掉另一邊 */
  merge: function (local, cloud) {
    var out = {};
    function add(src) {
      if (!src) return;
      Object.keys(src).forEach(function (k) {
        var b = src[k] || {};
        var a = out[k];
        if (!a) { out[k] = { best: b.best || 0, total: b.total || 0, done: !!b.done }; return; }
        a.best = Math.max(a.best || 0, b.best || 0);
        a.total = Math.max(a.total || 0, b.total || 0);
        a.done = !!(a.done || b.done);
      });
    }
    add(local); add(cloud);
    return out;
  }
};
if (typeof module !== 'undefined' && module.exports) { module.exports = NotesSync; }

/* 瀏覽器裡才有 document 與 firebase；node 跑測試時只用得到上面的 merge */
if (typeof document !== 'undefined' && typeof firebase !== 'undefined') (function () {
  firebase.initializeApp(FIREBASE_CONFIG);
  var auth = firebase.auth();
  var db = firebase.firestore();
  var course = window.NotesCourse;   // course.js 開的掛勾
  var hint = document.getElementById('syncHint');
  var synced = false;                // 目前是不是「已登入＋白名單」狀態
  var uid = null;

  function setHint(html) { if (hint) hint.innerHTML = html; }
  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }
  function bindLogout() {
    var a = document.getElementById('syncOut');
    if (a) a.addEventListener('click', function (e) { e.preventDefault(); auth.signOut(); });
  }

  /* 三狀態提示（文字照規格第 7 節的表格） */
  function showLoggedOut() {
    synced = false; uid = null;
    setHint('進度只存在這台裝置 · <a href="#" id="syncLogin">登入後跨裝置同步</a>');
    var a = document.getElementById('syncLogin');
    if (a) a.addEventListener('click', function (e) {
      e.preventDefault();
      auth.signInWithPopup(new firebase.auth.GoogleAuthProvider())['catch'](function () {});
    });
  }
  function showUnauthorized() {
    synced = false;
    setHint('此帳號未獲授權，進度僅存於本機（<a href="#" id="syncOut">登出</a>）');
    bindLogout();
  }
  function showSynced(user) {
    synced = true;
    setHint('已同步（' + esc(user.displayName || user.email) + '）（<a href="#" id="syncOut">登出</a>）');
    bindLogout();
  }

  function pushCloud(data) {
    if (!synced || !uid) return;
    var patch = {};
    patch[course.module] = data;
    db.collection('progress').doc(uid).set(patch, { merge: true })['catch'](function () {});
  }

  auth.onAuthStateChanged(function (user) {
    if (!user) { showLoggedOut(); return; }
    /* 白名單＝Firestore 裡一份 email 清單；文件存在才算在名單上 */
    db.collection('whitelist').doc(user.email).get().then(function (snap) {
      if (!snap.exists) { showUnauthorized(); return; }
      uid = user.uid;
      return db.collection('progress').doc(uid).get().then(function (p) {
        var cloud = (p.exists && p.data()[course.module]) || {};
        var merged = NotesSync.merge(course.loadDone(), cloud);
        course.saveDone(merged);   // 寫回本機（此刻 synced 還是 false，事件不會重複推雲端）
        course.refreshTicks();
        showSynced(user);          // 從這裡開始，之後的每次作答才會推雲端
        pushCloud(merged);         // 合併結果推上雲端一次
      });
    })['catch'](function () { showUnauthorized(); });
  });

  /* 之後每次對答案，course.js 存檔時會發這個事件 */
  document.addEventListener('notes:progress-saved', function (e) {
    if (e.detail && e.detail.module === course.module) pushCloud(e.detail.data);
  });
})();
```

- [ ] **步驟 4：跑測試確認通過**

```bash
python3 -m unittest discover -s builder/tests -v
node builder/tests/test_merge.js
```

預期：全綠；node 印出「merge 規則測試全部通過」。

- [ ] **步驟 5：commit**

```bash
git add builder/templates/sync.js builder/tests/test_merge.js builder/tests/test_sync.py
git commit -m "feat: sync.js——合併規則純函式、Google 登入、三狀態提示、Firestore 讀寫"
```

---

### 任務 3：builder 條件式注入 Firebase

**Files:**
- Modify: `builder/build.py`（`load_templates`、`load_site`、`render_module_page`、`build` 四處）
- Modify: `builder/templates/module.html`（`</body>` 前加 `__SYNC__`）
- Modify: `builder/tests/test_build.py`（加開／關兩情境的測試）

**Interfaces:**
- Consumes: `content/firebase.json`（可以不存在；格式見「介面」節）、任務 2 的 `builder/templates/sync.js`
- Produces: 設定存在時，模組頁在 `course.js` 之後依序載入：`FIREBASE_CONFIG` 宣告、三支 compat SDK、`../sync.js`；且 `dist/sync.js` 被寫出。設定不存在時以上全部沒有。首頁永遠不載 Firebase。

- [ ] **步驟 1：寫失敗的測試**

在 `builder/tests/test_build.py` 檔頭的 import 區確認有 `json, shutil, tempfile`（缺的補上），然後在 `TestBuild` 類別**外**加一個輔助函式與新測試類別：

```python
def build_variant(firebase_cfg):
    """複製 content/ 到暫存區，依參數放或拿掉 firebase.json，建置後回傳 dist 路徑。"""
    tmp = Path(tempfile.mkdtemp())
    content = tmp / 'content'
    shutil.copytree(ROOT / 'content', content)
    fb = content / 'firebase.json'
    if firebase_cfg is None:
        if fb.exists():
            fb.unlink()
    else:
        fb.write_text(json.dumps(firebase_cfg), encoding='utf-8')
    out = tmp / 'dist'
    builder.build(content_dir=content, out_dir=out)
    return out


class TestFirebaseInjection(unittest.TestCase):
    CFG = {'apiKey': 'test-key', 'authDomain': 'test.firebaseapp.com', 'projectId': 'test'}

    def test_off_without_config(self):
        out = build_variant(None)
        html = (out / 'k8s' / 'index.html').read_text(encoding='utf-8')
        self.assertNotIn('firebasejs', html)
        self.assertNotIn('FIREBASE_CONFIG', html)
        self.assertNotIn('sync.js', html)
        self.assertFalse((out / 'sync.js').exists())

    def test_on_with_config(self):
        out = build_variant(self.CFG)
        for mid in ('k8s', 'redis'):
            html = (out / mid / 'index.html').read_text(encoding='utf-8')
            self.assertIn('var FIREBASE_CONFIG=', html, mid)
            self.assertIn('"apiKey": "test-key"', html, mid)
            for part in ('firebase-app-compat.js', 'firebase-auth-compat.js',
                         'firebase-firestore-compat.js'):
                self.assertIn('https://www.gstatic.com/firebasejs/10.14.1/' + part, html, mid)
            self.assertIn('<script src="../sync.js"></script>', html, mid)
            # 順序：course.js 要先於 sync.js（sync.js 依賴 NotesCourse）
            self.assertLess(html.index('course.js'), html.index('sync.js'), mid)
        self.assertTrue((out / 'sync.js').exists())
        home = (out / 'index.html').read_text(encoding='utf-8')
        self.assertNotIn('firebasejs', home)

    def test_placeholder_never_leaks(self):
        for out in (build_variant(None), build_variant(self.CFG)):
            for page in out.rglob('*.html'):
                self.assertNotIn('__SYNC__', page.read_text(encoding='utf-8'), str(page))
```

（`test_on_with_config` 裡那行 `assertIn('"apiKey": "test-key"' …)`：實際斷言以 build.py 產出的 `json.dumps` 格式為準——`json.dumps` 預設分隔符是 `", "` 與 `": "`，所以嵌出來是 `{"apiKey": "test-key", …}`。照這個格式寫斷言即可，不要多想。）

- [ ] **步驟 2：跑測試，確認新測試失敗**

```bash
python3 -m unittest discover -s builder/tests -v
```

預期：`TestFirebaseInjection` 三個 FAIL（`__SYNC__` 還不存在、注入邏輯還沒寫），其餘全綠。

- [ ] **步驟 3：改 `builder/templates/module.html`**

結尾從：

```html
<script>__DATA__</script>
<script src="../course.js"></script>
</body>
</html>
```

改成：

```html
<script>__DATA__</script>
<script src="../course.js"></script>
__SYNC__
</body>
</html>
```

- [ ] **步驟 4：改 `builder/build.py` 四處**

`load_templates` 的檔名清單加入 `'sync.js'`：

```python
    names = ('style.css', 'course.js', 'sync.js', 'module.html', 'home.html')
```

`load_site` 在 `return` 前加（讀選配的設定檔）：

```python
    fb = content_dir / 'firebase.json'
    site['firebase'] = json.loads(fb.read_text(encoding='utf-8')) if fb.exists() else None
```

`render_module_page` 簽名加一個參數並組同步區塊——整個函式改成：

```python
def render_module_page(mod, mods, tpl, firebase=None):
    quiz = {L['slug']: L['quiz'] for L in mod['lessons']}
    slugs = [L['slug'] for L in mod['lessons']]
    data = ('var MODULE=%s;\nvar QUIZ=%s;\nvar SLUGS=%s;'
            % (json.dumps(mod['id']), json.dumps(quiz, ensure_ascii=False),
               json.dumps(slugs, ensure_ascii=False)))
    data = data.replace('</', '<\\/')   # 防護：測驗文字若含 </ 之類的字，不會提前把嵌入的 <script> 截斷
    if firebase:
        sdk = 'https://www.gstatic.com/firebasejs/10.14.1/firebase-%s-compat.js'
        sync = ('<script>var FIREBASE_CONFIG=%s;</script>\n' % json.dumps(firebase)
                + ''.join('<script src="%s"></script>\n' % (sdk % part)
                          for part in ('app', 'auth', 'firestore'))
                + '<script src="../sync.js"></script>')
    else:
        sync = ''
    arts = [overview_html(mod)] + [article_html(mod, i, L) for i, L in enumerate(mod['lessons'])]
    page = tpl['module.html']
    for key, val in (('__TITLE__', mod['title']), ('__MODSEL__', modsel_html(mods, mod['id'])),
                     ('__SIDEBAR__', sidebar_html(mod)), ('__ARTICLES__', ''.join(arts)),
                     ('__DATA__', data), ('__SYNC__', sync)):
        page = page.replace(key, val)
    return page
```

`build` 裡兩處：寫檔區在 `course.js` 那行之後加

```python
    if site['firebase']:
        (out_dir / 'sync.js').write_text(tpl['sync.js'], encoding='utf-8')
```

呼叫 `render_module_page` 的那行改成

```python
        (d / 'index.html').write_text(render_module_page(mod, mods, tpl, site['firebase']),
                                      encoding='utf-8')
```

- [ ] **步驟 5：跑測試確認通過**

```bash
python3 -m unittest discover -s builder/tests -v
```

預期：全綠（此刻 repo 裡沒有 `content/firebase.json`，正式建置走「關」的路徑，行為與第一期相同）。

- [ ] **步驟 6：commit**

```bash
git add builder/
git commit -m "feat: builder 依 content/firebase.json 有無，條件式注入 Firebase 與 sync.js"
```

---

### 任務 4：資料庫規則檔＋Tim 的一次性設定手冊

**Files:**
- Create: `firebase/firestore.rules`
- Create: `docs/firebase-setup.md`

**Interfaces:**
- Consumes: 「介面」節的 Firestore 資料佈局（`whitelist/{email}`、`progress/{uid}`）
- Produces: Tim 可以照著做完的手冊；規則檔的內容是手冊第 6 步要貼的東西

- [ ] **步驟 1：建 `firebase/firestore.rules`**

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    // 白名單：只能查「自己的 email 在不在名單上」；增刪改一律拒絕
    //（Tim 從 Firebase 管理網頁增刪名單——管理網頁不受這些規則限制）
    match /whitelist/{email} {
      allow get: if request.auth != null && request.auth.token.email == email;
      allow list, create, update, delete: if false;
    }

    // 進度：名單上的人只能讀寫自己的那一份
    match /progress/{uid} {
      allow read, write: if request.auth != null
        && request.auth.uid == uid
        && exists(/databases/$(database)/documents/whitelist/$(request.auth.token.email));
    }

    // 其他一律拒絕（沒寫 match 的路徑預設就是拒絕）
  }
}
```

- [ ] **步驟 2：建 `docs/firebase-setup.md`**

```markdown
# Firebase 一次性設定（第二期：進度跨裝置同步）

用**個人** Google 帳號做，全程免費方案（Spark），大約 10 分鐘。做完把第 2 步抄下的三個值交給 Claude Code（或自己填進 `content/firebase.json`）並 push，同步功能就上線。

## 1. 開專案

1. 開 https://console.firebase.google.com （用個人 Google 帳號登入）
2. 「建立專案」→ 名稱取 `notes-platform`（叫什麼都行）
3. Google Analytics 問你要不要開——**不用開**
4. 等它建好

## 2. 註冊網頁應用程式、抄設定值

1. 專案總覽頁 → 「將 Firebase 加入您的應用程式」選 **Web**（`</>` 圖示）
2. 暱稱隨意（例如 `notes`），**不要**勾 Firebase Hosting
3. 註冊後畫面會顯示一段 `firebaseConfig`，把其中三個值抄下來：
   - `apiKey`
   - `authDomain`（長得像 `notes-platform-xxxx.firebaseapp.com`）
   - `projectId`
4. 這三個值是公開識別碼，放進公開 repo 沒關係——安全靠的是第 6 步的資料庫規則，不是藏設定。

## 3. 開 Google 登入

1. 左側選單 → 建構 → **Authentication** → 「開始使用」
2. 「Sign-in method」分頁 → **Google** → 啟用 → 「專案支援電子郵件」選自己 → 儲存

## 4. 授權網域

1. Authentication → **Settings** → 「Authorized domains」
2. 確認清單裡有 `hhtim.github.io`；沒有就「Add domain」加進去
（少這步的症狀：網站上按登入，跳出視窗馬上關掉並報錯。）

## 5. 開 Firestore 資料庫

1. 左側選單 → 建構 → **Firestore Database** → 「建立資料庫」
2. 選**正式版模式**（production mode；規則等下第 6 步會換掉）
3. 位置選 `asia-east1`（台灣）→ 建立

## 6. 貼資料庫規則

1. Firestore → 「規則」分頁
2. 把編輯器裡的內容**全部**換成 repo 裡 `firebase/firestore.rules` 的內容
3. 「發佈」
（三條規則的意思：名單只有你能改；名單上的人只能讀寫自己的進度；其他一律拒絕。）

## 7. 建白名單、把自己加進去

1. Firestore → 「資料」分頁 → 「開始集合」
2. 集合 ID 填 `whitelist`
3. 文件 ID 填**你要用來登入的那個 Google 帳號的 email**（例如 `clown0715@gmail.com`）——大小寫照 Google 帳號的原樣，通常全小寫
4. 隨便加一個欄位（例如欄位 `note`、類型字串、值 `我自己`）→ 儲存
（之後要讓別的帳號同步，就在這個集合再加一份文件，文件 ID 是那個 email；移掉就刪文件。）

## 8. 把設定值接上網站

1. 把第 2 步的三個值填進 `content/firebase.json`：
   `{"apiKey": "…", "authDomain": "…", "projectId": "…"}`
2. push 到 main，等自動部署跑完
3. 手機開 https://hhtim.github.io/notes-platform/k8s/ → 側邊欄最下面出現
   「進度只存在這台裝置 · 登入後跨裝置同步」→ 點登入 → 選帳號
4. 登入後那行變成「已同步（你的名字）」，之前在別台裝置打的勾應該都在

## 出狀況時看哪裡

| 症狀 | 多半是 |
|---|---|
| 按登入，視窗跳出又立刻消失並報錯 | 第 4 步授權網域沒加 |
| 登入成功但顯示「此帳號未獲授權」 | 第 7 步白名單文件 ID 跟登入帳號的 email 不一致 |
| 顯示已同步但兩台裝置對不上 | 兩台是不是登了不同帳號；或其中一台還開著舊分頁，重新整理 |
```

- [ ] **步驟 3：確認全部測試仍綠**

```bash
python3 -m unittest discover -s builder/tests -v
```

- [ ] **步驟 4：commit**

```bash
git add firebase/ docs/firebase-setup.md
git commit -m "docs: Firestore 資料庫規則與 Firebase 一次性設定手冊"
```

---

### 任務 5：接上真專案、部署、驗收（與 Tim 協作）

**Files:**
- Create: `content/firebase.json`（值來自 Tim）
- Modify: `CLAUDE.md`（現況更新）

**Interfaces:**
- Consumes: 任務 4 的手冊與規則檔；Tim 完成手冊第 1〜7 步後給的三個設定值
- Produces: 線上網站的同步功能；規格第 9 節第二期驗收：「公司電腦勾兩課，手機登入看得到」

- [ ] **步驟 1：等 Tim 照 `docs/firebase-setup.md` 做完第 1〜7 步，拿到三個設定值**（這步是 Tim 的，不能替他做——會用到他的個人 Google 帳號）

- [ ] **步驟 2：把設定值寫進 `content/firebase.json`**（格式見「介面」節），跑

```bash
python3 -m unittest discover -s builder/tests -v
python3 builder/build.py && node --check dist/sync.js
```

預期：全綠（此刻正式建置走「開」的路徑）。

- [ ] **步驟 3：本機無頭瀏覽器檢查「沒登入」狀態**

開 `dist/k8s/index.html`：側邊欄底部顯示「已完成 n / 13 課」＋「進度只存在這台裝置 · 登入後跨裝置同步」；作答、打勾、重新整理保留——行為與第一期一致。（真的登入要 Google 帳號互動，無頭瀏覽器做不了，留給步驟 5 的真人實測。）

- [ ] **步驟 4：commit＋push，等自動部署**

```bash
git add content/firebase.json
git commit -m "feat: 接上 Firebase 專案設定，進度同步上線"
git push
```

- [ ] **步驟 5：Tim 實測驗收（規格的驗收條件）**

1. 公司電腦開線上網站 → 登入 → 勾兩課（做兩課的測驗到全對）
2. 手機開同網址 → 登入同帳號 → 兩個勾都看得到、側欄顯示「已同步（名字）」
3. 加測：手機沒登入時先勾一課，再登入 → 那一課的勾不能不見（聯集，不是覆蓋）
4. 有第二個 Google 帳號的話：用它登入 → 顯示「此帳號未獲授權，進度僅存於本機」，其餘功能照常

- [ ] **步驟 6：驗收通過後更新 `CLAUDE.md` 現況（第二期完成），commit＋push**

---

## 驗收對照（規格第 9 節「第二期」）

| 規格要求 | 由誰證明 |
|---|---|
| Firebase 專案（免費方案） | 任務 5 步驟 1（Tim＋手冊） |
| Google 登入 | 任務 2 sync.js；任務 5 步驟 5 實測 |
| 白名單（Tim 在管理網頁增刪；資料庫規則三條） | 任務 4 規則檔＋手冊第 6、7 步 |
| 合併規則（聯集、成績取較好、絕不覆蓋） | 任務 2 `test_merge.js`；任務 5 步驟 5 第 3 項實測 |
| 三狀態提示（固定位置、不跳視窗） | 任務 1、2；任務 5 步驟 3、5 |
| 沒登入一切照舊 | 任務 3 `test_off_without_config`；任務 5 步驟 3 |
| 驗收：公司電腦勾兩課，手機登入看得到 | 任務 5 步驟 5 |

## 刻意的取捨（不要當成 bug）

1. **首頁不載 Firebase**：首頁卡片的完成度照舊讀瀏覽器本機資料。登入合併發生在模組頁；一進模組頁合併結果就寫回本機，首頁自然跟上。首頁保持零外部程式。
2. **「登出」連結是規格文字之外的追加**：登錯帳號需要退路。
3. **登入用跳出視窗（popup）**：另一種轉址式登入在現在的手機瀏覽器上有第三方儲存限制的問題，跳出視窗反而穩。
4. **不用 Firebase 模擬器測資料庫規則**：要多裝一整套工具（Node 專案＋Java），個人站不值得；規則三條很短，靠任務 5 步驟 5 的真人實測（含未授權帳號那項）覆蓋。
5. **雲端寫入失敗不吵使用者**：`catch` 後靜默——本機一定有存，下次成功登入會再合併推上去；個人站不做重試佇列。
