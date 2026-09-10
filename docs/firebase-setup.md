# Firebase 一次性設定（第二期：進度跨裝置同步）

用**個人** Google 帳號做，全程免費方案（Spark），大約 10 分鐘。做完把第 2 步抄下的三個值交給 Claude Code（或自己填進 `content/firebase.json`）並 push，同步功能就上線。

## 1. 開專案

1. 開 https://console.firebase.google.com （用個人 Google 帳號登入）
2. 「建立專案」→ 名稱取 `notes-platform`（叫什麼都行）
3. Google Analytics 問你要不要開——**不用開**
4. 等它建好

## 2. 註冊網頁應用程式、抄設定值

1. 專案總覽頁 → 「將 Firebase 加入您的應用程式」選 **Web**（`</>` 圖示）
2. 暱稱隨意（例如 `notes`），**不要**勾 Firebase Hosting
3. 註冊後畫面會顯示一段 `firebaseConfig`，把其中三個值抄下來：
   - `apiKey`
   - `authDomain`（長得像 `notes-platform-xxxx.firebaseapp.com`）
   - `projectId`
4. 這三個值是公開識別碼，放進公開 repo 沒關係——安全靠的是第 6 步的資料庫規則，不是藏設定。

## 3. 開 Google 登入

1. 左側選單 → 建構 → **Authentication** → 「開始使用」
2. 「Sign-in method」分頁 → **Google** → 啟用 → 「專案支援電子郵件」選自己 → 儲存

## 4. 授權網域

1. Authentication → **Settings** → 「Authorized domains」
2. 確認清單裡有 `hhtim.github.io`；沒有就「Add domain」加進去
（少這步的症狀：網站上按登入，跳出視窗馬上關掉並報錯。）

## 5. 開 Firestore 資料庫

1. 左側選單 → 建構 → **Firestore Database** → 「建立資料庫」
2. 選**正式版模式**（production mode；規則等下第 6 步會換掉）
3. 位置選 `asia-east1`（台灣）→ 建立

## 6. 貼資料庫規則

1. Firestore → 「規則」分頁
2. 把編輯器裡的內容**全部**換成 repo 裡 `firebase/firestore.rules` 的內容
3. 「發佈」
（三條規則的意思：名單只有你能改；名單上的人只能讀寫自己的進度；其他一律拒絕。）

## 7. 建白名單、把自己加進去

1. Firestore → 「資料」分頁 → 「開始集合」
2. 集合 ID 填 `whitelist`
3. 文件 ID 填**你要用來登入的那個 Google 帳號的 email**（例如 `clown0715@gmail.com`）——大小寫照 Google 帳號的原樣，通常全小寫
4. 隨便加一個欄位（例如欄位 `note`、類型字串、值 `我自己`）→ 儲存
（之後要讓別的帳號同步，就在這個集合再加一份文件，文件 ID 是那個 email；移掉就刪文件。）

## 8. 把設定值接上網站

1. 把第 2 步的三個值填進 `content/firebase.json`：
   `{"apiKey": "…", "authDomain": "…", "projectId": "…"}`
2. push 到 main，等自動部署跑完
3. 手機開 https://hhtim.github.io/notes-platform/k8s/ → 側邊欄最下面出現
   「進度只存在這台裝置 · 登入後跨裝置同步」→ 點登入 → 選帳號
4. 登入後那行變成「已同步（你的名字）」，之前在別台裝置打的勾應該都在

## 出狀況時看哪裡

| 症狀 | 多半是 |
|---|---|
| 按登入，視窗跳出又立刻消失並報錯 | 第 4 步授權網域沒加 |
| 登入成功但顯示「此帳號未獲授權」 | 第 7 步白名單文件 ID 跟登入帳號的 email 不一致 |
| 顯示已同步但兩台裝置對不上 | 兩台是不是登了不同帳號；或其中一台還開著舊分頁，重新整理 |
