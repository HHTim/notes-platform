# 多益文法教材設計（2026-10-02 Tim 拍板）

Tim 的交代：「我認為我的英文不夠，我需要一份文法書，能夠完全掌握多益必考的文法……尤其是時態需要圖解＆大量例句、大量練習」。

## 拍板的三件事

1. **放進現有的「英文」模組**（不另開模組）。原本兩課歸分組「片語與口語」，文法課接在後面。
2. **練習形式**：課文內穿插「課中練習」（點選項馬上看對錯與解析，不計分、不記錄）＋課末測驗 10 題（全對打勾，沿用現有）。一課約 40〜60 題，時態課多放。
3. **從句子結構教起**，共 18 課。

## 課程表（資料夾編號＝最終課序；英文模組第 3〜20 課）

| 分組 | 資料夾 | 課名 |
|---|---|---|
| 句子基礎 | `03-grammar-sentence` | 詞性與句子骨架：五大句型與「這格填什麼詞性」 |
| 句子基礎 | `04-grammar-nouns` | 名詞、冠詞與數量詞 |
| 句子基礎 | `05-grammar-pronouns-agreement` | 代名詞與主詞動詞一致 |
| 時態 | `06-tense-simple` | 時間軸怎麼看＋簡單式三態 |
| 時態 | `07-tense-progressive` | 進行式三態 |
| 時態 | `08-tense-perfect` | 完成式三態：現在完成式對過去式 |
| 時態 | `09-tense-future-review` | 完成進行式、未來的各種說法與時態總整理 |
| 動詞的變化 | `10-grammar-passive` | 被動語態 |
| 動詞的變化 | `11-grammar-modals` | 助動詞 |
| 動詞的變化 | `12-grammar-infinitive-gerund` | 不定詞與動名詞 |
| 動詞的變化 | `13-grammar-participles` | 分詞與分詞構句 |
| 修飾與連接 | `14-grammar-adj-adv` | 形容詞與副詞（含比較級） |
| 修飾與連接 | `15-grammar-prepositions` | 介系詞 |
| 修飾與連接 | `16-grammar-conjunctions` | 連接詞與連接副詞 |
| 子句與特殊句型 | `17-grammar-relative` | 關係詞 |
| 子句與特殊句型 | `18-grammar-noun-clauses` | 名詞子句 |
| 子句與特殊句型 | `19-grammar-conditionals` | 假設語氣 |
| 子句與特殊句型 | `20-grammar-inversion-strategy` | 倒裝與省略＋多益文法題解題順序 |

英文模組內的指路**只寫課名不寫課序**（分批上線時課序會變）。

## 每課的內容規格

- 每條規則先用中文白話講，再給 5〜10 個例句；例句用多益的職場情境（開會、出貨、請款、徵才、出差），全部自編。
- 每條可驗證的文法規則掛 `fixsrc` 出處，以 Cambridge Dictionary 文法說明（dictionary.cambridge.org/grammar/british-grammar/）與 British Council LearnEnglish 文法頁為主；多益題型描述引 ETS 官網。英文原句括號附在中文翻譯後。
- **ETS 考古題有版權，練習題全部自編**；不抄任何參考書或題庫網站的題目。
- 時態每一個都有一張時間軸圖（inline SVG，畫法見計畫檔的範本），十二個時態同一套畫法。
- 課中練習：每個觀念後 5〜10 題四選一，多益閱讀第五部分（句子填空）的形狀。選項位置要分散，不要老是同一格。
- 課末測驗 10 題，`opts[0]` 正確（頁面會重排），正確答案不總是最長或最短。
- 零 `fixnote`、零 `data-note`（依官方文件新寫的課）；不寫第一人稱、不寫工作紀錄。
- 長度：中文講解不設硬上限（例句與練習是英文，不算字數），但每課讀加做練習抓 25〜40 分鐘；`mins` 依實際題量估。

## 網站改動（已做，2026-10-02）

- `builder/build.py`：`DrillChecker`／`drill_errors()`——每題正解剛好一個、要有解析、選項 2〜5 個，否則建置中止並指出課與行號。
- `builder/templates/course.js`：`initDrills()` 讓選項可點（也可用鍵盤 Enter／空白鍵），點下去公布對錯與解析。
- `builder/templates/style.css`：課中練習樣式，題號用 CSS 計數器自動編「練習 1、2…」，每課重新算。
- 課中練習的寫法：

```html
<div class="drill">
  <p class="dq">The shipment ______ yesterday afternoon.</p>
  <ul class="dopts"><li>arrive</li><li data-ok>arrived</li><li>has arrived</li><li>is arriving</li></ul>
  <p class="dexp"><span class="dtr">整句：貨昨天下午到了。</span>yesterday afternoon 是過去的時間點，用過去簡單式。</p>
</div>
```

- 題目有英文句子時，解析最前面放整句中譯 `<span class="dtr">整句：…</span>`（空格填正解再翻，答完才看得到）。2026-10-08 起全部文法課都有，起因是 Tim 朋友的多益站有這個功能。

## 分批

- **第一批**：課中練習功能＋`03-grammar-sentence`＋時態四課（06〜09）。上線後 Tim 先看圖解與練習的感覺，覺得對再做其他 13 課。
- 每課照面試課的流程：寫課 → 獨立審查 → 修正 → 範圍複審 → 註冊上線。
- 同時跑的代理不超過三個；Tim 叫停就全部停。
