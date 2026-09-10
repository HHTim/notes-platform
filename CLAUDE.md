# CLAUDE.md

## 這個專案是什麼

Tim（HHTim）的**個人筆記平台**：一個靜態網站，多個學習模組（K8s、Redis，之後有 Java、GCP、AWS、多益、面試集…），每個模組是一個課程站（側邊欄＋每課測驗＋進度）。

⚠️ **這是個人 side project，與公司的 kpi-platform 無關。** 不引用公司 repo 的任何東西，也不把這裡的東西放進公司文件。

## 單一權威文件

**先讀 [`docs/superpowers/specs/2026-09-04-notes-platform-design.md`](./docs/superpowers/specs/2026-09-04-notes-platform-design.md)**——完整設計規格，所有已拍板的決策都在裡面（repo 佈局、內容格式、建置部署、進度同步、`/add-note` 七步流程、分期驗收）。本檔不複述，與本檔有出入時以規格為準。

## 現況（2026-09-07）

- **第一期（救檔＋上線）與第二期（進度跨裝置同步）都已完成並驗收**（第一期 2026-09-08、第二期 2026-09-10 Tim 實測通過；計畫與過程在 `docs/superpowers/plans/`）。
- 第二期要點：Google 登入＋Firestore（專案 `notes-platform-82407`，Tim 個人帳號、免費方案）；設定在 `content/firebase.json`（三個值都是公開識別碼）；同步邏輯在 `builder/templates/sync.js`；資料庫規則正本在 `firebase/firestore.rules`（改規則要去 Firebase 主控台貼上發佈）；白名單＝Firestore 的 `whitelist` 集合，文件 ID 是 email，Tim 在主控台增刪；設定手冊在 `docs/firebase-setup.md`。
- 已知且接受的邊角：登出不清本機進度（規格：沒登入進度存本機）；兩裝置同時開著交錯作答時雲端可能暫時回退、較新裝置下次登入自癒。
- `rescue/`（舊對話救回的原始檔）已隨第一期驗收刪除；一致性測試自動跳過屬正常。
- 第三期（`/add-note`）未動工。前置：手機使用時在 claude.ai 連結 GitHub（規格第 9 節的一次性設定）。

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
