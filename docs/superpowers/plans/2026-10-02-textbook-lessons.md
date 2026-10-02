# 教材課（把面試集速查展開成完整教材）：計畫與進度

**Tim 交代（10-02）：不用留用量給他；用量用完就等重置後繼續；需要決定的地方都照主控的建議；做到 2026-10-05 09:00 停止。**

來源：`docs/superpowers/plans/2026-09-29-roadmap-expansion.md` 第三部分。面試集是「速查」，教材課是「打底」：面試集那課講到哪、這課從哪裡展開，寫完後回頭把面試集那課對應的題目加一句指路。

寫課守則：`docs/superpowers/plans/2026-10-02-algo-module.md` 的「寫課守則」（含 batch2 的 11 條，加程式碼一定實跑、課中練習）。每課有課中練習 40〜55 題＋課末測驗 10 題；依官方文件新寫（零 fixnote、零 data-note）；出處附英文原句。

已在別的計畫做掉的：作業系統（`java/15-os-process-io`）、CI/CD（`web/10-cicd-pipeline`）、Git（`web/09-git-branching`）。

## 課程表與進度（最急的 8 課）

| 資料夾 | 課名 | 分組 | 對應面試集 | 寫課 | 審查 | 修正與複審 | 上線 |
|---|---|---|---|---|---|---|---|
| `database/06-index-internals` | 索引是怎麼運作的 | （新）效能 | 〈資料庫面試題：索引、交易隔離與鎖〉 | ✅ `8a99e64`（55 題、3 圖；mins 55） | ✅ 10-02 審完：無錯誤級；B+ 樹圖葉節點掛錯、死結圖時間不符腳本、key_len 那句不是手冊說的；07 砍到 50 題；清單 `.superpowers/audit/database/findings-06-07.md`；修正交回 `write-algo-b`；「隔離層級」全站統一（`94fa56a`） | | |
| `database/07-transaction-isolation-locks` | 交易隔離層級與鎖 | （新）效能 | 同上 | ✅ `452c1c5`（58 題、9 圖；mins 60） | 同上 | | |
| `java/16-jvm-memory-gc` | JVM 記憶體與垃圾回收 | （新）JVM 與效能 | 〈Java 進階快答：JVM 記憶體、垃圾回收與類別載入〉 | ✅ `90f6756`（49 題、2 圖、41 出處；mins 55） | ✅ 10-02 審完：遞迴層數重現不了要寫範圍、K8s requests 不算處理器數、CompletionException 的原因講錯、兩課測驗正解太常最長；清單 `.superpowers/audit/java/findings-16-17.md`；修正交回 `write-java-a`（順序：執行緒池排第 11 課後、JVM 開新組排最後） | 修正 `75d6fcf`＋主控 `6913dce`；範圍複審 ✅ | ✅ 10-03 上線 | | |
| `java/17-thread-pool-concurrency` | 執行緒池與並行工具 | 並行與設計 | 〈Java 並行快答：執行緒池、鎖與並行集合〉 | ✅ `e3e7298`（51 題、1 圖、28 出處；mins 55） | 同上 | 同上 | ✅ 10-03 上線 |
| `spring/13-transactional-propagation` | @Transactional 的傳播、隔離與失效情境 | （新）進階 | 〈Spring 面試快答：IoC、Bean、AOP 與交易〉 | ✅ `99257bf`（58 題、4 圖；mins 80 偏長） | ✅ 10-02 審完：程式沒錯、實跑全部重現；漏一行實跑輸出、題數寫錯、失效情境數目跟面試集不同組、用詞；砍到 47 題、flush 一節縮成指路；清單 `.superpowers/audit/spring/findings-13-14.md`；修正交回 `write-algo-a` | 修正 `1401cbc`＋`7792424`；範圍複審 ✅（小尾巴主控改） | ✅ 10-03 上線 `9bf0db6` | | |
| `spring/14-boot-autoconfig-actuator` | Spring Boot 自動組態與 Actuator | （新）進階 | 同上、〈微服務與架構面試題〉 | ✅ `d83fa5b`（47 題、4 圖；mins 70） | ✅ 同上：刪亂碼段、砍到 39 題、JSON 只留關鍵行；兩課長陷阱選項反向洩題 | 同上 | ✅ 10-03 上線 | | |
| `web/11-tcp-udp-tls` | TCP、UDP 與 TLS 握手 | 網路與伺服器 | 〈網路與 HTTP 面試題：三向交握、TLS、REST 對 gRPC〉 | ✅ `f318961`（50 題、6 圖；mins 60） | ✅ 10-02 審完：Linux 原始碼註解引錯一處、四處補出處或前提；12 課砍到 50 題；清單 `.superpowers/audit/web/findings-11-12.md`；修正交回 `write-web-b` | 修正 `4b0c6c9`（10 條全改、各 50 題）；範圍複審 ✅（(304) 說明主控補） | ✅ 10-03 上線 `c59553f` | | | |
| `web/12-http-advanced` | HTTP 進階：狀態碼、快取、Keep-Alive 與版本演進 | 網路與伺服器 | 同上 | ✅ `6864ff6`（52 題、4 圖；mins 65） | 同上 | 同上 | ✅ 10-03 上線 | |
| `spring/15-security-jwt-oauth` | JWT 與 OAuth 2.0 在 Spring Security 裡怎麼接 | （新）進階 | 〈認證與安全面試題：JWT、OAuth 2.0、OIDC 與密碼保存〉 | ✅ `0653f43`（47 題、4 圖、31 出處；mins 60；Boot 4.1.1／Security 7.1.1） | ✅ 10-02 審完：程式片段漏 @Bean、舊雜湊升級說過頭、四處補原始碼出處、選項長度最嚴重；清單 `.superpowers/audit/spring/findings-15.md`；修正交回 `write-algo-d` | | | |

## 接著做（「可以等」那批）

| 資料夾 | 課名 | 寫課 | 審查 | 修正與複審 | 上線 |
|---|---|---|---|---|---|
| `database/08-cache-redis` | 快取放哪裡、怎麼失效 | ✅ `4979bf7`（49 題、5 圖、30 出處；mins 60） | ✅ 10-02 審完（修正 `15aa4d4`，範圍複審 ✅；10-02 上線 `4c7cb66`）：淘汰實驗兩個數不是同一次執行（加起來超過 3,000）、noeviction 預設找不到那一行；跟面試集〈系統設計：快取一致性與熱點〉大量重疊——主控決定本課留實跑、面試集留答題講法、互相指路、數字統一；清單 `.superpowers/audit/database/findings-08.md`；修正交給 `fix-db08` | | |
| `spring/16-jpa-performance` | JPA 效能：N+1、延遲載入與批次 | ✅ `e9b6a3e`＋`502d4b7`（49 題、4 圖；Boot 4.1.1／Hibernate 7.4.5 重跑；JOIN FETCH 加分頁在 7.4 改走子查詢） | ✅ 10-02 審完：Jackson 序列化那題其實是無限遞迴、手機撐到 501px、「聚合根」要換；縮到 mins 60 上下；清單 `.superpowers/audit/spring/findings-16.md`；修正交回 `fix-algo-1112` | | | |
| `spring/17-message-queue` | 訊息佇列：Spring 接 Kafka 與 RabbitMQ | ✅ `9cae8a9`（49 題、5 圖；Boot 4.1.1 重跑） | ✅ 10-03 審完：無錯誤級；手機撐寬、圖少畫箭頭、仲裁佇列與冪等生產者說法、跟 13 課 AFTER_COMMIT 互相指路；清單 `.superpowers/audit/spring/findings-17.md`；修正交回 `fix-algo-0910` | | | |
| `spring/18-integration-testing` | 整合測試：@SpringBootTest、MockMvc 與 Testcontainers | ✅ `ee2f5c2`（48 題、4 圖；Boot 4.1.1） | 審查中（`review-java-a`） | | | |
| `k8s/22-deploy-strategy-probes` | 部署策略與探針 | 撰寫中（`write-java-a`） | | | |
| `spring/20-observability` | 可觀測性：Micrometer、Prometheus 與 OpenTelemetry | ✅ `1ed20d6`（47 題、4 圖、20 網址；Boot 4.1.1、Jaeger OTLP） | 審查中（`review-algo-b`） | | | |
| `spring/21-api-design` | API 設計進階：版本、分頁、冪等與錯誤格式 | ✅ `a435e4f`（49 題、3 圖、25 網址；Boot 4.1.1、Framework 7 內建版本） | 審查中（`review-algo-d`） | | | |
| `web/13-owasp-security-headers` | OWASP 十大風險與安全標頭 | ✅ `d57361b`（47 題、3 圖、17 網址；mins 50） | ✅ 10-03 審完：無錯誤級；Thymeleaf／Angular 編碼補出處、「比網銀低」改成有理由的說法、選項長度；清單 `.superpowers/audit/web/findings-13.md`；修正 `579af10`（7 條全改、標頭重跑 10-03）；範圍複審 ✅ | ✅ 10-03 上線 `83c2471` | | | |
| `web/14-realtime-websocket-sse` | 即時通訊：WebSocket、SSE 與輪詢 | ✅ `7d76544`（45 題、6 圖、17 網址；mins 55；Nginx 待補 Docker 實跑） | ✅ 10-03 審完：無錯誤級；手機撐寬、curl 輸出新舊混用、Node 要加旗標、「訊息代理」白話；frame 統一譯「訊框」（`589e0f9`）；清單 `.superpowers/audit/web/findings-14.md`；修正交回 `write-web-b` | | | |
| `spring/22-db-migration` | 資料庫遷移：Flyway 與 Liquibase | ✅ `188d31a`（40 題、4 圖、17 網址；Flyway 12.4、MySQL 8.4 實跑 18 步）；Spring 9 課手機撐寬 `0da686c`；全站掃描另抓 6 頁撐寬交 `write-algo-d` 修 | 審查中（`review-algo-a`） | | | |
| `java/18-solid-antipatterns` | SOLID 與常見反模式 | ✅ `e305b96`（43 題、3 圖、21 出處；mins 50） | ✅ 10-03 審完：無錯誤級，5 條小修主控直接改（Liskov 1987 原文 ACM 擋 403 無法逐字核對，主控決定保留 DOI） | — | ✅ 10-03 上線 `214d03f` | | | |
| `cloud/16-aws-lb-autoscaling-messaging` | 負載平衡、自動擴展與訊息服務 | 撰寫中（`fix-algo-0910`） | | | |
| `cloud/17-dynamodb-nosql` | DynamoDB 與 NoSQL 選型 | 撰寫中（`fix-db08` 轉做） | | | |
| `database/09-sql-advanced` | SQL 進階：JOIN、子查詢、GROUP BY 與視窗函式 | 撰寫中（`fix-int17`） | | | |
| `web/15-linux-troubleshooting` | Linux 常用指令與線上排查 | 撰寫中（`fix-algo-0708`） | | | |
| `k8s/23-service-mesh-serverless` | Service Mesh 與 Serverless：什麼時候值得用 | 撰寫中（`write-algo-a`） | | | |
| `spring/23-spring-batch` | Spring Batch：銀行批次怎麼寫 | 撰寫中（`write-algo-c`） | | | |
| `spring/19-resilience` | 韌性模式：Resilience4j 的斷路器、重試與限流 | ✅ `a81d59d`（49 題、4 圖、40 出處；Boot 4.1.1、resilience4j 2.4.0） | ✅ 10-03 審完：手機撐到 653px、一題解析數字對不上、選項長度；清單 `.superpowers/audit/spring/findings-19.md`；修正交回 `fix-algo-0708` | | | |

**主控決定（10-02）：Spring 模組新課一律以 Spring Boot 4.1.x（Framework 7.0.x、Hibernate 7.x、Security 7.x）、Java 21 實跑**——第 13、14 課先用了 4.1.1，其他課跟進；套件還不支援 Boot 4 的在課文註明。

**主控提醒：** 主控 commit 只 add 指定檔案（`96cb2ff` 曾用 `git add content/web` 把別人的草稿一起帶進去）。

**主控決定（10-02）：新課一律課中練習 50 題以內、mins 60 上下**；超過的在審查時建議砍題或把重複段落縮成指路。

各課涵蓋範圍照 roadmap 計畫第三部分「最急」表格那一列。課序照資料夾編號接在各模組最後。
