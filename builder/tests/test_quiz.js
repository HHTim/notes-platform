// 錯題區的純邏輯（改版規格第 5 節）：指紋、進出規則、清單順序
var assert = require('assert');
var Q = require('../templates/course.js');

// 指紋：固定 6 碼、同文同碼、改一個字就不同
assert.strictEqual(Q.fingerprint('She spoke ___ about it.').length, 6);
assert.strictEqual(Q.fingerprint('abc'), Q.fingerprint('abc'));
assert.notStrictEqual(Q.fingerprint('abc'), Q.fingerprint('abd'));
assert.strictEqual(Q.wrongKey('l1', 2, 'abc'), 'l1|2|' + Q.fingerprint('abc'));

var k = Q.wrongKey('l1', 0, 'q0');
var bank;

// 隨堂測驗：答錯進去（連對 0）、答對不動
bank = Q.afterQuiz({}, [{slug:'l1',qi:0,q:'q0',right:false}, {slug:'l1',qi:1,q:'q1',right:true}], 100);
assert.deepStrictEqual(Object.keys(bank), [k]);
assert.deepStrictEqual(bank[k], {streak:0,removed:0,at:100});

// 已在裡面、連對 1，再答錯 → 歸零
bank = Q.afterQuiz({[k]:{streak:1,removed:0,at:50}}, [{slug:'l1',qi:0,q:'q0',right:false}], 100);
assert.deepStrictEqual(bank[k], {streak:0,removed:0,at:100});

// 移除過的題再答錯 → 復活
bank = Q.afterQuiz({[k]:{streak:2,removed:80,at:80}}, [{slug:'l1',qi:0,q:'q0',right:false}], 100);
assert.deepStrictEqual(bank[k], {streak:0,removed:0,at:100});

// 隨堂測驗裡答對不算（規格 5.1：只有錯題區練習才算連對）
bank = Q.afterQuiz({[k]:{streak:0,removed:0,at:50}}, [{slug:'l1',qi:0,q:'q0',right:true}], 100);
assert.deepStrictEqual(bank[k], {streak:0,removed:0,at:50});

// 練習：對一次連對 1；再對一次 → 連對 2 並記移除時間；錯一次歸零
bank = Q.afterPractice({[k]:{streak:0,removed:0,at:50}}, [{slug:'l1',qi:0,q:'q0',right:true}], 101);
assert.deepStrictEqual(bank[k], {streak:1,removed:0,at:101});
bank = Q.afterPractice(bank, [{slug:'l1',qi:0,q:'q0',right:true}], 102);
assert.deepStrictEqual(bank[k], {streak:2,removed:102,at:102});
bank = Q.afterPractice({[k]:{streak:1,removed:0,at:50}}, [{slug:'l1',qi:0,q:'q0',right:false}], 103);
assert.deepStrictEqual(bank[k], {streak:0,removed:0,at:103});

// 手動移除：保留連對數，記移除時間
bank = Q.remove({[k]:{streak:1,removed:0,at:50}}, k, 104);
assert.deepStrictEqual(bank[k], {streak:1,removed:104,at:104});

// 原物件不被改動
var orig = {}; orig[k] = {streak:0,removed:0,at:1};
Q.remove(orig, k, 9);
Q.afterPractice(orig, [{slug:'l1',qi:0,q:'q0',right:true}], 9);
assert.deepStrictEqual(orig[k], {streak:0,removed:0,at:1});

// active：依課序再依題序；已移除、連對兩次、指紋對不上（題目改過）的都不列；空物件也能用
var quiz = {l1:[{q:'q0'},{q:'q1'}], l2:[{q:'q2'}]};
var k1 = Q.wrongKey('l1', 1, 'q1'), k2 = Q.wrongKey('l2', 0, 'q2');
bank = {};
bank[k2] = {streak:0,removed:0,at:1};
bank[k1] = {streak:1,removed:0,at:1};
bank[k] = {streak:2,removed:5,at:5};
bank['l1|0|zzzzzz'] = {streak:0,removed:0,at:1};
var act = Q.active(bank, quiz, ['l1', 'l2']);
assert.deepStrictEqual(act.map(function (x) { return x.key; }), [k1, k2]);
assert.deepStrictEqual(act[0], {key:k1, slug:'l1', qi:1, q:quiz.l1[1], streak:1});
assert.deepStrictEqual(Q.active({}, quiz, ['l1', 'l2']), []);
assert.deepStrictEqual(Q.active(undefined, quiz, ['l1']), []);

console.log('錯題區純邏輯測試全部通過');
