---
name: english-review
description: 英文語音課後整理。口令「下課」；開始口令「上課」。僅處理 content/english/。
---

# 英文語音學習流程

「上課」：讀取可取得的歷史學習紀錄及英文課綱，安排一個口說情境；逐輪給簡短修正，讓學習者重說一次。

「下課」：以當前可取得的對話為依據，整理實際錯誤、修正理由、自然替代說法、新單字與三個複習任務。區分辨識疑點、文法錯誤與風格建議；沒有證據不捏造錯誤或發音評分。

## 教材維護

1. 讀取最新 main 的 content/english/module.json 及相關教材，避免重複；參考既有 add-note 規範與可靠文法來源。
2. 個人逐字稿與學習進度只回覆於私人聊天，禁止提交到公開 repo；公開教材僅用去識別化的自編例句。
3. 只改 content/english/，不動其他模組、共用程式或部署設定。由 main 建獨立分支，補強相關課或加入口說練習；每課測驗 6–10 題，opts[0] 正確。
4. 執行 python3 -m unittest discover -s builder/tests -v、python3 builder/build.py 及 dist/*.js 的 node --check；無法執行須明示。檢查 diff 全部在英文目錄。
5. 提供 PR 和獨立預覽（如可用）；不得切換正式 Pages 部署分支。只有使用者明確確認 OK 後才能合併；未授權或無寫入工具時只提供草稿。

本檔是工作規則，不是原生 ChatGPT Voice Hook。ChatGPT Project 必須另外設定口令指令；語音工具不可用時，離開語音後輸入「下課」。
