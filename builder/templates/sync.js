/* 進度跨裝置同步：Google 登入＋Firestore。
   只有 builder 在 content/firebase.json 存在時才把本檔放進頁面；
   頁面會先宣告 FIREBASE_CONFIG，並已載入 firebase compat SDK（app/auth/firestore）。 */
var NotesSync = {
  /* 合併規則（規格第 7 節）：勾過就算勾過、成績取較好那次，絕不以單邊蓋掉另一邊 */
  merge: function (local, cloud) {
    var out = {};
    function add(src) {
      if (!src) return;
      Object.keys(src).forEach(function (k) {
        var b = src[k] || {};
        var a = out[k];
        if (!a) { out[k] = { best: b.best || 0, total: b.total || 0, done: !!b.done }; return; }
        a.best = Math.max(a.best || 0, b.best || 0);
        a.total = Math.max(a.total || 0, b.total || 0);
        a.done = !!(a.done || b.done);
      });
    }
    add(local); add(cloud);
    return out;
  }
};
if (typeof module !== 'undefined' && module.exports) { module.exports = NotesSync; }

/* 瀏覽器裡才有 document 與 firebase；node 跑測試時只用得到上面的 merge */
if (typeof document !== 'undefined' && typeof firebase !== 'undefined') (function () {
  firebase.initializeApp(FIREBASE_CONFIG);
  var auth = firebase.auth();
  var db = firebase.firestore();
  /* 兩種頁面共用這支檔：模組頁有 course.js 開的 NotesCourse（單一模組的進度）；
     首頁沒有課，只有 home.html 開的 NotesHome（全部模組的 id 與重算卡片的函式）。 */
  var course = window.NotesCourse || null;
  var home = window.NotesHome || null;
  function localKey(mid) { return 'notes-progress:' + mid; }
  function loadLocal(mid) {
    try { return JSON.parse(localStorage.getItem(localKey(mid))) || {}; } catch (e) { return {}; }
  }
  function saveLocal(mid, d) {
    try { localStorage.setItem(localKey(mid), JSON.stringify(d)); } catch (e) {}
  }
  var hint = document.getElementById('syncHint');
  var synced = false;                // 目前是不是「已登入＋白名單」狀態
  var uid = null;

  function setHint(html) { if (hint) hint.innerHTML = html; }
  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }
  function bindLogout() {
    var a = document.getElementById('syncOut');
    if (a) a.addEventListener('click', function (e) { e.preventDefault(); auth.signOut(); });
  }

  /* 三狀態提示（文字照規格第 7 節的表格） */
  function showLoggedOut() {
    synced = false; uid = null;
    setHint('<span class="st">進度只存在這台裝置 · </span><a href="#" id="syncLogin">登入後跨裝置同步</a>');
    var a = document.getElementById('syncLogin');
    if (a) a.addEventListener('click', function (e) {
      e.preventDefault();
      auth.signInWithPopup(new firebase.auth.GoogleAuthProvider())['catch'](function () {});
    });
  }
  function showUnauthorized() {
    synced = false;
    setHint('<span class="st">此帳號未獲授權，進度僅存於本機</span><span class="sh">未獲授權</span> · <a href="#" id="syncOut">登出</a>');
    bindLogout();
  }
  function showSynced(user) {
    synced = true;
    setHint('已同步<span class="st">（' + esc(user.displayName || user.email) + '）</span> · <a href="#" id="syncOut">登出</a>');
    bindLogout();
  }
  /* 已登入、但白名單或進度暫時讀不到（例如斷線）：不是授權問題，也不是沒登入。
     不能借用「登入後跨裝置同步」那個連結當重試——同一個帳號再登入 uid 不變，
     Firebase 的 onAuthStateChanged 不會再觸發，點了沒有任何反應。
     所以這裡自己給一個「重試」連結，直接重跑 loadAndMerge。 */
  function showRetry(user) {
    synced = false;
    setHint('<span class="st">暫時連不上雲端</span><span class="sh">連不上雲端</span> · <a href="#" id="syncRetry">重試</a>');
    var a = document.getElementById('syncRetry');
    if (a) a.addEventListener('click', function (e) { e.preventDefault(); loadAndMerge(user); });
  }

  /* patch 的形狀是 { 模組id: 該模組的進度 }，可以一次帶多個模組；merge:true 不會蓋掉其他模組 */
  function pushCloud(patch) {
    if (!synced || !uid) return;
    db.collection('progress').doc(uid).set(patch, { merge: true })['catch'](function () {});
  }

  /* 把雲端文件與本機合併、寫回本機；回傳要推上雲端的 patch。
     模組頁只管自己這個模組；首頁把每個模組都合併一次，卡片上的完成數才會對。 */
  function mergeAll(cloudDoc) {
    var patch = {};
    if (course) {
      var merged = NotesSync.merge(course.loadDone(), cloudDoc[course.module] || {});
      course.saveDone(merged);   // 寫回本機（此刻 synced 還是 false，事件不會重複推雲端）
      course.refreshTicks();
      patch[course.module] = merged;
    } else if (home) {
      home.modules.forEach(function (mid) {
        var m = NotesSync.merge(loadLocal(mid), cloudDoc[mid] || {});
        saveLocal(mid, m);
        patch[mid] = m;
      });
      home.refresh();
    }
    return patch;
  }

  /* 登入後的整套流程：讀白名單 → 讀雲端進度 → 與本機合併 → 寫回本機並推上雲端。
     登入時跑一次；讀取失敗後點「重試」再跑一次。 */
  function loadAndMerge(user) {
    /* 白名單＝Firestore 裡一份 email 清單；文件存在才算在名單上 */
    db.collection('whitelist').doc(user.email).get().then(function (snap) {
      if (!auth.currentUser || auth.currentUser.uid !== user.uid) return;   // 重試中途登出或換帳號，遲到的回應不算
      if (!snap.exists) { showUnauthorized(); return; }
      db.collection('progress').doc(user.uid).get().then(function (p) {
        if (!auth.currentUser || auth.currentUser.uid !== user.uid) return;   // 重試中途登出或換帳號，遲到的回應不算
        uid = user.uid;
        var patch = mergeAll((p.exists && p.data()) || {});
        showSynced(user);          // 從這裡開始，之後的每次作答才會推雲端
        pushCloud(patch);          // 合併結果推上雲端一次
      })['catch'](function () {
        showRetry(user);           // 在名單上，但進度暫時讀不到
      });
    })['catch'](function (err) {
      /* 讀白名單失敗：規則拒絕（permission-denied）才是授權問題；其他失敗（例如斷線）給重試 */
      if (err && err.code === 'permission-denied') { showUnauthorized(); }
      else { showRetry(user); }
    });
  }

  auth.onAuthStateChanged(function (user) {
    if (!user) { showLoggedOut(); return; }
    loadAndMerge(user);
  });

  /* 之後每次對答案，course.js 存檔時會發這個事件 */
  document.addEventListener('notes:progress-saved', function (e) {
    if (!course || !e.detail || e.detail.module !== course.module) return;
    var patch = {};
    patch[course.module] = e.detail.data;
    pushCloud(patch);
  });
})();
