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
