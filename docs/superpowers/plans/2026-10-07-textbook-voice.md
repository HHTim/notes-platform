# 改成教科書寫法：不寫「某某說」（2026-10-07）

Tim 附兩張截圖（〈代名詞與主詞動詞一致〉的「根據：英國文化協會說……劍橋：……」、〈名詞、冠詞與數量詞〉的「劍橋：「單位詞讓我們……」（Piece words…）」）：

> 「類似這種什麼劍橋說，我根本不會想看，你應該參照各種教科書或文法書，看如何呈現給使用者讓使用者想看，或者用列點式，所有這種敘述全部都改掉，各個模組都是，不限於英文」

## 標準

教科書直接講規則、給例子，不轉述「誰說了什麼」。出處只留右上角那個「出處」小連結，給要查的人點。

1. **不在正文點名來源**：「劍橋說」「劍橋：」「英國文化協會提醒」「根據：」「表的根據：」「官方文件說」「API 文件原句」「JLS 說」「OWASP：」「fork(2) 手冊：」「Spring Boot 文件寫」這類全部拿掉，把內容直接寫成規則或事實，句尾接 `<a class="fixsrc">出處</a>`。
2. **拿掉英文原句**：括號裡的英文原句 `（We use …）` 和 `<span class="orig">…</span>` 小灰字都刪（span 裡的出處連結移出來放句尾）。英文本身就是教學內容時留下，放 `<code>`：例句、片語、指令、設定名、API 名。
3. **不用「」包轉述**：轉述來源的話不加引號，用自己的話寫短。「」只留給中文名詞、要特別指出的字眼。
4. **能列就列**：規則一句 → 例子條列；對錯對照寫成 `✗ <code>錯的</code> → ✓ <code>對的</code>`；三項以上的比較用表格。一條 `<li>` 一件事。
5. **整段只是在交代表格出處的**（例如「表的根據：……」）：縮成一行 `<p class="muted">出處：<a class="fixsrc" …>英國文化協會</a>、<a class="fixsrc" …>劍橋</a></p>`，連結文字可以是來源名稱；表格裡沒講到、但這段補充的規則，搬成正文一條。
6. **術語別名**：「這課把劍橋說的 possessive determiner 叫所有格形容詞」→「所有格形容詞（my、your 這類）有些書叫 possessive determiner」。

## 不能動的

- **知識內容與保留語氣**：保留條件、例外、版本（「Spring Boot 3.4 起」）、數字、「通常」「多數時候」這類程度詞。「口語常聽到 A，但比較正確是 B」→ 寫成「口語常聽到 A，考試與書面用 B」，不能變成「A 是錯的」。見記憶 `rewrite-preserve-reservation`。
- **來源本身有爭議、或兩個來源說法不同時**：可以點名，但只用一短句，例如「英式與美式字典標法不同，考試照美式」。
- **更正標記** `<mark class="fixnote" title="…">`：標籤與 title 不動，標籤裡的字可以照本標準改寫，意思不能變。
- 每個 `fixsrc` 連結都要留（可以移位置、可以合併同網址相鄰的兩個）。
- 檔案第一行 `<!-- 來源：… -->`。
- `quiz.json` 的 `exp` 也照這個標準改；選項文字不動。課中練習的 `dexp` 一樣。

## 範例（已改，`content/english/04`、`05`）

改前：
> 劍橋：「單位詞讓我們能說一個或幾個單位的不可數東西」（Piece words make it possible …），常用的有 piece、bit、item、article，後面接 of。出處 所以「一件設備」是 a piece of equipment……但英國文化協會提醒「accommodation、money、traffic 不能用這種方式變可數」（However, …），要換說法……

改後：
> 不可數名詞要數，前面加單位詞（piece、bit、item、article）＋ of：出處
> - 一件設備：`a piece of equipment`
> - 兩件家具：`two items of furniture`
> - 一個建議：`a piece of advice`
>
> 例外：accommodation、money、traffic 不能這樣數，要換說法：出處
> - ✗ `three pieces of money` → ✓ `three large sums of money`
> - ✗ `two pieces of traffic` → ✓ `two traffic jams`

技術模組的例子：
> 改前：危險在 Redis 用單一執行緒處理指令：「當一個請求很慢，所有其他用戶端都得等它」。<span class="orig">Redis 延遲文件：when a request is slow…</span>
> 改後：危險在 Redis 用單一執行緒處理指令，一個慢指令會讓其他用戶端全部排隊等。出處

## 檢查工具

`python3 .superpowers/audit/attrib/scan.py <模組>` 列出還在「某某說／英文原句／小灰字」的行。它只是找人工要看的地方，會有誤判（例如「說明」這個詞本身）；目標是每一處都看過，該改的改掉，不是把數字歸零。

## 做法

- 每人負責一批，只改自己那批的 `lesson.html` 與 `quiz.json`。
- 改完跑 `python3 -m unittest discover -s builder/tests` 與 `python3 builder/build.py`，只 `git add` 自己改的檔，commit 訊息「docs(<模組>): 改成教科書寫法」，不 push；遇到 index.lock 等幾秒重試。
- 回報：改了幾課、scan.py 前後各幾處、留下沒改的是哪類（一句話）。

## 分工與進度

| 範圍 | 負責 | 狀態 |
|---|---|---|
| 英文 03〜11 | `tv-en-a` | ✅ `2cfec3f`（9 課，312→4 處） |
| 英文 01、02、12〜21 | `tv-en-b` | ✅ `6acff3b`（11 課，526→9 處） |
| Spring | `tv-spring` | ✅ `dd8d3b6`（20 課，410→15 處） |
| 面試集 | `tv-interview` | ✅ `400f117`（23 課，297→18 處） |
| 演算法、Angular | `tv-algo` | ✅ `c542513`（演算法 15 課；Angular 不用改；271→8 處） |
| Java | `tv-java` | ✅ `a00ad8a`（16 課，276→19 處） |
| 網頁 | `tv-web` | ✅ `9e5b802`（9 課，276→16 處） |
| 資料庫、AI 工具 | `tv-db` | ✅ `d870d8d`（8 課，268→7 處） |
| K8s、雲端 | `tv-k8s` | ✅ `8ccd0e8`（32 課，244→21 處） |
| 漏網收尾（scan.py 加「中文來源名」：指南：、官方寫、MDN：） | `tv-sweep` | ✅ `8527890`（40 檔） |
| 改完抽查（知識內容與保留語氣有沒有被改掉、出處連結有沒有掉） | `tv-review` | ✅ `38848c5`（抽 33 課、修 18 處：12 處語氣被說滿、6 處寫壞）；主控補兩處：web 11 改回「規格預期」、spring 18 標明是 Pact 的主張 |
