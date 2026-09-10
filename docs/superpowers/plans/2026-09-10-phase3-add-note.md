# 第三期：`/add-note` 收錄流程 實作計畫

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**目標：** 把規格第 8 節的七步收錄流程做成 repo 內的 `/add-note` skill：丟一個網址（或文字、檔案）給 Claude Code，它讀取、查證、歸模組、防重複、改寫成課程頁、預覽、發佈。

**做法：** 兩塊。前置是建置端——規格第 4 節的「更正標記」（更正處加明顯底色、附出處連結、滑過或點一下顯示原筆記寫什麼）目前模板沒有樣式，先補進 `style.css` 並定死寫法；主體是 skill 本身——`.claude/skills/add-note/SKILL.md`，把七步、三個停問點、所有內容慣例（檔案格式、測驗規則、圖片規則、用詞規則）寫成一份完整的操作規程，skill 跟著 repo 走，電腦與手機的 Claude Code 都拿得到。

**技術：** 純 CSS（更正標記的提示不用 JavaScript）、Claude Code skill（Markdown）、既有的 builder 與測試。

**規格：** `docs/superpowers/specs/2026-09-04-notes-platform-design.md`——第 8 節是流程本體，第 4 節是內容格式慣例（來源註記、圖片、更正標記、測驗），第 9 節第三期是驗收。

## 全域限制（每個任務都適用）

- **會停下來找 Tim 的點只有三個**（規格逐字）：第 3 步歸模組拿不準、第 4 步與既有課重疊、第 6 步預覽確認。查證（第 2 步）不停——直接改，靠更正標記讓 Tim 事後看得到。**未經 Tim 點頭絕不新開模組。**
- **讀取來源的界線**（規格逐字）：抓不到不放棄——診斷該站要什麼、配合使用者提供的帳號、驗證碼完成正常登入；**偽裝、繞過封鎖等手段預設不做，除非使用者明確要求才照辦**。
- **內容慣例**（規格第 4 節）：每課 `lesson.html` 檔頭一行註解記「來源網址＋收錄日期」；不保留原始材料副本；圖片一律下載進該課 `assets/`（示意圖優先重畫成向量圖、照片截圖保留原檔）；測驗 5〜10 題、`opts[0]` 正確、前端亂序。
- **更正標記**（規格逐字）：該段文字加明顯底色（與暖色系不衝突但一眼可辨），旁附直達查證出處的小連結；滑鼠移上（手機點一下）顯示「原筆記此處寫 X，查證後更正」。
- 內容檔不含 `<style>`；不用框架；亮暖色不做深色模式；`dist/` 不進 git。
- 發佈前必過：`python3 -m unittest discover -s builder/tests -v` 全綠、`python3 builder/build.py` 成功。
- Git：遠端 SSH 別名不動、repo 身分 commit、直接在 `main` 上做；push 到 main 即發佈。
- 寫給人看的一切文字照 Tim 的用詞規則（台灣講法、不發明編號代號、不造字、新名詞第一次出現附白話、比喻括號附正式名詞）。
- 平台內容不進公司 repo、不從公司文件引用；產出頁面不得出現「KPI」（有測試守著）。

## 檔案結構總覽

```
notes-platform/
├── .claude/skills/add-note/
│   └── SKILL.md                    （任務 2 建）七步流程的完整操作規程
├── builder/
│   ├── templates/style.css         （任務 1 改）更正標記的樣式
│   └── tests/test_build.py         （任務 1 改）加一個樣式存在的檢查
└── CLAUDE.md                       （任務 3 改）驗收後更新現況
```

**責任分工**：樣式歸模板（任務 1）；「怎麼收一篇筆記」的全部知識歸 SKILL.md（任務 2）——它是給未來任何一個 Claude Code 對話（含手機）看的操作手冊，必須自足，不能假設讀者看過這份計畫。

## 介面（兩個任務共用）

更正標記的固定寫法（任務 1 提供樣式、任務 2 的 SKILL.md 教人這樣寫）：

```html
<mark class="fixnote" tabindex="0" data-note="原筆記此處寫「X」，查證後更正">更正後的正確敘述</mark><a class="fixsrc" href="查證出處網址" target="_blank" rel="noopener">出處</a>
```

- `data-note` 必寫原筆記原本的講法；`tabindex="0"` 讓手機點一下能觸發顯示
- `fixsrc` 連到能直接驗證的那一頁（官方文件優先）

---

### 任務 1：更正標記的樣式

**Files:**
- Modify: `builder/templates/style.css`（檔尾追加）
- Modify: `builder/tests/test_build.py`（`TestBuild` 加一個測試方法）

**Interfaces:**
- Consumes: 既有的暖色變數（`--slate`、`--slate-soft`、`--ink`）
- Produces: `mark.fixnote`（灰藍底標記＋hover/focus 顯示 `data-note`）與 `a.fixsrc`（上標小連結）兩個類別——「介面」節的寫法靠它們渲染

- [ ] **步驟 1：寫失敗的測試**

`builder/tests/test_build.py` 的 `TestBuild` 里加：

```python
    def test_fixnote_styles(self):
        css = (self.out / 'style.css').read_text(encoding='utf-8')
        self.assertIn('mark.fixnote', css)
        self.assertIn('attr(data-note)', css)   # 提示文字來自 data-note，純 CSS 不用 JavaScript
        self.assertIn('a.fixsrc', css)
```

- [ ] **步驟 2：跑測試，確認失敗**

```bash
python3 -m unittest discover -s builder/tests -v
```

預期：`test_fixnote_styles` FAIL，其餘照舊全綠。

- [ ] **步驟 3：`builder/templates/style.css` 檔尾追加**

```css
/* ── 更正標記：查證後改掉原筆記錯誤的地方（規格第 4 節） ──
   寫法：<mark class="fixnote" tabindex="0" data-note="原筆記此處寫「X」，查證後更正">正確敘述</mark><a class="fixsrc" href="出處">出處</a>
   灰藍底：與暖色系不衝突但一眼可辨；滑鼠移上或手機點一下顯示 data-note */
mark.fixnote{background:var(--slate-soft);color:inherit;padding:1px 4px;border-radius:3px;
  border-bottom:2px solid var(--slate);cursor:help;position:relative}
mark.fixnote:hover::after,mark.fixnote:focus::after{
  content:attr(data-note);position:absolute;left:0;top:calc(100% + 6px);z-index:20;
  background:var(--ink);color:#FFF8EC;font-size:12.5px;line-height:1.6;font-weight:400;
  padding:8px 12px;border-radius:6px;width:max-content;max-width:min(320px,72vw);white-space:normal}
mark.fixnote:focus{outline:2px solid var(--slate);outline-offset:1px}
a.fixsrc{font-size:11.5px;font-family:"JetBrains Mono",monospace;color:var(--slate);
  text-decoration:none;vertical-align:super;margin-left:2px}
a.fixsrc:hover{color:var(--gold);text-decoration:underline}
```

- [ ] **步驟 4：跑測試確認通過，目視驗證一次**

```bash
python3 -m unittest discover -s builder/tests -v
python3 builder/build.py
```

目視：把下面這段暫時貼進任意一份 dist 頁面（或存成引用 `dist/style.css` 的暫存 html），用 `/browse` 開起來截圖——底色可辨、滑過出現黑底提示、出處連結是上標小字。**看完把暫存物清掉，不留在 repo。**

```html
<p>Pod 的預設上限是 <mark class="fixnote" tabindex="0" data-note="原筆記此處寫「256 個」，查證後更正">每台 Node 110 個</mark><a class="fixsrc" href="https://kubernetes.io/docs/setup/best-practices/cluster-large/" target="_blank" rel="noopener">出處</a>，可以調整。</p>
```

- [ ] **步驟 5：commit**

```bash
git add builder/
git commit -m "feat: 更正標記樣式——灰藍底、出處上標連結、滑過或點一下顯示原筆記寫什麼"
```

---

### 任務 2：`/add-note` skill 本體

**Files:**
- Create: `.claude/skills/add-note/SKILL.md`

**Interfaces:**
- Consumes: 任務 1 的 `mark.fixnote`／`a.fixsrc` 寫法；既有的 content 檔案格式（modules.json、module.json、lesson.html、quiz.json）；既有的建置與測試指令
- Produces: 完整的 skill。下面是**全文**，逐字建檔（這份文件是給未來的 Claude Code 對話看的操作規程，必須自足）：

````markdown
---
name: add-note
description: 把一篇筆記收錄進筆記平台。輸入是一個網址、一段文字或一個檔案；流程是讀取、查證、歸模組、防重複、改寫成課程頁、預覽、發佈，共七步。當 Tim 丟來源材料要收進平台、說「收這篇」「加一課」或「/add-note」時使用。
---

# /add-note：收錄一篇筆記

把來源材料變成平台上的一課（或補強既有的一課）。流程照規格
`docs/superpowers/specs/2026-09-04-notes-platform-design.md` 第 8 節，內容慣例照第 4 節。

**會停下來問 Tim 的點只有三個：歸模組拿不準（第 3 步）、與既有課重疊（第 4 步）、預覽確認（第 6 步）。**
查證（第 2 步）不問——發現錯誤直接改寫成正確版本，用更正標記讓 Tim 事後一眼看到並可自行驗證。
順利時全程只在第 6 步問一次。

## 開工前

1. `git pull`——確保在最新版上工作（電腦和手機可能都在動這個 repo）。
2. 讀 `content/modules.json` 和每個模組的 `content/<模組>/module.json`，掌握現有模組與課表。

## 第 1 步：讀取來源

輸入是網址、一段文字或一個檔案。

- 網址：抓內容。**抓不到不放棄**：先診斷該站要什麼（要登入？有驗證碼？擋機器人？），
  回報 Tim 缺什麼，配合他提供的帳號、驗證碼**完成正常登入**後再抓。
- **界線（規格明訂）**：正常登入可做；偽裝身分、繞過封鎖等手段**預設不做**，除非 Tim 明確要求才照辦。
- 記下「來源網址＋今天日期」，第 5 步要寫進檔頭。**不保留來源的原始材料副本**——讀完、改寫完，原文即丟。
- 內文用到的圖：記下每張圖的網址與用途，第 5 步處理。

## 第 2 步：查證內容

- 放手用網路搜尋比對**官方文件**，查三件事：技術錯誤、過時內容、與平台既有課程的矛盾。
- **發現錯誤直接改寫成正確版本，不先徵詢。** 每個更正處必須用下面的固定寫法標記。
- 若矛盾出在平台的既有課（舊課錯了），一樣直接修舊課、加標記，並在第 7 步的報告裡講明。
- 查不出定論的地方：保守改寫（不斷言），並在報告的「存疑」清單列出來。

### 更正標記（固定寫法，樣式已在 builder/templates/style.css）

```html
<mark class="fixnote" tabindex="0" data-note="原筆記此處寫「X」，查證後更正">更正後的正確敘述</mark><a class="fixsrc" href="查證出處網址" target="_blank" rel="noopener">出處</a>
```

- `data-note` 一定要寫出原筆記原本怎麼寫
- `fixsrc` 連到能直接驗證的那一頁，官方文件優先
- 不要自帶任何樣式；`tabindex="0"` 不能省（手機點一下靠它）

## 第 3 步：歸模組

- 明確吻合某個既有模組 → 直接歸入，**事後**在報告說明放哪、為什麼。
- 不確定、或不屬於任何既有模組 → **停下來問 Tim**（用 AskUserQuestion）：
  選項列出所有既有模組（各附一句為什麼合／不合），最後一項是「新增模組」，附建議的模組名稱與理由。
- **未經 Tim 點頭絕不新開模組。** 點頭之後的新開步驟：
  1. `content/modules.json` 的 `modules` 加 `{"id": "<新id>", "icon": "<一個表情符號>"}`
  2. 建 `content/<新id>/module.json`，欄位齊全：`title`、`intro`（卡片一句話簡介）、`kick`（總覽大標上的小字）、`overview_intro`（總覽開場段）、`footer_note`（總覽頁尾小字）、`lessons`（陣列）

## 第 4 步：防重複

- 掃過目標模組每一課的標題與「重點整理」，判斷新內容是否與某課高度重疊。
- 高度重疊時**不硬開新課，停下來問 Tim**（AskUserQuestion）：合併補強那一課，還是另立一課？兩個選項各附一句影響說明。
- 合併補強＝把新內容編進該課 `lesson.html` 的適當位置（更正標記照用），並視需要補測驗題（總數仍在 5〜10 題內）。

## 第 5 步：改寫成課程頁

新課的檔案（與既有課完全同款）：

- 資料夾：`content/<模組>/<NN-slug>/`，NN 是該模組的下一個序號（兩位數），slug 全小寫連字號。
- `lesson.html`：
  - 第一行：`<!-- 來源：<網址> · 收錄日期：YYYY-MM-DD -->`
  - 接著依序：learn 框、內文 section 們、keys 框；**不含 `<style>`**：

```html
<div class="learn"><p class="lbl">讀完這課你會</p><ul><li>…2〜3 條…</li></ul></div>
<section>
  <p class="era">段落小標（全形逗號隔開的短語）</p>
  <h3 class="head">段落標題</h3>
  <p>內文…</p>
</section>
<div class="keys"><p class="lbl">重點整理</p><ul><li>…3〜5 條…</li></ul></div>
```

  - 可用的內容類別（樣式都在模板裡）：`formula`（金句條）、`muted`（補充小字）、`q`（提問框）、
    `plainlist`、`ledger`＋`box`（對照卡）、`terms`＋`term`（名詞卡）、`tablewrap`＋表格、
    `card`／`badge`／`pit`／`pits`／`grid2`（Redis 課用過的元件）。
- `quiz.json`：`{"questions": [{"q": "…", "opts": ["正確答案", "誘答", "誘答", "誘答"], "exp": "…"}]}`
  - **5〜10 題，`opts[0]` 一定是正確答案**（前端會亂序）
  - 題目風格照既有課：考理解不考背誦、誘答項要合理、`exp` 一句話點出為什麼
- 圖片：**一律下載存進該課 `assets/`，不連外站的圖**。`lesson.html` 用相對路徑
  `assets/<課資料夾名>/<檔名>` 引用（builder 會把 `assets/` 搬到 `dist/<模組>/assets/<課資料夾名>/`）。
  示意圖（架構圖、流程圖）優先重畫成 inline SVG，風格照既有課的圖（白底卡片、暖色、Noto Sans TC）；
  照片與畫面截圖保留原檔。
- `content/<模組>/module.json` 的 `lessons` 加一筆：
  `{"dir": "<NN-slug>", "slug": "<slug>", "title": "課名", "desc": "一句話", "mins": <分鐘>, "group": "<沿用該模組的分組名，單課模組填空字串>"}`
  （mins 用字數估：每 400 字約 1 分鐘，加測驗約再 2 分鐘。）
- 文字風格：白話、比喻第一次出現用括號附正式名詞；照 Tim 的用詞規則
  （台灣講法、不發明編號代號、不造字、新名詞第一次出現附一句白話）。

寫完必跑、必須全綠才進第 6 步：

```bash
python3 -m unittest discover -s builder/tests -v
python3 builder/build.py
```

## 第 6 步：預覽確認（一定停，Tim 說 OK 才進第 7 步）

**本機環境**：build 後用 gstack 的 `/browse` 開
`dist/<模組>/index.html#/lesson/<slug>`，截圖給 Tim 看——課首、有更正標記的段落（滑過顯示提示的樣子）、測驗區。

**手機／雲端環境**（不能開本機檔案時）：把模組頁組成單一檔案，發成**私人 artifact** 給 Tim 手機看：

```bash
python3 - <<'EOF'
from pathlib import Path
mid = '模組id'   # ← 換成實際模組 id
d = Path('dist')
page = (d / mid / 'index.html').read_text(encoding='utf-8')
page = page.replace('<link rel="stylesheet" href="../style.css">',
                    '<style>' + (d / 'style.css').read_text(encoding='utf-8') + '</style>')
page = page.replace('<script src="../course.js"></script>',
                    '<script>' + (d / 'course.js').read_text(encoding='utf-8') + '</script>')
Path('/tmp/preview.html').write_text(page, encoding='utf-8')
print('寫好 /tmp/preview.html')
EOF
```

發佈 `/tmp/preview.html` 為 artifact（不公開分享）。預覽裡的登入同步不會動（外站程式被 artifact 環境擋掉），這是正常的，跟 Tim 講一聲。

Tim 要求修改就改，改完重新預覽；他說 OK 才往下。

## 第 7 步：push 發佈

```bash
git add content/
git commit -m "feat: 收錄〈課名〉進 <模組> 模組（來源：<來源網域>）"
git push
```

等自動部署（repo 是公開的，可輪詢
`https://api.github.com/repos/HHTim/notes-platform/actions/runs?per_page=1`
看最新一筆 `completed`/`success`），然後開
`https://hhtim.github.io/notes-platform/<模組>/#/lesson/<slug>` 確認上線。

## 最終報告（第 7 步之後給 Tim）

- 最終網址
- 歸類：放進哪個模組、課名、排在第幾課、為什麼
- 更正清單：每處一行——原筆記寫什麼 → 改成什麼 → 出處連結
- 測驗：幾題、各考什麼
- 存疑清單（查不出定論的地方；沒有就寫沒有）
````

- [ ] **步驟 1：建檔**

照上面的全文建 `.claude/skills/add-note/SKILL.md`（含 frontmatter，逐字）。

- [ ] **步驟 2：驗證**

```bash
python3 -m unittest discover -s builder/tests -v
```

預期：全綠（skill 是純文件，不影響建置）。另外自查一遍 SKILL.md：三個停問點都在、第 2 步明寫「不先徵詢」、新開模組的兩個檔案步驟齊全、更正標記寫法與任務 1 的樣式對得上（`fixnote`／`fixsrc`／`data-note`／`tabindex`）。

- [ ] **步驟 3：commit**

```bash
git add .claude/skills/add-note/
git commit -m "feat: /add-note skill——七步收錄流程（三個停問點、更正標記、內容慣例）"
```

---

### 任務 3：端對端驗收（與 Tim）

**Files:**
- Modify: `CLAUDE.md`（驗收通過後更新現況）

**Interfaces:**
- Consumes: 任務 1、2 的產出；Tim 提供的一篇 HackMD 筆記網址
- Produces: 規格第 9 節第三期的驗收：「丟一篇 HackMD 網址全流程跑通，網站多一課，更正處有標記」

- [ ] **步驟 1：先 push 任務 1、2 的 commit**，等部署綠（更正標記樣式要先上線，新課的頁面才渲染得對）。

- [ ] **步驟 2：請 Tim 丟一篇 HackMD 筆記的網址**（挑一篇內容可能有點舊的最好——才驗得到查證與更正標記）。

- [ ] **步驟 3：用 `/add-note` 跑完整七步**。過程照 SKILL.md，不走捷徑：查證要真的查、該停的三個點真的停、預覽真的給 Tim 看。

- [ ] **步驟 4：對規格驗收條件逐項檢查**：
  - 網站多一課（線上網址開得起來、側欄與總覽有它、測驗可作答）
  - 更正處有標記（底色可辨、出處連結有效、滑過／點一下顯示原筆記寫什麼）
  - 報告含更正清單與歸類說明

- [ ] **步驟 5：Tim 說驗收通過後**，更新 `CLAUDE.md` 現況（第三期完成；三期全數完成，進入日常使用——把 HackMD 舊筆記逐篇餵給 `/add-note`），commit＋push。

---

## 驗收對照（規格第 9 節「第三期」）

| 規格要求 | 由誰證明 |
|---|---|
| 七步流程做成 skill | 任務 2（SKILL.md 全文）＋任務 3 步驟 3 實跑 |
| 丟一篇 HackMD 網址全流程跑通 | 任務 3 步驟 3 |
| 網站多一課 | 任務 3 步驟 4 |
| 更正處有標記 | 任務 1（樣式）＋任務 3 步驟 4 |
| 三個停問點、查證不停 | SKILL.md 明文＋任務 3 實跑觀察 |

## 刻意的取捨（不要當成 bug）

1. **更正標記的提示不用 JavaScript**：純 CSS（`:hover`／`:focus` 顯示 `data-note`），少一個維護點；代價是提示框樣式簡單，夠用。
2. **skill 不做成程式**，是操作規程文件：七步的每一步都需要判斷（查證、改寫、出題），本來就是給 Claude 執行的，不是給腳本執行的。
3. **mins 用字數估**不精算：每 400 字約 1 分鐘，個人站夠用。
4. **雲端預覽的登入同步不會動**（artifact 環境擋外站程式）：預覽是看內容，不是測同步——第二期已驗收過同步。
