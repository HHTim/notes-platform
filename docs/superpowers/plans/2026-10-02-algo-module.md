# 資料結構與演算法模組：計畫與進度

規格：`docs/superpowers/specs/2026-10-02-algo-module-design.md`。

**Tim 交代（10-02）：不用留用量給他；用量用完就等重置後繼續；需要決定的地方都照主控的建議；做到 2026-10-05 09:00 停止。他用手機看網站更新。**

斷線或重置後接手的人：先看下面進度表，照「下一步」欄接著做。審查清單一律存在 `.superpowers/audit/algo/findings-<資料夾>.md`（不進 git）。

## 進度（主控維護）

| 課 | 寫課 | 審查 | 修正與複審 | 上線 |
|---|---|---|---|---|
| `01-complexity` | 撰寫中（10-02，Opus `write-algo-a`） | | | |
| `02-array-string` | 撰寫中（10-02，Opus `write-algo-a`） | | | |
| `03-hash-table` | 撰寫中（10-02，Opus `write-algo-b`） | | | |
| `04-linked-list` | 撰寫中（10-02，Opus `write-algo-b`） | | | |
| `05-stack-queue` | 撰寫中（10-02，Opus `write-algo-c`） | | | |
| `06-recursion-backtracking` | 撰寫中（10-02，Opus `write-algo-c`） | | | |
| `07-sorting-binary-search` | | | | |
| `08-two-pointers-window` | | | | |
| `09-tree-bst` | | | | |
| `10-heap` | | | | |
| `11-graph` | | | | |
| `12-dynamic-programming` | | | | |
| `13-interview-strategy` | | | | |

流程照多益文法：寫課 → 獨立審查 → 交回原寫課代理修正 → 原審查者範圍複審 → 主控修小尾巴、註冊、推。兩課審好就先上線。同時跑的代理約四到五個。

## 寫課守則（每個寫課代理照做）

**先照多益文法第二批的寫課守則 11 條**（`docs/superpowers/plans/2026-10-02-toeic-grammar-batch2.md`「寫課守則」）——正解唯一、陷阱錯在考點、解析不用位置指選項、規則不說得比出處多、沒有官方出處的「面試最常考」改建議語氣、用詞、出處附英文原句、跨課一致、選項長度不洩題、SVG id 不重複、長度。另外加這幾條：

1. **程式碼一定實跑。** 每段 Java 程式碼放進完整的類別用 `javac` 編譯、`java` 執行（Java 25；若本機只有 21 就用 21 並在回報說明），課文寫的輸出要跟實跑一致。只是片段的，也要包成能編譯的類別測過。
2. **複雜度主張要撐得住。** 「`HashMap.get` 平均 O(1)」「`ArrayList.add` 攤銷 O(1)」「`Arrays.sort` 對基本型別用雙軸快速排序、對物件用 TimSort」這類講實作或複雜度的句子，掛 Java API 文件或 OpenJDK 原始碼（固定版本標籤）；一般演算法的複雜度掛 algs4 或 MIT 6.006。最壞、平均、攤銷要分清楚，不要混用。
3. **LeetCode 只列題號與英文題名、連到題目頁**（`https://leetcode.com/problems/<slug>/`），不抄題目敘述、不貼官方解答。課中練習的題目全部自編。
4. **白話優先、15 歲看得懂**：每個資料結構先用生活比喻講（第一次出現時括號附正式名稱），再上圖、再上程式碼。術語第一次出現附白話（例如「攤銷（把偶爾一次很貴的成本平均分攤到每次操作）」）。
5. **課中練習的題型**：複雜度判斷、程式輸出、操作後的狀態（例如「push 三次 pop 一次後頂端是什麼」）、該選哪種資料結構、演算法下一步。程式碼放題幹裡用 `<pre><code>`，題幹程式要短（10 行內）。不要考背誦 API 名稱。
6. **跨課指路**：只寫課名。指到 Java 模組（例如〈集合與泛型〉）或面試集（例如〈Java 進階快答：JVM 記憶體、垃圾回收與類別載入〉）也只寫課名；寫之前先打開那課確認講法一致，重疊的指路不重講。
7. **動手練清單**：每課最後一段，5〜8 題 LeetCode，表格欄位「題號＋題名（連結）／考這課的哪一招／難度」，先易後難。

## 圖的共同畫法（全模組一致）

SVG 一律 `role="img"` 加中文 `aria-label`；`id` 用課的前綴（`cx-`、`ar-`、`ht-`、`ll-`、`sq-`、`rc-`、`so-`、`tp-`、`tr-`、`hp-`、`gr-`、`dp-`、`is-`）加流水號，全模組不重複。文字自己寫 `fill` 才會上色（樣式表只在沒寫 fill 時套文字色）。

- **陣列格子**：寬 56、高 40 的方格，`fill="var(--surface)" stroke="currentColor"`，格內置中放值（`class="mono"`、14px）；格子下方 12px 灰字放索引 `0 1 2 …`（`opacity=".6"`）。被比較或正在處理的格子 `fill="var(--gold-soft)" stroke="var(--gold)"`。
- **指標**（雙指標、目前位置）：格子上方的小三角形或文字標籤 `i`、`j`、`left`、`right`，古銅色 `fill="var(--gold-deep)"`。
- **節點與箭頭**（鏈結串列、樹、圖）：節點是圓角方塊（鏈結串列）或圓（樹、圖，r=20），`fill="var(--surface)" stroke="currentColor"`；指向用 `currentColor` 線加箭頭 marker；`null` 用灰字。
- **重點節點**：古銅（`var(--gold)`）表示「正在處理」，灰藍（`var(--slate)`、`var(--slate-soft)`）表示「已處理過／已拜訪」。
- **圖下方 `<figcaption>`** 一句中文說明。
- 寬度 `viewBox` 以 760 為準（手機上會保持 600px、框內左右滑）。

## 下一步（主控）

1. 第一波：派 3 個寫課代理，各寫 2 課（01＋02、03＋04、05＋06）。
2. 寫好一組就派審查，審查與下一波寫課交錯（07＋08、09＋10、11＋12、13）。
3. 第一組通過時建立 `content/algo/module.json` 並加進 `content/modules.json`（id `algo`、圖示 🧮、放在 interview 後面）。
