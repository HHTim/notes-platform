# 日文文法第一批（網站改動＋N5 第 1〜4 課）實作計畫

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 網站能正確顯示日文（日文字形、漢字上方的讀音），建置時擋下「日文沒標 lang」「漢字漏標讀音」；新開「日文」模組並上線 N5 第 1〜4 課。

**Architecture:** 建置程式 `builder/build.py` 對 `module.json` 有 `"lang": "ja"` 的模組多跑一個檢查（`JaChecker`），課文與測驗題都檢查。樣式只加不改：`[lang|="ja"]` 換日文字型、`ruby`／`rt` 排版、例句清單 `ul.jx`。讀音另外有一支審查用的程式 `builder/tools/check_readings.py`，用 SudachiPy 斷詞比對，不是建置的一部分。課文由寫課代理照本計畫的守則寫，每課走「寫課 → 獨立審查 → 修正 → 範圍複審」。

**Tech Stack:** Python 3 標準函式庫（html.parser、re）、unittest；SudachiPy＋sudachidict_core（只在審查用）；HTML `<ruby>`；Google Fonts 的 Noto Sans JP。

**Spec:** `docs/superpowers/specs/2026-10-14-japanese-grammar-design.md`

## Global Constraints

- 只做文法；不做單字表、讀解、聽解、朗讀、羅馬拼音、五十音教學。
- 照級數排：模組內分組＝級數（「N5」）。資料夾 `01-n5-noun-sentence`、`02-n5-particles`、`03-n5-adjectives`、`04-n5-masu`。
- 日文句子裡每個漢字都用 `<ruby>` 標讀音（N5、N4 一律標）。
- 日文文字放在帶 `lang="ja"` 的元素裡；中文說明裡夾的日文（例如「用 は 標主題」）也要包 `<span lang="ja">`。
- 例句情境：日常生活為主，穿插職場。例句與題目全部自編。
- 課中練習沿用 `<div class="drill">`；題型：填空四選一、排列順序（★ 的位置是哪一個）。解析開頭 `<span class="dtr">整句：…</span>`。
- 課末測驗 10 題，`opts[0]` 正確。
- 級數是「常見分級」：只在模組簡介與第 1 課開頭各說一次。
- 出處優先：國際交流基金 → 文化廳「敬語の指針」→ jlpt.jp（只用於考試形式）→ 國語辭典線上條目。
- 零 `fixnote`、零 `data-note`；不寫寫課者旁白、教科書口吻、不寫「某某說」、保留語氣。
- 同時跑的代理不超過三個；Tim 叫停就全部停。
- 新顏色變數一律不加（只用既有變數），亮暗兩種模式都要看過。

## Review Focus

1. **測驗選項裡有 `<ruby>`**：`.opt` 是 flex 版面，讀音小字可能把選項撐高或歪掉；正常應該跟一般選項一樣高度一致、字對齊。→ Task 2 的瀏覽器檢查步驟。
2. **錯題區清單**直接放題目 HTML（`course.js` 的 `.wq`），讀音要正常顯示、不跟下一行擠在一起。→ Task 7 的瀏覽器檢查。
3. **小節標題有讀音時**，側欄與課首目錄抓的是標題純文字，`rt` 的假名會黏在漢字後面（「私わたし」）；應該只顯示漢字。→ Task 1 的 `test_section_title_drops_ruby_reading`。
4. **暗色模式下讀音小字**的顏色要看得清楚（`--ink2` 在暗色是 #B5AEA4）。→ Task 2 的瀏覽器檢查。
5. **跨行的文字**：檢查錯誤時報的行號要是那個字實際所在的行，不是那段文字開頭的行，不然寫課代理找不到。→ Task 1 的 `test_line_number_points_at_the_char`。

---

### Task 1: 日文檢查（假名要有 lang、漢字要有讀音）

**Files:**
- Modify: `builder/build.py`（`DrillChecker` 後面加 `JaChecker`、`ja_errors`、`ja_quiz_errors`；`load_site` 呼叫；`section_titles` 去掉 `rt`）
- Test: `builder/tests/test_checks.py`

**Interfaces:**
- Produces: `ja_errors(html: str) -> list[str]`（每筆「第 N 行…」）；`ja_quiz_errors(questions: list[dict]) -> list[str]`（每筆「第 N 題（q／選項 M／解析）…」）；`module.json` 的 `"lang": "ja"` 開關。

- [ ] **Step 1: 寫會失敗的測試**

`fake_site` 加一個參數讓模組可以設 `lang`：

```python
def fake_site(lessons, mod_extra=None):
    ...
    (mdir / 'module.json').write_text(json.dumps(dict({
        'title': '示範模組', ...原本的欄位...}, **(mod_extra or {})), ensure_ascii=False), encoding='utf-8')
```

`test_checks.py` 檔尾加：

```python
JA_OK = ('<p lang="ja"><ruby>私<rt>わたし</rt></ruby>は<ruby>学生<rt>がくせい</rt></ruby>です。</p>\n'
         '<p>我是學生。用 <span lang="ja">は</span> 標主題。</p>\n')


class TestJapanese(unittest.TestCase):
    """日文模組：假名不在 lang="ja" 底下會用中文字形顯示；lang="ja" 底下的漢字不在 <ruby> 裡就是漏標讀音。"""

    def test_good_passes(self):
        self.assertEqual(builder.ja_errors(JA_OK), [])

    def test_kana_without_lang_fails(self):
        errs = builder.ja_errors('<p>私はです</p>')
        self.assertEqual(len(errs), 1)
        self.assertIn('第 1 行', errs[0])
        self.assertIn('lang="ja"', errs[0])

    def test_kanji_without_ruby_fails(self):
        errs = builder.ja_errors('<p lang="ja"><ruby>私<rt>わたし</rt></ruby>は学生です。</p>')
        self.assertEqual(len(errs), 1)
        self.assertIn('学', errs[0])

    def test_chinese_kanji_and_middle_dot_ok(self):
        self.assertEqual(builder.ja_errors('<p>中文說明・甲乙</p>'), [])

    def test_zh_inside_ja_resets(self):
        self.assertEqual(builder.ja_errors('<p lang="ja">です<span lang="zh-Hant">中文</span></p>'), [])

    def test_line_number_points_at_the_char(self):
        errs = builder.ja_errors('<p>\n中文\n說明です</p>')
        self.assertIn('第 3 行', errs[0])

    def test_quiz_fields_checked(self):
        errs = builder.ja_quiz_errors([{'q': '<span lang="ja">私です</span>',
                                        'opts': ['<span lang="ja">は</span>', 'が'], 'exp': '中文'}])
        self.assertEqual(len(errs), 2)
        self.assertIn('第 1 題', errs[0])
        self.assertTrue(any('選項 2' in e for e in errs))

    def test_build_stops_for_ja_module(self):
        content, out = fake_site([('01-one', 'one', LESSON_OK + '<p>です</p>')], {'lang': 'ja'})
        with self.assertRaises(SystemExit) as cm:
            builder.build(content_dir=content, out_dir=out)
        self.assertIn('demo/01-one', str(cm.exception))

    def test_other_modules_not_checked(self):
        content, out = fake_site([('01-one', 'one', LESSON_OK + '<p>です</p>')])
        builder.build(content_dir=content, out_dir=out)

    def test_section_title_drops_ruby_reading(self):
        html = '<h3 class="head"><span lang="ja"><ruby>私<rt>わたし</rt></ruby>は</span>的用法</h3>'
        _, titles = builder.section_titles(html, 'x')
        self.assertEqual(titles, ['私は的用法'])
```

- [ ] **Step 2: 跑測試確認失敗**

Run: `python3 -m unittest builder.tests.test_checks 2>&1 | tail -5`（在 repo 根目錄；不行就 `cd builder/tests && python3 -m unittest test_checks`）
Expected: FAIL／ERROR，`module 'build' has no attribute 'ja_errors'`，`test_section_title_drops_ruby_reading` 得到 `['私わたしは的用法']`。

- [ ] **Step 3: 實作**

`build.py` 的 `drill_errors` 後面加：

```python
KANA_RE = re.compile(r'[ぁ-ゖゝ-ゟァ-ヺー-ヿ]')   # 不含「・」（中文也用）
KANJI_RE = re.compile(r'[㐀-䶿一-鿿々]')                       # 含「々」


class JaChecker(HTMLParser):
    """日文模組的兩條規則：假名一定在 lang="ja" 底下（不然日文漢字會用中文字形）；
    lang="ja" 底下的漢字一定在 <ruby> 裡（不然漏標讀音）。<rt>、<rp> 裡的字不檢查。"""

    def __init__(self):
        super().__init__()
        self.errors = []     # (行號, 說明)
        self.stack = []      # 每層 (tag, 是日文, 在 ruby 裡, 在 rt 裡)

    def _top(self):
        return self.stack[-1][1:] if self.stack else (False, False, False)

    def handle_starttag(self, tag, attrs):
        if tag in VOID_TAGS:
            return
        ja, ruby, rt = self._top()
        a = dict(attrs)
        if 'lang' in a:
            ja = (a['lang'] or '').lower().startswith('ja')
        self.stack.append((tag, ja, ruby or tag == 'ruby', rt or tag in ('rt', 'rp')))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        ja, ruby, rt = self._top()
        if rt:
            return
        line = self.getpos()[0]
        if not ja:
            m = KANA_RE.search(data)
            if m:
                self.errors.append((line + data.count('\n', 0, m.start()),
                                    '的「%s」有日文假名，要放在 lang="ja" 的元素裡' % data.strip()[:20]))
        elif not ruby:
            m = KANJI_RE.search(data)
            if m:
                self.errors.append((line + data.count('\n', 0, m.start()),
                                    '的漢字「%s」沒標讀音（要包在 <ruby> 裡）' % m.group()))


def _ja_check(html):
    p = JaChecker()
    p.feed(html)
    p.close()
    return p.errors


def ja_errors(html):
    return ['第 %d 行%s' % (line, msg) for line, msg in _ja_check(html)]


def ja_quiz_errors(questions):
    errs = []
    for i, q in enumerate(questions, 1):
        fields = [('題目', q.get('q', ''))] + [('選項 %d' % j, o) for j, o in enumerate(q.get('opts', []), 1)] \
            + [('解析', q.get('exp', ''))]
        for name, text in fields:
            errs += ['第 %d 題（%s）%s' % (i, name, msg) for _, msg in _ja_check(text)]
    return errs
```

`load_site`：把讀 quiz 那行移到 drill 檢查後面，再加：

```python
            L['quiz'] = json.loads((ldir / 'quiz.json').read_text(encoding='utf-8'))['questions']
            if mod.get('lang') == 'ja':
                errs = ja_errors(L['html']) + ja_quiz_errors(L['quiz'])
                if errs:
                    raise SystemExit('建置中止：%s/%s 的日文沒標好\n  ' % (entry['id'], L['dir'])
                                     + '\n  '.join(errs))
```

（原本 `L['quiz'] = ...` 那行刪掉，避免讀兩次。）

`section_titles` 的 `rep` 裡，算純文字前先去掉讀音：

```python
RT_RE = re.compile(r'<(rt|rp)>.*?</\1>', re.S)
...
        titles.append(re.sub(r'\s+', ' ', TAG_RE.sub('', RT_RE.sub('', m.group(1)))).strip())
```

- [ ] **Step 4: 跑測試確認通過**

Run: `python3 -m unittest discover -s builder/tests 2>&1 | tail -3`
Expected: `OK`（全部測試，含既有的）

- [ ] **Step 5: Commit**

```bash
git add builder/build.py builder/tests/test_checks.py
git commit -m "feat(build): 日文模組檢查假名要有 lang=\"ja\"、漢字要有讀音；小節標題的讀音不進目錄"
```

---

### Task 2: 日文字型、讀音排版、例句清單、圖示

**Files:**
- Modify: `builder/templates/module.html:9`（字型連結）
- Modify: `builder/templates/style.css`（檔尾加日文段）
- Modify: `builder/templates/icons.svg`（加 `ic-japanese`）
- Test: `builder/tests/test_build.py`

**Interfaces:**
- Produces: CSS class `ul.jx`（例句清單：`li > span.jp[lang=ja]` ＋ `span.zh`）；`[lang|="ja"]` 字型；圖示名 `japanese`。

- [ ] **Step 1: 寫會失敗的測試**（`test_build.py` 檔尾；照檔內既有方式取 `TPL` 路徑，沒有就用 `ROOT / 'builder' / 'templates'`）

```python
class TestJapaneseStyle(unittest.TestCase):
    """日文：日文字型只套在 lang="ja"、讀音有樣式、例句清單、模組圖示。"""
    TPL = ROOT / 'builder' / 'templates'

    def test_module_page_loads_jp_font(self):
        self.assertIn('Noto+Sans+JP', (self.TPL / 'module.html').read_text(encoding='utf-8'))

    def test_lang_ja_uses_jp_font(self):
        css = (self.TPL / 'style.css').read_text(encoding='utf-8')
        self.assertRegex(css, r'\[lang\|="ja"\]\{[^}]*"Noto Sans JP"')

    def test_ruby_and_example_list_styled(self):
        css = (self.TPL / 'style.css').read_text(encoding='utf-8')
        self.assertIn('rt{', css)
        self.assertIn('.jx', css)

    def test_japanese_icon(self):
        self.assertIn('id="ic-japanese"', (self.TPL / 'icons.svg').read_text(encoding='utf-8'))
```

- [ ] **Step 2: 跑測試確認失敗**

Run: `python3 -m unittest discover -s builder/tests 2>&1 | tail -3`
Expected: 4 個 FAIL（找不到 Noto+Sans+JP、`[lang|="ja"]`、`rt{`、`ic-japanese`）

- [ ] **Step 3: 實作**

`module.html` 第 9 行字型網址的 `family=Noto+Sans+TC:wght@400;500;700;900` 後面加 `&family=Noto+Sans+JP:wght@400;700`。（Google Fonts 的日文字型切成很多小檔、照用到的字下載；只有 `lang="ja"` 的字用它，其他模組不會下載。）

`style.css` 檔尾加：

```css
/* ── 日文 ── 日文字只用日文字型（中文字型的漢字是中文字形）；漢字上方的讀音（振假名）；例句清單 */
/* 用屬性選擇器只蓋「寫了 lang 的那個元素」，裡面的字繼承；用 :lang() 會蓋過每個子元素自己的字型（例如 code） */
[lang|="ja"]{font-family:"Noto Sans JP","Hiragino Sans","Yu Gothic",sans-serif}
main [lang|="zh"]{font-family:"Noto Sans TC","PingFang TC","Microsoft JhengHei",sans-serif}
ruby{ruby-position:over}
rt{font-size:.55em;font-weight:400;color:var(--ink2);letter-spacing:0}
:is(p,li,td,th,h3,.dq,.qt,.wq,.opt .tx,.dexp):has(ruby){line-height:2.2}
.jx{list-style:none;padding:0;margin:10px 0 16px}
.jx li{margin:0 0 10px;padding:2px 0 2px 12px;border-left:3px solid var(--mint-soft)}
.jx .jp{display:block;font-size:17px;color:var(--ink)}
.jx .zh{display:block;font-size:14px;color:var(--ink2);line-height:1.6}
```

`icons.svg` 在 `ic-ai-tools` 那行後面加（鳥居；桃色填上方橫木）：

```xml
<symbol id="ic-japanese" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path fill="#FBC580" stroke="none" d="M3 5c4 1.5 14 1.5 18 0v3H3z"/><path d="M3 5c4 1.5 14 1.5 18 0M5 11h14M7 7.5V21M17 7.5V21M12 7.5V11"/></symbol>
```

- [ ] **Step 4: 跑測試確認通過**

Run: `python3 -m unittest discover -s builder/tests 2>&1 | tail -3`
Expected: `OK`（其中「每個 CSS 變數都有定義」「暗色蓋過每個顏色」等既有測試也過，因為只用既有變數）

- [ ] **Step 5: 瀏覽器檢查**（Task 4 有課之後一起看也可以；這裡先用暫存頁看）

在 scratchpad 寫一頁只含 `<link rel=stylesheet href="style.css">`、一段 `ul.jx`、一題 `.drill`、一個模擬的 `.opt` 按鈕（內含 ruby）的 HTML，放進 `dist/` 旁邊用 `python3 -m http.server` 開，用 gstack browse 在 1280 與 390 寬、亮與暗（`document.documentElement.dataset.theme='dark'`）各截一張圖。看：讀音在漢字正上方、不跟上一行重疊、`.opt` 內文字垂直置中、暗色讀音看得清楚、鳥居圖示認得出來。不對就調 CSS（只動本段）再看。

- [ ] **Step 6: Commit**

```bash
git add builder/templates/module.html builder/templates/style.css builder/templates/icons.svg builder/tests/test_build.py
git commit -m "feat(ui): 日文字型只套在 lang=ja、漢字上方讀音的樣式、例句清單、日文模組圖示"
```

---

### Task 3: 讀音比對程式（審查用）

**Files:**
- Create: `builder/tools/check_readings.py`
- Test: `builder/tests/test_readings.py`

**Interfaces:**
- Produces: `python3 builder/tools/check_readings.py <課的資料夾>…`，印出對不上的句子；結束碼 0＝全部對上、1＝有對不上的。函式：`units(html) -> list[(line, plain, reading)]`、`hira(s) -> str`、`compare(units, read_fn) -> list[(line, plain, ours, theirs)]`。

- [ ] **Step 1: 寫會失敗的測試**

```python
# -*- coding: utf-8 -*-
# 讀音比對程式的純函式部分；真的斷詞要裝 SudachiPy，這裡用假的讀音函式，不用裝
import sys, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'builder' / 'tools'))
import check_readings as cr


class TestReadings(unittest.TestCase):
    def test_units_split_base_and_reading(self):
        u = cr.units('<p>中文</p>\n<p lang="ja"><ruby>食<rt>た</rt></ruby>べる</p>')
        self.assertEqual(u, [(2, '食べる', 'たべる')])

    def test_hira_and_strip_symbols(self):
        self.assertEqual(cr.hira('コーヒー（　　）を、ください。'), 'こーひーをください')

    def test_compare_reports_mismatch_only(self):
        u = [(1, '私です', 'わたしです'), (2, '学生', 'がくせ')]
        fake = {'私です': 'ワタシデス', '学生': 'ガクセイ'}.get
        self.assertEqual(cr.compare(u, fake), [(2, '学生', 'がくせ', 'がくせい')])
```

- [ ] **Step 2: 跑測試確認失敗**

Run: `python3 -m unittest discover -s builder/tests -p 'test_readings.py' 2>&1 | tail -3`
Expected: ERROR，`No module named 'check_readings'`

- [ ] **Step 3: 實作** `builder/tools/check_readings.py`

```python
#!/usr/bin/env python3
"""審查用：把日文模組裡我們標的讀音，跟 SudachiPy（日文斷詞程式，會把句子切成詞並查出讀音）比對。
不是建置的一部分。對不上不一定是我們錯（例如「私」辭典讀わたくし），要逐條人工確認。
用法：python3 builder/tools/check_readings.py content/japanese/01-n5-noun-sentence [其他課…]
需要：pip3 install sudachipy sudachidict_core"""
import json, re, sys
from html.parser import HTMLParser
from pathlib import Path

VOID = {'br', 'img', 'wbr', 'hr', 'input', 'meta', 'link', 'source'}


class _Units(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack, self.out, self.cur = [], [], None   # stack: (tag, ja, ruby, rt)

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        ja, ruby, rt = self.stack[-1][1:] if self.stack else (False, False, False)
        lang = dict(attrs).get('lang')
        if lang is not None:
            ja = lang.lower().startswith('ja')
        if ja and self.cur is None:
            self.cur = [self.getpos()[0], '', '', len(self.stack)]
        self.stack.append((tag, ja, ruby or tag == 'ruby', rt or tag in ('rt', 'rp')))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break
        if self.cur is not None and len(self.stack) <= self.cur[3]:
            self.out.append((self.cur[0], self.cur[1], self.cur[2]))
            self.cur = None

    def handle_data(self, data):
        if self.cur is None or not self.stack:
            return
        _, ja, ruby, rt = self.stack[-1]
        if not ja:
            return
        if rt:
            self.cur[2] += data
        elif ruby:
            self.cur[1] += data
        else:
            self.cur[1] += data
            self.cur[2] += data


def units(html):
    p = _Units()
    p.feed(html)
    p.close()
    return p.out


def hira(s):
    s = ''.join(chr(ord(c) - 0x60) if 'ァ' <= c <= 'ヶ' else c for c in s)
    return re.sub(r'[^ぁ-ゖー]', '', s)


def compare(us, read_fn):
    bad = []
    for line, plain, ours in us:
        theirs = hira(read_fn(plain))
        if hira(ours) != theirs:
            bad.append((line, plain, hira(ours), theirs))
    return bad


def sudachi_reader():
    from sudachipy import dictionary, tokenizer
    tok = dictionary.Dictionary().create()
    mode = tokenizer.Tokenizer.SplitMode.C
    return lambda text: ''.join(m.reading_form() for m in tok.tokenize(re.sub(r'[＿★（）　]', '', text), mode))


def main(dirs):
    read = sudachi_reader()
    total = 0
    for d in map(Path, dirs):
        files = [('lesson.html', (d / 'lesson.html').read_text(encoding='utf-8'))]
        for i, q in enumerate(json.loads((d / 'quiz.json').read_text(encoding='utf-8'))['questions'], 1):
            for f in [q['q']] + q['opts'] + [q['exp']]:
                files.append(('quiz 第 %d 題' % i, f))
        for name, html in files:
            for line, plain, ours, theirs in compare(units(html), read):
                total += 1
                where = '%s 第 %d 行' % (name, line) if name == 'lesson.html' else name
                print('%s/%s：%s\n  我們標：%s\n  斷詞讀：%s' % (d.name, where, plain, ours, theirs))
    print('對不上 %d 句' % total)
    return 1 if total else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
```

- [ ] **Step 4: 跑測試確認通過**

Run: `python3 -m unittest discover -s builder/tests 2>&1 | tail -3`
Expected: `OK`

- [ ] **Step 5: 裝 SudachiPy 並實跑一次**

Run: `pip3 install --user sudachipy sudachidict_core 2>&1 | tail -1`，然後在 scratchpad 造一個假課資料夾（`lesson.html` 放 `JA_OK` 那兩句、`quiz.json` 放一題），跑 `python3 builder/tools/check_readings.py <那個資料夾>`。
Expected: 印出結果、不當掉。若「私」被讀成わたくし而列出來，屬預期（人工確認的範例）。裝不起來就在 ledger 記一筆 Ruling，審查改成人工逐字核對。

- [ ] **Step 6: Commit**

```bash
git add builder/tools/check_readings.py builder/tests/test_readings.py
git commit -m "feat(tools): 讀音比對程式，用 SudachiPy 斷詞比對課文標的讀音（審查用）"
```

---

### Task 4: 日文模組骨架＋第 1 課〈名詞句：AはBです〉

**Files:**
- Modify: `content/modules.json`（`english` 後面加 `{"id": "japanese", "icon": "japanese"}`）
- Create: `content/japanese/module.json`
- Create: `content/japanese/01-n5-noun-sentence/lesson.html`、`quiz.json`

**Interfaces:**
- Consumes: Task 1 的檢查、Task 2 的 `ul.jx` 與字型、Task 3 的讀音程式。
- Produces: 第 1 課是後面三課的範本（標記寫法、語氣、份量）。

- [ ] **Step 1: 寫 `content/japanese/module.json`**

```json
{
 "title": "日文",
 "lang": "ja",
 "intro": "日檢文法從 N5 教起，一路排到 N1。例句的漢字都標讀音，每個句型配例句與點了就對答案的練習。",
 "kick": "JAPANESE · 日檢文法 N5〜N1",
 "overview_intro": [
  "照日檢級數分組，每一級學完可以去考那一級：",
  [
   "<b>N5</b>：〈名詞句：AはBです〉〈助詞（一）〉〈形容詞〉〈動詞的三類與ます形〉，之後還有存在與數量、て形、ない形與た形、普通形。"
  ]
 ],
 "footer_note": "日檢官方從 2010 年起不公布各級文法清單；課裡標的級數是常見分級（依改制前的官方出題範圍與參考書整理），各家大致一致、不完全相同。例句與練習全部自編。",
 "lessons": []
}
```

`lessons` 每加一課就加一筆（`dir`、`slug`、`title`、`desc`、`mins`、`group: "N5"`）。第一批四課 slug：`n5-noun-sentence`、`n5-particles`、`n5-adjectives`、`n5-masu`。

- [ ] **Step 2: 派寫課代理寫第 1 課**（一個代理，給它下面「寫課代理的交代」全文＋這課的範圍）

第 1 課範圍：です／だ（只介紹です，だ一句帶過「之後〈普通形與連接句子〉會教」）、〜じゃありません／〜ではありません、〜でした／〜じゃありませんでした、名詞＋の＋名詞、こ・そ・あ・ど（これ／それ／あれ／どれ、この／その／あの／どの、ここ／そこ／あそこ／どこ）、〜か（疑問句）、〜も（「也是」）。開頭先講「這份教材怎麼讀」：句子結構跟中文的差別（動詞在最後）、讀音標在漢字上方、級數是常見分級（一次）。

- [ ] **Step 3: 建置與讀音檢查**

Run: `python3 builder/build.py && python3 builder/tools/check_readings.py content/japanese/01-n5-noun-sentence`
Expected: 建置成功；讀音對不上的每一條，代理已在回報裡說明是哪一種（辭典另一種讀法、人名、量詞）並確認我們標的對。

- [ ] **Step 4: 獨立審查**（另一個代理，給它「審查代理的交代」）→ 修正 → 範圍複審（只看修過的地方）

- [ ] **Step 5: 自己在瀏覽器看第 1 課**（1280 與 390、亮與暗）：讀音、例句清單、課中練習點選、課末測驗（選項有讀音）、側欄小節。不對就修。

- [ ] **Step 6: Commit**（還不 push）

```bash
git add content/modules.json content/japanese
git commit -m "feat(content): 新增日文模組，第 1 課〈名詞句：AはBです〉"
```

---

### Task 5: 第 2〜4 課（三個寫課代理同時跑）

**Files:**
- Create: `content/japanese/02-n5-particles/`、`03-n5-adjectives/`、`04-n5-masu/`（各 `lesson.html`、`quiz.json`）
- Modify: `content/japanese/module.json`（加三筆 lessons）——**由主控統一加**，代理不碰，避免同時改同一個檔。

各課範圍：
- **〈助詞（一）〉**：は（主題）、が（N5 只教「疑問詞當主詞用が」「好き／上手／ある・いる 前用が」，は／が 的完整差別寫「之後的課再談」）、を、に（時間點、目的地、對象）、へ、で（地點、手段）、と（和、一起）、も、から／まで、や。
- **〈形容詞〉**：い形容詞與な形容詞怎麼分（きれい、有名 是な形容詞的陷阱）、現在肯定否定、過去肯定否定、修飾名詞（高い本、静かな町）、いい→よくない的例外、〜くて／〜で 連接兩個形容詞。
- **〈動詞的三類與ます形〉**：第一類／第二類／第三類動詞怎麼分（看 ます 前一個音、帰る・入る 這種長得像第二類的第一類）、辭書形↔ます形、ます／ません／ました／ませんでした、〜ましょう、〜ませんか、時間與頻率的說法（毎日、よく、ときどき、あまり〜ません）。

- [ ] **Step 1:** 三個代理各寫一課（交代全文＋範圍＋「第 1 課已上線的檔，照它的標記與份量」）。
- [ ] **Step 2:** 主控把三筆加進 `module.json`，跑 `python3 builder/build.py` 與三課的 `check_readings.py`。Expected: 建置成功；讀音對不上的都有說明。
- [ ] **Step 3: Commit**

```bash
git add content/japanese
git commit -m "feat(content): 日文 N5〈助詞（一）〉〈形容詞〉〈動詞的三類與ます形〉"
```

---

### Task 6: 第 2〜4 課審查與修正

- [ ] **Step 1:** 三個審查代理同時跑，各審一課（交代全文）。
- [ ] **Step 2:** 依審查結果修正（原寫課代理或主控），再派範圍複審（只看修過的地方）。
- [ ] **Step 3:** `python3 -m unittest discover -s builder/tests` 全過、`python3 builder/build.py` 成功。
- [ ] **Step 4: Commit**

```bash
git add content/japanese
git commit -m "fix(content): 日文 N5 第 2〜4 課依審查修正"
```

---

### Task 7: 上線

- [ ] **Step 1: 瀏覽器整體看一遍**：首頁有日文卡片與圖示；四課在 1280／390、亮／暗各看一次；故意答錯兩題測驗，看錯題區清單與練習頁的讀音（Review Focus 第 2 條）。
- [ ] **Step 2:** `CLAUDE.md` 現況加一條「2026-10-14 日文模組」：規格與計畫路徑、`"lang": "ja"` 會開日文檢查、讀音比對程式在 `builder/tools/check_readings.py`。
- [ ] **Step 3: Commit 與 push**

```bash
git add CLAUDE.md
git commit -m "docs: CLAUDE.md 記日文模組"
git push
```

- [ ] **Step 4:** `GH_TOKEN=$(gh auth token -u HHTim) gh run list --repo HHTim/notes-platform --limit 1` 直到 `completed success`；線上打開日文模組確認。

---

## 寫課代理的交代（Task 4、5 給寫課代理的全文）

你要寫 Tim 的筆記平台「日文」模組的一課（N5 文法）。讀者是台灣人，五十音會、沒有文法基礎。說明一律繁體中文、台灣用語。

**先讀：**
- 規格 `docs/superpowers/specs/2026-10-14-japanese-grammar-design.md`。
- 英文模組的 `content/english/03-grammar-sentence/lesson.html` 看整課結構（檔頭來源註解、`learn` 框、`section`／`era`／`h3.head`、`keys` 重點整理、`drill` 課中練習）。
- 第 1 課上線後：`content/japanese/01-n5-noun-sentence/` 是日文課的範本，標記寫法與份量照它。
- 記憶檔 `~/.claude/projects/-Users-twinb00597734-Workspace-notes-platform/memory/` 裡的 `no-meta-preamble.md`、`textbook-voice.md`、`bullets-not-long-paragraphs.md`、`rewrite-preserve-reservation.md`。

**標記寫法：**

例句：
```html
<ul class="jx">
  <li><span class="jp" lang="ja"><ruby>私<rt>わたし</rt></ruby>は<ruby>学生<rt>がくせい</rt></ruby>です。</span><span class="zh">我是學生。</span></li>
</ul>
```

課中練習（填空）：
```html
<div class="drill">
  <p class="dq" lang="ja"><ruby>私<rt>わたし</rt></ruby>（　　）<ruby>林<rt>りん</rt></ruby>です。</p>
  <ul class="dopts" lang="ja"><li>が</li><li data-ok>は</li><li>を</li><li>に</li></ul>
  <p class="dexp"><span class="dtr">整句：我姓林。</span>自我介紹「我是～」用 <span lang="ja">は</span> 標出主題。</p>
</div>
```

課中練習（排列順序，日檢「★」題）：題目寫成 `あの　＿＿　＿＿　★　＿＿　です。` 這種形狀，四個選項就是四個片段，正解是放在 ★ 的那一個；解析先寫整句中譯，再寫完整順序。

課末測驗 `quiz.json`：
```json
{"questions": [
  {"q": "<span lang=\"ja\"><ruby>駅<rt>えき</rt></ruby>（　　）<ruby>行<rt>い</rt></ruby>きます。</span>",
   "opts": ["<span lang=\"ja\">へ</span>", "<span lang=\"ja\">を</span>", "<span lang=\"ja\">で</span>", "<span lang=\"ja\">が</span>"],
   "exp": "整句：去車站。……"}
]}
```

**寫課守則：**

1. **正解必須唯一。** 每個陷阱選項放回句子問「在任何合理的讀法下，這句日文對嗎？」日文常見翻車：は／が 兩個都通（要有上下文鎖住）、に／へ 表方向兩個都可以、で／に 表地點、敬體常體混用、口語可以省略助詞。
2. **陷阱選項要錯在本課考的那一點**，不靠語序壞掉製造錯誤。
3. **解析不用位置指選項**（測驗會重排）；直接引那個字。
4. **規則不要說得比出處多。** 「一定」「只能」「不能」「都」要有出處撐；想到後面的課會不會打架（例如「は 標主題」在 N4 以後會遇到對比用法，寫「這課先學」而不是「は 只有這個用法」）。
5. **日檢怎麼出題沒有官方細節**：jlpt.jp 只公布題型與各級「認定の目安」。「最常考」一律改建議語氣。
6. **用詞統一**：い形容詞、な形容詞、第一類動詞（五段動詞）／第二類動詞（一段動詞）／第三類動詞（する、来る）——括號裡的別名只在第一次出現時附；ます形、て形、辭書形、普通形；敬體（です、ます 的說法）、常體（普通形的說法）；主題（は）、主詞（が）；陷阱選項。台灣用語照 `~/.claude/tim-style/china-terms.md`。
7. **讀音**：`lang="ja"` 底下每個漢字都要在 `<ruby>` 裡；`<rt>` 只蓋漢字，送假名放外面（`<ruby>食<rt>た</rt></ruby>べる`）；整個詞的讀音不能拆時整詞標（`<ruby>今日<rt>きょう</rt></ruby>`）；數字＋量詞整組標（`<ruby>3人<rt>さんにん</rt></ruby>`）。寫完跑 `python3 builder/tools/check_readings.py content/japanese/<這課>`，對不上的逐條確認，回報時列出「斷詞讀法不同但我們對」的每一條與理由。
8. **每句日文都有中文翻譯**：例句的 `.zh`、練習解析開頭的 `整句：`、測驗解析開頭的 `整句：`。
9. **例句只用這課和前面課教過的句型**（單字可以新，有讀音與翻譯就好）。
10. **情境**：日常生活為主（買東西、搭車、約朋友、學校、餐廳），穿插職場（公司、會議、跟客戶）。人名用常見日本姓（田中、山田、佐藤、鈴木）與台灣姓（林、陳、王）。全部自編，不抄考古題、參考書、題庫網站。
11. **出處**：可驗證的文法說明掛 `<a class="fixsrc" href="…" target="_blank" rel="noopener">出處</a>`；優先國際交流基金（いろどり https://www.irodori.jpf.go.jp/ 的文法說明、JF 日本語教育スタンダード）、國語辭典線上條目（kotobank 的デジタル大辞泉）。連結要實際打得開且頁面真的支撐那句話（curl 確認；網頁是 JavaScript 產生的就用 gstack browse 看）。不寫「某某說」、不附日文原文長句。查不到出處的規則，寫法保留語氣。
12. **選項長度不洩題**；課中練習正解位置分散在四格；測驗正解放 `opts[0]`。
13. **份量**：課中練習 40〜55 題、課末測驗 10 題；`mins` 照實估（讀加做 25〜40 分鐘）。
14. **不寫寫課者旁白**：開頭不自述、中段不寫「讀者看資料時要怎麼做」、`learn` 框每條一句短的；並列項目用條列，不用「；」串長段。零 `fixnote`、零 `data-note`。
15. **指路只寫課名不寫課序**（〈助詞（一）〉這樣）。

**完成條件：** `python3 builder/build.py` 成功（日文檢查、練習檢查都過）；`check_readings.py` 跑過且每條對不上都有說明。回報：題數、`mins`、出處清單、讀音說明。**不要碰 `module.json` 以外別課的檔，也不要 commit**（第 1 課的代理例外：`module.json` 的 lessons 由主控加）。

## 審查代理的交代（Task 4、6）

你要審 Tim 筆記平台日文模組的一課。照「寫課代理的交代」的 15 條守則逐條檢查，另外：

- **每一題都自己作答一次**（課中練習與測驗），把每個陷阱選項放回句子判斷是否也對；正解不唯一列為最嚴重。
- 跑 `python3 builder/tools/check_readings.py content/japanese/<這課>`，對不上的每一條自己判斷誰對。
- 文法說明有沒有錯、有沒有說得比出處多；出處連結打得開、真的支撐那句話。
- 日文自然度：例句是不是日本人會這樣說（不自然但文法對的也列）。
- 用詞：台灣用語、守則第 6 條的術語。

回報格式：每條問題寫「位置（第幾行或第幾題）→ 問題 → 建議改法」，分「一定要改」「建議改」兩組。不要自己改檔。
