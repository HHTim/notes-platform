# 問 AI 的 Firebase 設定手冊

給 Tim 照著按。全部在 Firebase 主控台（console.firebase.google.com）的專案 `notes-platform-82407` 裡做，用建專案的那個 Google 帳號登入。主控台的按鈕名稱偶爾會改，對不上時找意思最接近的那個。

做完第 1〜4 步，把兩個值貼給 Claude：`appId`（第 2 步）和網站金鑰（第 3 步）。兩個都是公開的值，貼在對話裡沒關係。

## 1. 開啟 AI Logic

1. 左側選單找「AI 服務」底下的「AI Logic」。
2. 按「開始使用」。
3. 選 **Gemini Developer API**，照畫面按完。
   - **不要選 Vertex AI**，那個要綁信用卡。
   - 過程中如果出現「升級方案」或「綁定帳單」，先停下來，不要按，回報給 Claude。

## 2. 取得網頁 app 的 appId

1. 左上角齒輪 →「專案設定」→「一般」分頁，往下捲到「你的應用程式」。
2. 已經有網頁 app（圖示是 `</>`）：點它，複製 `appId`。
3. 沒有的話：按「新增應用程式」→ 選 `</>`（網頁）→ 名稱填 `notes-platform` → **不要**勾 Firebase Hosting → 註冊。畫面上的設定碼裡有 `appId`，複製下來。
4. `appId` 長得像 `1:123456789012:web:abcdef123456`。

## 3. 開啟 App Check（確認呼叫是從我們網站發出的）

1. 左側選單「App Check」→「應用程式」分頁。
2. 點第 2 步那個網頁 app →「reCAPTCHA Enterprise」。
3. 照畫面建立網站金鑰：
   - 網域填兩個：`hhtim.github.io`、`localhost`。
   - 免費額度是每月 1 萬次驗證，不用綁卡。
4. 儲存。把**網站金鑰**（site key，一長串英數字）複製下來。

## 4. 對 AI Logic 開啟強制驗證

1. 「App Check」→「API」分頁。
2. 找「Firebase AI Logic」→ 按「強制執行」。
3. 不開的話，2026-11-02 起 Firebase 也會自動強制。

## 5. 本機測試才需要：登記除錯碼

只有在自己電腦用 `localhost` 開網站測試時需要，平常用手機開網站不用做。

1. 在 `localhost` 開網站，登入，選一段字按「問 AI」送出一題。
2. 瀏覽器開發者工具（Mac 按 ⌥⌘I）→「Console」，會看到一行 `App Check debug token: xxxx-xxxx…`，複製那串。
3. 主控台「App Check」→「應用程式」→ 網頁 app 右邊的「⋮」→「管理除錯權杖」→ 新增，貼上。

## 6. 看每天用了多少

1. 打開 aistudio.google.com，用同一個 Google 帳號登入。
2. 左側選單找用量或「Rate limit」頁面，選專案 `notes-platform-82407`。
3. 這裡看得到每分鐘、每天的上限，還有已經用了多少。

## 7. 切回沒有 AI 的網站

1. GitHub 的 repo 頁面 → Settings → Secrets and variables → Actions →「Variables」分頁。
2. 把 `DEPLOY_BRANCH` 改成 `main`。
3. 到 Actions 分頁 → 左側「deploy」→ 右邊「Run workflow」→ 分支選 `main` → 執行。
4. 要再切回 AI 版：值改回 `ask-ai`，一樣手動執行一次，分支選 `ask-ai`。
