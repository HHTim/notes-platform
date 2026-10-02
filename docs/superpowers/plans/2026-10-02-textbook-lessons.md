# 教材課（把面試集速查展開成完整教材）：計畫與進度

**Tim 交代（10-02）：不用留用量給他；用量用完就等重置後繼續；需要決定的地方都照主控的建議；做到 2026-10-05 09:00 停止。**

來源：`docs/superpowers/plans/2026-09-29-roadmap-expansion.md` 第三部分。面試集是「速查」，教材課是「打底」：面試集那課講到哪、這課從哪裡展開，寫完後回頭把面試集那課對應的題目加一句指路。

寫課守則：`docs/superpowers/plans/2026-10-02-algo-module.md` 的「寫課守則」（含 batch2 的 11 條，加程式碼一定實跑、課中練習）。每課有課中練習 40〜55 題＋課末測驗 10 題；依官方文件新寫（零 fixnote、零 data-note）；出處附英文原句。

已在別的計畫做掉的：作業系統（`java/15-os-process-io`）、CI/CD（`web/10-cicd-pipeline`）、Git（`web/09-git-branching`）。

## 課程表與進度（最急的 8 課）

| 資料夾 | 課名 | 分組 | 對應面試集 | 寫課 | 審查 | 修正與複審 | 上線 |
|---|---|---|---|---|---|---|---|
| `database/06-index-internals` | 索引是怎麼運作的 | （新）效能 | 〈資料庫面試題：索引、交易隔離與鎖〉 | 撰寫中（`write-algo-b`） | | | |
| `database/07-transaction-isolation-locks` | 交易隔離層級與鎖 | （新）效能 | 同上 | 撰寫中（`write-algo-b`） | | | |
| `java/16-jvm-memory-gc` | JVM 記憶體與垃圾回收 | （新）JVM 與效能 | 〈Java 進階快答：JVM 記憶體、垃圾回收與類別載入〉 | 撰寫中（`write-java-a`） | | | |
| `java/17-thread-pool-concurrency` | 執行緒池與並行工具 | 並行與設計 | 〈Java 並行快答：執行緒池、鎖與並行集合〉 | 撰寫中（`write-java-a`） | | | |
| `spring/13-transactional-propagation` | @Transactional 的傳播、隔離與失效情境 | （新）進階 | 〈Spring 面試快答：IoC、Bean、AOP 與交易〉 | 撰寫中（`write-algo-a`） | | | |
| `spring/14-boot-autoconfig-actuator` | Spring Boot 自動組態與 Actuator | （新）進階 | 同上、〈微服務與架構面試題〉 | 撰寫中（`write-algo-a`） | | | |
| `web/11-tcp-udp-tls` | TCP、UDP 與 TLS 握手 | 網路與伺服器 | 〈網路與 HTTP 面試題：三向交握、TLS、REST 對 gRPC〉 | 撰寫中（`write-web-b`） | | | |
| `web/12-http-advanced` | HTTP 進階：狀態碼、快取、Keep-Alive 與版本演進 | 網路與伺服器 | 同上 | 撰寫中（`write-web-b`） | | | |
| `spring/15-security-jwt-oauth` | JWT 與 OAuth 2.0 在 Spring Security 裡怎麼接 | （新）進階 | 〈認證與安全面試題：JWT、OAuth 2.0、OIDC 與密碼保存〉 | | | | |

各課涵蓋範圍照 roadmap 計畫第三部分「最急」表格那一列。課序照資料夾編號接在各模組最後。
