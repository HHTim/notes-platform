# 第一期：救檔＋平台上線 實作計畫

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**目標：** 把 `rescue/` 裡救回的 K8s 課程站（13 課）與 Redis 鎖頁面拆成 `content/` 格式、每課測驗補到至少 5 題、做出 `builder/` 建置工具與平台首頁，接 GitHub Actions＋GitHub Pages 上線。

**做法：** 內容與外觀分開——`content/` 只放不含樣式的內容檔，版型、配色、測驗互動集中在 `builder/templates/`。`builder/build.py`（Python 3 標準庫）整站重建輸出到 `dist/`；push 到 `main` 即發佈。

**技術：** Python 3 標準庫（json、re、pathlib、shutil、unittest），無框架、無第三方套件。前端是純 HTML＋CSS＋原生 JavaScript。

**規格：** `docs/superpowers/specs/2026-09-04-notes-platform-design.md`（本計畫實作其第 9 節「第一期」）

## 全域限制（每個任務都適用）

- **不用任何框架與第三方套件**：builder 只用 Python 3 標準庫；網頁只用原生 JavaScript。
- **色系定稿**：奶油底 `#F7F0E3`、白卡片 `#FFFFFF`、古銅 `#B5730F`、灰藍 `#5E7A9B`。**不做深色模式。**
- **`dist/` 不進 git**；每次建置整站從頭重建，不做「只重建有改的頁」。
- **測驗**：每課 5〜10 題；`quiz.json` 裡每題的 `opts[0]` 是正確答案，選項順序由前端隨機打亂。
- **來源註記**：每個 `lesson.html` 第一行是 HTML 註解，記來源與收錄日期。
- **內容檔不含樣式**：`lesson.html` 裡不准出現 `<style>`；可以用 CSS 類別（類別的定義都在 `builder/templates/style.css`）。
- **公司內容不上站**：建好的頁面裡不准出現「KPI」「kpi-platform」字樣（Tim 已拍板：Redis 頁最後一段改寫成一般化例子）。
- **Git**：遠端維持 SSH 別名 `git@github-hhtim:HHTim/notes-platform.git` 不要動；commit 身分用 repo 內已設好的 `HHTim <clown0715@gmail.com>`；直接在 `main` 上做。
- **寫給人看的文字**照 Tim 的用詞規則（台灣講法、不發明編號代號、不造字；名詞第一次出現附一句白話）。
- `rescue/` **在 Tim 驗收整期之前不准刪**——它是遷移的輸入，也是一致性比對的基準。

## 檔案結構總覽

```
notes-platform/
├── .gitignore                         （任務 1 建）dist/、__pycache__/
├── content/
│   ├── modules.json                   （任務 1 建，任務 2 加 redis）模組總表：順序、圖示、站名
│   ├── k8s/
│   │   ├── module.json                （任務 1 建）模組名稱、簡介、13 課的順序與中繼資料
│   │   ├── 01-physical/lesson.html    每課一個資料夾：內文＋測驗
│   │   ├── 01-physical/quiz.json
│   │   └── …（02-vm … 13-when，共 13 個資料夾）
│   └── redis/
│       ├── module.json                （任務 2 建）
│       └── 01-distributed-lock/lesson.html、quiz.json
├── builder/
│   ├── build.py                       （任務 4 建）讀 content/ 全部，組出整站到 dist/
│   ├── templates/
│   │   ├── style.css                  （任務 4 建，任務 6 加首頁樣式）全站版面與配色
│   │   ├── course.js                  （任務 4 建）測驗互動、路由、進度
│   │   ├── module.html                （任務 4 建）模組頁骨架
│   │   └── home.html                  （任務 6 建）平台首頁骨架
│   └── tests/
│       ├── test_content.py            （任務 1 建，任務 2、3 擴充）內容檔的格式檢查
│       ├── test_build.py              （任務 4 建，任務 6 擴充）建置結果檢查
│       └── test_parity.py             （任務 5 建）新舊 K8s 頁面內容一致性比對
├── rescue/
│   ├── migrate_k8s.py                 （任務 1 建）一次性遷移腳本，跟 rescue/ 一起最後刪
│   └── migrate_redis.py               （任務 2 建）同上
└── .github/workflows/deploy.yml       （任務 8 建）
```

**責任分工**：`content/` 是唯一要長期維護的內容；`builder/` 是唯一要長期維護的程式；`rescue/migrate_*.py` 是一次性工具，產出被 commit 之後它們的任務就結束（但檔案留著直到 Tim 驗收）。

## 資料格式（所有任務共用的介面）

`content/modules.json`：

```json
{
 "site_title": "Tim 的筆記平台",
 "site_intro": "多個學習模組，每個模組是一個課程站：側邊欄選課、課末隨堂測驗、全對打勾。",
 "modules": [
  {"id": "k8s", "icon": "📦"},
  {"id": "redis", "icon": "🔐"}
 ]
}
```

`content/<模組>/module.json`（模組自己的名稱與課表；`group` 是側邊欄的分組標題，值一樣的課排在同一組下）：

```json
{
 "title": "從一台機器到一堆貨櫃",
 "intro": "卡片上的一句話簡介",
 "kick": "總覽頁大標上面那行小字",
 "overview_intro": "總覽頁的開場段落",
 "footer_note": "總覽頁最底下的小字",
 "lessons": [
  {"dir": "01-physical", "slug": "physical", "title": "一台機器一個服務",
   "desc": "一句話描述", "mins": 7, "group": "歷史：為什麼會有容器"}
 ]
}
```

`content/<模組>/<課>/lesson.html`：第一行來源註解，接著「讀完這課你會」框、內文 `<section>` 們、「重點整理」框——**不含**課名、麵包屑、測驗、上下課連結（那些由 builder 從 module.json 組出來）：

```html
<!-- 來源：rescue/vm-container-k8s.html（舊對話救回的教材原稿）· 收錄日期：2026-09-04 -->
<div class="learn"><p class="lbl">讀完這課你會</p><ul><li>…</li></ul></div>
<section>…</section>
<div class="keys"><p class="lbl">重點整理</p><ul><li>…</li></ul></div>
```

`content/<模組>/<課>/quiz.json`（**`opts[0]` 一定是正確答案**，前端負責打亂順序）：

```json
{"questions": [{"q": "題目", "opts": ["正確答案", "誘答 1", "誘答 2", "誘答 3"], "exp": "解析"}]}
```

進度存瀏覽器 localStorage，一個模組一把鑰匙：鑰匙名 `notes-progress:<模組 id>`，值是 `{"<課 slug>": {"best": 3, "total": 5, "done": false}}`——`best` 是歷來最高答對題數、`done` 是有沒有全對過。（這個形狀是為第二期的雲端合併規則準備的：勾過就算勾過、成績取較好那次。）

---

### 任務 1：K8s 內容遷移（rescue → content/k8s/，13 課）

**Files:**
- Create: `.gitignore`
- Create: `rescue/migrate_k8s.py`
- Create: `builder/tests/test_content.py`
- Create（腳本產出）: `content/modules.json`、`content/k8s/module.json`、`content/k8s/01-physical/`〜`13-when/` 各含 `lesson.html`＋`quiz.json`

**Interfaces:**
- Consumes: `rescue/vm-container-k8s.html`（21 個 `<section>`）、`rescue/build_spa.py` 裡的 `LESSONS`、`QUIZ`、`CH5_BODY`、換色與修字邏輯
- Produces: 上節「資料格式」定義的 content 檔——後續所有任務都吃這個格式

- [ ] **步驟 1：建 `.gitignore`**

```
dist/
__pycache__/
.DS_Store
```

- [ ] **步驟 2：寫內容格式檢查（先寫、先看它失敗）**

建 `builder/tests/test_content.py`：

```python
# -*- coding: utf-8 -*-
# content/ 的格式檢查：檔案齊全、來源註記、不含樣式、換色乾淨、測驗格式
import json, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / 'content'


def load_modules():
    site = json.loads((CONTENT / 'modules.json').read_text(encoding='utf-8'))
    mods = []
    for entry in site['modules']:
        mod = json.loads((CONTENT / entry['id'] / 'module.json').read_text(encoding='utf-8'))
        mod['id'] = entry['id']
        mods.append(mod)
    return site, mods


class TestContent(unittest.TestCase):
    def test_modules_json(self):
        site, mods = load_modules()
        self.assertTrue(site['site_title'])
        for mod in mods:
            for key in ('title', 'intro', 'kick', 'overview_intro', 'footer_note', 'lessons'):
                self.assertIn(key, mod, mod['id'])

    def test_lesson_files(self):
        _, mods = load_modules()
        for mod in mods:
            for L in mod['lessons']:
                ldir = CONTENT / mod['id'] / L['dir']
                html = (ldir / 'lesson.html').read_text(encoding='utf-8')
                with self.subTest(lesson=str(ldir)):
                    self.assertTrue(html.startswith('<!-- 來源：'), '第一行要是來源註解')
                    self.assertNotIn('<style', html, '內容檔不准帶樣式')
                    for old in ('var(--teal', 'var(--amber', 'var(--brass'):
                        self.assertNotIn(old, html, '換色沒換乾淨：' + old)
                    self.assertIn('class="learn"', html)
                    self.assertIn('class="keys"', html)
                    self.assertTrue((ldir / 'quiz.json').exists())

    def test_quiz_format(self):
        _, mods = load_modules()
        for mod in mods:
            for L in mod['lessons']:
                qf = CONTENT / mod['id'] / L['dir'] / 'quiz.json'
                qs = json.loads(qf.read_text(encoding='utf-8'))['questions']
                with self.subTest(lesson=str(qf)):
                    # 任務 3 補完題後把下限改成 5（規格：每課 5〜10 題）
                    self.assertTrue(3 <= len(qs) <= 10, '目前 %d 題' % len(qs))
                    for q in qs:
                        self.assertTrue(q['q'].strip())
                        self.assertTrue(q['exp'].strip())
                        self.assertGreaterEqual(len(q['opts']), 3)
                        self.assertTrue(all(o.strip() for o in q['opts']))

    def test_k8s_migration_details(self):
        _, mods = load_modules()
        k8s = [m for m in mods if m['id'] == 'k8s'][0]
        self.assertEqual(len(k8s['lessons']), 13)
        read = lambda d: (CONTENT / 'k8s' / d / 'lesson.html').read_text(encoding='utf-8')
        # 修字有帶到、圖有搬對位子（對應 rescue/build_spa.py 的加工）
        self.assertIn('第 9 課要講的 Service 背後的執行者', read('07-cluster-brain'))
        self.assertIn('（v1.24，2022 年）', read('06-pod-node'))
        self.assertIn('Gateway API', read('10-ingress'))
        self.assertIn('Kubernetes 的核心迴圈', read('05-why-k8s'))
        self.assertNotIn('Kubernetes 的核心迴圈', read('08-deployment'))
        self.assertIn('ReplicaSet', read('08-deployment'))


if __name__ == '__main__':
    unittest.main()
```

- [ ] **步驟 3：跑測試，確認失敗**

```bash
python3 -m unittest discover -s builder/tests -v
```

預期：FAIL／ERROR（`content/modules.json` 還不存在）。

- [ ] **步驟 4：寫遷移腳本 `rescue/migrate_k8s.py`**

腳本的前半段**逐字照抄** `rescue/build_spa.py`：
- 讀檔＋切 21 個 section、抽「核心迴圈」那張圖（`build_spa.py` 開頭到 `assert m` 那段）
- `recolor()` 換色與五處內文修字（`# ---- 內文修字 ----` 那整段）
- `CH5_BODY`（第 5 課的自製內文）
- `LESSONS` 清單、`QUIZ` 字典（兩大段資料，原樣照抄）

後半段換成寫檔（取代原本組 HTML 的部分）：

```python
GROUPS = {0: '歷史：為什麼會有容器', 3: 'DOCKER：一台機器上的事',
          4: 'K8S：由小到大', 12: '判斷'}
HEADER = '<!-- 來源：rescue/vm-container-k8s.html（舊對話救回的教材原稿）· 收錄日期：2026-09-04 -->'

def box(cls, label, items):
    return ('<div class="%s"><p class="lbl">%s</p><ul>%s</ul></div>'
            % (cls, label, ''.join('<li>%s</li>' % x for x in items)))

group = ''
lessons_meta = []
for i, L in enumerate(LESSONS):
    if i in GROUPS:
        group = GROUPS[i]
    dirname = '%02d-%s' % (i + 1, L['slug'])
    d = ROOT / 'content' / 'k8s' / dirname
    d.mkdir(parents=True, exist_ok=True)
    body = [CH5_BODY] if L['slug'] == 'why-k8s' else []
    body += [secs[si] for si in L['body']]
    parts = [HEADER, box('learn', '讀完這課你會', L['learn'])] + body + [box('keys', '重點整理', L['keys'])]
    (d / 'lesson.html').write_text('\n'.join(parts) + '\n', encoding='utf-8')
    (d / 'quiz.json').write_text(
        json.dumps({'questions': QUIZ[L['slug']]}, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    lessons_meta.append(dict(dir=dirname, slug=L['slug'], title=L['title'],
                             desc=L['desc'], mins=L['mins'], group=group))

module = dict(
    title='從一台機器到一堆貨櫃',
    intro='從實體機、虛擬機、容器一路講到 Kubernetes：每一代解決了上一代的什麼痛。',
    kick='實體機 → 虛擬機 → 容器 → KUBERNETES',
    overview_intro=('一份從零開始的教材，共 13 課，照學習順序排列：先懂歷史（每一代解決了上一代的什麼痛），'
                    '再把 Kubernetes 由小到大一層層拆開。每課末有隨堂測驗，全對就在側邊欄打勾。'),
    footer_note='圖裡的時間與數量（40 秒、110 個、2–10 GB）都是預設值或常見量級，不是硬規定。',
    lessons=lessons_meta)
(ROOT / 'content' / 'k8s' / 'module.json').write_text(
    json.dumps(module, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')

site = {'site_title': 'Tim 的筆記平台',
        'site_intro': '多個學習模組，每個模組是一個課程站：側邊欄選課、課末隨堂測驗、全對打勾。',
        'modules': [{'id': 'k8s', 'icon': '📦'}]}
(ROOT / 'content' / 'modules.json').write_text(
    json.dumps(site, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('content/k8s/ 完成，共', len(LESSONS), '課')
```

檔頭補上（原腳本用相對路徑讀檔，改成不依賴執行位置）：

```python
import json, re
from pathlib import Path
HERE = Path(__file__).resolve().parent   # rescue/
ROOT = HERE.parent
s = (HERE / 'vm-container-k8s.html').read_text(encoding='utf-8')
```

注意兩點：原腳本的 `overview_intro` 寫「每課末有 3 題隨堂測驗」，這裡改成不寫死題數（上面已改好）；`GROUPS` 的第一組在原腳本是寫死在 HTML 裡的「歷史：為什麼會有容器」，別漏。

- [ ] **步驟 5：跑遷移，跑測試確認通過**

```bash
python3 rescue/migrate_k8s.py
python3 -m unittest discover -s builder/tests -v
```

預期：全部 PASS。另外肉眼抽查 `content/k8s/05-why-k8s/lesson.html`（要有核心迴圈那張 SVG）和 `01-physical/lesson.html`（第一行是來源註解）。

- [ ] **步驟 6：commit**

```bash
git add .gitignore rescue/migrate_k8s.py builder/tests/test_content.py content/
git commit -m "feat: K8s 課程站拆成 content/ 格式（13 課，含遷移腳本與格式檢查）"
```

---

### 任務 2：Redis 內容遷移（剝殼、換暖色、公司段落改寫、新寫 8 題測驗）

**Files:**
- Create: `rescue/migrate_redis.py`
- Modify: `content/modules.json`（腳本加上 redis 那筆）
- Create（腳本產出）: `content/redis/module.json`、`content/redis/01-distributed-lock/lesson.html`、`quiz.json`

**Interfaces:**
- Consumes: `rescue/distributed-lock-redis.artifact.html`（`<title>` 之後才是本體；9 個 `<section>`；收尾有一個 `takeaway` 框）
- Produces: 與任務 1 相同格式的 content 檔。內文用到的類別 `card`、`badge`、`pit`、`pits`、`grid2`、`good` 由任務 4 的 `style.css` 提供

**遷移規則（Tim 已拍板的與既定慣例）：**
1. 剝殼：從 `<title>` 開始取，前面是 artifact 發佈系統的程式碼，丟掉。
2. 換色：內文與 SVG 裡的 `var(--brass)` 全部換成 `var(--gold)`（暖色系裡對應的古銅色）；`var(--danger)`、`var(--ok)` 名字相同，不用動。
3. 對齊全站段落樣式：`class="tag"` 換成 `class="era"`；`<h2>` 換成 `<h3 class="head">`。
4. 第 9 個 section（「KPI 平台用 Redis 做什麼」）**整段換成下面的一般化版本**（Tim 拍板：不提公司，保留教學價值）。
5. 頁尾 `takeaway` 框的五句話變成這課的「重點整理」；hero 區的文案進 `module.json`。

- [ ] **步驟 1：擴充內容檢查（先寫、先看它失敗）**

在 `builder/tests/test_content.py` 的 `TestContent` 里加：

```python
    def test_redis_module(self):
        site, mods = load_modules()
        self.assertIn('redis', [m['id'] for m in mods])
        redis = [m for m in mods if m['id'] == 'redis'][0]
        self.assertEqual(len(redis['lessons']), 1)
        html = (CONTENT / 'redis' / redis['lessons'][0]['dir'] / 'lesson.html').read_text(encoding='utf-8')
        self.assertNotIn('KPI', html, '公司內容不上站')
        self.assertNotIn('CLAUDE.md', html)
        self.assertNotIn('class="tag"', html, '段落標籤要換成全站的 era')
        self.assertNotIn('<h2', html, '段落標題要換成全站的 h3.head')
        self.assertEqual(html.count('<section'), 9)
        self.assertIn('SET', html)          # 指令那段還在
        self.assertIn('fencing token', html)  # 遞增編號那段還在
```

跑 `python3 -m unittest discover -s builder/tests -v`，預期新測試 FAIL（redis 還不存在）。

- [ ] **步驟 2：寫 `rescue/migrate_redis.py`**

```python
# -*- coding: utf-8 -*-
# 把 rescue/distributed-lock-redis.artifact.html 剝殼、換暖色，寫成 content/redis/
import json, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / 'content' / 'redis' / '01-distributed-lock'

s = (HERE / 'distributed-lock-redis.artifact.html').read_text(encoding='utf-8')
body = s[s.find('<title>'):]                       # 剝掉 artifact 發佈系統的外殼
secs = re.findall(r'<section[^>]*>.*?</section>', body, re.S)
assert len(secs) == 9, len(secs)

# 第 9 段：公司內容改寫成一般化例子（Tim 拍板）
secs[8] = '''<section>
    <p class="era">回到現實</p>
    <h3 class="head">放登入資訊沒問題，想當鎖要三思</h3>
    <p>一個常見的用法：把登入者的身份與權限暫存在 Redis（雲端上就是 GCP 的 Memorystore、AWS 的 ElastiCache 這類託管服務）。<strong>這個用途沒有上面的問題</strong>——換主機時真的掉了幾筆，使用者頂多重新登入一次。</p>
    <p>要留意的是<strong>哪天想拿 Redis 來當鎖</strong>的時候，例如「同一份文件不要被兩個人同時送出審核」。那種情境屬於上面的「不能重複」，建議先看資料庫的唯一索引擋不擋得住，擋得住就不用架鎖。</p>
  </section>'''

def warm(h):
    h = h.replace('var(--brass)', 'var(--gold)')
    h = h.replace('class="tag"', 'class="era"')
    h = re.sub(r'<h2(\s[^>]*)?>', '<h3 class="head">', h)
    h = h.replace('</h2>', '</h3>')
    return h

secs = [warm(x) for x in secs]

LEARN = ['說出鎖搬到多台機器後為什麼失效、分散式鎖怎麼補救',
         '看懂 SET … NX EX 這行指令，講出用 Redis 當鎖的三個坑',
         '分清四種擺法差在哪，以及為什麼哨兵和叢集也救不了鎖']
KEYS = ['機器變多，各自記憶體裡的鎖就互相看不到，等於沒鎖。',
        '分散式鎖就是把鎖搬到一個大家都看得到的地方，Redis 是常見選擇。',
        'Redis 四種擺法差在「裝得下多少」和「主機掛了誰來救」：單機沒人救、主從要人工救、哨兵自動救、叢集自動救而且裝得更多。',
        '但四種都救不了鎖——因為複製是非同步的，換主機的瞬間鎖會憑空消失。',
        '先問「重複做一次會怎樣」。沒差就用 Redis；不能重複就加遞增編號，或乾脆用資料庫、etcd。']

HEADER = '<!-- 來源：rescue/distributed-lock-redis.artifact.html（舊對話救回的 artifact，已剝殼）· 收錄日期：2026-09-04 -->'

def box(cls, label, items):
    return ('<div class="%s"><p class="lbl">%s</p><ul>%s</ul></div>'
            % (cls, label, ''.join('<li>%s</li>' % x for x in items)))

OUT.mkdir(parents=True, exist_ok=True)
parts = [HEADER, box('learn', '讀完這課你會', LEARN)] + secs + [box('keys', '重點整理', KEYS)]
(OUT / 'lesson.html').write_text('\n'.join(parts) + '\n', encoding='utf-8')

QUIZ = [
 dict(q='鎖在程式裡是為了防止什麼？',
      opts=['同一份資料同一時間被兩個人改——例如同時扣款、扣成一次', '程式碼被別人偷看',
            '伺服器被關機', '資料庫被塞滿'],
      exp='跟廁所門閂一樣：一個人進去、閂上，其他人只能在外面等。'),
 dict(q='程式複製成三台之後，原本的鎖為什麼失效？',
      opts=['鎖是記在各自記憶體裡的旗子，A 台舉的旗子 B 台看不到——三把鎖各鎖各的',
            '三台機器的時鐘不同步', '網路太慢', '記憶體不夠大'],
      exp='每台機器的記憶體互相獨立，等於沒鎖——所以要把鎖搬到大家都看得到的地方。'),
 dict(q='SET 訂單123 我的名字 NX EX 30 這行裡的 NX 是什麼意思？',
      opts=['「這個名字目前沒人用，才寫得進去」——第一個寫進去的人贏，其他人收到失敗',
            '把資料加密', '30 秒後這筆自動消失', '通知其他機器來搶'],
      exp='NX 就是「搶鎖」的關鍵：只有一個人能寫成功。「30 秒後自動消失」是 EX 30 的事。'),
 dict(q='為什麼鎖一定要設過期時間（EX）？',
      opts=['拿到鎖的機器如果當場斷電，鎖會永遠留在那裡，後面全部卡死',
            'Redis 規定不設就不能用', '設了可以加快讀取速度', '為了省記憶體'],
      exp='三個坑的第一個：沒有 EX，一次意外就把整條路堵死。'),
 dict(q='解鎖前為什麼要先確認「鎖上寫的是不是我的名字」，而且確認和刪除要一氣呵成？',
      opts=['我的鎖可能已經過期、換別人拿到了——不確認就刪，刪掉的是別人的鎖；分兩步做，中間可能被插隊',
            'Redis 會拒絕沒署名的刪除', '為了留下操作紀錄', '名字寫錯會被扣款'],
      exp='實務上用 Lua 腳本讓「確認＋刪除」整段在 Redis 裡一起跑，中間不會被插隊。'),
 dict(q='四種擺法裡，哪一種能裝的資料量可以靠加機器一直往上加？',
      opts=['叢集（Cluster）——資料切成 16384 個號碼段，分給好幾組主從各管一段',
            '單機（Standalone）', '主從複製（Master–Replica）', '哨兵（Sentinel）'],
      exp='前三種能裝的都是「一台的量」；哨兵解決的是「掛了誰救」，不是容量。'),
 dict(q='架成哨兵或叢集之後，鎖為什麼還是會破？',
      opts=['主機複製資料給從機是非同步的——鎖剛給出去、還沒複製過去主機就掛了，升上來的新主機根本沒看過那把鎖',
            '設定檔寫錯了才會破，設對就不會', '哨兵會定期清掉所有的鎖', '叢集不支援 SET 指令'],
      exp='這不是設定錯，是這種複製方式本來就這樣——「架成哨兵就安全了」剛好想反了。'),
 dict(q='「絕對不能重複執行」的場景，建議的做法是？',
      opts=['別用 Redis 當鎖——改用 etcd 或 ZooKeeper（寫入要多數節點點頭才算成功），或先看資料庫的唯一索引擋不擋得住',
            '把 Redis 的過期時間設成一年', '多架幾台 Redis 就安全了', '在程式裡多睡一秒再執行'],
      exp='判斷起點是「鎖破了會怎樣」：重做沒差就直接用 Redis；不能重複但想留 Redis 就加遞增編號（fencing token）；絕對不行就換工具或讓資料庫擋。'),
]
(OUT / 'quiz.json').write_text(
    json.dumps({'questions': QUIZ}, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')

module = dict(
    title='分散式鎖與 Redis',
    intro='機器一多，好好的鎖為什麼失效；Redis 四種擺法差在哪、什麼時候別用它當鎖。',
    kick='分散式鎖 / REDIS',
    overview_intro=('「分散式」就是同一套程式同時跑在好幾台機器上。機器一多，原本好好的鎖就失效了。'
                    '這個模組講為什麼，以及 Redis 的四種擺法差在哪。'),
    footer_note='圖裡的號碼段 0–16383 是 Redis 叢集固定的切法；其餘數字（30 秒、幾十秒）是常見的量級，實際依設定而定。',
    lessons=[dict(dir='01-distributed-lock', slug='distributed-lock',
                  title='一把鑰匙，很多台機器在搶',
                  desc='為什麼鎖會破、一行指令怎麼當鎖、三個坑、四種擺法，以及該不該用 Redis 當鎖。',
                  mins=9, group='')])
(ROOT / 'content' / 'redis' / 'module.json').write_text(
    json.dumps(module, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')

# modules.json 加上 redis
mj = ROOT / 'content' / 'modules.json'
site = json.loads(mj.read_text(encoding='utf-8'))
if 'redis' not in [m['id'] for m in site['modules']]:
    site['modules'].append({'id': 'redis', 'icon': '🔐'})
mj.write_text(json.dumps(site, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('content/redis/ 完成')
```

- [ ] **步驟 3：跑遷移，跑測試確認通過**

```bash
python3 rescue/migrate_redis.py
python3 -m unittest discover -s builder/tests -v
```

預期：全部 PASS。肉眼抽查 `content/redis/01-distributed-lock/lesson.html`：最後一個 section 是「放登入資訊沒問題，想當鎖要三思」，整份檔案搜不到「KPI」。

- [ ] **步驟 4：commit**

```bash
git add rescue/migrate_redis.py builder/tests/test_content.py content/
git commit -m "feat: Redis 鎖頁面剝殼遷移成 redis 模組（公司段落改寫成一般化例子，新增 8 題測驗）"
```

---

### 任務 3：K8s 測驗補題（每課 3 題 → 5 題）

**Files:**
- Modify: `content/k8s/01-physical/quiz.json` 〜 `content/k8s/13-when/quiz.json`（各追加 2 題到最後）
- Modify: `builder/tests/test_content.py`（題數下限 3 → 5，並加「原有題目沒被動到」的檢查）

**Interfaces:**
- Consumes: 任務 1 產出的 13 個 `quiz.json`
- Produces: 每課 5 題的 `quiz.json`，格式不變（`opts[0]` 為正確答案）

**規則：只追加、不改動也不刪除原有的 3 題**（驗收條件是「與現行 artifact 內容一致（加補題）」）。

- [ ] **步驟 1：收緊測試（先改、先看它失敗）**

`test_quiz_format` 裡的下限改成 5：

```python
                    self.assertTrue(5 <= len(qs) <= 10, '規格要求每課 5〜10 題，目前 %d 題' % len(qs))
```

並在 `TestContent` 加一條「原題還在原位」的抽查：

```python
    def test_original_questions_untouched(self):
        first_q = {
            '01-physical': '為什麼以前不把兩個服務裝在同一台機器上？',
            '05-why-k8s': 'K8s 的核心運作方式是？',
            '13-when': '該不該從 Docker 轉 K8s，最根本的判斷是？',
        }
        for d, q in first_q.items():
            qs = json.loads((CONTENT / 'k8s' / d / 'quiz.json').read_text(encoding='utf-8'))['questions']
            self.assertEqual(qs[0]['q'], q, d)
```

跑測試，預期 `test_quiz_format` 對 13 個 k8s 課全部 FAIL（都只有 3 題）。

- [ ] **步驟 2：把下面 26 題逐課追加到對應 `quiz.json` 的 `questions` 陣列尾端**

每題照 `{"q": …, "opts": [正確, 誘答, 誘答, 誘答], "exp": …}` 格式。

**01-physical：**
1. q「公司要上線第二個服務，當年的標準做法是？」opts:「再買一台新機器、再等它就位——一台機器一個服務是鐵律」/「把它裝進現有那台閒置的九成效能裡」/「用虛擬機切一台出來」/「租一台雲端主機」exp:「當年還沒有虛擬機也沒有雲端，只能再買再等——切一台出來是下一課才出現的招。」
2. q「服務 A 突然吃光整台機器的記憶體，同一台上的服務 B 會怎樣？」opts:「跟著遭殃——沒有任何隔離手段，B 會被拖垮（陪葬）」/「完全不受影響，作業系統會保護它」/「B 會自動搬去別台機器」/「B 會暫停等 A 用完」exp:「資源互搶沒有裁判，這就是當年寧可一台只跑一個的原因。」

**02-vm：**
1. q「用了虛擬機之後，「開一台新機器」要多久？」opts:「幾分鐘——切一台出來是軟體動作，不用採購、不用進機房」/「還是兩個月，跟以前一樣」/「至少一星期，要重灌系統」/「不可能再開新機」exp:「等待從兩個月變幾分鐘，效能也用得滿——這是虛擬機解決掉的那一半；另一半（環境靠人裝）留給了容器。」
2. q「虛擬機時代，「在我電腦上跑得起來、到測試機就掛」這個問題解決了嗎？」opts:「沒有——機器是好開了，但每台裡面的環境還是靠人裝，裝得不一樣照樣掛」/「解決了，虛擬機的環境全自動一致」/「解決了，因為大家都用同一台虛擬機」/「這個問題當年不存在」exp:「虛擬機給你「幾台機器」，沒管「機器裡裝什麼」。這個痛要等容器把環境一起打包才治好。」

**03-container：**
1. q「容器啟動大約多快？為什麼能這麼快？」opts:「一秒內——不用等一套作業系統開機，因為系統早就在跑了」/「跟虛擬機一樣要一分鐘左右」/「要好幾個小時」/「取決於網路速度」exp:「少背一套 Guest OS：體積從幾 GB 掉到幾十 MB，啟動從分鐘級掉到秒級。」
2. q「「虛擬機隔兩道牆、容器共用一道」這句話在講什麼？」opts:「隔離的徹底程度——容器共用同一套作業系統，那道牆有洞就可能被跨過去」/「機房實體牆壁的厚度」/「防火牆要設定幾層」/「網路速度的差別」exp:「隔離是「牆的厚度」問題：要切得徹底選虛擬機，要輕要快選容器——是取捨，不是誰淘汰誰。」

**04-docker：**
1. q「同一個映像檔可以同時跑幾份容器？」opts:「要幾份有幾份——成品做一次，跑起來的每一份是獨立的容器」/「只能一份，跑第二份要重新 build」/「最多兩份」/「每跑一份都要重寫一次 Dockerfile」exp:「食譜寫一次（build）、成品做一次，run 幾次就有幾個容器——「三百個容器誰管」也是這樣來的。」
2. q「改了程式碼之後，要讓正式機跑到新版本，正確流程是？」opts:「重新 build 一個新映像檔、推上倉庫，正式機拉新的下來跑」/「直接登入正式機，改容器裡面的檔案」/「把 Dockerfile 寄給正式機就會自動更新」/「等容器自己同步最新程式碼」exp:「映像檔是不會再變的成品——要新內容就做新成品。直接改跑起來的那一份，重開就消失了。」

**05-why-k8s：**
1. q「半夜一個容器掛了，K8s 會怎麼處理？」opts:「比對迴圈發現「現況 2 份 ≠ 單子 3 份」，自己補一份回來，不用叫醒任何人」/「發簡訊叫工程師起床重開」/「等到早上上班時間再處理」/「把整台機器重開一遍」exp:「這就是管家的價值：你只寫「要 3 份」，補回去的步驟它自己想。」
2. q「「K8s」這個簡寫是怎麼來的？」opts:「Kubernetes 的 K 和 s 中間剛好有 8 個字母」/「它是第 8 個版本」/「它有 8 個核心元件」/「發明它的團隊有 8 個人」exp:「純粹是縮寫的玩法：K-ubernete-s，中間數一數 8 個字母。」

**06-pod-node：**
1. q「kubelet 存在的理由是什麼？」opts:「當大腦在這台機器上的聯絡窗口——接指令、回報狀況；「啟動容器」本來就是容器執行環境的事」/「負責啟動容器，取代 containerd」/「幫機器掃毒」/「負責畫出管理介面」exp:「沒有 kubelet，這台就只是一台裝了容器執行環境的普通機器，大腦叫不動它。」
2. q「你的 Pod 重開了一次，它會回到原本那台機器上嗎？」opts:「不一定——放哪台是大腦決定的，重開就可能換位子，你不用管也管不著」/「一定回到原機器，位置是固定的」/「規定一定要換一台」/「要自己登入機器把它搬回去」exp:「「Pod 落在哪台不用你管」——也因為位置會變，才需要之後的 Service 來找路。」

**07-cluster-brain：**
1. q「大腦（Control Plane）的四個角色，對應的比喻是？」opts:「櫃檯（kube-apiserver）、檔案室（etcd）、排班的（kube-scheduler）、巡邏的（kube-controller-manager）」/「警衛、廚師、司機、老闆」/「前端、後端、資料庫、快取」/「主機、從機、哨兵、叢集」exp:「交單子找櫃檯、單子存進檔案室、新 Pod 由排班的決定放哪台、巡邏的盯著現況跟單子一不一樣。」
2. q「大腦的四個角色是用什麼形式在跑的？」opts:「各自是一個 Pod，跑在 master node 上」/「燒在硬體晶片裡」/「是四台獨立的實體機器」/「是裝在你電腦上的桌面程式」exp:「大腦自己也用 K8s 的方式跑——所以 master 上也要有 kubelet 和 containerd 那三樣。」

**08-deployment：**
1. q「Deployment 那張單子上會寫哪些事？」opts:「跑哪個映像檔、跑幾份、每份保留多少資源、怎麼換版本」/「程式的原始碼」/「機器的採購清單」/「使用者的帳號密碼」exp:「這張單子管「上線」；「這包裡有什麼」是 Dockerfile 在打包時就決定好的事，兩張單子互不相識。」
2. q「新版本上線後發現有問題，怎麼退回舊版？」opts:「rollback（退回）——舊映像檔還在倉庫裡，把單子上的版本改回去就好」/「來不及了，舊版已經被刪掉」/「要把舊版程式碼重寫一遍再打包」/「把所有機器重灌」exp:「映像檔是不會變的成品，倉庫裡每一版都在；退版只是把單子改回去，大腦會照著換。」

**09-service：**
1. q「請求經過 Service 時，有經過一台「Service 伺服器」嗎？」opts:「沒有——在呼叫方自己那台機器上，位址就被 kube-proxy 寫好的轉發表當場改寫了」/「有，所有流量都先到 Service 主機集中再轉發」/「有，Service 是一台實體設備」/「要看當天的網路狀況」exp:「所以 Service 不會塞車、也沒有單點故障——它是一筆規則，不是一台機器。」
2. q「「東西住在哪」和「請求怎麼走」是兩個垂直的軸——意思是？」opts:「Pod 放哪台是排班的事、請求找到 Pod 是 Service 的事，兩者互不干涉」/「Service 決定 Pod 要放在哪台機器」/「Pod 的位置決定了請求的路線」/「兩個軸指的是 CPU 和記憶體」exp:「Service 只管第二個軸：不管 Pod 搬到哪台，名字都找得到它。」

**10-ingress：**
1. q「Service 的名字在叢集外面打得到嗎？」opts:「打不到——那個名字只在叢集內有效，外面的人要進來得靠對外入口依網址分流」/「打得到，名字是全世界通用的」/「加上密碼就打得到」/「只有付費方案打得到」exp:「叢集內互叫用 Service 名字就夠；叢集外的使用者要進來，就是這一課入口要解決的事。」
2. q「L4 和 L7 兩種負載平衡器差在哪？」opts:「L4 只認位址；L7 看得懂網址，能依 /api、/shop 這種路徑分流」/「L7 比 L4 多 3 個功能」/「L4 是硬體、L7 一定是軟體」/「數字越大速度越慢」exp:「雲端的 L7 負載平衡器自己就是「看得懂網址的執行者」，nginx 的活被它包掉了——這就是託管環境常常沒有 nginx 的原因。」

**11-pattern：**
1. q「「單子」和「執行者」的配對，哪一組是對的？」opts:「Deployment→Pod；Service→每台機器的轉發表；Ingress→nginx（Ingress Controller）」/「Pod→Deployment；轉發表→Service；nginx→Ingress」/「Deployment→nginx；Service→Pod；Ingress→轉發表」/「三張單子共用同一個執行者」exp:「左欄是存在 etcd 的願望，右欄是真的在跑（或真的存在）的東西。你永遠只寫左欄。」
2. q「想把服務從 3 份加到 5 份，宣告式的做法是？」opts:「把 Deployment 單子上的份數改成 5、交給櫃檯，剩下的大腦自己做」/「登入兩台機器，手動各啟動一份」/「打電話請雲端商加兩台機器」/「把現有 3 份重開一次就會變 5 份」exp:「改單子是你唯一要做的事——排班的找位子、巡邏的補到 5 份。」

**12-failure：**
1. q「master 全部掛掉，已經在跑的 Pod 會怎樣？」opts:「照跑——但叢集凍結了：Pod 再掛沒人補、單子再改沒人理，還在動但沒人管」/「立刻全部停止服務」/「自動搬去別的叢集」/「其中一個 Pod 會升級成大腦」exp:「「還在動但沒人管」反而更危險——表面看起來正常，出事才發現大腦早就不在了。」
2. q「「補位」和「選舉」差在哪？」opts:「Pod 或 worker 掛了→大腦補一個新的（補位）；master 掛了→剩下的靠過半數同意繼續運作（選舉），台數不會自己變回來」/「兩個詞是同一件事的兩種說法」/「worker 掛了要選舉、master 掛了要補位」/「只有雲端環境才有這兩件事」exp:「方向是「上面補下面」：大腦能補 worker 上的東西；大腦自己壞了沒有更上層來補，補台是人的工作。」

**13-when：**
1. q「一台機器就撐得住、流量穩定的小服務，建議用什麼？」opts:「Docker Compose 就夠了——不需要跨機器做決定，就不要上 K8s」/「一定要上 K8s 才專業」/「回去用實體機、一台一服務」/「不要部署，只在自己電腦跑」exp:「分水嶺是「需不需要跨機器決定東西放哪台」；不需要卻上 K8s，是把一份全職維運工作往自己身上攬。」
2. q「用 Cloud Run、ECS Fargate 這類託管服務，你交出什麼、換到什麼？」opts:「交出映像檔，換到「跨機器那一層有人幫你顧」——代價是可調的選項變少」/「交出原始碼，換到自動寫程式」/「交出信用卡，換到無限效能」/「交出 Dockerfile，換到一台實體機」exp:「大多數團隊實際落腳在中間這格：需要跨機器，但不想養一個全職顧 K8s 的人。」

- [ ] **步驟 3：跑測試確認通過**

```bash
python3 -m unittest discover -s builder/tests -v
```

預期：全部 PASS（每課 5 題、原題沒動、格式正確）。

- [ ] **步驟 4：commit**

```bash
git add content/k8s builder/tests/test_content.py
git commit -m "feat: K8s 每課測驗補到 5 題（追加 26 題，原 39 題不動）"
```

---

### 任務 4：builder——模板抽出＋模組頁產生

**Files:**
- Create: `builder/build.py`
- Create: `builder/templates/style.css`、`builder/templates/course.js`、`builder/templates/module.html`
- Create: `builder/tests/test_build.py`

**Interfaces:**
- Consumes: 任務 1〜3 的 content 檔（格式見開頭「資料格式」）
- Produces:
  - `build(content_dir=None, tpl_dir=None, out_dir=None)`——參數都是 `pathlib.Path`，不給就用 repo 預設（`content/`、`builder/templates/`、`dist/`）；會先刪掉 `out_dir` 再整站重建
  - `load_site(content_dir) -> (site: dict, mods: list)`——mods 每項是 module.json 內容加上 `id`、`icon`，每課加上 `html`（lesson.html 全文）與 `quiz`（題目 list）
  - 產出 `dist/<模組>/index.html`、`dist/style.css`、`dist/course.js`（首頁 `dist/index.html` 是任務 6 的事，本任務先產一個「建置中」佔位頁讓 build 跑得完）
  - 模組頁網址規則：`#/` 是課綱總覽、`#/lesson/<slug>` 直達某課（沿用現況）

- [ ] **步驟 1：寫建置測試（先寫、先看它失敗）**

建 `builder/tests/test_build.py`：

```python
# -*- coding: utf-8 -*-
# 建置結果檢查：檔案齊、模組頁的側邊欄／文章／測驗資料都組對
import json, re, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'builder'))
import build as builder


class TestBuild(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = Path(tempfile.mkdtemp()) / 'dist'
        builder.build(out_dir=cls.out)
        cls.site, cls.mods = builder.load_site(ROOT / 'content')

    def test_output_files(self):
        for name in ('index.html', 'style.css', 'course.js'):
            self.assertTrue((self.out / name).exists(), name)
        for mod in self.mods:
            self.assertTrue((self.out / mod['id'] / 'index.html').exists(), mod['id'])

    def test_module_page_k8s(self):
        html = (self.out / 'k8s' / 'index.html').read_text(encoding='utf-8')
        k8s = [m for m in self.mods if m['id'] == 'k8s'][0]
        # 側邊欄：總覽 + 13 課
        self.assertEqual(html.count('data-nav='), len(k8s['lessons']) + 1)
        # 分組標題四個都在
        for g in ('歷史：為什麼會有容器', 'DOCKER：一台機器上的事', 'K8S：由小到大', '判斷'):
            self.assertIn(g, html)
        # 每課一篇文章
        for L in k8s['lessons']:
            self.assertIn('<article id="pg-%s"' % L['slug'], html)
        # 測驗資料整包嵌進頁面，抽查第一課第一題
        self.assertIn(json.dumps(k8s['lessons'][0]['quiz'][0]['q'], ensure_ascii=False), html)
        self.assertIn("var MODULE=\"k8s\"", html)
        # 共用樣式與腳本用相對路徑
        self.assertIn('../style.css', html)
        self.assertIn('../course.js', html)
        # 頂欄：回首頁連結與模組下拉選單，選單有全部模組
        self.assertIn('href="../"', html)
        self.assertEqual(html.count('<option'), len(self.mods))

    def test_no_company_terms(self):
        for page in self.out.rglob('*.html'):
            self.assertNotIn('KPI', page.read_text(encoding='utf-8'), str(page))

    def test_progress_key_per_module(self):
        js = (self.out / 'course.js').read_text(encoding='utf-8')
        self.assertIn("'notes-progress:'+MODULE", js)
        self.assertNotIn('k8s-course-done', js)


if __name__ == '__main__':
    unittest.main()
```

跑 `python3 -m unittest discover -s builder/tests -v`，預期 test_build 整批 ERROR（`build` 模組不存在）。

- [ ] **步驟 2：建 `builder/templates/style.css`**

內容分三段：
1. **整份照抄** `rescue/build_spa.py` 裡 `CSS = '''` 到收尾 `'''` 之間的全部內容（從 `:root{` 到 `*:focus-visible{…}`）。
2. 頂欄改版需要的新規則，附加在後面：

```css
/* ── 頂欄：回平台首頁＋模組下拉選單 ── */
.topbar .home{text-decoration:none;color:var(--ink);font-weight:700;font-size:14.5px;white-space:nowrap}
.topbar .home:hover{color:var(--gold)}
.topbar .sep{color:var(--mut)}
.topbar .modsel{font-family:inherit;font-size:14px;font-weight:700;color:var(--ink);
  background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:5px 8px;
  max-width:min(52vw,320px)}
```

3. Redis 模組內文用到、原站沒有的類別（從 Redis 原頁的樣式搬來、換成暖色變數、字型改 JetBrains Mono）：

```css
/* ── Redis 模組沿用的內容元件 ── */
.card{background:var(--surface);border:1px solid var(--line);border-radius:6px;
  padding:20px;display:flex;flex-direction:column;gap:10px;box-shadow:var(--shadow)}
.card p{font-size:15px;line-height:1.75}
.card .badge{font-family:"JetBrains Mono",monospace;font-size:11px;letter-spacing:.12em;
  color:var(--gold);background:var(--gold-soft);align-self:flex-start;padding:2px 8px;border-radius:99px}
.pits{display:flex;flex-direction:column;gap:14px}
.pit{display:grid;grid-template-columns:auto 1fr;gap:14px;align-items:start;
  background:var(--surface);border:1px solid var(--line);border-left:4px solid var(--danger);
  border-radius:4px;padding:14px 18px}
.pit .n{font-family:"JetBrains Mono",monospace;color:var(--danger);font-weight:600;font-size:15px;line-height:1.85}
.pit p{font-size:15px;line-height:1.75}
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:26px}
.good{color:var(--ok);font-weight:700}
```

- [ ] **步驟 3：建 `builder/templates/course.js`**

以 `rescue/build_spa.py` 最後那段 `<script>` 裡的 JavaScript（`(function(){` 到 `})();`）為底照抄，做以下修改（`MODULE`、`QUIZ`、`SLUGS` 三個變數改由頁面先宣告，見步驟 4 的資料腳本）：

1. 刪掉開頭的 `var QUIZ=…;` 與 `var SLUGS=…;` 兩行（頁面會先宣告好）。
2. `var KEY='k8s-course-done';` → `var KEY='notes-progress:'+MODULE;`
3. `refreshTicks()` 裡三處「有沒有做完」的判斷，從布林改成物件：
   - `if(d[s])n++;` → `if(d[s]&&d[s].done)n++;`
   - `el.hidden=!d[slug];` → `el.hidden=!(d[slug]&&d[slug].done);`
   - `el.hidden=!d[el.getAttribute('data-ovtick')];` → `var k=el.getAttribute('data-ovtick');el.hidden=!(d[k]&&d[k].done);`
4. 對答案那段，原本只在全對時記錄：

```js
    if(allRight){
      var d=loadDone();d[slug]=true;saveDone(d);refreshTicks();
```

改成每次都記最好成績（給第二期的「成績取較好那次」用）：

```js
    var rightCount=0;
    qs.forEach(function(q,qi){if(picks[qi]===0)rightCount++;});
    var d=loadDone();
    var rec=d[slug]||{best:0,total:qs.length,done:false};
    rec.total=qs.length;
    if(rightCount>rec.best)rec.best=rightCount;
    if(allRight)rec.done=true;
    d[slug]=rec;saveDone(d);refreshTicks();
    if(allRight){
```

（後面訊息顯示的兩個分支不變。）

5. `localStorage.setItem('k8s-course-last',h)` 與 `localStorage.getItem('k8s-course-last')` → 鑰匙名改 `'notes-last:'+MODULE`。
6. 檔案最後（還在閉包裡）加模組下拉選單的跳轉：

```js
var modsel=document.getElementById('modsel');
if(modsel)modsel.addEventListener('change',function(){location.href='../'+this.value+'/';});
```

- [ ] **步驟 4：建 `builder/templates/module.html`**

佔位符用 `__大寫__` 字串、Python 端用 `str.replace` 換（**不用** `str.format`，CSS/JS 的大括號會炸）：

```html
<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Chivo:wght@600;900&family=JetBrains+Mono:wght@400;600&family=Noto+Sans+TC:wght@400;500;700;900&display=swap">
<link rel="stylesheet" href="../style.css">
</head>
<body>
<header class="topbar">
  <button class="burger" id="burger" aria-label="開關章節選單">☰</button>
  <a class="home" href="../">🏠 筆記平台</a>
  <span class="sep">›</span>
  <select class="modsel" id="modsel" aria-label="切換模組">__MODSEL__</select>
</header>
<div class="scrim" id="scrim"></div>
<nav class="sidebar" id="sidebar" aria-label="章節選單">
__SIDEBAR__
</nav>
<main class="main" id="main">
__ARTICLES__
</main>
<script>__DATA__</script>
<script src="../course.js"></script>
</body>
</html>
```

- [ ] **步驟 5：建 `builder/build.py`**

```python
# -*- coding: utf-8 -*-
# 讀 content/ 全部，組出整個平台到 dist/（每次整站重建，不做增量）
import json, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_templates(tpl_dir):
    names = ('style.css', 'course.js', 'module.html', 'home.html')
    return {n: (tpl_dir / n).read_text(encoding='utf-8') for n in names if (tpl_dir / n).exists()}


def load_site(content_dir):
    site = json.loads((content_dir / 'modules.json').read_text(encoding='utf-8'))
    mods = []
    for entry in site['modules']:
        mdir = content_dir / entry['id']
        mod = json.loads((mdir / 'module.json').read_text(encoding='utf-8'))
        mod['id'], mod['icon'] = entry['id'], entry['icon']
        for L in mod['lessons']:
            ldir = mdir / L['dir']
            L['html'] = (ldir / 'lesson.html').read_text(encoding='utf-8')
            L['quiz'] = json.loads((ldir / 'quiz.json').read_text(encoding='utf-8'))['questions']
            L['assets'] = ldir / 'assets'
        mods.append(mod)
    return site, mods


def sidebar_html(mod):
    out = ['  <a href="#/" data-nav="ov" class="ov">📖&nbsp; 課綱總覽</a>\n']
    group = None
    for i, L in enumerate(mod['lessons']):
        if L.get('group') and L['group'] != group:
            group = L['group']
            out.append('  <div class="group">%s</div>\n' % group)
        out.append('  <a href="#/lesson/%s" data-nav="%s"><span class="n">%d.</span>'
                   '<span>%s</span><span class="tick" data-tick hidden>✓</span></a>\n'
                   % (L['slug'], L['slug'], i + 1, L['title']))
    return ''.join(out)


def overview_html(mod):
    o = ['<article id="pg-ov">\n<div class="ov-hero">\n<p class="kick">%s</p>\n<h1>%s</h1>\n'
         % (mod['kick'], mod['title'])]
    o.append('<p>%s</p>\n' % mod['overview_intro'])
    o.append('<p class="ov-progress" id="ovProgress"></p>\n</div>\n<div class="lesson-list">\n')
    for i, L in enumerate(mod['lessons']):
        o.append('<a href="#/lesson/%s"><span class="n">%d</span><span class="tt"><b>%s</b>'
                 '<span>%s</span></span><span class="done" data-ovtick="%s" hidden>✓</span>'
                 '<span class="mins">%d 分</span></a>\n'
                 % (L['slug'], i + 1, L['title'], L['desc'], L['slug'], L['mins']))
    o.append('</div>\n<footer class="site">%s</footer>\n</article>\n' % mod['footer_note'])
    return ''.join(o)


def article_html(mod, i, L):
    N = len(mod['lessons'])
    a = ['<article id="pg-%s" hidden>\n' % L['slug']]
    a.append('<p class="crumb"><a href="#/">課綱總覽</a> › 第 %d 課 / 共 %d 課</p>\n' % (i + 1, N))
    a.append('<h1 class="lt">%s</h1>\n' % L['title'])
    a.append('<div class="meta"><span class="chip g">第 %d 課 / 共 %d 課</span>'
             '<span class="chip">約 %d 分鐘</span></div>\n' % (i + 1, N, L['mins']))
    a.append('<p class="sub">%s</p>\n' % L['desc'])
    a.append(L['html'] + '\n')   # 「讀完這課你會」框、內文、「重點整理」框都在 lesson.html 裡
    a.append('<div class="quiz" data-quiz="%s"></div>\n' % L['slug'])
    a.append('<nav class="pager">')
    if i > 0:
        P = mod['lessons'][i - 1]
        a.append('<a href="#/lesson/%s"><span class="dir">← 上一課</span><span class="t">%s</span></a>'
                 % (P['slug'], P['title']))
    if i < N - 1:
        Nx = mod['lessons'][i + 1]
        a.append('<a class="next" href="#/lesson/%s"><span class="dir">下一課 →</span>'
                 '<span class="t">%s</span></a>' % (Nx['slug'], Nx['title']))
    else:
        a.append('<a class="next" href="#/"><span class="dir">回到</span><span class="t">課綱總覽</span></a>')
    a.append('</nav>\n</article>\n')
    return ''.join(a)


def modsel_html(mods, current_id):
    return ''.join('<option value="%s"%s>%s %s</option>'
                   % (m['id'], ' selected' if m['id'] == current_id else '', m['icon'], m['title'])
                   for m in mods)


def render_module_page(mod, mods, tpl):
    quiz = {L['slug']: L['quiz'] for L in mod['lessons']}
    slugs = [L['slug'] for L in mod['lessons']]
    data = ('var MODULE=%s;\nvar QUIZ=%s;\nvar SLUGS=%s;'
            % (json.dumps(mod['id']), json.dumps(quiz, ensure_ascii=False),
               json.dumps(slugs, ensure_ascii=False)))
    arts = [overview_html(mod)] + [article_html(mod, i, L) for i, L in enumerate(mod['lessons'])]
    page = tpl['module.html']
    for key, val in (('__TITLE__', mod['title']), ('__MODSEL__', modsel_html(mods, mod['id'])),
                     ('__SIDEBAR__', sidebar_html(mod)), ('__ARTICLES__', ''.join(arts)),
                     ('__DATA__', data)):
        page = page.replace(key, val)
    return page


def render_home_page(site, mods, tpl):
    # 任務 6 換成真正的首頁模板；先給佔位頁讓整條流程跑得通
    if 'home.html' not in tpl:
        links = ''.join('<li><a href="%s/">%s %s</a></li>' % (m['id'], m['icon'], m['title'])
                        for m in mods)
        return ('<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><title>%s</title>'
                '</head><body><h1>%s</h1><ul>%s</ul></body></html>'
                % (site['site_title'], site['site_title'], links))
    raise NotImplementedError('home.html 模板由任務 6 實作')


def build(content_dir=None, tpl_dir=None, out_dir=None):
    content_dir = content_dir or ROOT / 'content'
    tpl_dir = tpl_dir or ROOT / 'builder' / 'templates'
    out_dir = out_dir or ROOT / 'dist'
    site, mods = load_site(content_dir)
    tpl = load_templates(tpl_dir)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    (out_dir / 'style.css').write_text(tpl['style.css'], encoding='utf-8')
    (out_dir / 'course.js').write_text(tpl['course.js'], encoding='utf-8')
    (out_dir / 'index.html').write_text(render_home_page(site, mods, tpl), encoding='utf-8')
    for mod in mods:
        d = out_dir / mod['id']
        d.mkdir()
        (d / 'index.html').write_text(render_module_page(mod, mods, tpl), encoding='utf-8')
        for L in mod['lessons']:
            if L['assets'].is_dir():   # 規格：每課的圖放自己的 assets/；建置時搬到 assets/<課資料夾>/
                shutil.copytree(L['assets'], d / 'assets' / L['dir'])
    print('built →', out_dir)


if __name__ == '__main__':
    build()
```

- [ ] **步驟 6：跑測試確認通過，並實際建一次**

```bash
python3 -m unittest discover -s builder/tests -v
python3 builder/build.py
```

預期：測試全 PASS；`dist/k8s/index.html`、`dist/redis/index.html` 產出。用瀏覽器開 `dist/k8s/index.html` 抽查一課有內文有測驗。

- [ ] **步驟 7：commit**

```bash
git add builder/
git commit -m "feat: builder 建置工具——模板抽出、模組頁產生、每模組獨立進度鑰匙"
```

---

### 任務 5：K8s 內容一致性驗收測試（新舊頁面逐課比對）

**Files:**
- Create: `builder/tests/test_parity.py`

**Interfaces:**
- Consumes: `rescue/k8s-course.html`（比對基準）、任務 4 的 `builder.build()`
- Produces: 規格驗收條件「K8s 模組與現行 artifact 內容一致（加補題）」的自動化證明

- [ ] **步驟 1：寫比對測試**

```python
# -*- coding: utf-8 -*-
# 驗收：新工具組出來的 K8s 模組頁，逐課文字要跟 rescue/k8s-course.html 一致
# （總覽頁開場段落刻意改過措辭、測驗有補題，所以只比 13 課的文章與總覽的課程列表）
import re, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'builder'))
import build as builder

RESCUE = ROOT / 'rescue' / 'k8s-course.html'


def text_of(html):
    html = re.sub(r'<!--.*?-->', ' ', html, flags=re.S)
    html = re.sub(r'<[^>]+>', ' ', html)
    return re.sub(r'\s+', ' ', html).strip()


def article(html, slug):
    m = re.search(r'<article id="pg-%s"[^>]*>.*?</article>' % re.escape(slug), html, re.S)
    assert m, 'pg-%s not found' % slug
    return m.group(0)


@unittest.skipUnless(RESCUE.exists(), 'rescue/ 已刪，跳過一致性比對')
class TestParity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old = RESCUE.read_text(encoding='utf-8')
        out = Path(tempfile.mkdtemp()) / 'dist'
        builder.build(out_dir=out)
        cls.new = (out / 'k8s' / 'index.html').read_text(encoding='utf-8')
        _, mods = builder.load_site(ROOT / 'content')
        cls.k8s = [m for m in mods if m['id'] == 'k8s'][0]

    def test_all_13_lessons_match(self):
        for L in self.k8s['lessons']:
            with self.subTest(lesson=L['slug']):
                self.assertEqual(text_of(article(self.old, L['slug'])),
                                 text_of(article(self.new, L['slug'])))

    def test_overview_lesson_list_matches(self):
        pick = lambda h: re.search(r'<div class="lesson-list">.*?</div>', h, re.S).group(0)
        self.assertEqual(text_of(pick(article(self.old, 'ov'))),
                         text_of(pick(article(self.new, 'ov'))))


if __name__ == '__main__':
    unittest.main()
```

- [ ] **步驟 2：跑測試**

```bash
python3 -m unittest discover -s builder/tests -v
```

預期：PASS。**如果哪一課不一致，修的是遷移腳本或 builder，不是改測試**——除非查出來是刻意的差異（像總覽開場段落那種），那就把該差異寫進測試檔開頭的註解並排除比對。

- [ ] **步驟 3：commit**

```bash
git add builder/tests/test_parity.py
git commit -m "test: 新舊 K8s 頁面逐課文字一致性比對（驗收條件自動化）"
```

---

### 任務 6：平台首頁＋完成度顯示

**Files:**
- Create: `builder/templates/home.html`
- Modify: `builder/build.py`（`render_home_page` 換成真實作）
- Modify: `builder/templates/style.css`（追加首頁樣式）
- Modify: `builder/tests/test_build.py`（追加首頁檢查）

**Interfaces:**
- Consumes: `site`（modules.json）、`mods`（含每模組課數）、任務 4 的模板機制
- Produces: `dist/index.html`——側邊欄列模組、主畫面模組卡片（圖示、名稱、一句話簡介、課數、完成度）；完成度由瀏覽器端讀 `notes-progress:<模組>` 算出

- [ ] **步驟 1：擴充建置測試（先寫、先看它失敗）**

`test_build.py` 加：

```python
    def test_home_page(self):
        html = (self.out / 'index.html').read_text(encoding='utf-8')
        self.assertIn(self.site['site_title'], html)
        for mod in self.mods:
            self.assertIn('href="%s/"' % mod['id'], html)
            self.assertIn(mod['icon'], html)
            self.assertIn(mod['title'], html)
            self.assertIn('data-stat="%s"' % mod['id'], html)
            self.assertIn('共 %d 課' % len(mod['lessons']), html)
        self.assertIn('style.css', html)
        self.assertIn('viewport', html)
```

跑測試，預期這條 FAIL（現在的首頁是佔位頁）。

- [ ] **步驟 2：建 `builder/templates/home.html`**

```html
<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__SITE_TITLE__</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Chivo:wght@600;900&family=JetBrains+Mono:wght@400;600&family=Noto+Sans+TC:wght@400;500;700;900&display=swap">
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="topbar">
  <button class="burger" id="burger" aria-label="開關模組選單">☰</button>
  <a class="brand" href="./">Tim 的<b>筆記平台</b></a>
</header>
<div class="scrim" id="scrim"></div>
<nav class="sidebar" id="sidebar" aria-label="模組選單">
  <div class="group">模組</div>
__SIDEBAR__
</nav>
<main class="main">
  <div class="ov-hero">
    <p class="kick">NOTES · 個人筆記平台</p>
    <h1>__SITE_TITLE__</h1>
    <p>__SITE_INTRO__</p>
  </div>
  <div class="mod-cards">
__CARDS__
  </div>
  <footer class="site">內容公開；學習進度存在你這台裝置的瀏覽器裡。</footer>
</main>
<script>
(function(){
var MODS=__MODS__;
var sidebar=document.getElementById('sidebar'),scrim=document.getElementById('scrim');
document.getElementById('burger').addEventListener('click',function(){
  sidebar.classList.toggle('open');scrim.classList.toggle('show');
});
scrim.addEventListener('click',function(){sidebar.classList.remove('open');scrim.classList.remove('show');});
MODS.forEach(function(m){
  var done=0;
  try{
    var d=JSON.parse(localStorage.getItem('notes-progress:'+m.id))||{};
    Object.keys(d).forEach(function(k){if(d[k]&&d[k].done)done++;});
  }catch(e){}
  var el=document.querySelector('[data-stat="'+m.id+'"]');
  if(el)el.innerHTML='完成 <b>'+done+'</b> / '+m.count+' 課';
});
})();
</script>
</body>
</html>
```

- [ ] **步驟 3：`style.css` 追加首頁卡片樣式**

```css
/* ── 平台首頁 ── */
.mod-cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:18px}
.mod-card{display:flex;flex-direction:column;gap:8px;background:var(--surface);
  border:1px solid var(--line);border-top:4px solid var(--gold);border-radius:10px;
  padding:20px 22px;text-decoration:none;color:var(--ink);box-shadow:var(--shadow)}
.mod-card:hover{border-color:var(--gold)}
.mod-card .icon{font-size:30px;line-height:1}
.mod-card b{font-family:"Chivo","Noto Sans TC",sans-serif;font-size:18px}
.mod-card>span{font-size:14px;color:var(--ink2);line-height:1.7}
.mod-card .stats{margin-top:6px;font-family:"JetBrains Mono",monospace;font-size:12px;color:var(--ink2)}
.mod-card .stats b{color:var(--gold-deep);font-family:inherit;font-size:12px}
```

- [ ] **步驟 4：`build.py` 的 `render_home_page` 換成真實作**

```python
def render_home_page(site, mods, tpl):
    side = ''.join('  <a href="%s/"><span class="n">%s</span><span>%s</span></a>\n'
                   % (m['id'], m['icon'], m['title']) for m in mods)
    cards = ''.join(
        '<a class="mod-card" href="%s/"><span class="icon">%s</span><b>%s</b>'
        '<span>%s</span><span class="stats"><span data-stat="%s"></span> · 共 %d 課</span></a>\n'
        % (m['id'], m['icon'], m['title'], m['intro'], m['id'], len(m['lessons']))
        for m in mods)
    mods_js = json.dumps([{'id': m['id'], 'count': len(m['lessons'])} for m in mods],
                         ensure_ascii=False)
    page = tpl['home.html']
    for key, val in (('__SITE_TITLE__', site['site_title']), ('__SITE_INTRO__', site['site_intro']),
                     ('__SIDEBAR__', side), ('__CARDS__', cards), ('__MODS__', mods_js)):
        page = page.replace(key, val)
    return page
```

（同時刪掉原本的佔位實作與 `NotImplementedError`。）

- [ ] **步驟 5：跑全部測試、建一次、肉眼看首頁**

```bash
python3 -m unittest discover -s builder/tests -v
python3 builder/build.py
```

預期：全 PASS。開 `dist/index.html`：兩張模組卡片、點卡片同分頁進模組、模組頁頂欄能回首頁與下拉切換模組。

- [ ] **步驟 6：commit**

```bash
git add builder/
git commit -m "feat: 平台首頁——模組卡片、課數與完成度、側邊欄模組清單"
```

---

### 任務 7：整站互動檢查（本機預覽）

**Files:** 無新檔案；發現問題就修對應的 builder／content 檔並重跑測試。

用無頭瀏覽器（gstack 的 `/browse` 技能）逐項檢查，每項截圖存證：

- [ ] **步驟 1：建置並開首頁** `python3 builder/build.py`，開 `file://…/dist/index.html`。確認：兩張卡片、完成度顯示「完成 0 / N 課」。
- [ ] **步驟 2：進 K8s 模組**：點卡片 → 課綱總覽 13 課；點第 1 課 → 內文、SVG 圖、5 題測驗都在。
- [ ] **步驟 3：測驗流程**：全按正確答案（注意選項是亂序的，要按文字判斷）→「全對！已在側邊欄打勾」→ 側邊欄與總覽出現 ✓；重新整理後 ✓ 還在（localStorage 有存）。
- [ ] **步驟 4：故意答錯一題** → 顯示解析、「再測一次」能重來；打勾狀態不會被答錯洗掉。
- [ ] **步驟 5：回首頁** → K8s 卡片完成度變「完成 1 / 13 課」。
- [ ] **步驟 6：Redis 模組**：內文 9 段都在、SVG 是暖色（沒有跑出舊配色）、最後一段是一般化版本、8 題測驗可作答。
- [ ] **步驟 7：直達網址**：開 `dist/k8s/index.html#/lesson/pod-node` → 直接落在第 6 課。
- [ ] **步驟 8：手機寬度**（視窗縮到 400px 寬）：側邊欄收起、漢堡按鈕能開關、內容不破版。
- [ ] **步驟 9：** 有修任何東西就重跑 `python3 -m unittest discover -s builder/tests -v`，然後 commit：

```bash
git add -A && git commit -m "fix: 本機整站預覽檢查發現的問題修正"
```

（沒修東西就跳過 commit。）

---

### 任務 8：GitHub Actions 部署上線

**Files:**
- Create: `.github/workflows/deploy.yml`

**Interfaces:**
- Consumes: 任務 4 的 `python3 builder/build.py`（產出 `dist/`）、全部測試
- Produces: push 到 `main` 即發佈到 `https://hhtim.github.io/notes-platform/`

- [ ] **步驟 1：建 `.github/workflows/deploy.yml`**

```yaml
name: deploy
on:
  push:
    branches: [main]
  workflow_dispatch:
permissions:
  contents: read
  pages: write
  id-token: write
concurrency:
  group: pages
  cancel-in-progress: true
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: 測試
        run: python3 -m unittest discover -s builder/tests -v
      - name: 建置
        run: python3 builder/build.py
      - uses: actions/configure-pages@v5
        with:
          enablement: true
      - uses: actions/upload-pages-artifact@v3
        with:
          path: dist
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

- [ ] **步驟 2：commit 並推上去**

```bash
git add .github/workflows/deploy.yml
git commit -m "ci: push 到 main 自動建置並發佈到 GitHub Pages"
git push
```

（遠端就是設好的 `git@github-hhtim:…` 別名，直接 `git push` 即可。）

- [ ] **步驟 3：確認 Actions 跑完、網站上線**

等幾分鐘後用瀏覽器開 `https://hhtim.github.io/notes-platform/`，看到平台首頁與兩個模組即成功。

**如果 Actions 在 configure-pages 那步失敗**（權杖權限不夠自動開通 Pages）：請 Tim 到 GitHub 網頁 → repo 的 Settings → Pages → Build and deployment → Source 選「GitHub Actions」，然後在 Actions 頁面把失敗的那次 re-run。這是規格裡列的 Tim 一次性設定，程式這邊不用改。

- [ ] **步驟 4：線上抽查**

開線上網址走一遍任務 7 的步驟 2、6、7（進模組、看 Redis、直達網址），確認跟本機一致。

---

## 驗收對照（規格第 9 節「第一期」）

| 規格驗收條件 | 由誰證明 |
|---|---|
| 手機開網址見平台首頁與兩個模組 | 任務 8 步驟 3、4（＋Tim 用手機實測） |
| K8s 模組與現行 artifact 內容一致 | 任務 5 的 `test_parity.py`（13 課逐課比對） |
| 每課測驗至少 5 題 | 任務 3 收緊後的 `test_quiz_format` |
| rescue/ 檔案拆成 content/ 格式 | 任務 1、2 的 `test_content.py` |
| builder 改造完成、整站重建 | 任務 4、6 的 `test_build.py` |

**上線後交給 Tim 的事**：手機開網址實測；實測 OK、Tim 說驗收通過之後，才刪 `rescue/` 整個資料夾（含兩支遷移腳本）並把 `test_parity.py` 的 skip 行為留著（rescue 刪掉後它會自動跳過）。

## 刻意與舊站不同的地方（比對時不要當成 bug）

1. 總覽頁開場段落：「每課末有 3 題隨堂測驗」改成不寫死題數（因為補題到 5 題）。
2. 進度的 localStorage 鑰匙從 `k8s-course-done` 換成 `notes-progress:k8s`，值從布林換成 `{best, total, done}`（為第二期合併規則鋪路）。舊 artifact 網域不同，進度本來就帶不過來，不需要搬。
3. 頂欄從「站名」變成「回平台首頁＋模組下拉選單」。
4. 補了 `<meta name="viewport">` 與 `<!doctype html>`（舊檔是 artifact 外殼提供的）。
5. CSS 與 JavaScript 從每頁內嵌改成共用的 `style.css`、`course.js`。
