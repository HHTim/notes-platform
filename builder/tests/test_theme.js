// 亮色／暗色的選擇（2026-10-13 Tim 要的開關）：按過就照按的，沒按過就跟系統
var assert = require('assert');
var T = require('../templates/theme.js');

assert.strictEqual(T.pick(null, false), 'light');
assert.strictEqual(T.pick(null, true), 'dark');
assert.strictEqual(T.pick('dark', false), 'dark');
assert.strictEqual(T.pick('light', true), 'light');
assert.strictEqual(T.pick('亂寫', true), 'dark');      // 存的值壞掉就當沒按過
assert.strictEqual(T.next('light'), 'dark');
assert.strictEqual(T.next('dark'), 'light');

console.log('亮暗選擇測試全部通過');
