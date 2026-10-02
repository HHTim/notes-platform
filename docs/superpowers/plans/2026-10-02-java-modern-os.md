# Java 現代寫法與作業系統基礎：計畫與進度

**Tim 交代（10-02）：不用留用量給他；用量用完就等重置後繼續；需要決定的地方都照主控的建議；做到 2026-10-05 09:00 停止。**

缺口分析（10-02）：Java 模組素材停在 Java 8〜11 的年代，lambda、Stream、Optional 只零星提到，沒有一課正式教；作業系統只有 Java 第 10 課一段比喻。主控照建議拍板：

- Java 模組新增 4 課（分組「現代 Java」與「作業系統」），依官方文件新寫（零 fixnote、零 data-note、每個主張附出處），以 **Java 21（LTS）為主軸、標出 25 的差異**（本機只有 Java 21，25 的範例用 Docker `eclipse-temurin:25` 跑）。
- 面試集新增 1 課快答，把上面 4 課的面試題整理成問答形狀。
- 有課中練習（`<div class="drill">`），每課 40〜55 題；課末測驗 10 題。
- 寫課守則：照 `docs/superpowers/plans/2026-10-02-algo-module.md` 的守則（它包含多益文法第二批的 11 條，加上程式碼一定實跑等 7 條）。出處以 Oracle Java SE 21／25 API 文件、Java Language Specification、dev.java 教學、OpenJDK JEP 頁為主；作業系統以 man7.org Linux 手冊與 OSTEP（ostep.org，免費教科書）為主。

## 課程表

| 資料夾 | 課名 | 分組 |
|---|---|---|
| `content/java/12-lambda-functional` | Lambda 與函式介面 | 現代 Java |
| `content/java/13-stream-api` | Stream API：把迴圈寫成資料流 | 現代 Java |
| `content/java/14-modern-syntax` | 現代 Java 語法：var、record、switch、文字區塊與 sealed | 現代 Java |
| `content/java/15-os-process-io` | 作業系統怎麼跑程式：行程、執行緒、記憶體與 I/O | 作業系統 |
| `content/interview/17-java-modern-qa` | Java 現代語法快答：Lambda、Stream、Optional 與 record | Java |

## 進度（主控維護）

| 課 | 寫課 | 審查 | 修正與複審 | 上線 |
|---|---|---|---|---|
| `java/12-lambda-functional` | ✅ `86ea72a`＋`075d33e`（55 題；mins 55） | ✅ 10-02 審完：132 題正解都唯一（三題只在 JDK 實作上唯一，要標明實跑）；出處連結裡塞了 wbr 點不開；測驗正解太常最長；清單 `.superpowers/audit/java/findings-12-13.md`；修正交給 `fix-java-1213` | ✅ 10-02 上線 |
| `java/13-stream-api` | ✅ `c09e024`（57 題；mins 55） | 同上 | ✅ 10-02 上線 |
| `java/14-modern-syntax` | 撰寫中（`write-java-a` 第二輪） | | | |
| `java/15-os-process-io` | 撰寫中（`write-java-a` 第二輪） | | | |
| `interview/17-java-modern-qa` | | | | |

## 同一輪加做（10-02 主控照缺口分析排）

| 課 | 寫課 | 審查 | 修正與複審 | 上線 |
|---|---|---|---|---|
| `interview/17-java-modern-qa` 見上表 | ✅ `7957332`（14 題、15 個實跑類別；mins 18） | 審查中（`review-algo-c`） | | |
| `web/09-git-branching` Git 分支與協作 | 撰寫中（`write-algo-c` 轉做） | | | |
| `web/10-cicd-pipeline` CI/CD：從 push 到上線 | 撰寫中（`write-algo-d` 轉做） | | | |

Git 與 CI/CD 兩課放網頁模組，分組「開發流程」（跟〈軟體開發生命週期〉同組）；出處以 Pro Git（git-scm.com/book）與 GitHub Docs 為主；CI/CD 以本站自己的 `.github/workflows/deploy.yml` 當範例。
