> 主控備註：本檔由規劃代理產出、原樣收進 repo。文中「課 A〜M」「序 1〜20」是計畫內部的指稱，**上站一律用課名**，不得出現在課文、測驗或 module.json（Tim 的規則：不發明編號代號）。逐節點對照表在同目錄 `2026-09-29-roadmap-coverage.md`。

# 後端 roadmap 缺口報告與擴充計畫（2026-09-29）

Tim 的交代：「根據 roadmap.sh/backend，我的筆記哪裡有缺漏？幫我補齊。尤其面試集太少，下個月要面試。」

這份計畫只做分析與規劃，不寫課文。逐節點對照表在同目錄 `coverage.md`，roadmap 原始資料在 `backend.json`（節點清單 `nodes.txt`），92 課的段落大綱在 `outline.txt`。

## 這次跟先前十波不一樣的地方

先前 92 課全是「收錄 HackMD 舊筆記」：有原文可比對，查證後的差異用黃底更正標記呈現。這次是**從零新寫**，沒有原筆記，所以：

- 不會有任何黃底更正標記；`data-note` 也不會有「原筆記寫…」。
- 每一個可以被問「你怎麼知道」的主張，都要能附 `<a class="fixsrc">` 連到官方文件——這是 Tim 驗證的唯一手段。每課下面列的「出處」就是為此準備的，寫課的代理要逐條開來對。
- 來源註記第一行照慣例寫，但寫的是「依 ○○ 官方文件新寫 · 日期」，不是檔名（沒有檔）。這條要在 `2026-09-21-batch-intake.md` 補一句慣例，避免之後覆蓋率稽核對不回去。
- 測驗題數照批次慣例：預設 8 題、內容密 10 題、最少 6 題。
- 面試課的答案深度照現有面試集第 2 課的形狀：「一句話定義 → 差別與取捨 → 一個版本或實務註記」，每題 150〜300 字，附出處。

---


## 進度（主控維護）

| 面試課 | 撰寫 | 審查 | 註冊上線 |
|---|---|---|---|
| Spring 面試快答：IoC、Bean、AOP 與交易 | ✅ `3862f6d`（15 題、66 出處、5,965 字；以 Spring 7.0／Boot 4.1 為準、標 6.x／3.x 差異） | ✅ 09-29 通過：15 題零錯誤、35 網址全 200、36 處引文語境一致、與 Spring 六課零矛盾；五條字面小修已改（`5666401`） | 已註冊、待推 |
| 資料庫面試題：索引、交易隔離與鎖 | ✅ `b8e0b0f`（15 題、70 出處、4,591 字；以 MySQL 8.4 InnoDB 為準，SQL 在 Docker mysql:8.4 實跑） | ✅ 09-29 通過：15 題零錯誤、40 網址全 200、18 錨點都在、28 頁引文逐句核過；四條不精確＋兩處指路課名＋譯名（聚簇→叢集、優化器→最佳化器、自增→自動遞增）已改（`e8ae091`） | ✅ `aa6de51` 第 5 課，待推 |
| Java 進階快答：JVM 記憶體、垃圾回收與類別載入 | ✅ `c69fb6c`（14 題、71 出處、7,596 字——比估計多一倍，待審查意見再決定要不要縮；以 Java 25 為主軸、標 21 差異） | ✅ 09-29 通過：14 題零錯誤、51 網址全 200、引文逐句吻合；七條用詞／出處小修＋四條可修已改（`cd9b547`：常量池→字串池／常數池、引用→參考計數、內聯→內嵌、兩處出處接回正確頁、刪預告不存在的課）；長度保留（審查說沒有離題段落） | ✅ 第 6 課，待推 |
| 網路與 HTTP 面試題：三向交握、TLS、REST 對 gRPC | ✅ `94e5f38`（15 題、112 出處／96 網址、去標籤 16,056 字——遠超估計；RFC 章節逐一錨定） | ✅ 09-29 審完：錯誤 1（TIME_WAIT 應 4 分鐘＝2 倍 MSL，Linux 60 秒）、不精確 6、用詞 7、體例 3（含五個 RFC 錨點接錯章節、重點整理 9 條）；清單在 `.superpowers/audit/interview/findings-net.md`；修正 ✅ `33e082b`（17 條全改；出處 112→117；長度七處刪約 280 字但補白話與 CORS 段後淨多 416 字→14,185）；複審 ✅ 09-29 15:14：17 條全改對、8 個新增出處全驗過、12 個白話沒講錯；三個小瑕疵（重點整理掉了 TIME_WAIT 為什麼等、引號內 RFC 原文寫法、RFC 1122 錨點頁碼）主控順手修。「工作階段／會話」留給跨模組修正統一 Spring 第 2 課 | ✅ 第 8 課，待推 |
| 系統設計：秒殺與限流 | ✅ `2f8ed58`（13 題、40 出處／24 網址、正文約 4,700 字；Lua／SQL／Nginx 設定在 Docker 實跑；計畫列的 Gateway 與 Redis 網址已改成現行網址） | ✅ 09-29 通過：13 題零錯誤、24 網址全核到原句、Lua 實跑一致；七條不精確／用詞（指路課名、DECR 出處、Nginx 缺 upstream、雜湊標籤槽≠節點、RabbitMQ 延遲外掛名、斷路器＝熔斷、限流詞條那格）＋四條可以等，主控已改並用 Docker `nginx -t` 驗過 | ✅ 第 7 課，待推 |
| 認證與安全面試題：JWT、OAuth 2.0、OIDC 與密碼保存 | ✅ `19e9580`（15 題、51 出處／27 網址、4,663 字；OWASP Top 10 採 2025 版；計畫列的 OWASP JWT for Java 頁已 404，改引改名後的 JWT 速查表） | ✅ 09-29 通過：15 題零錯誤、27 網址全 200、引文逐句核過；不精確 7（JWT 驗證章節、RS256 用公鑰驗證、PKCE 寫 S256、Spring `audiences`、SSRF 引文、指路寫明 Spring 模組）＋用詞 8＋體例 4 主控已改（`1f18ce1`）；清單在 `.superpowers/audit/interview/findings-auth.md` | ✅ 第 9 課，待推 |
| 系統設計：訊息佇列與最終一致性 | ✅ `d01cfea`（13 題、63 出處／32 網址、5,084 字；Kafka 舊網址已是轉址殼，改引 4.3 分頁網址；AWS Saga 拆成 orchestration／choreography 兩頁） | ✅ 09-29 17:33 審完：錯誤 1（測驗第 9 題——轉換失敗預設直接拒絕不重排）、不精確 8（借貸方向反了、learn 承諾 Outbox 狀態機沒畫、序號保序、去重表主鍵、AWS CDC 說法…）、用詞 6、體例 3、要砍到 4,200 字；清單在 `.superpowers/audit/interview/findings-mq.md`；修正 ✅ `7d152b6`（19 條全改；5,084→4,191 字，清單外另刪「叢集協調」列與兩條金句）；複審 ✅ 20:16：19 條全改對、52 個 fixsrc 無孤兒；三個小瑕疵（仲裁佇列白話、「上一節的表」、剛好一次英文截斷）與補回 KRaft／仲裁佇列兩句由主控順手做（`820c0ac`，4,250 字） | ✅ `820c0ac` 第 11 課，待推 |
| 系統設計：快取一致性與熱點 | ✅ `53aca4c`（11 題、43 出處／28 網址、4,472 字；Redis 8.10.2 實跑淘汰／UNLINK／io-threads；Write-Behind 改引 Oracle Coherence 文件；Redis FAQ 現行版已無單執行緒段，改引 latency 文件＋6.0 版本說明；版本主軸寫 Spring 6.x 待對齊 7.0） | ✅ 09-29 20:15 審完：錯誤 1（淘汰策略官方頁現列十種，8.6 起多 LRM 兩種）、不精確 4、用詞 4、體例 3，主控已改（`d7fb344`）；審查總評：先修十種策略即可上線 | ✅ `820c0ac` 第 10 課，待推 |
| Java 並行快答：執行緒池、鎖與並行集合 | ✅ `1bb3680`（09-30；14 題、60 出處／39 網址、4,424 字；四段範例用 javac 21 實編；以 Java 25 為準，虛擬執行緒釘住寫 21／24／25 三段） | ✅ 09-30 09:58 審完：錯誤 1（common pool 平行度是處理器數減一，不是等於）、不精確 6（CompletableFuture 例外會包成 CompletionException、容器 CPU 配額前提、飢餓解法太滿、JEP 491 另列釘住情況、毒藥物件該比同一性、TIMED_WAITING）、用詞 3、體例 2；清單在 `.superpowers/audit/interview/findings-concurrency.md`；修正 ✅ `c140854`（12 條全改；兩段程式碼 javac 21 重編實跑；4,585 字，超上限 85 字主控決定不砍）；複審 ✅ 10:12 七項全過（原始碼那行、三處新引文、兩段程式碼複審者重編實跑）；兩處措辭主控順手補 | ✅ `a7c6a1f` 第 13 課，已推 |
| 資料庫面試題：複寫、分片與 CAP | ✅ `86e07e3`（11 題、50 出處／32 網址、4,491 字；SQL 在 Docker mysql:8.4 實跑；計畫列的 replication-implementation-details 頁 404 改引 replication-threads） | ✅ 09-29 20:16 審完：錯誤 1（半同步 MySQL 該歸 PA/EC 不是 PC/EC——課文自己寫逾時退回非同步；測驗第 7 題連動）、不精確 6（AFTER_SYNC 對 AFTER_COMMIT、非同步丟的是「未收到」、磁碟滿那節只限 MyISAM 與 binlog…）、用詞 8、體例 5；清單在 `.superpowers/audit/interview/findings-dbscale.md`；修正 ✅ `deea765`（20 條全改；quiz 第 7 題重寫成 PA/EC 正解；三處合理保留）；複審 ✅ 20:25：七項全過（PA/EC 論證、三句手冊引文、HikariCP 前提翻譯皆逐字對上；三處保留同意） | ✅ 第 12 課，已推 |

**09-29 收工摘要（20:30）**：面試集 3 課 → 12 課全部上線（第 4〜12 課皆「寫課 → 獨立審查 → 修正 → 範圍複審」四關走完；審查抓到的錯誤級問題共 6 個：QoS／TIME_WAIT 4 分鐘／Spring AMQP 轉換失敗不重排／淘汰策略十種／半同步 MySQL 歸 PA/EC／秒殺課 Nginx 缺 upstream 等，全部修掉才註冊）。跨模組一致性（09-24 審查遺留）也做完推上線。**尚未動的**：計畫第二部分其他模組的補課（容器與部署面試題、微服務與架構面試題、程式題等 K〜M 課），以及各模組新課；等 Tim 排。資料夾編號撞號（兩個 `04-`）保留，slug 不撞、建置不受影響。

已推：`f5f07a9`（09-29 12:30）——面試集第 5 課（資料庫面試題）、第 6 課（JVM）上線，Spring 面試課五條小修、資料庫第 4、5 課小修一併上線；`94e5f38` 網路課隨這次 push 進了 repo 但**未註冊、未上線**，等審查通過再註冊。

**09-29 15:25 暫停（Tim 指示：token 留 20% 給他做別的業務，他下班前說「繼續」才能繼續）**。當時四個代理被主控停掉，恢復時用 SendMessage 各送一句「接著做」即可（代理保有上下文）：
- `review-iv-mq`：審〈訊息佇列與最終一致性〉（`d01cfea`），剛開始。
- `review-iv-auth`：審〈認證與安全面試題〉（`19e9580`），剛開始。
- `write-iv-cache`：寫〈系統設計：快取一致性與熱點〉（資料夾 `10-cache-consistency-hotspots`），剛開始，工作目錄可能還沒有檔案。
- `write-iv-dbscale`：寫〈資料庫面試題：複寫、分片與 CAP〉（資料夾 `11-db-replication-sharding-cap`），剛開始。
本機未推：`d01cfea`（訊息佇列課，未註冊）、`19e9580`（認證課，未註冊）＋本檔的進度更新。線上已是面試集 8 課。恢復後順序：兩個審查 → 修正 → 註冊第 9、10 課 → 推；再喚醒兩個撰寫。

用量上限事故（第四次）：09-29 17:55 四個代理（跨模組複審、複寫課審查、快取課審查、訊息佇列修正）撞上限，重置 20:10；20:11 喚醒續做。17:31 恢復到 17:55 只撐了兩個半小時，這段同時跑五個（兩個寫課）。

用量上限事故（第三次）：09-29 12:41 四個代理（網路課複審、秒殺課審查、認證與安全撰寫、訊息佇列撰寫）同時撞到五小時上限，重置 15:10；15:11 逐一用 SendMessage 喚醒續做。這輪同時跑的只有四〜五個，仍在兩個半小時內燒完——寫課代理（每課開 40〜100 個網址、Docker 實跑）比審查代理貴很多，之後同時跑的寫課代理控制在兩個以內。

資料夾編號備註：`04-db-index-isolation-locks` 與 `04-spring-quick-answers` 撞號（兩個寫課代理同時開工）。slug 不撞、建置不受影響；審查中不改名，待推之前再決定要不要 `git mv`。

## 第一部分：roadmap 對照與缺口分級

### 數字

roadmap 共 **155 個節點**（大節點 23、子節點 132）。對照結果：**有教 56、只點到 35、完全沒有 64**。

「完全沒有」的 64 個裡有 33 個是特定產品或語言（Go、Rust、PHP、Cassandra、Solr……），roadmap 自己都寫「大多數你永遠用不到，知道是什麼就好」，歸次要缺口。真正要補的是剩下 31 個「完全沒有」加 35 個「只點到」。

### 核心缺口（roadmap 有、後端面試常考、站上完全沒有或只點到）

依「下個月面試會不會被問到」排序，越前面越急。

| 缺口 | 站上現況 | 補在哪裡（見第二、三部分） |
|---|---|---|
| **資料庫索引**：B+ 樹、聚簇與二級索引、複合索引的最左前綴、覆蓋索引、什麼情況索引失效、EXPLAIN | 全站零命中——「索引」兩字只出現在 Java 的陣列索引 | 面試課 D＋資料庫模組新課 |
| **交易隔離與鎖**：四個隔離層級、髒讀／不可重複讀／幻讀、MVCC、悲觀鎖與樂觀鎖、間隙鎖、死結排查 | Spring 第 6 課與資料庫第 2 課各提「隔離」兩次，沒展開 | 同上 |
| **JVM 記憶體與垃圾回收**：堆與 Metaspace、各代、G1／ZGC、OOM 種類與排查、類別載入、JIT | Java 第 1 課一句「垃圾回收」 | 面試課 B＋Java 模組新課 |
| **Java 並行工具**：執行緒池七個參數與拒絕策略、`ExecutorService`、`CompletableFuture`、`ConcurrentHashMap` 原理、happens-before | Java 第 10 課講到 CAS 與死結就停 | 面試課 C＋Java 模組新課 |
| **Spring 原理**：Bean 生命週期完整版、循環相依、`@Transactional` 傳播行為與失效情境、Spring Boot 自動組態、Actuator | Spring 第 5、6 課各一段起手 | 面試課 A＋Spring 模組新課 |
| **網路基礎進階**：TCP 三向交握與四向揮手、TCP 對 UDP、TLS 1.3 握手、HTTP/1.1 對 HTTP/2 對 HTTP/3、Keep-Alive、OSI 分層 | 網頁第 1、2 課有 TCP／UDP 取捨一段、TLS 交握一段，沒到握手步驟 | 面試課 E＋網頁模組新課 |
| **快取策略**：Cache-Aside／Write-Through／Write-Behind、失效順序、雪崩／穿透／擊穿、快取與資料庫一致性、HTTP 快取標頭、Redis 資料結構與持久化 | 面試集第 3 課有多層快取與 Bloom Filter；一致性、Redis 本身零 | 面試課 I＋資料庫模組新課 |
| **訊息佇列**：Kafka／RabbitMQ 差別、送達保證、冪等消費、順序、死信、Outbox | 面試集第 2、3 課各一句 | 面試課 H＋Spring 模組新課 |
| **認證協定全貌**：JWT 三段結構與風險、OAuth 2.0 四種授權流程與 PKCE、OIDC、SAML、Basic、Refresh Token、密碼雜湊該用哪個演算法 | JWT／OAuth 一句話定義；bcrypt／Argon2 零命中 | 面試課 G＋Spring 模組新課 |
| **API 設計進階**：版本策略、分頁三種做法、冪等鍵、錯誤格式（RFC 9457）、OpenAPI、REST 對 gRPC 對 GraphQL 對 SOAP | Spring 第 7 課有基礎；gRPC／GraphQL／SOAP／OpenAPI 零或一次 | 面試課 E（對比部分）＋Spring 模組新課 |
| **限流與韌性模式**：令牌桶對漏桶對滑動視窗、斷路器三態、重試與退避、隔艙、背壓、優雅降級 | 令牌桶一段、熔斷一句 | 面試課 F＋Spring 模組新課 |
| **測試策略**：測試金字塔、`@SpringBootTest` 對切片測試、MockMvc、Testcontainers、契約測試 | Spring 第 11 課只有單元測試 | Spring 模組新課 |
| **CI/CD 與部署策略**：管線階段、GitHub Actions、映像建置與推送、滾動／藍綠／金絲雀、就緒與存活探針 | 面試集第 2 課一題；K8s 第 18、19 課各提探針一次 | 面試課 K＋K8s 模組新課＋網頁模組新課 |
| **監控與可觀測性**：指標／日誌／追蹤、四個黃金訊號、Prometheus、Grafana、OpenTelemetry、Micrometer、Actuator | 面試集第 2 課一題 | 面試課 L＋Spring 模組新課 |
| **作業系統基礎**：行程對執行緒、上下文切換、虛擬記憶體、I/O 模型（阻塞、非阻塞、多路複用）、檔案描述子 | Java 第 10 課一段比喻；K8s 第 20 課的 namespace／cgroup | Java 模組新課 |
| **分片、複寫與 CAP**：分片策略（範圍、雜湊、一致性雜湊）、主從延遲與讀寫分離、CAP 與 PACELC | 資料庫第 4 課一段、雲端第 6 課 RDS | 面試課 J＋資料庫模組新課 |
| **OWASP 十大風險與 CSP**：注入、失效的存取控制、加密失敗、SSRF、CSP 標頭、伺服器加固 | Spring 第 10 課提 OWASP 兩次 | 面試課 G＋網頁模組新課 |
| **即時通訊**：WebSocket、SSE、長輪詢 | 零 | 網頁模組新課（可以等） |
| **架構模式**：十二要素、SOA 對微服務、Service Mesh、Serverless 取捨 | 零或一句 | 面試課 L（補強既有第 2 課） |
| **Git 分支與協作** | 一段 | 網頁模組新課（可以等） |
| **資料庫遷移**（Flyway／Liquibase）、**N+1** | 零 | Spring 模組新課「JPA 效能」帶 N+1；遷移一課可以等 |
| **SOLID 原則**（roadmap 的 Design & Architecture 按鈕） | 零 | 併進 Java 第 11 課補強，或面試課 B 帶一題 |

### 次要缺口（roadmap 有，但面試少考或不是 Tim 的方向）

Go、Python、Ruby、C#、PHP、Rust；PostgreSQL、MariaDB、SQLite、Oracle、MS SQL 各家；Apache、Caddy、IIS；Memcached；Elasticsearch、Solr；GitLab；Cursor、Antigravity；Gemini、OpenAI；AI 的 Streaming、Structured Outputs、Refactoring、Documentation Generation；NoSQL 十二個特定產品（Cassandra、Neo4j、InfluxDB、DynamoDB……）。

建議做法：不開課，在對應面試課裡各帶一題「差在哪」（例如 MySQL 對 PostgreSQL、Kafka 對 RabbitMQ、Elasticsearch 是什麼時候才需要）。DynamoDB 例外——Tim 走 AWS，可以在雲端模組加一課，但不急。

### 已涵蓋（不動）

網際網路、HTTP 基礎、DNS、託管、瀏覽器、HTML／CSS／JavaScript、Java 語言、MySQL 與 SQL、正規化、ACID 與交易基礎、ORM、REST 基礎、Cookie／Session／權杖、CORS、HTTPS 基礎、Nginx、Docker、Kubernetes 基礎、單體對微服務、單元測試、LLM／RAG／嵌入、Claude Code／Copilot／MCP／Agents、提示技巧、函式呼叫、限流的令牌桶。

---

## 第二部分：面試集擴充計畫（重點）

### Tim 的背景與面試會考什麼

從 CLAUDE.md 與十個模組推：Java／Spring Boot 後端、Angular 前端、Kubernetes 與 OpenShift、AWS 與 GCP、銀行業。銀行業 Java 後端面試的固定菜單，依被問到的機率排：

1. Java 基礎與集合（已有第 1 課）→ **JVM 與並行**（缺）
2. **Spring 原理**（缺，最常考）
3. **資料庫：索引、交易、鎖**（缺，銀行業必考）
4. 網路與 HTTP（缺）
5. 系統設計一題（已有短網址；銀行業偏好**高併發交易、秒殺、最終一致性**）
6. 微服務與雲端（已有第 2 課，偏問答）
7. 容器與部署（缺）
8. 安全（銀行業會問；缺）
9. 行為面試與專題（第 1 課有一段）

### 分組安排

現有分組「Java」「後端與雲端」「系統設計」保留；新開四組：「Spring」「資料庫」「網路、安全與部署」「準備與表達」。新課排序照下表（優先序＝寫作順序，最急的先寫）。

### 建議新增的 13 課

---

#### 面試課 A：Spring 面試快答：IoC、Bean、AOP 與交易（分組：Spring）——最急

**常考題（15 題）**
1. IoC 與 DI 差在哪？Spring 容器做了什麼？
2. `BeanFactory` 與 `ApplicationContext` 差在哪？
3. Bean 的作用域有哪幾種？singleton 的 Bean 是執行緒安全的嗎？
4. Bean 的完整生命週期（實體化 → 屬性填入 → Aware 介面 → `BeanPostProcessor` 前置 → 初始化 → 後置 → 使用 → 銷毀）
5. 建構式注入、setter 注入、欄位注入怎麼選？為什麼官方建議建構式？
6. 循環相依 Spring 怎麼處理？為什麼建構式注入會直接失敗？
7. `@Autowired`、`@Resource`、`@Qualifier`、`@Primary` 差在哪？
8. AOP 的代理是 JDK 動態代理還是 CGLIB？Spring Boot 預設哪個？
9. 為什麼同一個類別內部呼叫，`@Transactional` 或 `@Cacheable` 不會生效？
10. `@Transactional` 的傳播行為有哪些？`REQUIRED` 與 `REQUIRES_NEW` 差在哪？
11. `@Transactional` 什麼情況會失效？（非 public、self-invocation、受檢例外預設不回復、多執行緒、例外被吃掉）
12. Spring Boot 自動組態怎麼運作？`@Conditional` 家族、`AutoConfiguration.imports` 檔
13. `@SpringBootApplication` 包了哪三個註解？
14. Spring MVC 一次請求走過哪些元件？（`DispatcherServlet` → `HandlerMapping` → `HandlerAdapter` → Controller → `ViewResolver` 或 `HttpMessageConverter`）
15. Filter、Interceptor、AOP 三者的位置與分工

**出處**
- IoC 容器：https://docs.spring.io/spring-framework/reference/core/beans.html
- Bean 作用域：https://docs.spring.io/spring-framework/reference/core/beans/factory-scopes.html
- 生命週期回呼與 Aware：https://docs.spring.io/spring-framework/reference/core/beans/factory-nature.html
- `BeanPostProcessor`：https://docs.spring.io/spring-framework/reference/core/beans/factory-extension.html
- 注入方式與循環相依：https://docs.spring.io/spring-framework/reference/core/beans/dependencies/factory-collaborators.html
- 自動綁定與 `@Primary`／`@Qualifier`：https://docs.spring.io/spring-framework/reference/core/beans/annotation-config/autowired-qualifiers.html
- AOP 代理機制與 self-invocation：https://docs.spring.io/spring-framework/reference/core/aop/proxying.html
- 交易傳播：https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/tx-propagation.html
- `@Transactional` 設定與回復規則：https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html 、https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/rolling-back.html
- 自動組態：https://docs.spring.io/spring-boot/reference/using/auto-configuration.html 、https://docs.spring.io/spring-boot/reference/features/developing-auto-configuration.html
- `@SpringBootApplication`：https://docs.spring.io/spring-boot/reference/using/using-the-springbootapplication-annotation.html
- `DispatcherServlet`：https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-servlet.html

**與既有課的關係**：IoC 基礎見 Spring 第 5 課、AOP 角色與 self-invocation 見第 6 課、MVC 分層見第 7 課、Filter 對 Controller 見第 12 課——這四處用「見 Spring 模組第 N 課」指路，本課只寫面試官會追問的那一層（生命週期完整順序、傳播行為表、失效情境清單、自動組態原理）。

**估計**：3,200〜3,600 中文字；測驗 10 題。

---

#### 面試課 B：Java 進階快答：JVM 記憶體、垃圾回收與類別載入（分組：Java）——最急

**常考題（14 題）**
1. JVM 執行期資料區有哪些？哪些是執行緒共用、哪些私有？
2. 堆裡的新生代、老年代是什麼？物件什麼時候晉升？
3. Metaspace 取代永久代解決了什麼？
4. 什麼是 GC Root？可達性分析怎麼判斷物件死了？
5. 常見垃圾回收器：Serial、Parallel、G1、ZGC 各適合什麼？現在預設是哪個？
6. Stop-The-World 是什麼？G1 怎麼縮短停頓？
7. `OutOfMemoryError` 有哪幾種？（heap、Metaspace、unable to create native thread、direct buffer）各怎麼排查？
8. 記憶體洩漏在 Java 怎麼發生？常見來源（static 集合、未關閉資源、ThreadLocal、監聽器）
9. 類別載入的三步（載入、連結、初始化）與雙親委派模型
10. JIT 是什麼？分層編譯做了什麼？為什麼「暖機」後比較快？
11. 強、軟、弱、虛參考差在哪？
12. `HashMap` 的內部結構、擴容、Java 8 為什麼加紅黑樹？`HashMap` 對 `ConcurrentHashMap` 對 `Hashtable`
13. `String` 常量池、`intern()`、為什麼 `String` 不可變？
14. 常用的 JVM 診斷工具：`jcmd`、`jstack`、`jmap`、JFR

**出處**
- 執行期資料區：https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-2.html#jvms-2.5
- 類別載入與連結：https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-5.html
- HotSpot GC 調校指南（各回收器、各代、選擇準則）：https://docs.oracle.com/en/java/javase/21/gctuning/
- G1 成為預設：https://openjdk.org/jeps/248
- ZGC：https://openjdk.org/jeps/377 、分代 ZGC：https://openjdk.org/jeps/439
- Metaspace：https://openjdk.org/jeps/122
- OOM 與記憶體洩漏排查：https://docs.oracle.com/en/java/javase/21/troubleshoot/troubleshooting-memory-leaks.html
- JVM 指南（JIT、分層編譯、類別資料共享）：https://docs.oracle.com/en/java/javase/21/vm/index.html
- 參考型別：https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/ref/package-summary.html
- `HashMap`：https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/HashMap.html （紅黑樹化的門檻寫在 OpenJDK 原始碼註解，要引就指出搜 `TREEIFY_THRESHOLD`）
- `String.intern`：https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/String.html#intern()
- 診斷工具：https://docs.oracle.com/en/java/javase/21/troubleshoot/diagnostic-tools.html

**與既有課的關係**：JVM／JRE／JDK 三個縮寫與編譯流程見 Java 第 1 課；`String` 不可變見第 3 課；集合怎麼選見第 9 課；`equals`／`hashCode` 見第 6 課。本課寫「原理」那層。

**估計**：3,000〜3,400 字；測驗 10 題。

---

#### 面試課 C：Java 並行快答：執行緒池、鎖與並行集合（分組：Java）——最急

**常考題（14 題）**
1. 行程與執行緒差在哪？Java 執行緒與作業系統執行緒的關係？虛擬執行緒改變了什麼？
2. 執行緒的狀態有哪幾種？（`Thread.State` 六種）
3. `ThreadPoolExecutor` 七個參數；任務進來的處理順序（核心 → 佇列 → 最大 → 拒絕）
4. 四種拒絕策略；為什麼不建議用 `Executors.newFixedThreadPool` 這類工廠方法？
5. 執行緒池大小怎麼估？（CPU 密集對 I/O 密集）
6. `synchronized` 與 `ReentrantLock` 差在哪？公平鎖、可中斷、條件變數
7. `volatile` 保證什麼、不保證什麼？happens-before 是什麼？
8. CAS 的 ABA 問題；`AtomicInteger` 對 `LongAdder`
9. `ConcurrentHashMap` 怎麼做到高並行？Java 8 之後的結構（CAS＋synchronized 桶）
10. `CountDownLatch`、`CyclicBarrier`、`Semaphore` 各解決什麼？
11. `CompletableFuture` 怎麼組合非同步任務？跟 `Future` 差在哪？
12. `ThreadLocal` 的用途與記憶體洩漏風險
13. 死結四條件與排查（`jstack`）；活鎖、飢餓
14. 生產者消費者用 `BlockingQueue` 怎麼寫？

**出處**
- `ThreadPoolExecutor`（參數、佇列、拒絕策略）：https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ThreadPoolExecutor.html
- `Executors` 工廠方法：https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/Executors.html
- `Thread.State`：https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Thread.State.html
- 虛擬執行緒：https://openjdk.org/jeps/444
- Java 記憶體模型與 happens-before：https://docs.oracle.com/javase/specs/jls/se21/html/jls-17.html#jls-17.4
- `java.util.concurrent` 套件總覽（記憶體一致性那一節）：https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/package-summary.html
- `ReentrantLock`：https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/locks/ReentrantLock.html
- `ConcurrentHashMap`：https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ConcurrentHashMap.html
- `LongAdder`：https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/atomic/LongAdder.html
- `CompletableFuture`：https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/CompletableFuture.html
- `ThreadLocal`：https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/ThreadLocal.html
- `BlockingQueue`：https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/BlockingQueue.html

**與既有課的關係**：競爭條件、`synchronized`、`volatile`、CAS、死結、虛擬執行緒的基礎全在 Java 第 10 課——本課每題開頭一句「基礎見 Java 第 10 課」，只寫面試追問層（參數、原理、選型、排查）。

**估計**：3,000〜3,400 字；測驗 10 題。

---

#### 面試課 D：資料庫面試題：索引、交易隔離與鎖（分組：資料庫）——最急

**常考題（15 題）**
1. 索引是什麼？為什麼用 B+ 樹不用雜湊或二元樹？
2. InnoDB 的聚簇索引與二級索引差在哪？回表是什麼？
3. 複合索引的最左前綴原則；`(a, b, c)` 哪些查詢用得到？
4. 覆蓋索引是什麼？怎麼從 EXPLAIN 看出來（`Using index`）？
5. 哪些寫法會讓索引用不上？（對欄位做函數、隱含型別轉換、前置萬用字元、`OR` 混用、否定條件）
6. 主鍵為什麼建議用自增整數而不是 UUID？
7. EXPLAIN 要看哪幾欄？（`type`、`key`、`rows`、`Extra`）
8. 慢查詢怎麼找？慢查詢日誌與 `long_query_time`
9. 四個隔離層級各允許哪些讀異常？MySQL 預設哪個？PostgreSQL 預設哪個？
10. MVCC 是什麼？InnoDB 怎麼用 undo log 讀到舊版本？
11. 悲觀鎖對樂觀鎖：`SELECT ... FOR UPDATE` 對版本欄位，各適合什麼？
12. 記錄鎖、間隙鎖、Next-Key 鎖是什麼？為什麼可以擋幻讀？
13. 死結怎麼發生、InnoDB 怎麼處理、怎麼看 `SHOW ENGINE INNODB STATUS`？
14. 大表加欄位或加索引會鎖表嗎？Online DDL
15. MySQL 與 PostgreSQL 主要差在哪？（面試官愛問，一題帶過）

**出處（以 MySQL 8.4 手冊為主）**
- 索引結構（B-tree、聚簇、二級）：https://dev.mysql.com/doc/refman/8.4/en/innodb-index-types.html
- MySQL 怎麼用索引：https://dev.mysql.com/doc/refman/8.4/en/mysql-indexes.html
- 複合索引與最左前綴：https://dev.mysql.com/doc/refman/8.4/en/multiple-column-indexes.html
- 覆蓋索引（詞彙表）：https://dev.mysql.com/doc/refman/8.4/en/glossary.html#glos_covering_index
- EXPLAIN 輸出：https://dev.mysql.com/doc/refman/8.4/en/explain-output.html
- 慢查詢日誌：https://dev.mysql.com/doc/refman/8.4/en/slow-query-log.html
- 隔離層級：https://dev.mysql.com/doc/refman/8.4/en/innodb-transaction-isolation-levels.html
- MVCC：https://dev.mysql.com/doc/refman/8.4/en/innodb-multi-versioning.html
- 鎖的種類：https://dev.mysql.com/doc/refman/8.4/en/innodb-locking.html
- 鎖定讀：https://dev.mysql.com/doc/refman/8.4/en/innodb-locking-reads.html
- 死結：https://dev.mysql.com/doc/refman/8.4/en/innodb-deadlocks.html
- Online DDL：https://dev.mysql.com/doc/refman/8.4/en/innodb-online-ddl.html
- PostgreSQL 隔離層級（對照用；讀異常的定義這一頁最清楚）：https://www.postgresql.org/docs/current/transaction-iso.html

**與既有課的關係**：ACID 與交易基礎見資料庫第 2 課、正規化見第 3 課、Spring 端的 `@Transactional` 見面試課 A、分散式鎖見資料庫第 5 課。本課全部是新內容（索引全站零）。

**估計**：3,400〜3,800 字；測驗 10 題。

---

#### 面試課 E：網路與 HTTP 面試題：三向交握、TLS、REST 對 gRPC（分組：網路、安全與部署）——最急

**常考題（15 題）**
1. OSI 七層與 TCP/IP 四層怎麼對應？HTTP、TCP、IP 各在哪層？
2. TCP 三向交握每一步在做什麼？為什麼是三次不是兩次？
3. 四向揮手；TIME_WAIT 是什麼、為什麼伺服器上會很多？
4. TCP 對 UDP：可靠性、順序、壅塞控制；什麼場景選 UDP？
5. TLS 1.3 握手流程；跟 TLS 1.2 少了什麼？憑證鏈怎麼驗？
6. HTTPS 是對稱還是非對稱加密？各用在哪個階段？
7. HTTP/1.1 的 Keep-Alive 與隊頭阻塞；HTTP/2 的多路複用；HTTP/3 為什麼改用 QUIC？
8. 常見狀態碼：200／201／204／301／302／304／400／401／403／404／409／422／429／500／502／503／504 各代表什麼？401 與 403 差在哪？
9. GET／POST／PUT／PATCH／DELETE 的語意；哪些是冪等、哪些是安全？
10. RESTful 的約束是什麼？（無狀態、統一介面、資源、表述）
11. REST 對 gRPC：協定、序列化、串流、瀏覽器支援；什麼時候選 gRPC？
12. REST 對 GraphQL；REST 對 SOAP（銀行業舊系統）
13. 從輸入網址到看到網頁（面試官常要你講一遍）
14. Cookie 的 `HttpOnly`、`Secure`、`SameSite` 各擋什麼？
15. HTTP 快取：`Cache-Control`、`ETag`、`Last-Modified`、304 怎麼配合？

**出處**
- TCP（三向交握、狀態機、TIME_WAIT）：https://www.rfc-editor.org/rfc/rfc9293
- UDP：https://www.rfc-editor.org/rfc/rfc768
- TLS 1.3：https://www.rfc-editor.org/rfc/rfc8446
- HTTP 語意（方法、冪等與安全、狀態碼）：https://www.rfc-editor.org/rfc/rfc9110
- HTTP/1.1 訊息語法與連線管理：https://www.rfc-editor.org/rfc/rfc9112
- HTTP/2：https://www.rfc-editor.org/rfc/rfc9113
- HTTP/3：https://www.rfc-editor.org/rfc/rfc9114 ；QUIC：https://www.rfc-editor.org/rfc/rfc9000
- HTTP 快取：https://www.rfc-editor.org/rfc/rfc9111
- Cookie 屬性：https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies
- REST 約束（Fielding 論文第 5 章）：https://ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm
- gRPC 介紹與核心概念：https://grpc.io/docs/what-is-grpc/introduction/ 、https://grpc.io/docs/what-is-grpc/core-concepts/
- GraphQL：https://graphql.org/learn/
- SOAP 1.2：https://www.w3.org/TR/soap12-part0/
- MDN HTTP 總覽（狀態碼、標頭的白話對照）：https://developer.mozilla.org/en-US/docs/Web/HTTP

**與既有課的關係**：四層分工與 TCP／UDP 取捨見網頁第 1 課、HTTP 訊息結構與 TLS 三種保護見第 2 課、輸入網址的流程見第 3 課、Cookie 見 Spring 第 2 課、CORS 見 Spring 第 10 課、REST 基本設計見 Spring 第 7 課。本課補握手步驟、版本差異、狀態碼表、協定對比。

**估計**：3,400〜3,800 字；測驗 10 題。

---

#### 面試課 F：系統設計：秒殺與限流（分組：系統設計）——最急

銀行業面試常用「發紅包」「限量優惠」「搶購」當高併發題。

**常考題（13 題）**
1. 開場怎麼問需求？（商品數、預估流量峰值、能不能超賣、能不能少賣、公平性要求）
2. 流量怎麼一層層擋？（前端按鈕與驗證碼 → CDN 靜態化 → Gateway 限流 → 應用層 → 快取 → 資料庫）
3. 限流演算法：固定視窗、滑動視窗、漏桶、令牌桶各適合什麼？分散式限流怎麼做（Redis＋Lua）？
4. 庫存放哪裡？Redis 預扣庫存怎麼保證不超賣？（原子遞減、Lua 腳本）
5. 為什麼資料庫直接 `UPDATE stock = stock - 1 WHERE stock > 0` 在高併發下會慢？（行鎖排隊）
6. 非同步下單：請求先進佇列、下單結果怎麼通知使用者？
7. 熱點資料怎麼處理？（本地快取、分桶庫存、多個 key）
8. 冪等：同一個人重複點兩次怎麼只扣一次？（冪等鍵、唯一約束）
9. 搶到但沒付款的庫存怎麼還？（延遲訊息、定時任務）
10. 斷路器與降級：下游掛了怎麼保住主流程？
11. 怎麼防機器人與黃牛？（限購、風控、驗證碼）
12. 容量估算：QPS、頻寬、連線數怎麼算？
13. 壓測與觀測：怎麼知道系統扛得住？

**出處**
- Redis 原子操作與 Lua 腳本：https://redis.io/docs/latest/develop/interact/programmability/eval-intro/
- Redis 限流模式（各演算法）：https://redis.io/glossary/rate-limiting/
- 令牌桶實作範例（Spring Cloud Gateway 的 `RequestRateLimiter`）：https://docs.spring.io/spring-cloud-gateway/reference/spring-cloud-gateway/filter-factories/requestratelimiter-factory.html
- 漏桶實作範例（Nginx `limit_req` 官方寫明是漏桶）：https://nginx.org/en/docs/http/ngx_http_limit_req_module.html
- 節流模式：https://learn.microsoft.com/en-us/azure/architecture/patterns/throttling
- 以佇列平衡負載：https://learn.microsoft.com/en-us/azure/architecture/patterns/queue-based-load-leveling
- 斷路器模式：https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker
- 過載處理與連鎖故障（Google SRE 書）：https://sre.google/sre-book/handling-overload/ 、https://sre.google/sre-book/addressing-cascading-failures/
- 冪等鍵（Stripe 的做法是業界範本）：https://docs.stripe.com/api/idempotent_requests ；IETF 草案：https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/
- InnoDB 行鎖：https://dev.mysql.com/doc/refman/8.4/en/innodb-locking.html
- 429 狀態碼：https://www.rfc-editor.org/rfc/rfc6585#section-4

**與既有課的關係**：多層快取、Bloom Filter、令牌桶基礎、號段模式見面試集第 3 課；分散式鎖為什麼會破見資料庫第 5 課；Gateway 限流見面試集第 2 課。本課接著第 3 課寫，題型從「讀多寫少」換成「寫多且要搶」。

**估計**：3,000〜3,400 字；測驗 9 題。

---

#### 面試課 G：認證與安全面試題：JWT、OAuth 2.0、OIDC 與密碼保存（分組：網路、安全與部署）——最急（銀行業）

**常考題（15 題）**
1. 認證與授權差在哪？Session 對 Token 各自的優缺點？
2. JWT 三段是什麼？簽章怎麼驗？`alg: none` 與演算法混淆攻擊是什麼？
3. JWT 怎麼過期、怎麼撤銷？Refresh Token 的角色；Token 放 Cookie 還是 localStorage？
4. OAuth 2.0 的四個角色與授權碼流程；為什麼不建議 Implicit 流程？
5. PKCE 解決什麼？
6. OAuth 2.0 與 OIDC 差在哪？ID Token 對 Access Token
7. SAML 是什麼、跟 OIDC 差在哪？企業單一登入為什麼還在用 SAML？
8. Basic 認證與 Bearer 認證的格式與風險
9. 密碼怎麼存？為什麼 MD5／SHA-256 加鹽也不夠？bcrypt、scrypt、Argon2、PBKDF2 怎麼選？
10. Spring Security 的 `DelegatingPasswordEncoder` 做了什麼？
11. Spring Security 當 OAuth 2.0 資源伺服器怎麼驗 JWT？
12. OWASP 十大風險現行版有哪幾項？各給一個例子與防法
13. SQL 注入、XSS、CSRF、SSRF 各怎麼防？
14. CSP 標頭在擋什麼？跟 XSS 的關係
15. 機密（API 金鑰、資料庫密碼）該放哪？（環境變數、Secret 管理服務、不進 git）

**出處**
- JWT：https://www.rfc-editor.org/rfc/rfc7519 ；JWT 安全最佳實務（演算法混淆等）：https://www.rfc-editor.org/rfc/rfc8725
- OAuth 2.0：https://www.rfc-editor.org/rfc/rfc6749 ；PKCE：https://www.rfc-editor.org/rfc/rfc7636 ；OAuth 2.0 安全最佳實務（不建議 Implicit）：https://www.rfc-editor.org/rfc/rfc9700
- Bearer：https://www.rfc-editor.org/rfc/rfc6750 ；Basic：https://www.rfc-editor.org/rfc/rfc7617
- OIDC Core：https://openid.net/specs/openid-connect-core-1_0.html
- SAML 技術總覽：https://docs.oasis-open.org/security/saml/Post2.0/sstc-saml-tech-overview-2.0.html
- 密碼保存（OWASP 速查表，含各演算法的建議參數）：https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- NIST 數位身分指引（密碼規則）：https://pages.nist.gov/800-63-4/sp800-63b.html
- Spring Security 密碼儲存：https://docs.spring.io/spring-security/reference/features/authentication/password-storage.html
- Spring Security JWT 資源伺服器：https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html
- OWASP Top 10：https://owasp.org/Top10/ （寫課時確認現行是哪一版——2025 版已於 2025 年底發佈，清單跟 2021 版不同）
- CSP：https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP 、https://www.w3.org/TR/CSP3/
- SSRF：https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html

**與既有課的關係**：Spring Security 認證流程與 Filter 鏈見 Spring 第 9 課；CORS、CSRF、雜湊與鹽見第 10 課；Gateway 驗 Token 見面試集第 2 課。本課補協定本身與演算法名字。

**估計**：3,400〜3,800 字；測驗 10 題。

---

#### 面試課 H：系統設計：訊息佇列與最終一致性（分組：系統設計）——可以等（但建議面試前做完）

**常考題（13 題）**
1. 什麼時候該引進訊息佇列？（解耦、削峰、非同步）代價是什麼？
2. Kafka 與 RabbitMQ 差在哪？（日誌對佇列、拉對推、消費者群組對交換器）
3. 三種送達保證：至多一次、至少一次、剛好一次——哪個做得到、代價是什麼？
4. 消費者怎麼做到冪等？（去重表、唯一鍵、版本號）
5. 訊息順序怎麼保證？Kafka 的分區與 key
6. 訊息丟了怎麼辦？（生產者確認、副本、消費者手動 ack）
7. 訊息堆積怎麼處理？（增加消費者、分區數限制、批次）
8. 死信佇列是什麼、什麼時候用？
9. 交易式 Outbox：為什麼「先寫資料庫再發訊息」會不一致？Outbox 怎麼解？
10. Saga 的兩種協調方式與補償設計（面試集第 2 課已有一句話，這裡展開狀態機）
11. 最終一致性對強一致性：業務上怎麼跟人解釋「暫時看不到」？
12. 銀行轉帳可以用最終一致嗎？（帳務分錄、對帳、冪等）
13. 訊息佇列在 Spring 怎麼接？（`@KafkaListener`、`@RabbitListener` 各一眼）

**出處**
- Kafka 設計與訊息送達語意：https://kafka.apache.org/documentation/#design 、https://kafka.apache.org/documentation/#semantics
- Kafka 消費者群組與分區：https://kafka.apache.org/documentation/#intro_consumers
- RabbitMQ 可靠性指南：https://www.rabbitmq.com/docs/reliability ；確認機制：https://www.rabbitmq.com/docs/confirms ；死信交換器：https://www.rabbitmq.com/docs/dlx
- 交易式 Outbox：https://microservices.io/patterns/data/transactional-outbox.html 、AWS 版：https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html
- Saga：https://microservices.io/patterns/data/saga.html 、AWS 版：https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/saga.html
- Spring for Apache Kafka：https://docs.spring.io/spring-kafka/reference/ ；Spring AMQP：https://docs.spring.io/spring-amqp/reference/
- Amazon SQS 的可見性逾時與 FIFO（Tim 走 AWS，帶一段）：https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html

**與既有課的關係**：Saga 一句話、2PC 對最終一致見面試集第 2 課；Outbox 提及見第 3 課。本課是那兩處的展開版。

**估計**：3,000〜3,400 字；測驗 9 題。

---

#### 面試課 I：系統設計：快取一致性與熱點（分組：系統設計）——可以等

**常考題（11 題）**
1. 三種快取讀寫模式：Cache-Aside、Read/Write-Through、Write-Behind
2. 更新資料時先刪快取還是先更新資料庫？延遲雙刪解決什麼、沒解決什麼？
3. 快取雪崩、穿透、擊穿各是什麼、各怎麼防？（隨機 TTL、Bloom Filter、互斥重建、邏輯過期）
4. 熱 key 怎麼發現、怎麼拆？
5. 大 key 為什麼危險？
6. Redis 的資料結構各適合什麼？（String、Hash、List、Set、ZSet、Bitmap、HyperLogLog）
7. Redis 為什麼快？單執行緒模型與 I/O 多路複用
8. Redis 持久化：RDB 對 AOF
9. Redis 的淘汰策略（`maxmemory-policy`）
10. 本地快取對分散式快取：Caffeine 加 Redis 的兩層怎麼失效？
11. HTTP 層的快取（CDN、`Cache-Control`）跟應用層快取怎麼分工？

**出處**
- 快取策略白皮書（AWS，含 Cache-Aside、Write-Through、TTL）：https://docs.aws.amazon.com/whitepapers/latest/database-caching-strategies-using-redis/welcome.html
- Cache-Aside 模式：https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside
- Redis 資料型別：https://redis.io/docs/latest/develop/data-types/
- Redis 持久化：https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/
- Redis 淘汰策略：https://redis.io/docs/latest/develop/reference/eviction/
- Redis 執行緒模型（FAQ）：https://redis.io/docs/latest/develop/get-started/faq/
- Redis 客戶端快取：https://redis.io/docs/latest/develop/reference/client-side-caching/
- Caffeine：https://github.com/ben-manes/caffeine/wiki
- Spring Cache 抽象：https://docs.spring.io/spring-framework/reference/integration/cache.html
- HTTP 快取：https://www.rfc-editor.org/rfc/rfc9111

**與既有課的關係**：多層快取查詢順序、Bloom Filter 防穿透見面試集第 3 課；Redis 四種擺法見資料庫第 5 課。

**估計**：2,800〜3,200 字；測驗 9 題。

---

#### 面試課 J：資料庫面試題：複寫、分片與 CAP（分組：資料庫）——可以等

**常考題（11 題）**
1. 主從複寫怎麼運作？（binlog、非同步對半同步）複寫延遲造成什麼問題？
2. 讀寫分離後「剛寫完讀不到」怎麼處理？
3. 垂直分割對水平分割；什麼時候該分片？
4. 分片鍵怎麼選？按範圍、按雜湊、一致性雜湊各適合什麼？
5. 跨分片的 JOIN、事務、全域唯一 ID 怎麼辦？
6. CAP 定理到底說什麼？為什麼「三選二」是誤解？PACELC
7. 什麼是 BASE？
8. 資料庫連線池為什麼重要？大小怎麼估？（HikariCP）
9. 資料庫常見的壞法：連線耗盡、鎖等待、磁碟滿、複寫斷掉——各怎麼發現？
10. 冷熱資料分離、歸檔
11. 什麼時候該用 NoSQL？（帶 DynamoDB 一眼，Tim 走 AWS）

**出處**
- MySQL 複寫：https://dev.mysql.com/doc/refman/8.4/en/replication.html ；半同步：https://dev.mysql.com/doc/refman/8.4/en/replication-semisync.html ；GTID：https://dev.mysql.com/doc/refman/8.4/en/replication-gtids.html
- CAP 作者 Brewer 十二年後的澄清：https://www.infoq.com/articles/cap-twelve-years-later-how-the-rules-have-changed/ ；Gilbert 與 Lynch 的形式證明：https://users.ece.cmu.edu/~adrian/731-sp04/readings/GL-cap.pdf
- 一致性雜湊（Dynamo 論文第 4.2 節）：https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf
- HikariCP 連線池大小：https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing
- Spring Boot 資料來源設定：https://docs.spring.io/spring-boot/reference/data/sql.html
- DynamoDB 核心元件與分割鍵：https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.CoreComponents.html
- Aurora 讀取複本：https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Replication.html

**與既有課的關係**：分片對複寫一段見資料庫第 4 課、RDS 的 Standby 對 Read Replica 見雲端第 6 課、Redis 叢集見資料庫第 5 課。

**估計**：2,800〜3,200 字；測驗 9 題。

---

#### 面試課 K：容器與部署面試題：映像分層、K8s 部署策略與探針（分組：網路、安全與部署）——可以等

**常考題（14 題）**
1. 容器與虛擬機差在哪？（namespace、cgroup）
2. Docker 映像分層怎麼運作？為什麼改一行 Dockerfile 會讓後面全部重建？
3. 多階段建置解決什麼？Spring Boot 的分層 JAR（layered jar）是什麼？
4. `CMD` 對 `ENTRYPOINT`；`COPY` 對 `ADD`
5. 容器裡跑 Java 要注意什麼？（JVM 讀得到 cgroup 限制嗎、堆大小、`-XX:MaxRAMPercentage`）
6. Pod、Deployment、ReplicaSet、Service、Ingress 各是什麼？
7. 滾動更新的 `maxSurge`、`maxUnavailable`；怎麼回退？
8. 藍綠對金絲雀對滾動：各適合什麼？K8s 原生做得到哪些？
9. 存活、就緒、啟動三種探針各決定什麼？設錯會怎樣？
10. `requests` 對 `limits`；QoS 等級；OOMKilled 是什麼？
11. ConfigMap 對 Secret；Secret 其實只是 base64 該怎麼看？
12. HPA 依什麼擴縮？
13. CI/CD 管線長什麼樣？（建置 → 測試 → 掃描 → 打映像 → 推 registry → 部署）GitHub Actions 的 workflow 基本結構
14. 十二要素應用是什麼？哪幾條跟容器化直接相關？

**出處**
- 映像分層：https://docs.docker.com/get-started/docker-concepts/building-images/understanding-image-layers/
- Dockerfile 最佳實務（快取順序、`CMD`／`ENTRYPOINT`）：https://docs.docker.com/build/building/best-practices/
- 多階段建置：https://docs.docker.com/build/building/multi-stage/
- Dockerfile 參考：https://docs.docker.com/reference/dockerfile/
- Spring Boot 容器映像與分層 JAR：https://docs.spring.io/spring-boot/reference/packaging/container-images/index.html
- JVM 容器感知（`-XX:MaxRAMPercentage`）：https://docs.oracle.com/en/java/javase/21/docs/specs/man/java.html （搜 `MaxRAMPercentage`、`UseContainerSupport`）
- Deployment 策略與回退：https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- 金絲雀（官方管理部署頁）：https://kubernetes.io/docs/concepts/cluster-administration/manage-deployment/#canary-deployments
- 探針：https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/ 、https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
- 資源與 QoS：https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ 、https://kubernetes.io/docs/concepts/workloads/pods/pod-qos/
- Secret：https://kubernetes.io/docs/concepts/configuration/secret/
- HPA：https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/
- 藍綠部署定義（Fowler）：https://martinfowler.com/bliki/BlueGreenDeployment.html
- GitHub Actions 工作流程語法：https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions
- 十二要素：https://12factor.net/

**與既有課的關係**：K8s 模組 21 課已把 Pod／Deployment／Service／Ingress／Dockerfile／多階段建置／namespace／cgroup 教完——本課每題一句「見 K8s 第 N 課」，只寫面試追問層（參數、探針分工、QoS、JVM 在容器裡、管線）。

**估計**：3,000〜3,400 字；測驗 10 題。

---

#### 面試課 L：微服務與架構面試題：服務發現、韌性、可觀測性與十二要素（分組：後端與雲端）——可以等

跟既有第 2 課重疊最多，寫法是「第 2 課答過的不重寫，只補第 2 課沒展開的」。

**常考題（13 題）**
1. 單體對 SOA 對微服務：SOA 的 ESB 跟 API Gateway 差在哪？（銀行業必問）
2. 服務發現兩種模式（客戶端對伺服器端）；K8s 的 Service 算哪種？
3. 集中設定怎麼做？（Spring Cloud Config、K8s ConfigMap）
4. 斷路器的三個狀態怎麼切換？滑動視窗、失敗率門檻、半開試探（Resilience4j 的參數名）
5. 重試要配什麼才安全？（退避、抖動、冪等、上限）
6. 隔艙（Bulkhead）解決什麼？
7. 逾時怎麼設？為什麼逾時比重試更重要？
8. 可觀測性三種訊號怎麼分工？四個黃金訊號是什麼？
9. Prometheus 的拉取模型、Micrometer 與 Actuator 怎麼把指標吐出來？
10. 分散式追蹤：trace ID 怎麼傳遞？OpenTelemetry 在做什麼？
11. Service Mesh 是什麼、解決什麼、代價是什麼？
12. Serverless 適合什麼、不適合什麼？冷啟動
13. 十二要素裡最常被問的：設定、日誌當事件流、無狀態行程

**出處**
- Resilience4j 斷路器（狀態、參數）：https://resilience4j.readme.io/docs/circuitbreaker ；重試：https://resilience4j.readme.io/docs/retry ；隔艙：https://resilience4j.readme.io/docs/bulkhead
- 斷路器、重試、隔艙模式（Azure 架構中心）：https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker 、https://learn.microsoft.com/en-us/azure/architecture/patterns/retry 、https://learn.microsoft.com/en-us/azure/architecture/patterns/bulkhead
- 四個黃金訊號：https://sre.google/sre-book/monitoring-distributed-systems/
- OpenTelemetry 訊號：https://opentelemetry.io/docs/concepts/signals/
- Prometheus 總覽：https://prometheus.io/docs/introduction/overview/
- Micrometer：https://docs.micrometer.io/micrometer/reference/
- Spring Boot Actuator 指標與追蹤：https://docs.spring.io/spring-boot/reference/actuator/metrics.html 、https://docs.spring.io/spring-boot/reference/actuator/tracing.html
- Spring Cloud 服務發現與設定：https://docs.spring.io/spring-cloud-netflix/reference/ 、https://docs.spring.io/spring-cloud-config/reference/
- Istio 是什麼：https://istio.io/latest/docs/overview/what-is-istio/
- AWS Lambda 執行環境生命週期（冷啟動）：https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtime-environment.html
- 十二要素：https://12factor.net/
- 微服務模式（Richardson）：https://microservices.io/patterns/index.html

**與既有課的關係**：第 2 課已答服務發現／熔斷／Saga／監控／Gateway 各一題——本課開頭就寫「第 2 課那五題是骨架，這課補肉」，每題指回去。

**估計**：3,000〜3,400 字；測驗 9 題。

---

#### 面試課 M：行為面試與專題表達（分組：準備與表達）——可以等（但寫起來最快，可以插隊）

**內容（不是問答題，是方法＋範例）**
1. STAR 法（情境、任務、行動、結果）怎麼套在工程師的故事上；常見的五類行為題（衝突、失敗、壓力、學新東西、影響別人）
2. 「介紹一下你自己」的兩分鐘骨架
3. 專題表達：問題 → 為什麼難 → 我的決定與取捨 → 結果與數字 → 事後會改什麼（第 1 課那段訂房網站範例升級成通用模板）
4. 被問「你最有挑戰的技術問題」時，怎麼把 K8s／Spring／資料庫的經驗講成有數字的故事
5. 反問面試官的十個問題（技術債、上線流程、值班、團隊怎麼做決定）
6. 銀行業特有：法遵與資安意識怎麼在回答裡自然帶到
7. 薪資與時程問題怎麼回
8. 面試前一週的複習清單（把本站哪幾課排進去——這一段就是面試集的目錄）

**出處**：行為面試沒有「官方文件」，用大公司公開的面試指引：
- Amazon 面試指引（STAR 法的官方描述）：https://www.amazon.jobs/content/en/how-we-hire/interviewing-at-amazon
- Google 結構化面試指引：https://rework.withgoogle.com/en/guides/hiring-use-structured-interviewing
- Google「我們怎麼面試」：https://www.google.com/about/careers/applications/how-we-hire/

這一課的每句主張都不是技術事實，出處只證明「STAR 法是這幾家公司公開建議的方法」，其餘是建議，寫的時候用「可以」「建議」不用「一定」。

**與既有課的關係**：把面試集第 1 課「專題怎麼答」那段升級；第 1 課保留原範例、加一句「通用骨架見第 M 課」。

**估計**：2,200〜2,600 字；測驗 6 題（考方法，不考事實）。

---

### 面試集擴充後的樣子

| 分組 | 課 |
|---|---|
| Java | 1 基礎快答（既有）、B JVM 記憶體與垃圾回收、C 並行 |
| Spring | A Spring 面試快答 |
| 資料庫 | D 索引、交易隔離與鎖、J 複寫、分片與 CAP |
| 後端與雲端 | 2 後端與雲端問答（既有）、L 微服務與架構 |
| 網路、安全與部署 | E 網路與 HTTP、G 認證與安全、K 容器與部署 |
| 系統設計 | 3 短網址（既有）、F 秒殺與限流、H 訊息佇列與最終一致性、I 快取一致性 |
| 準備與表達 | M 行為面試與專題表達 |

3 課 → 16 課。面試集的 `module.json` 的 `overview_intro` 與 `footer_note` 要改寫（現在寫的是「把面試筆記整理成問答集…更正過的地方都有標記」，新課沒有更正標記）。

---

## 第三部分：其他模組要補的課

面試課是「速查」，教材課是「打底」。面試課先寫，教材課後寫；教材課寫完後回頭把面試課裡「這裡先簡述」的段落改成「見 ○ 模組第 N 課」。

排序原則：面試下個月會考的排最前；同等級的，面試課已經寫過、教材課只是展開的排後面。

### 最急（面試會考，且面試課無法完整涵蓋）

| 序 | 模組 | 課名（暫定） | 涵蓋 | 主要出處 | 與既有課關係 | 字數／題數 |
|---|---|---|---|---|---|---|
| 1 | 資料庫 | 索引是怎麼運作的 | B+ 樹、聚簇與二級索引、回表、複合索引與最左前綴、覆蓋索引、索引失效寫法、EXPLAIN 逐欄、慢查詢日誌、什麼欄位不該建索引 | MySQL 8.4 手冊索引章、EXPLAIN 章（面試課 D 的出處） | 接第 2 課 SQL、第 3 課正規化之後；面試課 D 指回來 | 2,800〜3,200／10 |
| 2 | 資料庫 | 交易隔離層級與鎖 | 三種讀異常、四個層級、MVCC 與 undo log、記錄鎖／間隙鎖／Next-Key、悲觀與樂觀、死結範例與排查、Online DDL | MySQL 8.4 手冊交易與鎖章、PostgreSQL 隔離頁 | 第 2 課 ACID 一段的展開；Spring 第 6 課 `@Transactional` 指回來 | 2,800〜3,200／10 |
| 3 | Java | JVM 記憶體與垃圾回收 | 執行期資料區、堆的分代、GC Root 與可達性、Serial／Parallel／G1／ZGC、STW、OOM 種類、記憶體洩漏來源、類別載入與雙親委派、JIT 分層編譯、`jcmd`／`jstack`／`jmap`／JFR 各看什麼 | JVMS 第 2、5 章、HotSpot GC 調校指南、JEP 248／377／439、Oracle 疑難排解指南 | 第 1 課「從 .java 到 .class」的下一層；建議新開「JVM 與效能」組放在「並行與設計」組之前 | 3,000〜3,400／10 |
| 4 | Java | 執行緒池與並行工具 | `ThreadPoolExecutor` 參數與流程、拒絕策略、大小估算、`Executors` 的坑、`CompletableFuture` 組合、`ConcurrentHashMap` 原理、`CountDownLatch`／`Semaphore`、`ThreadLocal`、`BlockingQueue` 生產者消費者、happens-before 表 | Java 21 API 文件、JLS 第 17 章 | 第 10 課的續篇 | 2,800〜3,200／10 |
| 5 | Spring | `@Transactional` 的傳播、隔離與失效情境 | 七種傳播行為對照表與範例、隔離層級在 Spring 怎麼設、`rollbackFor`、唯讀交易、self-invocation 失效、非 public 失效、多執行緒失效、事件監聽與交易（`@TransactionalEventListener`）、交易與 JPA 的 flush 時機 | Spring Framework 交易章、Spring Data JPA 參考 | 第 6 課只講「交給 Spring 管理交易邊界」與 self-invocation——本課接在第 6 課後面（新序號，不插隊） | 2,600〜3,000／9 |
| 6 | Spring | Spring Boot 自動組態與 Actuator | 自動組態原理、`@Conditional` 家族、`AutoConfiguration.imports`、怎麼看哪些組態生效（`--debug`）、外部化設定優先順序、Profile、Actuator 端點、健康檢查與 K8s 探針對接、指標端點 | Spring Boot 參考：auto-configuration、external-config、actuator | 第 5 課「三種設定風格」的下一層；K8s 第 19 課探針指回來 | 2,600〜3,000／9 |
| 7 | 網頁 | TCP、UDP 與 TLS 握手 | OSI 對 TCP/IP 分層、三向交握逐步、四向揮手與 TIME_WAIT、流量控制與壅塞控制一眼、UDP 適用場景、TLS 1.3 握手逐步、憑證鏈驗證、TLS 1.2 對 1.3 | RFC 9293、768、8446 | 第 1 課「封包、TCP/IP 與四層分工」與第 2 課「TLS 交握做了什麼」的展開；放「網路與伺服器」組 | 2,600〜3,000／9 |
| 8 | 網頁 | HTTP 進階：狀態碼、快取、Keep-Alive 與版本演進 | 狀態碼分類與常見 16 個、方法的冪等與安全、Keep-Alive 與隊頭阻塞、HTTP/2 多路複用與標頭壓縮、HTTP/3 與 QUIC、`Cache-Control`／`ETag`／304、`Vary`、內容協商 | RFC 9110、9111、9112、9113、9114、MDN | 第 2 課的展開 | 2,600〜3,000／9 |
| 9 | Spring | JWT 與 OAuth 2.0 在 Spring Security 裡怎麼接 | JWT 結構與驗簽、Refresh Token、資源伺服器設定、授權碼流程逐步、PKCE、OIDC 登入（`oauth2Login`）、`DelegatingPasswordEncoder`、方法層級授權 | RFC 7519／6749／7636／9700、OIDC Core、Spring Security 參考 | 第 9 課「認證與授權」的下一層；放「安全」組 | 2,800〜3,200／10 |

### 可以等（面試可能考，面試課已能撐住）

| 序 | 模組 | 課名（暫定） | 涵蓋 | 主要出處 | 與既有課關係 | 字數／題數 |
|---|---|---|---|---|---|---|
| 10 | 資料庫 | 快取放哪裡、怎麼失效 | 三種讀寫模式、失效順序與延遲雙刪、雪崩／穿透／擊穿、熱 key 與大 key、Redis 資料結構、持久化、淘汰策略、兩層快取 | AWS 快取白皮書、Redis 官方文件、Spring Cache | 第 5 課把 Redis 當鎖講，本課把它當快取講；面試集第 3 課多層快取指回來 | 2,800〜3,200／10 |
| 11 | Spring | 訊息佇列：Spring 接 Kafka 與 RabbitMQ | 為什麼要佇列、Kafka 對 RabbitMQ 模型、送達保證、`@KafkaListener` 與手動 ack、冪等消費、死信、Outbox 實作骨架 | Kafka、RabbitMQ、Spring Kafka、Spring AMQP 官方文件 | 新內容；面試課 H 指回來；放「測試與工具」組或新開「整合」組 | 2,800〜3,200／9 |
| 12 | Spring | 整合測試：`@SpringBootTest`、MockMvc 與 Testcontainers | 測試金字塔、切片測試（`@WebMvcTest`、`@DataJpaTest`）對全容器、MockMvc、Testcontainers 起真資料庫、`@MockitoBean`、測試資料與交易回復、契約測試一眼 | Spring Boot testing 章、Spring Framework MockMvc、Testcontainers、Fowler 測試金字塔 | 第 11 課單元測試的續篇 | 2,600〜3,000／9 |
| 13 | Spring | JPA 效能：N+1、延遲載入與批次 | N+1 怎麼發生、`JOIN FETCH`、`@EntityGraph`、`@BatchSize`、開放式 Session 的坑（`open-in-view`）、批次寫入、一級快取與 flush、投影 DTO | Hibernate 6 使用指南 fetching 章、Spring Data JPA 參考、Spring Boot `spring.jpa.open-in-view` 說明 | 第 3 課「延遲載入與交易邊界」與第 4 課「投影與 DTO」的展開 | 2,600〜3,000／9 |
| 14 | Spring | 韌性模式：Resilience4j 的斷路器、重試與限流 | 三態切換、參數、重試與退避、隔艙、逾時、限流器、與 Actuator 指標的接法、降級回呼 | Resilience4j 文件、Azure 架構模式、SRE 書 | 第 12 課「微服務不是免費的效能按鈕」提到的降級與熔斷，本課實作；面試課 L 指回來 | 2,600〜3,000／9 |
| 15 | Spring | 可觀測性：Micrometer、Prometheus 與 OpenTelemetry | 三種訊號、四個黃金訊號、Actuator 指標端點、Prometheus 拉取、Grafana 一眼、Micrometer Tracing 與 trace ID 傳遞、結構化日誌與 MDC、告警怎麼定 | Micrometer、Spring Boot Actuator、Prometheus、OpenTelemetry、SRE 書 | 面試集第 2 課「端到端監控」一題的教材版 | 2,800〜3,200／9 |
| 16 | Spring | API 設計進階：版本、分頁、冪等與錯誤格式 | 版本策略三種、分頁三種（偏移、游標、鍵集）、冪等鍵、`ProblemDetail`（RFC 9457）、OpenAPI 與 springdoc、REST 對 gRPC 對 GraphQL 對 SOAP 選型表 | RFC 9110／9457、OpenAPI 規格、springdoc 文件、gRPC／GraphQL 官方 | 第 7 課「RESTful API 的基本設計」的下一層 | 2,600〜3,000／9 |
| 17 | K8s | 部署策略與探針 | 滾動更新參數、回退、藍綠與金絲雀在 K8s 怎麼做（原生對 Argo Rollouts 一眼）、三種探針、QoS 與 OOMKilled、PodDisruptionBudget、JVM 在容器裡的記憶體設定 | K8s 官方文件、Spring Boot 容器映像章、Java 21 `java` 指令手冊 | 第 8 課「換版本不停機」、第 18／19 課探針一句的展開；放「實作篇」 | 2,600〜3,000／9 |
| 18 | 網頁 | CI/CD：從 push 到上線 | 管線階段、GitHub Actions 結構（workflow／job／step／runner）、快取相依、建映像推 registry、部署到 K8s 的兩種方式（推對拉，GitOps 一眼）、環境與核准、以本站自己的 `deploy.yml` 當範例 | GitHub Actions 文件、Docker 文件、Argo CD 或 Flux 概念頁 | 第 5 課 SDLC 的「落地做法」；放「開發流程」組 | 2,400〜2,800／8 |
| 19 | Java | 作業系統怎麼跑程式：行程、執行緒、記憶體與 I/O | 行程對執行緒、上下文切換成本、使用者態對核心態、虛擬記憶體與分頁、I/O 五種模型（阻塞、非阻塞、多路複用、訊號驅動、非同步）、`select`／`epoll`、檔案描述子、零拷貝一眼、Java NIO 對應 | man7 手冊（`fork`、`pthreads`、`epoll`、`namespaces`、`cgroups`）、OSTEP 教科書（https://pages.cs.wisc.edu/~remzi/OSTEP/ ）、Java NIO API | 第 10 課「程式、行程與執行緒」比喻的正式版；K8s 第 20 課 namespace／cgroup 指回來；放第 10 課之前（新開「JVM 與效能」組） | 2,800〜3,200／9 |
| 20 | 網頁 | OWASP 十大風險與 CSP | 現行版十大風險逐條一例一防、注入／XSS／SSRF、CSP 標頭、安全標頭清單（HSTS、X-Content-Type-Options、Referrer-Policy）、伺服器加固基本（SSH 金鑰、防火牆、最小權限）、機密管理 | OWASP Top 10、OWASP 速查表、MDN CSP、CIS Benchmarks 概念頁 | Spring 第 10 課三題的外圍；放「網路與伺服器」組 | 2,600〜3,000／9 |

### 有空再說

| 模組 | 課名（暫定） | 涵蓋 | 出處 |
|---|---|---|---|
| 網頁 | 即時通訊：WebSocket、SSE 與輪詢 | 三種做法對比、握手、Spring WebSocket 與 STOMP 一眼、SSE 在 Spring 的 `SseEmitter` | RFC 6455、WHATWG SSE 規格、Spring WebSocket 章 |
| 網頁 | Git 分支與協作 | 三區模型、分支與合併、rebase 對 merge、衝突解法、reflog 救回、常見分支策略（trunk-based、GitHub Flow）、PR 流程 | Pro Git 第 2、3、7 章、GitHub 文件 |
| Spring | 資料庫遷移：Flyway 與 Liquibase | 為什麼不能靠 `ddl-auto`、版本化腳本、Spring Boot 整合、回退策略 | Flyway、Liquibase 文件、Spring Boot data-initialization 章 |
| Java | SOLID 與常見反模式 | 五原則各一例、與設計模式的關係 | 沒有單一官方出處；引 Robert C. Martin 原文與 Fowler 文章，寫的時候用「原則」不用「規定」——也可以併進第 11 課補強 |
| 雲端 | 負載平衡、自動擴展與訊息服務 | ALB 對 NLB、目標群組與健康檢查、Auto Scaling、SQS／SNS | AWS 官方文件 |
| 雲端 | DynamoDB 與 NoSQL 選型 | 分割鍵、單表設計、一致性讀、與 RDS 的取捨 | DynamoDB 開發者指南 |
| K8s | Service Mesh 與 Serverless 取捨 | sidecar、mTLS、流量切分；Lambda／Cloud Run 適用場景 | Istio、AWS Lambda、Cloud Run 文件 |

### 不建議新開模組

「系統設計」目前放面試集就好——四課（短網址、秒殺、訊息佇列、快取一致性）都是面試題形狀。等超過六課再問 Tim 要不要獨立成模組（規格：未經 Tim 點頭不新開模組）。

---

## 第一批（本週）：先做這五課

| 序 | 課 | 為什麼先做 |
|---|---|---|
| 1 | 面試課 A〈Spring 面試快答〉 | Tim 主力技術，Java 後端面試百分之百會問 Spring；Spring 模組已有 12 課可指路，新寫量最小、查證負擔最輕（出處全在 docs.spring.io 一個站） |
| 2 | 面試課 D〈資料庫面試題：索引、交易隔離與鎖〉 | 全站最大單一缺口（索引零命中）；銀行業後端面試的必考題；MySQL 手冊是最穩定、最精確的出處，寫錯的風險低 |
| 3 | 面試課 B〈Java 進階快答：JVM 記憶體與垃圾回收〉 | Java 面試的第二道菜，站上幾乎為零；JVMS、JEP、Oracle 調校指南都是穩定出處 |
| 4 | 面試課 E〈網路與 HTTP 面試題〉 | 不分公司都會問的通用題（三向交握、HTTPS、狀態碼、REST 對 gRPC）；RFC 是最不會改版的出處，寫一次能用很多年 |
| 5 | 面試課 F〈系統設計：秒殺與限流〉 | 銀行業系統設計題的典型形狀（高併發交易）；直接接在既有第 3 課之後，思路連貫；同時把限流、佇列、快取一致性、斷路器四個核心缺口一次帶到（後面 H、I、L 三課再展開） |

第二批（下週）：C 並行、G 認證與安全、K 容器與部署、M 行為面試（M 寫得快，可以插隊）。第三批：H、I、J、L，然後開始教材課 1〜9。

寫作節奏照批次慣例：一次一課、實作代理用 Fable、審查代理用 Opus、每課建置預覽給 Tim 看過才 push；push 前看 `git log --oneline origin/main..HEAD`。

---

## 給寫課代理的注意事項

1. **每個技術主張都要有出處連結**。這次沒有原筆記當擋箭牌，「常識」也要連到文件。查不到的就不寫，或改寫成「常見做法是…」並附能找到的最接近出處。
2. **版本要寫明**：Java 以 21 為準（25 也是長期支援版，差異處註明）、Spring Boot 以 3.x 為準（4.0 若已正式發佈，寫課當天查一次 https://spring.io/projects/spring-boot#support ）、MySQL 以 8.4 為準、Kubernetes 以當下穩定版為準。
3. **面試課的答案形狀**照既有第 2 課：一句話定義 → 差別與取捨 → 版本或實務註記 → 出處。每題 150〜300 字。
4. **用詞**照 `~/.claude/tim-style/RULES.md`：台灣講法（快取、資料庫、執行緒、伺服器、記憶體、物件、函式）；第一次出現的名詞附白話（例如「MVCC（多版本並行控制——每筆資料留多個版本，讀的人看舊版、寫的人寫新版，兩邊不必互等）」）；不發明編號代號；不造字。「上下文切換」「隊頭阻塞」「回表」「熔斷」這些是業界通用譯名，第一次出現一樣要附白話。
5. **不寫第一人稱、不寫工作紀錄**（「這裡查了…」「本課選擇…」不准出現）。
6. **跨課指路一律寫「見 ○ 模組第 N 課〈課名〉」**，不寫「另一課」「前面提過」。
7. **AI 工具那批出處改版快**，這批的出處（RFC、JVMS、MySQL 手冊、Spring 參考）相對穩，但 Spring Boot 與 Kubernetes 文件會隨版本搬頁，寫完當天再開一次每個連結確認引文還在。
8. `module.json` 的 `overview_intro`／`footer_note` 提到「更正過的地方都有標記」的字句，在新課加入的模組要改寫，因為新課沒有更正標記。
9. 面試集新開四個分組（Spring、資料庫、網路安全與部署、準備與表達），`group` 欄位照上表填；既有三課的 `group` 不動。
10. 本計畫的「課 A〜M」「序 1〜20」只是這份計畫內部的指稱，**不能出現在課文或 `module.json` 裡**——上站一律用課名。
