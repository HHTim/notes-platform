# CLAUDE.md

## 這個專案是什麼

Tim（HHTim）的**個人筆記平台**：一個靜態網站，多個學習模組（清單見 `content/modules.json`，持續增加中），每個模組是一個課程站（側邊欄＋每課測驗＋進度）。

⚠️ **這是個人 side project，與公司的 kpi-platform 無關。** 不引用公司 repo 的任何東西，也不把這裡的東西放進公司文件。

## 單一權威文件

**先讀 [`docs/superpowers/specs/2026-09-04-notes-platform-design.md`](./docs/superpowers/specs/2026-09-04-notes-platform-design.md)**——完整設計規格，所有已拍板的決策都在裡面（repo 佈局、內容格式、建置部署、進度同步、`/add-note` 七步流程、分期驗收）。本檔不複述，與本檔有出入時以規格為準。

## 現況（2026-10-02）

- **第一期（救檔＋上線）與第二期（進度跨裝置同步）都已完成並驗收**（第一期 2026-09-08、第二期 2026-09-10 Tim 實測通過；計畫與過程在 `docs/superpowers/plans/`）。
- 第二期要點：Google 登入＋Firestore（專案 `notes-platform-82407`，Tim 個人帳號、免費方案）；設定在 `content/firebase.json`（三個值都是公開識別碼）；同步邏輯在 `builder/templates/sync.js`；資料庫規則正本在 `firebase/firestore.rules`（改規則要去 Firebase 主控台貼上發佈）；白名單＝Firestore 的 `whitelist` 集合，文件 ID 是 email，Tim 在主控台增刪；設定手冊在 `docs/firebase-setup.md`。
- 已知且接受的邊角：登出不清本機進度（規格：沒登入進度存本機）；兩裝置同時開著交錯作答時雲端可能暫時回退、較新裝置下次登入自癒。
- `rescue/`（舊對話救回的原始檔）已隨第一期驗收刪除；一致性測試自動跳過屬正常。
- **第三期（`/add-note`）已完成並驗收**（2026-09-18 用真 HackMD 筆記全流程跑通，新增「面試集」模組）。收筆記的流程整套在 `.claude/skills/add-note/SKILL.md`——七步、三個停問點、更正標記寫法、內容慣例都在裡面，直接用 `/add-note` 觸發。
- **三期全數完成，進入日常使用**：把 HackMD 舊筆記逐篇餵給 `/add-note`。手機要用的前置：在 claude.ai 連結 GitHub（規格第 9 節的一次性設定）。
- **2026-09-21 起的批次收錄**：Tim 把整包 HackMD 筆記下載下來一次消化，分十波進行，慣例與進度表在 `docs/superpowers/plans/2026-09-21-batch-intake.md`。一課的測驗題數在那一輪改成預設 8 題（內容密的 10 題、薄的最少 6 題）。批次收錄踩過最多次的坑是**更正標記把對的筆記標成錯的**，判準寫在 `~/.claude/projects/-Users-twinb00597734-Workspace-notes-platform/memory/fixnote-burden-of-proof.md`。
- **2026-09-24 全站審查**（架構＋十個模組內容＋跨模組一致性，計畫與結果在 `docs/superpowers/plans/2026-09-24-full-audit.md`）與 **2026-09-29 面試集擴充**（對照 roadmap.sh/backend 的缺口分析在 `2026-09-29-roadmap-coverage.md`，計畫與進度在 `2026-09-29-roadmap-expansion.md`；面試集從 3 課擴到 12 課，每課「依官方文件新寫」：零更正標記、每個主張附出處、獨立審查加範圍複審後才上線）。新寫課的慣例寫在 `.claude/skills/add-note/SKILL.md` 第 5 步。
- **2026-10-02 多益文法**：英文模組新增 18 課文法書（第 3〜20 課，從句子骨架、時態四課到倒裝與解題順序），規格在 `docs/superpowers/specs/2026-10-02-toeic-grammar-design.md`，兩批計畫與審查紀錄在 `docs/superpowers/plans/2026-10-02-toeic-grammar-batch1.md`、`…-batch2.md`。網站新增「課中練習」（課文裡的四選一，點了馬上看對錯，`builder/build.py` 的 `DrillChecker` 檢查每題正解剛好一個）。題目全部自編、不得照抄 ETS 範例題；寫課守則 11 條在第二批計畫裡。同期面試集再加 3 課（微服務、容器與部署、行為面試）共 16 課。
- **2026-10-13 改版與錯題區**：外觀換成白底配色塊、測驗回饋改圈叉加成績卡、每個模組有錯題區（連對兩次或手動移除）、首頁有「繼續上次」。規格在 `docs/superpowers/specs/2026-10-13-redesign-and-wrong-bank-design.md`，計畫在 `docs/superpowers/plans/2026-10-13-redesign-and-wrong-bank.md`。進度物件多了 `_last` 與 `_wrong` 兩個保留鍵，合併規則在 `builder/templates/sync.js`。
- **2026-10-14 日文模組**：日檢文法從 N5 排到 N1、只做文法；N5 八課、N4 十課全部上線（計畫與進度在 `docs/superpowers/plans/2026-10-14-japanese-n5-batch2.md`、`…-n4-batch1.md`、`…-n4-batch2.md`，寫課守則累積到 30 條）。規格 `docs/superpowers/specs/2026-10-14-japanese-grammar-design.md`，計畫與寫課守則（21 條）在 `docs/superpowers/plans/2026-10-14-japanese-n5-batch1.md`。`module.json` 有 `"lang": "ja"` 的模組，建置會擋「假名不在 `lang="ja"` 底下」「漢字沒包 `<ruby>` 標讀音」；讀音另外用 `builder/tools/check_readings.py`（SudachiPy，裝在 `~/.cache/notes-sudachi`）比對，審查時用、不在建置裡。
- **2026-10-14 選字問 AI（只在 `ask-ai` 分支）**：日文、英文模組選字可問 Gemini 免費版，走 Firebase AI Logic＋App Check（Fraud Defense，舊稱 reCAPTCHA Enterprise），不架後端。規格 `docs/superpowers/specs/2026-10-14-ask-ai-design.md`、計畫 `docs/superpowers/plans/2026-10-14-ask-ai.md`、Tim 的設定手冊 `docs/ask-ai-setup.md`。哪條分支上線由 repo 變數 `DEPLOY_BRANCH` 決定（2026-10-29 起是 `ask-ai`）；`main` 保持沒有 AI。

## 工程慣例

- **沒有框架**：網站是 `builder/build.py`（Python 3）產出的靜態 HTML，維護點只有 `builder/` 與 `content/`。
- **內容與外觀分開**：`content/` 只放不含樣式的內容檔；版型、配色、測驗互動集中在 `builder/templates/`。
- 色系定稿：白底配色塊（白底、深綠灰墨色 #233831、薄荷與桃橘六個淡色只當記號；色號表在 `docs/superpowers/specs/2026-10-13-redesign-and-wrong-bank-design.md` 第 2 節）。2026-10-13 起有暗色模式：頂欄右上的開關切換，沒按過就跟系統設定，選擇只存在該裝置（`builder/templates/theme.js`）；暗色變數在 `style.css` 的 `[data-theme="dark"]` 段，新增顏色變數時亮暗兩段都要加（測試會擋）。圖示全部是 `builder/templates/icons.svg` 裡自己畫的 SVG，不用 emoji。
- 建置=整站重建，`dist/` 不進 git；push 到 `main` 即發佈（GitHub Actions → GitHub Pages）。
- 網站網址：https://hhtim.github.io/notes-platform/

## Git 與帳號

- 遠端走 SSH 別名：`git@github-hhtim:HHTim/notes-platform.git`（`~/.ssh/config` 的 `github-hhtim`，用 `~/.ssh/id_ed25519_hhtim` 這把鑰匙）。**不要**把遠端改成一般的 `github.com` 網址，會撞到這台電腦的公司帳號認證。
- commit 身分：repo 內已設 `HHTim <clown0715@gmail.com>`，不要用全域（公司）身分。
- 個人專案、單人開發：直接在 `main` 上做即可，不強制開分支。

## 寫給 Tim 看的東西

輸出給 Tim 的文字照他的全域規則（`~/.claude/tim-style/RULES.md`）：不發明編號代號、不用中國講法、不造字、比喻第一次出現用括號附正式名詞。網站內容本身也適用同一套。
