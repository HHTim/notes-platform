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
  var course = window.NotesCourse;   // course.js 開的掛勾
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
    setHint('進度只存在這台裝置 · <a href="#" id="syncLogin">登入後跨裝置同步</a>');
    var a = document.getElementById('syncLogin');
    if (a) a.addEventListener('click', function (e) {
      e.preventDefault();
      auth.signInWithPopup(new firebase.auth.GoogleAuthProvider())['catch'](function () {});
    });
  }
  function showUnauthorized() {
    synced = false;
    setHint('此帳號未獲授權，進度僅存於本機（<a href="#" id="syncOut">登出</a>）');
    bindLogout();
  }
  function showSynced(user) {
    synced = true;
    setHint('已同步（' + esc(user.displayName || user.email) + '）（<a href="#" id="syncOut">登出</a>）');
    bindLogout();
  }

  function pushCloud(data) {
    if (!synced || !uid) return;
    var patch = {};
    patch[course.module] = data;
    db.collection('progress').doc(uid).set(patch, { merge: true })['catch'](function () {});
  }

  auth.onAuthStateChanged(function (user) {
    if (!user) { showLoggedOut(); return; }
    /* 白名單＝Firestore 裡一份 email 清單；文件存在才算在名單上 */
    db.collection('whitelist').doc(user.email).get().then(function (snap) {
      if (!snap.exists) { showUnauthorized(); return; }
      uid = user.uid;
      db.collection('progress').doc(uid).get().then(function (p) {
        var cloud = (p.exists && p.data()[course.module]) || {};
        var merged = NotesSync.merge(course.loadDone(), cloud);
        course.saveDone(merged);   // 寫回本機（此刻 synced 還是 false，事件不會重複推雲端）
        course.refreshTicks();
        showSynced(user);          // 從這裡開始，之後的每次作答才會推雲端
        pushCloud(merged);         // 合併結果推上雲端一次
      })['catch'](function () {
        /* 在名單上，但進度暫時讀不到（例如斷線）：不是授權問題。
           顯示「沒登入」那行——「進度只存在這台裝置」此刻是事實，
           點登入連結會重跑登入流程，等於重試一次。 */
        showLoggedOut();
      });
    })['catch'](function (err) {
      /* 讀白名單失敗：規則拒絕（permission-denied）才是授權問題；
         其他失敗（例如斷線）照「沒登入」那行顯示，內容才是真的。 */
      if (err && err.code === 'permission-denied') { showUnauthorized(); }
      else { showLoggedOut(); }
    });
  });

  /* 之後每次對答案，course.js 存檔時會發這個事件 */
  document.addEventListener('notes:progress-saved', function (e) {
    if (e.detail && e.detail.module === course.module) pushCloud(e.detail.data);
  });
})();
