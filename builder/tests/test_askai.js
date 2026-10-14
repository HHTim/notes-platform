// 選字問 AI 的純函式（規格 docs/superpowers/specs/2026-10-14-ask-ai-design.md）
var assert = require('assert');
var A = require('../templates/askai.js');

// 濾讀音：整段、切到讀音中間、只選到讀音
assert.strictEqual(A.stripReadings('<ruby>私<rt>わたし</rt></ruby>が<ruby>行<rt>い</rt></ruby>きます'), '私が行きます');
assert.strictEqual(A.stripReadings('<ruby>私<rp>(</rp><rt class="x">わたし</rt><rp>)</rp></ruby>'), '私');
assert.strictEqual(A.stripReadings('<rt>わたし</rt></ruby>が'), 'が');
assert.strictEqual(A.stripReadings('<ruby><rt>わたし</rt></ruby>'), '');
assert.strictEqual(A.stripReadings('たし</rt></ruby>が'), 'が');          // 選取從讀音中間開始
assert.strictEqual(A.stripReadings('私<rt>わた'), '私');                 // 選取停在讀音中間
assert.strictEqual(A.stripReadings('A&lt;B &amp; C<br>下一行'), 'A<B & C\n下一行');
assert.strictEqual(A.stripReadings('  多個   空白\t '), '多個 空白');

// 截斷
assert.deepStrictEqual(A.clip('一二三', 5), { text: '一二三', cut: false });
assert.deepStrictEqual(A.clip('一二三四五六', 5), { text: '一二三四五…', cut: true });

// 系統指示
assert.ok(A.systemText('ja').indexOf('N5') >= 0);
assert.ok(A.systemText('en').indexOf('多益') >= 0);
assert.ok(A.systemText('ja').indexOf('羅馬拼音') >= 0);
assert.strictEqual(A.systemText('zh').indexOf('N5'), -1);

// 組問題
var p = A.buildPrompt({ module: '日文', lesson: '助詞（一）', section: 'が', context: '私が行きます。', selected: '私が', question: '為什麼用が？' });
assert.ok(p.indexOf('模組：日文') >= 0 && p.indexOf('課：助詞（一）') >= 0 && p.indexOf('小節：が') >= 0);
assert.ok(p.indexOf('我選的字：「私が」') >= 0 && p.indexOf('問題：為什麼用が？') >= 0);
assert.strictEqual(A.buildPrompt({ selected: 'x', question: 'q' }).indexOf('小節：'), -1);   // 沒有就不寫那行

// 回答顯示：先跳脫
assert.strictEqual(A.renderAnswer('<img src=x onerror=alert(1)>'), '<p>&lt;img src=x onerror=alert(1)&gt;</p>');
assert.strictEqual(A.renderAnswer('<script>x</script>').indexOf('<script>'), -1);
assert.strictEqual(A.renderAnswer('[點我](javascript:alert(1))'), '<p>[點我](javascript:alert(1))</p>');
assert.strictEqual(A.renderAnswer('**粗體**和`code`'), '<p><b>粗體</b>和<code>code</code></p>');
assert.strictEqual(A.renderAnswer('沒配對的 ** 星號'), '<p>沒配對的 ** 星號</p>');
assert.strictEqual(A.renderAnswer('結論\n- 一\n- 二'), '<p>結論</p><ul><li>一</li><li>二</li></ul>');
assert.strictEqual(A.renderAnswer('1. 甲\n2. 乙'), '<ol><li>甲</li><li>乙</li></ol>');
assert.strictEqual(A.renderAnswer('第一段\n\n第二段'), '<p>第一段</p><p>第二段</p>');
// 日文包 lang="ja"：假名、以及後面帶（讀音）的漢字
assert.strictEqual(A.renderAnswer('這裡的が表示主語'), '<p>這裡的<span lang="ja">が</span>表示主語</p>');
assert.strictEqual(A.renderAnswer('私（わたし）'), '<p><span lang="ja">私（わたし）</span></p>');

// 錯誤分類
function E(code, status, details, message) { return { code: code, customErrorData: status ? { status: status, errorDetails: details } : undefined, message: message || '' }; }
assert.strictEqual(A.classifyError(E('fetch-error', 429, [{ violations: [{ quotaId: 'GenerateRequestsPerDayPerProjectPerModel-FreeTier' }] }])), 'quota-day');
assert.strictEqual(A.classifyError(E('fetch-error', 429, [{ violations: [{ quotaId: 'GenerateRequestsPerMinutePerProjectPerModel-FreeTier' }] }])), 'quota-minute');
assert.strictEqual(A.classifyError(E('fetch-error', 403, [], 'App Check token is invalid')), 'appcheck');
assert.strictEqual(A.classifyError(E('fetch-error', 401, [])), 'appcheck');
assert.strictEqual(A.classifyError(E('response-error')), 'blocked');
assert.strictEqual(A.classifyError(E('error', 0, null, 'Failed to fetch')), 'network');
assert.strictEqual(A.classifyError({ name: 'TypeError', message: 'Failed to fetch' }), 'network');
assert.strictEqual(A.classifyError(E('fetch-error', 500, [])), 'other');
assert.strictEqual(A.classifyError(null), 'other');
['quota-day', 'quota-minute', 'appcheck', 'network', 'blocked', 'other'].forEach(function (k) { assert.ok(A.MESSAGES[k], k); });
assert.strictEqual(A.MESSAGES['quota-day'], '今天的免費額度用完了，明天再試。');

console.log('問 AI 純函式測試全部通過');
