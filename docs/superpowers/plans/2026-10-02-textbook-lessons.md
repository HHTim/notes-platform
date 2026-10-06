# 教材課（把面試集速查展開成完整教材）：計畫與進度

**Tim 交代（10-02）：不用留用量給他；用量用完就等重置後繼續；需要決定的地方都照主控的建議；做到 2026-10-05 09:00 停止。**

來源：`docs/superpowers/plans/2026-09-29-roadmap-expansion.md` 第三部分。面試集是「速查」，教材課是「打底」：面試集那課講到哪、這課從哪裡展開，寫完後回頭把面試集那課對應的題目加一句指路。

寫課守則：`docs/superpowers/plans/2026-10-02-algo-module.md` 的「寫課守則」（含 batch2 的 11 條，加程式碼一定實跑、課中練習）。每課有課中練習 40〜55 題＋課末測驗 10 題；依官方文件新寫（零 fixnote、零 data-note）；出處附英文原句。

已在別的計畫做掉的：作業系統（`java/15-os-process-io`）、CI/CD（`web/10-cicd-pipeline`）、Git（`web/09-git-branching`）。

## 課程表與進度（最急的 8 課）

| 資料夾 | 課名 | 分組 | 對應面試集 | 寫課 | 審查 | 修正與複審 | 上線 |
|---|---|---|---|---|---|---|---|
| `database/06-index-internals` | 索引是怎麼運作的 | （新）效能 | 〈資料庫面試題：索引、交易隔離與鎖〉 | ✅ `8a99e64`（55 題、3 圖；mins 55） | ✅ 10-02 審完：無錯誤級；B+ 樹圖葉節點掛錯、死結圖時間不符腳本、key_len 那句不是手冊說的；07 砍到 50 題；清單 `.superpowers/audit/database/findings-06-07.md`；修正交回 `write-algo-b`；「隔離層級」全站統一（`94fa56a`） | 修正 `29d636e`（16 條全改、07 砍到 50 題）；範圍複審 ✅（@Version 一句主控改） | ✅ 10-03 上線 `bd92486` | | |
| `database/07-transaction-isolation-locks` | 交易隔離層級與鎖 | （新）效能 | 同上 | ✅ `452c1c5`（58 題、9 圖；mins 60） | 同上 | | |
| `java/16-jvm-memory-gc` | JVM 記憶體與垃圾回收 | （新）JVM 與效能 | 〈Java 進階快答：JVM 記憶體、垃圾回收與類別載入〉 | ✅ `90f6756`（49 題、2 圖、41 出處；mins 55） | ✅ 10-02 審完：遞迴層數重現不了要寫範圍、K8s requests 不算處理器數、CompletionException 的原因講錯、兩課測驗正解太常最長；清單 `.superpowers/audit/java/findings-16-17.md`；修正交回 `write-java-a`（順序：執行緒池排第 11 課後、JVM 開新組排最後） | 修正 `75d6fcf`＋主控 `6913dce`；範圍複審 ✅ | ✅ 10-03 上線 | | |
| `java/17-thread-pool-concurrency` | 執行緒池與並行工具 | 並行與設計 | 〈Java 並行快答：執行緒池、鎖與並行集合〉 | ✅ `e3e7298`（51 題、1 圖、28 出處；mins 55） | 同上 | 同上 | ✅ 10-03 上線 |
| `spring/13-transactional-propagation` | @Transactional 的傳播、隔離與失效情境 | （新）進階 | 〈Spring 面試快答：IoC、Bean、AOP 與交易〉 | ✅ `99257bf`（58 題、4 圖；mins 80 偏長） | ✅ 10-02 審完：程式沒錯、實跑全部重現；漏一行實跑輸出、題數寫錯、失效情境數目跟面試集不同組、用詞；砍到 47 題、flush 一節縮成指路；清單 `.superpowers/audit/spring/findings-13-14.md`；修正交回 `write-algo-a` | 修正 `1401cbc`＋`7792424`；範圍複審 ✅（小尾巴主控改） | ✅ 10-03 上線 `9bf0db6` | | |
| `spring/14-boot-autoconfig-actuator` | Spring Boot 自動組態與 Actuator | （新）進階 | 同上、〈微服務與架構面試題〉 | ✅ `d83fa5b`（47 題、4 圖；mins 70） | ✅ 同上：刪亂碼段、砍到 39 題、JSON 只留關鍵行；兩課長陷阱選項反向洩題 | 同上 | ✅ 10-03 上線 | | |
| `web/11-tcp-udp-tls` | TCP、UDP 與 TLS 握手 | 網路與伺服器 | 〈網路與 HTTP 面試題：三向交握、TLS、REST 對 gRPC〉 | ✅ `f318961`（50 題、6 圖；mins 60） | ✅ 10-02 審完：Linux 原始碼註解引錯一處、四處補出處或前提；12 課砍到 50 題；清單 `.superpowers/audit/web/findings-11-12.md`；修正交回 `write-web-b` | 修正 `4b0c6c9`（10 條全改、各 50 題）；範圍複審 ✅（(304) 說明主控補） | ✅ 10-03 上線 `c59553f` | | | |
| `web/12-http-advanced` | HTTP 進階：狀態碼、快取、Keep-Alive 與版本演進 | 網路與伺服器 | 同上 | ✅ `6864ff6`（52 題、4 圖；mins 65） | 同上 | 同上 | ✅ 10-03 上線 | |
| `spring/15-security-jwt-oauth` | JWT 與 OAuth 2.0 在 Spring Security 裡怎麼接 | （新）進階 | 〈認證與安全面試題：JWT、OAuth 2.0、OIDC 與密碼保存〉 | ✅ `0653f43`（47 題、4 圖、31 出處；mins 60；Boot 4.1.1／Security 7.1.1） | ✅ 10-02 審完：程式片段漏 @Bean、舊雜湊升級說過頭、四處補原始碼出處、選項長度最嚴重；清單 `.superpowers/audit/spring/findings-15.md`；修正交回 `write-algo-d` | 修正 `85acf3f`（11 條全改）；範圍複審 ✅ | ✅ 10-03 上線 `a90319c` | | | |

## 接著做（「可以等」那批）

| 資料夾 | 課名 | 寫課 | 審查 | 修正與複審 | 上線 |
|---|---|---|---|---|---|
| `database/08-cache-redis` | 快取放哪裡、怎麼失效 | ✅ `4979bf7`（49 題、5 圖、30 出處；mins 60） | ✅ 10-02 審完（修正 `15aa4d4`，範圍複審 ✅；10-02 上線 `4c7cb66`）：淘汰實驗兩個數不是同一次執行（加起來超過 3,000）、noeviction 預設找不到那一行；跟面試集〈系統設計：快取一致性與熱點〉大量重疊——主控決定本課留實跑、面試集留答題講法、互相指路、數字統一；清單 `.superpowers/audit/database/findings-08.md`；修正交給 `fix-db08` | | |
| `spring/16-jpa-performance` | JPA 效能：N+1、延遲載入與批次 | ✅ `e9b6a3e`＋`502d4b7`（49 題、4 圖；Boot 4.1.1／Hibernate 7.4.5 重跑；JOIN FETCH 加分頁在 7.4 改走子查詢） | ✅ 10-02 審完：Jackson 序列化那題其實是無限遞迴、手機撐到 501px、「聚合根」要換；縮到 mins 60 上下；清單 `.superpowers/audit/spring/findings-16.md`；修正交回 `fix-algo-1112` | 修正 `5082003`（43 題、約 25,300 字）；範圍複審 ✅ | ✅ 10-03 上線 `6a6e0fd` | | | |
| `spring/17-message-queue` | 訊息佇列：Spring 接 Kafka 與 RabbitMQ | ✅ `9cae8a9`（49 題、5 圖；Boot 4.1.1 重跑） | ✅ 10-03 審完：無錯誤級；手機撐寬、圖少畫箭頭、仲裁佇列與冪等生產者說法、跟 13 課 AFTER_COMMIT 互相指路；清單 `.superpowers/audit/spring/findings-17.md`；修正交回 `fix-algo-0910` | 修正 `d64ed92`（12 條全改、45 題）；範圍複審 ✅ | ✅ 10-03 上線（mins 65） | | | |
| `spring/18-integration-testing` | 整合測試：@SpringBootTest、MockMvc 與 Testcontainers | ✅ `ee2f5c2`（48 題、4 圖；Boot 4.1.1） | ✅ 10-03 審完：手機撐到 467px、3.4 預設說太滿、出處歸屬、「假陽性」改「假綠燈」；縮到 mins 60；清單 `.superpowers/audit/spring/findings-18.md`；修正交回 `fix-int17` | 修正 `d02f81e`＋`547f0fc`；範圍複審 ✅ | ✅ 10-03 上線（mins 65） | | | |
| `k8s/22-deploy-strategy-probes` | 部署策略與探針 | ✅ `a654d17`（50 題、2 圖、16 網址；kind v1.36.4 實跑） | ✅ 10-03 審完：探針預設值出處掛錯頁、就緒探針實際行為、每次會變的數字寫成定數、failureThreshold 那題正解；清單 `.superpowers/audit/k8s/findings-22.md`；修正交回 `write-java-a` | 修正 `a7eaf18`（10 條全改）；範圍複審 ✅ | ✅ 10-03 上線 | | | |
| `spring/20-observability` | 可觀測性：Micrometer、Prometheus 與 OpenTelemetry | ✅ `1ed20d6`（47 題、4 圖、20 網址；Boot 4.1.1、Jaeger OTLP） | ✅ 10-03 審完：可上線，用詞與體例小修主控改；選項長度待補（`.superpowers/audit/spring/findings-20.md`） | — | ✅ 10-03 上線 `ccdc32c` | | | |
| `spring/21-api-design` | API 設計進階：版本、分頁、冪等與錯誤格式 | ✅ `a435e4f`（49 題、3 圖、25 網址；Boot 4.1.1、Framework 7 內建版本） | ✅ 10-03 審完：範例冪等沒存失敗結果（跟草案不一致）、工作紀錄寫法、learn 5 條；縮到 mins 60；清單 `.superpowers/audit/spring/findings-21.md`；修正交給 `fix-db08`（原寫課者在修資料庫 06、07） | 修正 `6ce6c3a`（4xx 也存並重跑、36 題）；範圍複審 ✅ | ✅ 10-03 上線（mins 65） | | | |
| `web/13-owasp-security-headers` | OWASP 十大風險與安全標頭 | ✅ `d57361b`（47 題、3 圖、17 網址；mins 50） | ✅ 10-03 審完：無錯誤級；Thymeleaf／Angular 編碼補出處、「比網銀低」改成有理由的說法、選項長度；清單 `.superpowers/audit/web/findings-13.md`；修正 `579af10`（7 條全改、標頭重跑 10-03）；範圍複審 ✅ | ✅ 10-03 上線 `83c2471` | | | |
| `web/14-realtime-websocket-sse` | 即時通訊：WebSocket、SSE 與輪詢 | ✅ `7d76544`（45 題、6 圖、17 網址；mins 55；Nginx 待補 Docker 實跑） | ✅ 10-03 審完：無錯誤級；手機撐寬、curl 輸出新舊混用、Node 要加旗標、「訊息代理」白話；frame 統一譯「訊框」（`589e0f9`）；清單 `.superpowers/audit/web/findings-14.md`；修正交回 `write-web-b` | 修正 `540278b`（Docker nginx 實測）＋`b1e8803`；範圍複審 ✅（`review-java-a` 代） | ✅ 10-03 上線 | | | |
| `spring/22-db-migration` | 資料庫遷移：Flyway 與 Liquibase | ✅ `188d31a`（40 題、4 圖、17 網址；Flyway 12.4、MySQL 8.4 實跑 18 步）；Spring 9 課手機撐寬 `0da686c`；全站掃描另抓 6 頁撐寬，已修 `cde2a24`（全站 153 頁 0 頁撐寬） | ✅ 10-03 審完：一句引文找不到出處、repair 那題跟實跑不符、測驗正解太長；清單 `.superpowers/audit/spring/findings-22.md`；修正交回 `write-algo-d` | 修正 `93a6f78`（8 條全改）；範圍複審 ✅ | ✅ 10-03 上線 | | | |
| `java/18-solid-antipatterns` | SOLID 與常見反模式 | ✅ `e305b96`（43 題、3 圖、21 出處；mins 50） | ✅ 10-03 審完：無錯誤級，5 條小修主控直接改（Liskov 1987 原文 ACM 擋 403 無法逐字核對，主控決定保留 DOI） | — | ✅ 10-03 上線 `214d03f` | | | |
| `cloud/16-aws-lb-autoscaling-messaging` | 負載平衡、自動擴展與訊息服務 | ✅ `2430fc9`（40 題、4 圖、17 網址；LocalStack 4.14 實跑 SQS／SNS，ALB／Auto Scaling 只寫概念） | ✅ 10-03 審完：圖把 Auto Scaling 群組與目標群組畫成一件、一題正解可能不唯一、四處說得比出處多；用詞「健康檢查」「監聽器」保留補 AWS 中文叫法；清單 `.superpowers/audit/cloud/findings-16.md`；修正交回 `fix-algo-0910` | 修正 `5d855b2`（9 條全改）；範圍複審 ✅ | ✅ 10-03 上線 | | | |
| `cloud/17-dynamodb-nosql` | DynamoDB 與 NoSQL 選型 | ✅ `5dcc4b7`（44 題、3 圖、26 網址；DynamoDB Local 3.3.1） | ✅ 10-03 審完：測驗一題正解可能不唯一、採 AWS 繁中官方譯名、分割區統一；縮到 mins 60；清單 `.superpowers/audit/cloud/findings-17.md`；修正排給 `fix-db08` | 修正 `b9fd0a8`（39 題、約 26,900 字）；範圍複審 ✅ | ✅ 10-03 上線（mins 65） | | | |
| `database/09-sql-advanced` | SQL 進階：JOIN、子查詢、GROUP BY 與視窗函式 | ✅ `88d46c5`（47 題、4 圖、18 網址；MySQL 8.4 與 PostgreSQL 18 對照） | ✅ 10-03 審完（`write-algo-b`）：長字串撐寬整頁、一題錯誤原因講錯、測驗一題洩題；「聚合函數」兩課改「聚合函式」；清單 `.superpowers/audit/database/findings-09.md`；修正交回 `fix-int17` | 修正 `6edeb2e`（15 條全改）；範圍複審 ✅（RANK 一句主控改） | ✅ 10-03 上線 | | | |
| `web/15-linux-troubleshooting` | Linux 常用指令與線上排查 | ✅ `83c1720`（47 題、4 圖、35 出處；Ubuntu 24.04 容器實跑） | ✅ 10-03 審完：無錯誤級；143 的來源、容器裡 free 看主機記憶體、截斷只在附加模式成立；縮到 mins 60；清單 `.superpowers/audit/web/findings-15.md`；修正交回 `fix-algo-0708`；順帶更正 TCP 課 ss 用連字號（`886e36a`） | 修正 `b0d28f7`（14 條全改；47→40 題、4→3 圖；字數 34,201→31,511，mins 設 75 不再砍）；範圍複審 ✅（日誌框架那句縮範圍補出處等六處小修，主控直接改） | ✅ 10-06 上線（mins 75） | |
| `k8s/23-service-mesh-serverless` | Service Mesh 與 Serverless：什麼時候值得用 | ✅ `45378e2`（45 題、5 圖、30 網址；kind＋Istio 1.31.1 實跑） | ✅ 10-03 審完：第一段 YAML 被截斷、正解太常最短；清單 `.superpowers/audit/k8s/findings-23.md`；修正交給 `fix-db08` | 修正 `d43a257`（4 條全改）；範圍複審 ✅ | ✅ 10-03 上線 | | | |
| `spring/23-spring-batch` | Spring Batch：銀行批次怎麼寫 | ✅ `d631eeb`（42 題、4 圖、12 網址；Batch 6.0.5、MySQL 8.4 四次執行實跑） | ✅ 10-03 審完：可上線，7 條順手修（結束代碼 5 的來源、兩處補出處、行／筆、選項長度）；清單 `.superpowers/audit/spring/findings-23.md`；交回 `write-algo-c` | 修正 `8c2501c`；範圍複審 ✅ | ✅ 10-03 上線 | | | |
| `algo/14-trie-bit-math` | Trie、位元運算與常見數學題 | ✅ `12c638f`（48 題、3 圖、20 出處） | ✅ 10-03 審完：測驗角括號沒跳脫（註冊後測試會失敗）等 5 處小修，主控直接改 | — | ✅ 10-03 上線 | | | |
| `interview/18-mock-interview` | 模擬面試：Java 後端一面 40 題 | ✅ `fcc43e1`（40 題追問鏈、15 題銀行情境、32 題練習） | ✅ 10-03 審完：技術說法都一致；課中練習補成四選一、熔斷改斷路器；清單 `.superpowers/audit/interview/findings-18.md`；修正交回 `write-algo-d` | 修正 `6c9ef61`（四選一、位置各 8 題）；範圍複審 ✅（跳躍掃描兩處主控改） | ✅ 10-03 上線 | | | |
| `interview/19-system-design-transfer` | 系統設計：銀行轉帳系統 | ✅ `007996f`＋`11c870a`（39 題、2 圖、21 出處；MySQL 8.4 實跑死結對照；圖 id xfer-） | ✅ 10-03 審完：冪等鍵失敗結果講法跟 API 設計課相反沒點出、帳號權限說太寬、削峰／熔斷／寫入分片用詞；清單 `.superpowers/audit/interview/findings-19.md`；修正交給 `fix-algo-0910` | 修正 `419aead`（8 條全改）；範圍複審 ✅ | ✅ 10-03 上線 | | | |
| `algo/15-greedy-intervals` | 貪婪演算法與區間題 | ✅ `b54abe2`（47 題、4 圖；暴力比對驗證） | ✅ 10-03 審完：一處解析錯、452 與 2406 端點規則相反、補比對、採用 Kozen–Zaks 證明；清單 `.superpowers/audit/algo/findings-15.md`；修正交回 `fix-algo-1112` | 修正 `7e52eb8`（11 條全改，端點比較與合併插入各 20000 組隨機比對 0 錯）；範圍複審 ✅（新增 452 起始值、張→枚、比對方式三處，主控直接改） | ✅ 10-06 上線 | |
| `english/21-english-interview` | 英文面試：自我介紹、講專案與常見問答 | ✅ `d98b6ad`（45 題、1 圖、40 網址；STAR 比例跟行為面試課統一照 MIT `f832433`） | ✅ 10-03 審完：無錯誤級；範例時態與主詞、三個字的念法、缺點範例換掉；清單 `.superpowers/audit/english/findings-21.md`；修正交回 `write-algo-a` | 修正 `91f57d1`（14 條全改）；範圍複審 ✅ | ✅ 10-03 上線 | | | |
| `interview/20-handwritten-coding` | 手寫程式題：LRU 快取、阻塞佇列、執行緒安全單例與生產者消費者 | ✅ `d6a001d` | 待審（`review-algo-d` 10-03 週用量用完，未開始） | | |
| `interview/21-system-design-method` | 系統設計面試怎麼答：釐清需求、粗估容量、畫架構與講取捨 | ✅ `671ef86`（42 題、3 圖、21 出處；示範題銀行交易通知服務） | ✅ 10-06 審完：無錯誤級；FCM 配額每專案共用要給交易留份、拿掉「分散到多個專案」、避開整刻的時段算錯；清單 `.superpowers/audit/interview/findings-21.md`；修正交回 `write-algo-b` | 修正 `3dee64d`（13 條全改）＋主控補第 14 條 `bb86f98`；範圍複審 ✅（重複選項值、配額申請條件兩處小修，主控直接改） | ✅ 10-06 上線（系統設計組第一課） | |
| `interview/22-production-troubleshooting` | 線上問題排查面試題：CPU 飆高、記憶體不足、API 變慢與連線用盡 | 撰寫中（`write-algo-c`） | | | |
| `spring/19-resilience` | 韌性模式：Resilience4j 的斷路器、重試與限流 | ✅ `a81d59d`（49 題、4 圖、40 出處；Boot 4.1.1、resilience4j 2.4.0） | ✅ 10-03 審完：手機撐到 653px、一題解析數字對不上、選項長度；清單 `.superpowers/audit/spring/findings-19.md`；修正交回 `fix-algo-0708` | 修正 `9b96d95`＋`9b5c116`；範圍複審 ✅ | ✅ 10-03 上線 | | | |

**主控決定（10-02）：Spring 模組新課一律以 Spring Boot 4.1.x（Framework 7.0.x、Hibernate 7.x、Security 7.x）、Java 21 實跑**——第 13、14 課先用了 4.1.1，其他課跟進；套件還不支援 Boot 4 的在課文註明。

**主控決定（10-03）：全站拿掉課序指路。** 網站上的「第 N 課」照 module.json 順序算，跟資料夾編號已經有五個模組不一致（新課插隊），課序指路會悄悄變錯；`write-java-a` 掃出 205 處課序指路、9 處課名錯誤，一律改成只寫〈完整課名〉；本站課名才用〈〉，外部文章改「」或《》。新課寫作同樣只寫課名（守則原本就這樣規定）。

**主控提醒（10-03）：** kubeconfig 所有代理共用，kubectl／istioctl 一律加 `--context`，不要切 current-context；Docker 資源吃緊，課寫完就刪自己的 kind 叢集。

**主控提醒：** 主控 commit 只 add 指定檔案（`96cb2ff` 曾用 `git add content/web` 把別人的草稿一起帶進去）。

**主控決定（10-02）：新課一律課中練習 50 題以內、mins 60 上下**；超過的在審查時建議砍題或把重複段落縮成指路。

各課涵蓋範圍照 roadmap 計畫第三部分「最急」表格那一列。課序照資料夾編號接在各模組最後。
