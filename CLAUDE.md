# CLAUDE.md

## 這個專案是什麼

Tim（HHTim）的**個人筆記平台**：一個靜態網站，多個學習模組（K8s、Redis，之後有 Java、GCP、AWS、多益、面試集…），每個模組是一個課程站（側邊欄＋每課測驗＋進度）。

⚠️ **這是個人 side project，與公司的 kpi-platform 無關。** 不引用公司 repo 的任何東西，也不把這裡的東西放進公司文件。

## 單一權威文件

**先讀 [`docs/superpowers/specs/2026-09-04-notes-platform-design.md`](./docs/superpowers/specs/2026-09-04-notes-platform-design.md)**——完整設計規格，所有已拍板的決策都在裡面（repo 佈局、內容格式、建置部署、進度同步、`/add-note` 七步流程、分期驗收）。本檔不複述，與本檔有出入時以規格為準。

## 現況（2026-09-07）

- **第一期已實作完成**（計畫與過程：`docs/superpowers/plans/2026-09-07-phase1-rescue-and-launch.md`）：`content/` 有 k8s（13 課）與 redis（1 課）兩個模組、每課測驗 5〜8 題、`builder/` 建置工具與測試（含新舊頁面一致性比對）、`.github/workflows/deploy.yml`。
- **上線差最後一步**：GitHub Pages 尚未開通，需 Tim 到 repo Settings → Pages → Source 選「GitHub Actions」，再 re-run 失敗的 Actions；之後用手機開網址驗收。
- 第二期（進度同步）、第三期（`/add-note`）未動工。
- `rescue/` 是舊對話搶救出來的原始檔，是遷移的**輸入**，遷移驗收後可刪：
  - `vm-container-k8s.html` — K8s 教材長頁版（21 個 section，內容來源）
  - `build_spa.py` — 現行建置腳本（13 課切法、39 題測驗、亮暖色版型都在裡面），改造成 `builder/` 的起點
  - `k8s-course.html` — 現行成品（遷移後的比對基準：新工具組出來要跟它一致）
  - `distributed-lock-redis.artifact.html` — Redis 鎖頁面，外層包著 artifact 發佈系統的程式碼，取用時剝殼（`<title>` 之後才是本體）

## 工程慣例

- **沒有框架**：網站是 `builder/build.py`（Python 3）產出的靜態 HTML，維護點只有 `builder/` 與 `content/`。
- **內容與外觀分開**：`content/` 只放不含樣式的內容檔；版型、配色、測驗互動集中在 `builder/templates/`。
- 色系定稿：亮暖色（奶油底 #F7F0E3、白卡片、古銅 #B5730F、灰藍 #5E7A9B），**刻意不做深色模式**。
- 建置=整站重建，`dist/` 不進 git；push 到 `main` 即發佈（GitHub Actions → GitHub Pages）。
- 網站網址：https://hhtim.github.io/notes-platform/

## Git 與帳號

- 遠端走 SSH 別名：`git@github-hhtim:HHTim/notes-platform.git`（`~/.ssh/config` 的 `github-hhtim`，用 `~/.ssh/id_ed25519_hhtim` 這把鑰匙）。**不要**把遠端改成一般的 `github.com` 網址，會撞到這台電腦的公司帳號認證。
- commit 身分：repo 內已設 `HHTim <clown0715@gmail.com>`，不要用全域（公司）身分。
- 個人專案、單人開發：直接在 `main` 上做即可，不強制開分支。

## 寫給 Tim 看的東西

輸出給 Tim 的文字照他的全域規則（`~/.claude/tim-style/RULES.md`）：不發明編號代號、不用中國講法、不造字、比喻第一次出現用括號附正式名詞。網站內容本身也適用同一套。
