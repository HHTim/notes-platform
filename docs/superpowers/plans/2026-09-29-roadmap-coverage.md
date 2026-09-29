# roadmap.sh/backend 對照表（2026-09-29）

資料來源：`https://roadmap.sh/api/v1-official-roadmap/backend`（roadmap.sh 網站自己讀的那份 JSON，已存成同目錄 `backend.json`；節點清單在 `nodes.txt`）。
節點型別：`topic`（大節點）23 個、`subtopic`（子節點）132 個，合計 **155 個**；另有 6 個「連到別張 roadmap」的按鈕（Docker、Kubernetes、System Design、Design & Architecture、DevOps、API Security Best Practices），不計入 155，但在最後一節另列。

對照方法：把 92 課 `lesson.html` 去掉標籤後做關鍵字掃描，再逐課看段落標題（`outline.txt`）確認是真的有教還是只是提到名字。

三種判定：
- **有教**：有一段或一課專門講，讀完能回答面試官的追問。
- **只點到**：出現過名字或一句話定義，沒有展開（例如只在面試集某題答案裡帶到）。
- **完全沒有**：全站零命中，或命中的是同字不同義（例如 Java 課的「陣列索引」不是資料庫索引）。

## 總計

| | 大節點（23） | 子節點（132） | 合計（155） |
|---|---|---|---|
| 有教 | 12 | 44 | **56** |
| 只點到 | 9 | 26 | **35** |
| 完全沒有 | 2 | 62 | **64** |

完全沒有的 64 個裡，有 33 個是「特定產品或語言」（Go、Rust、Cassandra、Solr 之類），屬次要缺口；剩下 31 個加上「只點到」的 35 個，才是要補課的對象。分級見 `plan.md` 第一部分。

## 逐節點對照

### Introduction（大節點：有教）

| 子節點 | 判定 | 在哪裡 |
|---|---|---|
| How does the internet work? | 有教 | 網頁模組第 1 課〈網路是怎麼運作的〉全課 |
| What is HTTP? | 有教 | 網頁第 2 課〈HTTP 與 HTTPS〉；Spring 第 1、7 課也各有一段 |
| What is Domain Name? | 有教 | 網頁第 1 課「網域名稱、URL 與 DNS 不一樣」 |
| What is hosting? | 有教 | 網頁第 4 課〈Web Hosting 與 Nginx〉前兩段 |
| DNS and how it works? | 有教 | 網頁第 1 課「網路電話簿」、第 3 課「DNS 解析與快取」 |
| Browsers and how they work? | 有教 | 網頁第 3 課「瀏覽器渲染不是收到整頁才開始」（一段，偏淺） |

### Frontend Basics（有教）

| 子節點 | 判定 | 在哪裡 |
|---|---|---|
| HTML | 有教 | 網頁第 6 課 |
| CSS | 有教 | 網頁第 7 課 |
| JavaScript | 有教 | 網頁第 8 課 |

### Pick a Backend Language（有教——Java）

| 子節點 | 判定 | 在哪裡 |
|---|---|---|
| Java | 有教 | Java 模組 11 課、Spring 模組 12 課 |
| JavaScript | 有教 | 網頁第 8 課（基礎；沒有 Node.js 後端） |
| Go、Python、Ruby、C#、PHP、Rust | 完全沒有 | 次要缺口：roadmap 說「學一種就好」，Tim 的一種是 Java |

### Version Control Systems（只點到）

| 子節點 | 判定 | 在哪裡 |
|---|---|---|
| Git | 只點到 | 面試集第 1 課「專題怎麼答」一段講 Git 與 GitHub 差別；Angular 第 6 課提 lockfile。沒有任何一課教分支、合併、rebase、衝突 |

### Repo Hosting Services（只點到）

| 子節點 | 判定 | 在哪裡 |
|---|---|---|
| GitHub | 只點到 | 同上；AI 工具模組把 GitHub 當 Copilot 的家講 |
| GitLab | 完全沒有 | 次要 |

### Relational Databases（有教）

| 子節點 | 判定 | 在哪裡 |
|---|---|---|
| MySQL | 有教 | 資料庫第 1、2 課 |
| PostgreSQL | 完全沒有 | 次要，但面試常拿「MySQL 跟 PostgreSQL 差在哪」問，值得在資料庫面試課帶一題 |
| MariaDB、SQLite、Oracle | 完全沒有 | 次要 |
| MS SQL | 只點到 | 資料庫模組頁尾說「容易跟 SQL Server 規則混淆的地方課內標了更正」 |
| Migrations（Flyway／Liquibase） | 完全沒有 | 全站零命中 |
| N+1 Problem | 完全沒有 | Spring 第 3 課有「延遲載入與交易邊界」一段，但沒有點出 N+1 這個問題本身與解法（fetch join、批次） |

### Learn about APIs（有教）

| 子節點 | 判定 | 在哪裡 |
|---|---|---|
| REST | 有教 | Spring 第 7 課「RESTful API 的基本設計」；網頁第 2 課講方法與冪等 |
| JSON APIs | 只點到 | Spring 第 7 課講 JSON 七種值；沒講 JSON:API 這類規範 |
| SOAP | 完全沒有 | 銀行業舊系統常見，面試可能問「SOAP 跟 REST 差在哪」 |
| gRPC | 完全沒有 | |
| GraphQL | 完全沒有 | |
| Open API Specs | 只點到 | 面試集第 2 課「API 契約」那題提了一次 |
| Authentication | 有教 | Spring 第 9 課「認證與授權是兩道不同的門」 |
| JWT | 只點到 | 面試集第 2 課一句話定義＋Gateway 驗簽；沒講三段結構、演算法、過期與撤銷 |
| OAuth | 只點到 | 面試集第 2 課一句話；沒講四種授權流程、PKCE |
| Basic Authentication | 完全沒有 | |
| Token Authentication | 有教 | Spring 第 9 課「Cookie、Session 與權杖」 |
| Cookie Based Auth | 有教 | Spring 第 2 課 Cookie 與 Session、第 9 課 |
| OpenID | 完全沒有 | |
| SAML | 完全沒有 | 銀行業單一登入常用，面試可能問 |

### Caching（有教，偏面試題而非教材）

| 子節點 | 判定 | 在哪裡 |
|---|---|---|
| Redis | 有教 | 資料庫第 5 課把 Redis 當鎖講、面試集第 3 課當快取講；**沒有**資料結構、持久化、淘汰策略 |
| Memcached | 完全沒有 | 次要 |
| HTTP Caching | 只點到 | 網頁第 3 課各提一次 Cache-Control、ETag；沒講快取新鮮度、驗證、Vary |

### Learn about Web Servers（有教）

| 子節點 | 判定 | 在哪裡 |
|---|---|---|
| Nginx | 有教 | 網頁第 4 課反向代理、上游 DNS、rewrite |
| Apache、Caddy、MS IIS | 完全沒有 | 次要。站上另有 Tomcat（Spring 第 1 課），roadmap 沒列 |

### Web Security（有教，缺 OWASP 全貌）

| 子節點 | 判定 | 在哪裡 |
|---|---|---|
| Web Security | 有教 | Spring 第 10 課〈網站安全三題〉 |
| MD5 | 只點到 | Spring 第 10 課提一次 |
| SHA | 有教（雜湊觀念） | Spring 第 10 課「編碼、加密與雜湊」講雜湊與鹽；沒點名 SHA 家族 |
| scrypt、bcrypt | 完全沒有 | Spring 第 10 課「安全保存密碼」講了「不能只做一次快速雜湊」，但沒點名任何演算法（bcrypt、scrypt、Argon2、PBKDF2 全部零命中） |
| OWASP Risks | 只點到 | Spring 第 10 課提 OWASP 兩次、XSS 兩次；沒有十大風險的清單與各自解法 |
| HTTPS | 有教 | 網頁第 2 課 |
| SSL/TLS | 有教 | 網頁第 2 課「TLS 交握做了什麼」（一段；沒到 ClientHello、憑證鏈驗證步驟、TLS 1.3 少一趟往返這個深度） |
| CORS | 有教 | Spring 第 10 課兩段、Angular 第 4 課 |
| CSP | 完全沒有 | |
| Server Security | 完全沒有 | SSH 金鑰、防火牆、最小權限帳號、修補 |

### Learn the Basics（AI，有教）

| 子節點 | 判定 | 在哪裡 |
|---|---|---|
| How LLMs work | 有教 | 雲端第 8 課「生成原理」 |
| AI vs Traditional Coding | 有教 | AI 工具第 1、3 課 |
| Embeddings | 有教 | 雲端第 13 課主題二 |
| Vectors | 有教 | 同上＋AI 工具第 7 課知識庫 |
| RAGs | 有教 | 雲端第 8 課、AI 工具第 8 課 |

### AI Assisted Coding（有教）

| 子節點 | 判定 | 在哪裡 |
|---|---|---|
| Claude Code | 有教 | AI 工具第 1、2 課 |
| Cursor、Antigravity | 完全沒有 | 次要 |
| Copilot | 有教 | AI 工具第 3〜5 課 |
| Prompting Techniques | 有教 | 雲端第 9 課、AI 工具第 3 課 |
| Agents | 有教 | AI 工具第 4、8 課 |
| MCP | 有教 | AI 工具第 2、5、8 課 |
| Skills | 只點到 | AI 工具第 5 課講 Copilot 的提示檔與自訂代理人（同一件事的 Copilot 版）；Claude Code 的 skills 沒講 |

### Applications（AI 應用，只點到）

| 子節點 | 判定 | 在哪裡 |
|---|---|---|
| Code Reviews | 只點到 | AI 工具第 3 課「驗收」 |
| Refactoring、Documentation Generation | 完全沒有 | 次要 |

### AI Providers（只點到）

| 子節點 | 判定 | 在哪裡 |
|---|---|---|
| Anthropic | 只點到 | AI 工具模組頁尾與第 1 課 |
| Gemini、OpenAI | 完全沒有 | 次要（站上是用 Bedrock 講模型供應） |

### Integration Patterns（只點到）

| 子節點 | 判定 | 在哪裡 |
|---|---|---|
| Streaming | 完全沒有 | |
| Structured Outputs | 只點到 | 雲端第 9 課「符合格式的回答」 |
| Function Calling | 有教 | AI 工具第 8 課 |

### CI / CD（只點到，無子節點）

| 節點 | 判定 | 在哪裡 |
|---|---|---|
| CI / CD | 只點到 | 網頁第 5 課 SDLC 提一次「持續整合」；面試集第 2 課藍綠／金絲雀那題。沒有任何一課教管線長什麼樣、GitHub Actions 怎麼寫（雖然這個站自己就是靠 Actions 部署的） |

### Testing（有教）

| 子節點 | 判定 | 在哪裡 |
|---|---|---|
| Unit Testing | 有教 | Spring 第 11 課 |
| Integration Testing | 只點到 | Spring 第 11 課提一次；沒講 `@SpringBootTest`、MockMvc、Testcontainers |
| Functional Testing | 完全沒有 | |

### More about Databases（有教）

| 子節點 | 判定 | 在哪裡 |
|---|---|---|
| Transactions | 有教 | 資料庫第 2 課「TCL、交易與 ACID」、Spring 第 6 課 |
| ACID | 有教 | 同上 |
| ORMs | 有教 | Spring 第 3、4、8 課 |
| Normalization | 有教 | 資料庫第 3 課 |
| Failure Modes | 只點到 | 雲端第 6 課講 RDS 的 Multi-AZ 與 Failover；沒講資料庫本身會怎麼壞（連線耗盡、鎖等待、複寫延遲、磁碟滿） |
| Profiling Performance | 完全沒有 | EXPLAIN、慢查詢日誌全站零命中 |

### Message Brokers（只點到）

| 子節點 | 判定 | 在哪裡 |
|---|---|---|
| Kafka | 只點到 | 面試集第 3 課提一次 |
| RabbitMQ | 完全沒有 | |
| （訊息佇列概念） | 只點到 | 面試集第 2 課 Saga／Outbox、第 3 課「先保證映射存好，再非同步做其他事」；沒有一課講送達保證、消費者群組、重複與順序 |

### Containerization／Container Orchestration（連結到別張 roadmap）

| 節點 | 判定 | 在哪裡 |
|---|---|---|
| LXC | 只點到 | K8s 第 20 課時間軸提到 |
| Docker（按鈕） | 有教 | K8s 第 4、14〜17、21 課 |
| Kubernetes（按鈕） | 有教 | K8s 第 5〜13、18、19 課 |

### Architectural Patterns（有教）

| 子節點 | 判定 | 在哪裡 |
|---|---|---|
| Monolith | 有教 | Spring 第 12 課「單體式系統與微服務」 |
| Microservices | 有教 | Spring 第 12 課、面試集第 2 課整段 |
| SOA | 完全沒有 | 銀行業常見詞（ESB），面試可能問「SOA 跟微服務差在哪」 |
| Serverless | 只點到 | 雲端第 2 課用 Lambda 講權限、第 7 課「從 VM 到函式」一段；沒講冷啟動、適用場景、取捨 |
| Service Mesh | 只點到 | K8s 第 6 課 sidecar 兩次 |
| Twelve Factor Apps | 完全沒有 | |

### Search Engines（完全沒有）

| 子節點 | 判定 |
|---|---|
| Elasticsearch、Solr | 完全沒有（雲端第 11 課的 Kendra 是另一回事）。次要 |

### Real-Time Data（完全沒有）

| 子節點 | 判定 |
|---|---|
| Server Sent Events、WebSockets、Long / Short Polling | 完全沒有。Angular 第 5 課只講 Ajax |

### Scaling Databases（只點到）

| 子節點 | 判定 | 在哪裡 |
|---|---|---|
| Database Indexes | **完全沒有** | 全站唯一命中「索引」的地方是 Java 課講陣列索引、AI 工具課講程式碼索引——資料庫索引一個字都沒有。這是最大的單一缺口 |
| Data Replication | 有教 | 雲端第 6 課 Primary／Standby／Read Replica；資料庫第 4 課「切開是為了容量，複製是為了韌性」 |
| Sharding Strategies | 只點到 | 資料庫第 4 課一段講為什麼分片；沒講按範圍、按雜湊、一致性雜湊、跨分片查詢 |
| CAP Theorem | 完全沒有 | |

### NoSQL Databases（只點到）

| 子節點 | 判定 | 在哪裡 |
|---|---|---|
| Redis | 有教 | 見 Caching |
| MongoDB | 只點到 | 資料庫第 4 課「文件式資料庫的嵌入與參照」點名三次 |
| Firebase、DynamoDB、CouchDB、RethinkDB、Neo4j、ClickHouse、Influx DB、AWS Neptune、Cassandra、TimescaleDB、DGraph、ScyllaDB | 完全沒有 | 12 個都是特定產品，次要。資料庫第 4 課已把「鍵值、文件、欄族、圖」四類講過 |

### Building For Scale（只點到）

| 子節點 | 判定 | 在哪裡 |
|---|---|---|
| Observability | 只點到 | 面試集第 2 課「怎麼做端到端的監控」一題：三種訊號、trace ID、Micrometer Tracing。沒有教材課 |
| Instrumentation | 完全沒有 | |
| Monitoring | 只點到 | 同上；AI 工具第 7 課講 Dify 的日誌 |
| Telemetry | 完全沒有 | OpenTelemetry、Prometheus、Grafana 全站零命中 |
| Graceful Degradation | 只點到 | Spring 第 12 課「微服務不是免費的效能按鈕」提降級 |
| Throttling | 有教 | 面試集第 3 課「限流」一段（令牌桶）；第 2 課 Gateway 限流 |
| Backpressure | 完全沒有 | |
| Loadshifting | 完全沒有 | |
| Circuit Breaker | 只點到 | 面試集第 2 課熔斷五次、Resilience4j；沒講三個狀態怎麼切換、門檻怎麼設 |

## 連到別張 roadmap 的按鈕（不計入 155）

| 按鈕 | 對應 | 站上狀況 |
|---|---|---|
| Docker | roadmap.sh/docker | 有教（K8s 模組實作篇） |
| Kubernetes | roadmap.sh/kubernetes | 有教，但缺部署策略與探針的專課 |
| System Design | roadmap.sh/system-design | 只有面試集第 3 課一題 |
| Design & Architecture | roadmap.sh/software-design-architecture | Java 第 11 課設計模式；SOLID 零命中 |
| DevOps | roadmap.sh/devops | CI/CD、監控兩塊都只點到 |
| API Security Best Practices | roadmap.sh/best-practices/api-security | 分散在 Spring 第 9、10 課 |

## roadmap 沒列、但後端面試必考且站上也缺的

roadmap 是「後端」的，所以沒列 Java 專屬與作業系統的東西。這幾個在 `plan.md` 一樣算核心缺口：

- JVM 記憶體區域、垃圾回收器、OOM 排查、類別載入、JIT——Java 第 1 課只有「從 .java 到 .class」與一句垃圾回收。
- 執行緒池參數、`ExecutorService`、`CompletableFuture`、`ConcurrentHashMap` 原理、Java 記憶體模型的 happens-before——Java 第 10 課講到 CAS 與死結就停了，執行緒池只提兩次。
- 作業系統：行程與執行緒的差別（Java 第 10 課有一段比喻）、上下文切換、虛擬記憶體、I/O 模型（阻塞、非阻塞、多路複用）——沒有課。
- `HashMap` 內部結構、擴容、Java 8 的紅黑樹化——Java 第 9 課講怎麼選集合，沒講原理。
- 交易隔離層級、髒讀／不可重複讀／幻讀、MVCC、悲觀鎖與樂觀鎖——Spring 第 6 課「隔離」兩次、資料庫第 2 課兩次，都沒展開。
- Spring Bean 生命週期細節、循環相依、交易傳播行為、Spring Boot 自動組態原理——Spring 第 5、6 課各有一段起手，`Propagation`、`@Conditional`、`BeanPostProcessor` 零命中。
- SOLID 原則——零命中。
