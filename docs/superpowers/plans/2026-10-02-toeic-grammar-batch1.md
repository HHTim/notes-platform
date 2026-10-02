# 多益文法第一批：句子骨架＋時態四課

規格：`docs/superpowers/specs/2026-10-02-toeic-grammar-design.md`。

## 進度（主控維護）

| 課 | 寫課 | 審查 | 修正與複審 | 上線 |
|---|---|---|---|---|
| 課中練習功能 | ✅ 10-02（`DrillChecker`、`initDrills()`、樣式；34 項測試通過） | — | — | 隨第一批一起推 |
| `03-grammar-sentence` 詞性與句子骨架 | | | | |
| `06-tense-simple` 時間軸怎麼看＋簡單式三態 | | | | |
| `07-tense-progressive` 進行式三態 | | | | |
| `08-tense-perfect` 完成式三態 | | | | |
| `09-tense-future-review` 完成進行式、未來與時態總整理 | | | | |

## 時間軸圖的共同畫法（四課時態必須一致）

整個模組的所有課在**同一個 HTML 頁**裡，SVG 的 `id`（例如 `<marker id=…>`）全模組不能重複：一律加課的前綴，例如 `ts-arr`（simple）、`tp-arr`（progressive）、`tf-arr`（perfect）、`tr-arr`（future-review）。

- `viewBox="0 0 760 170"`，`role="img"`，`aria-label` 用一句中文講這張圖在說什麼。
- 時間軸：`y=110` 從 `x=30` 到 `x=730` 的灰線（`currentColor`、`stroke-opacity=".45"`、寬 2），右端箭頭；左下 `過去`、右下 `未來`（`font-size=12`、`opacity=.6`）。
- 「現在」：`x=380` 的直線（`stroke="currentColor"`、寬 2），上方標 `現在 now`。
- **一次性動作（點）**：古銅實心圓 `r=7`、`fill="var(--gold)"`，上方標動作（英文例句的動詞，`class="mono"`）。
- **持續中／進行中（段）**：灰藍色條 `fill="var(--slate-soft)" stroke="var(--slate)"`，高 18、以軸線為中心；進行式的段在參考時間點那一刻要涵蓋到它（參考點落在段中間）。
- **反覆（習慣）**：同一條軸上 5〜7 個小古銅圓 `r=4`，間距相等，左右兩端各一個淡化（`opacity=.4`）表示「一直這樣」。
- **參考時間點（過去某時、未來某時）**：灰藍虛線直線 `stroke-dasharray="5 4"`，上方標時間（例如 `yesterday 3 p.m.`、`by Friday`）。
- **「一直到參考點」的關係（完成式的核心）**：古銅色箭頭從動作的點或段的起點畫到參考點那條線，箭頭線上方標 `到那時為止`（現在完成式標 `到現在為止`）。
- 圖下方 `<figcaption>`：一句中文說明，加一個英文例句。

範本（過去簡單式＋現在完成式並排，複製後改）：

```html
<figure>
<svg viewBox="0 0 760 170" role="img" aria-label="過去簡單式：過去的某一點發生、已經結束，跟現在沒有連在一起">
  <defs><marker id="ts-arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="currentColor"/></marker></defs>
  <line x1="30" y1="110" x2="730" y2="110" stroke="currentColor" stroke-opacity=".45" stroke-width="2" marker-end="url(#ts-arr)"/>
  <text x="30" y="140" font-size="12" opacity=".6">過去</text>
  <text x="700" y="140" font-size="12" opacity=".6">未來</text>
  <line x1="380" y1="60" x2="380" y2="130" stroke="currentColor" stroke-width="2"/>
  <text x="380" y="50" font-size="12.5" text-anchor="middle">現在 now</text>
  <circle cx="200" cy="110" r="7" fill="var(--gold)"/>
  <text x="200" y="88" font-size="13" text-anchor="middle" class="mono" fill="var(--gold-deep)">shipped</text>
  <line x1="200" y1="60" x2="200" y2="130" stroke="var(--slate)" stroke-dasharray="5 4"/>
  <text x="200" y="50" font-size="12" text-anchor="middle" fill="var(--slate)" class="mono">last Monday</text>
</svg>
<figcaption>過去簡單式：過去某個時間點發生、已經結束。We shipped the order last Monday.</figcaption>
</figure>
```

## 給寫課代理的共同交代

- 規格檔全文照做；課中練習寫法、出處規則、版權（題目全部自編、不抄 ETS 與參考書）都在裡面。
- 每課結構：`learn` 框 3〜4 條 → 各段講解（例句 5〜10 個）→ 每段後接課中練習 5〜10 題 → `keys` 重點整理 4〜7 條。課末測驗 10 題放 `quiz.json`。
- 中文講解照 Tim 的用詞規則（`~/.claude/tim-style/RULES.md`、`china-terms.md`）：文法術語第一次出現附白話（例如「及物動詞（後面一定要接受詞的動詞）」），不造字、不發明編號代號。台灣慣用的文法術語：現在式、過去式、現在完成式、進行式、被動語態、不定詞、動名詞、分詞、關係代名詞、假設語氣、主詞、動詞、受詞、補語。
- 例句全部自編、職場情境；不出現真實公司與人名。
- 出處：Cambridge Dictionary 文法頁、British Council LearnEnglish 文法頁；每個網址自己開過、200、引的那句在頁上（這兩站有時擋自動抓取——curl 不行就用 WebFetch 或 Playwright MCP）。
- 驗收：`git archive HEAD` 副本加入自己的資料夾、副本的 `content/english/module.json` 暫加那筆，跑 `python3 -m unittest discover -s builder/tests` 與 `python3 builder/build.py`（建置會檢查課中練習的正解與解析）。
- 只 `git add` 自己的資料夾；不動真正的 `module.json`；不 push；不派子代理。
