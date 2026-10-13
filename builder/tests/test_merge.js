// 合併規則（規格第 7 節）：勾過就算勾過、成績取較好那次、絕不以單邊蓋掉另一邊
var assert = require('assert');
var NotesSync = require('../templates/sync.js');

// 聯集：兩邊各有對方沒有的課
assert.deepStrictEqual(
  NotesSync.merge({a:{best:2,total:5,done:false}}, {b:{best:5,total:5,done:true}}),
  {a:{best:2,total:5,done:false}, b:{best:5,total:5,done:true}});

// 同一課：done 勾過就算勾過（本機 true 雲端 false）、best 取高（雲端高）
assert.deepStrictEqual(
  NotesSync.merge({a:{best:3,total:5,done:true}}, {a:{best:5,total:5,done:false}}),
  {a:{best:5,total:5,done:true}});

// 反向：雲端勾過、本機成績高
assert.deepStrictEqual(
  NotesSync.merge({a:{best:4,total:5,done:false}}, {a:{best:1,total:5,done:true}}),
  {a:{best:4,total:5,done:true}});

// total 取大（補題後兩邊題數不同）
assert.deepStrictEqual(
  NotesSync.merge({a:{best:3,total:3,done:true}}, {a:{best:4,total:5,done:false}}),
  {a:{best:4,total:5,done:true}});

// 空邊與缺欄位：任一邊空、或紀錄缺 best/total/done，都要能合
assert.deepStrictEqual(NotesSync.merge(null, {a:{best:1,total:5,done:false}}),
  {a:{best:1,total:5,done:false}});
assert.deepStrictEqual(NotesSync.merge({}, {}), {});
assert.deepStrictEqual(NotesSync.merge({a:{done:true}}, {a:{best:2}}),
  {a:{best:2,total:0,done:true}});

// ── 改版規格第 5.5 節：_last 時間新的贏、_wrong 同鍵時間新的整筆贏 ──

// _last：時間新的贏；只有一邊有就用那邊
assert.deepStrictEqual(
  NotesSync.merge({_last:{slug:'a',at:10}}, {_last:{slug:'b',at:20}})._last, {slug:'b',at:20});
assert.deepStrictEqual(NotesSync.merge({_last:{slug:'a',at:30}}, {})._last, {slug:'a',at:30});

// 保留鍵不會被當成課的紀錄
assert.deepStrictEqual(
  Object.keys(NotesSync.merge({_last:{slug:'a',at:1}, a:{best:1,total:5,done:false}}, {})).sort(),
  ['_last', 'a']);

// _wrong：兩邊各有不同的題，取聯集
var m = NotesSync.merge({_wrong:{k1:{streak:0,removed:0,at:5}}}, {_wrong:{k2:{streak:1,removed:0,at:6}}});
assert.deepStrictEqual(m._wrong, {k1:{streak:0,removed:0,at:5}, k2:{streak:1,removed:0,at:6}});

// 同一題：時間新的整筆贏（雲端那筆是手動移除、時間較新 → 移除保留）
m = NotesSync.merge({_wrong:{k1:{streak:1,removed:0,at:5}}}, {_wrong:{k1:{streak:0,removed:9,at:9}}});
assert.deepStrictEqual(m._wrong.k1, {streak:0,removed:9,at:9});

// 反向：舊裝置上「還在錯題區」的舊紀錄，不能讓已移除的題復活
m = NotesSync.merge({_wrong:{k1:{streak:0,removed:9,at:9}}}, {_wrong:{k1:{streak:0,removed:0,at:3}}});
assert.deepStrictEqual(m._wrong.k1, {streak:0,removed:9,at:9});

// 缺欄位的錯題紀錄要補成完整形狀
assert.deepStrictEqual(NotesSync.merge({_wrong:{k1:{}}}, {})._wrong.k1, {streak:0,removed:0,at:0});

// 沒有錯題、沒有最後看的課，就不多長保留鍵（舊格式進新版不變形）
assert.deepStrictEqual(NotesSync.merge({a:{best:1,total:5,done:false}}, {}), {a:{best:1,total:5,done:false}});

console.log('merge 規則測試全部通過');
