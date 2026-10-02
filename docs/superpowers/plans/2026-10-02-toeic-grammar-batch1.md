# 多益文法第一批：句子骨架＋時態四課

規格：`docs/superpowers/specs/2026-10-02-toeic-grammar-design.md`。

## 進度（主控維護）

| 課 | 寫課 | 審查 | 修正與複審 | 上線 |
|---|---|---|---|---|
| 課中練習功能 | ✅ 10-02（`DrillChecker`、`initDrills()`、樣式；34 項測試通過） | — | — | ✅ 10-02 |
| 手機上的圖可左右滑 | ✅ `cc224dd`（審查發現 760 寬的時態圖在手機上字只剩約 5px；窄於 640px 時圖保持 600px 寬、框內左右滑） | — | — | ✅ 10-02 |
| 圖上文字顏色修正 | ✅ `4ef613e`（寫課代理發現 `svg text{fill:currentColor}` 蓋掉所有圖上自訂的文字顏色；改成只在沒寫 fill 時套用，既有 20 課的圖也恢復古銅、灰藍標籤） | — | — | ✅ 10-02 |
| `03-grammar-sentence` 詞性與句子骨架 | ✅ `bed73e6`（53 題課中練習、52 出處／30 網址用 Playwright 逐頁核過、mins 38；沒有圖、全用表格） | ✅ 10-02 審完：63 題正解全部唯一；錯誤 5（-le 結尾副詞、「一組有時態的動詞」自相矛盾、make／keep 句尾填形容詞、重點整理「動詞後面填副詞」、sales figures 反例）、不精確 9、用詞 2、體例 2；清單在 `.superpowers/audit/english/findings-sentence.md`；修正交回原寫課代理 | ✅ 修正 `f517205`（18 條全改、零駁回；work 換 fall 而非 occur——表下註明字例都在劍橋同一頁）；範圍複審 ✅ 18 條全改對、fall 比原建議好；兩條小尾巴（加「同一個主詞」前提、例外補 leave）主控順手修 | ✅ 10-02 一起上線 | | |
| `06-tense-simple` 時間軸怎麼看＋簡單式三態 | ✅ `f0a87f9`（57 題課中練習、5 張圖含圖例、24 出處／20 網址；mins 42） | ✅ 10-02 審完（06＋07）：3 題正解不唯一（cafeteria doesn't open、Mr. Wang will miss、Mr. Tsai worked）、-ed／-ing 雙寫規則兩課打架、時間子句的例外、不規則動詞背法漏 4 字、虛線穿過動作標籤；清單在 `.superpowers/audit/english/findings-tense1.md`；修正交回原寫課代理 | ✅ 修正 `14788a2`（16 條全改；蔡先生題換誘答而非補線索；三張圖的動作標籤移到點的右側）；範圍複審 ✅ 可上線；07 測驗第 2、3、5 題陷阱選項改成真正的時態錯誤（主控改） | ✅ 10-02 一起上線 |
| `07-tense-progressive` 進行式三態 | ✅ `d8578ba`（53 題課中練習、6 張圖、28 出處／15 網址；mins 40） | 同上 | | |
| `08-tense-perfect` 完成式三態 | ✅ `71e3071`（60 題課中練習、7 張圖、40 出處；mins 45） | ✅ 10-02 審完（08＋09）：錯誤 10（7 題正解不唯一、解析用「第一句」指位置但測驗會重排、重點整理說 start 不用進行式、When 問句太絕對）、不精確 12、用詞 4、體例 3；清單在 `.superpowers/audit/english/findings-tense2.md`；長度超規格主控決定接受；修正交回原寫課代理。順帶全站掃「第幾個選項」，抓到並修好行為面試課測驗一處 | ✅ 修正 `eb9991c`（08＋09 一起；10 條錯誤全改；the first time 照劍橋條件寫而非「主要子句是 This is」；When 問句標成解題建議；未來說法縮短、練習改 12 題；7 張圖照新範本改）；範圍複審 ✅ 10 條全改對、兩處反駁成立；五個小尾巴主控順手修 | ✅ 10-02 與 03、06、07 一起註冊上線（英文模組第 3〜7 課） |
| `09-tense-future-review` 完成進行式、未來與時態總整理 | ✅ `5f750b5`（70 題課中練習含 24 題綜合、4 張圖＋總表 12 個小圖示、46 出處；mins 50） | 同上 | | |

## 時間軸圖的共同畫法（四課時態必須一致）

整個模組的所有課在**同一個 HTML 頁**裡，SVG 的 `id`（例如 `<marker id=…>`）全模組不能重複：一律加課的前綴，例如 `ts-arr`（simple）、`tp-arr`（progressive）、`tf-arr`（perfect）、`tr-arr`（future-review）。

- `viewBox="0 0 760 170"`，`role="img"`，`aria-label` 用一句中文講這張圖在說什麼。
- 時間軸：`y=110` 從 `x=30` 到 `x=730` 的灰線（`currentColor`、`stroke-opacity=".45"`、寬 2），右端箭頭；左下 `過去`、右下 `未來`（`font-size=12`、`opacity=.6`）。
- 「現在」：`x=380` 的直線（`stroke="currentColor"`、寬 2），上方標 `現在 now`。
- **一次性動作（點）**：古銅實心圓 `r=7`、`fill="var(--gold)"`，上方標動作（英文例句的動詞，`class="mono"`）。
- **持續中／進行中（段）**：灰藍色條 `fill="var(--slate-soft)" stroke="var(--slate)"`，高 18、以軸線為中心；進行式的段在參考時間點那一刻要涵蓋到它（參考點落在段中間）。
- **反覆（習慣）**：同一條軸上 5〜7 個小古銅圓 `r=4`，間距相等，左右兩端各一個淡化（`opacity=.4`）表示「一直這樣」。
- **參考時間點（過去某時、未來某時）**：灰藍虛線直線 `stroke-dasharray="5 4"`，**從軸線上方一點（y≈96）畫到軸線下方，時間標在軸線下方**（例如 `yesterday 3 p.m.`、`by Friday`），不要穿過上方的動作標籤（第一批審查抓到虛線把 "will｜call" 切開）。
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
  <line x1="200" y1="96" x2="200" y2="130" stroke="var(--slate)" stroke-dasharray="5 4"/>
  <text x="200" y="148" font-size="12" text-anchor="middle" fill="var(--slate)" class="mono">last Monday</text>
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
