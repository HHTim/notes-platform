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

console.log('merge 規則測試全部通過');
