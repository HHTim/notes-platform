/* 亮色／暗色切換。放在 <head> 裡同步載入，頁面畫出來之前就決定好顏色，不會先閃一下亮色。
   規則：按過開關就照按的（存在這台裝置的 localStorage，不跟雲端同步）；沒按過就跟系統設定。 */
var NotesTheme = {
  KEY: 'notes-theme',
  pick: function (saved, systemDark) {
    if (saved === 'dark' || saved === 'light') return saved;
    return systemDark ? 'dark' : 'light';
  },
  next: function (cur) { return cur === 'dark' ? 'light' : 'dark'; }
};
if (typeof module !== 'undefined' && module.exports) { module.exports = NotesTheme; }

if (typeof document !== 'undefined') (function () {
  var root = document.documentElement;
  var mq = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
  function saved() { try { return localStorage.getItem(NotesTheme.KEY); } catch (e) { return null; } }
  function apply() { root.setAttribute('data-theme', NotesTheme.pick(saved(), !!(mq && mq.matches))); }
  apply();
  /* 沒按過開關時，系統切換深淺色要跟著變 */
  if (mq && mq.addEventListener) mq.addEventListener('change', apply);
  document.addEventListener('DOMContentLoaded', function () {
    var btn = document.getElementById('themeBtn');
    if (!btn) return;
    btn.addEventListener('click', function () {
      var t = NotesTheme.next(root.getAttribute('data-theme'));
      try { localStorage.setItem(NotesTheme.KEY, t); } catch (e) {}
      root.setAttribute('data-theme', t);
    });
  });
})();
