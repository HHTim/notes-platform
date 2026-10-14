# -*- coding: utf-8 -*-
# 建置時的內容把關：標籤沒配對、slug 撞名或不合法，build 要直接失敗並講清楚是哪一課
import json, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'builder'))
import build as builder

LESSON_OK = ('<!-- 來源：測試用 -->\n<div class="learn"><p class="lbl">讀完這課你會</p><ul><li>一件事</li></ul></div>\n'
             '<section><p class="era">段落</p><h3 class="head">標題</h3><p>內文<br>換行<img src="x.png" alt=""></p></section>\n'
             '<div class="keys"><p class="lbl">重點整理</p><ul><li>一點</li></ul></div>\n')
QUIZ = {'questions': [{'q': '題目？', 'opts': ['對', '錯', '不知道'], 'exp': '因為。'}] * 5}


def fake_site(lessons, mod_extra=None):
    """在暫存目錄造一個只有一個模組的假 content/。lessons 是 [(dir, slug, html), ...]。"""
    tmp = Path(tempfile.mkdtemp())
    content = tmp / 'content'
    mdir = content / 'demo'
    mdir.mkdir(parents=True)
    (content / 'modules.json').write_text(json.dumps(
        {'site_title': '測試站', 'site_intro': '介紹', 'modules': [{'id': 'demo', 'icon': 'java'}]},
        ensure_ascii=False), encoding='utf-8')
    (mdir / 'module.json').write_text(json.dumps(dict({
        'title': '示範模組', 'intro': '介紹', 'kick': 'DEMO', 'overview_intro': '總覽', 'footer_note': '註',
        'lessons': [{'dir': d, 'slug': s, 'title': '第 %s 課' % d, 'desc': '說明', 'mins': 5}
                    for d, s, _ in lessons]}, **(mod_extra or {})), ensure_ascii=False), encoding='utf-8')
    for d, _, html in lessons:
        ldir = mdir / d
        ldir.mkdir()
        (ldir / 'lesson.html').write_text(html, encoding='utf-8')
        (ldir / 'quiz.json').write_text(json.dumps(QUIZ, ensure_ascii=False), encoding='utf-8')
    return content, tmp / 'dist'


class TestTagBalance(unittest.TestCase):
    def test_balanced_lesson_builds(self):
        content, out = fake_site([('01-one', 'one', LESSON_OK)])
        builder.build(content_dir=content, out_dir=out)   # void 元素（br、img）不算未關閉
        self.assertTrue((out / 'demo' / 'index.html').exists())

    def test_extra_close_tag_fails_with_lesson_name(self):
        bad = LESSON_OK + '</article>\n'   # 多一個 </article>，會把後面的測驗與導覽擠出文章
        content, out = fake_site([('01-one', 'one', LESSON_OK), ('02-two', 'two', bad)])
        with self.assertRaises(SystemExit) as cm:
            builder.build(content_dir=content, out_dir=out)
        msg = str(cm.exception)
        self.assertIn('demo/02-two', msg)
        self.assertIn('</article>', msg)

    def test_unclosed_tag_fails_with_lesson_name(self):
        bad = LESSON_OK.replace('</section>', '')   # 少一個 </section>
        content, out = fake_site([('01-one', 'one', bad)])
        with self.assertRaises(SystemExit) as cm:
            builder.build(content_dir=content, out_dir=out)
        msg = str(cm.exception)
        self.assertIn('demo/01-one', msg)
        self.assertIn('<section>', msg)


class TestSlugs(unittest.TestCase):
    def test_duplicate_slug_fails_naming_both_lessons(self):
        # 兩課同 slug：頁面裡的 QUIZ 字典後者會蓋掉前者，網址也分不出是哪一課
        content, out = fake_site([('01-one', 'same', LESSON_OK), ('02-two', 'same', LESSON_OK)])
        with self.assertRaises(SystemExit) as cm:
            builder.build(content_dir=content, out_dir=out)
        msg = str(cm.exception)
        self.assertIn('demo/01-one', msg)
        self.assertIn('demo/02-two', msg)
        self.assertIn('same', msg)

    def test_illegal_slug_fails(self):
        # course.js 的路由只接 ^[a-z0-9-]+$；大寫、底線、中文都進不了頁
        for bad in ('Has-Upper', 'has_underscore', '中文', 'has space'):
            with self.subTest(slug=bad):
                content, out = fake_site([('01-one', bad, LESSON_OK)])
                with self.assertRaises(SystemExit) as cm:
                    builder.build(content_dir=content, out_dir=out)
                msg = str(cm.exception)
                self.assertIn('demo/01-one', msg)
                self.assertIn(bad, msg)


if __name__ == '__main__':
    unittest.main()


class TestOverviewIntro(unittest.TestCase):
    def test_string_is_one_paragraph(self):
        self.assertEqual(builder.intro_html('一段'), '<p>一段</p>\n')

    def test_list_mixes_paragraphs_and_points(self):
        html = builder.intro_html(['開場', ['第一點', '第二點'], '結尾'])
        self.assertEqual(html, '<p>開場</p>\n<ul class="ov-points">\n<li>第一點</li>\n<li>第二點</li>\n</ul>\n<p>結尾</p>\n')



DRILL_OK = ('<div class="drill"><p class="dq">The order ______ yesterday.</p>'
            '<ul class="dopts"><li>ship</li><li data-ok>shipped</li><li>shipping</li><li>has shipped</li></ul>'
            '<p class="dexp">yesterday 是過去的時間點。</p></div>\n')


class TestDrills(unittest.TestCase):
    """課中練習：每題剛好一個正解、要有解析、選項 2〜5 個。寫錯會變成點了沒反應或永遠答錯，建置時抓。"""

    def check(self, html):
        return builder.drill_errors(html)

    def test_good_drill_passes(self):
        self.assertEqual(self.check(DRILL_OK), [])

    def test_no_answer_fails(self):
        errs = self.check(DRILL_OK.replace(' data-ok', ''))
        self.assertEqual(len(errs), 1)
        self.assertIn('正解', errs[0])

    def test_two_answers_fail(self):
        errs = self.check(DRILL_OK.replace('<li>ship</li>', '<li data-ok>ship</li>'))
        self.assertIn('正解', errs[0])

    def test_missing_explanation_fails(self):
        errs = self.check(DRILL_OK.replace('<p class="dexp">yesterday 是過去的時間點。</p>', ''))
        self.assertIn('解析', errs[0])

    def test_build_stops_with_lesson_name(self):
        bad = LESSON_OK + DRILL_OK.replace(' data-ok', '')
        content, out = fake_site([('01-one', 'one', bad)])
        with self.assertRaises(SystemExit) as cm:
            builder.build(content_dir=content, out_dir=out)
        self.assertIn('demo/01-one', str(cm.exception))


class TestIcons(unittest.TestCase):
    """圖示名稱要對得到 icons.svg 的 <symbol id="ic-名稱">；對不到建置要停，並講是哪個模組"""

    def test_icon_names_from_svg(self):
        names = builder.icon_names('<svg><symbol id="ic-java"></symbol><symbol id="ic-ai-tools"></symbol></svg>')
        self.assertEqual(names, {'java', 'ai-tools'})

    def test_icon_html(self):
        self.assertEqual(builder.icon_html('java'),
                         '<svg class="ic" aria-hidden="true"><use href="#ic-java"/></svg>')
        self.assertIn('class="ic big"', builder.icon_html('java', 'ic big'))

    def test_unknown_icon_stops_build(self):
        content, out = fake_site([('01-one', 'one', LESSON_OK)])
        mj = content / 'modules.json'
        mj.write_text(mj.read_text(encoding='utf-8').replace('"icon": "java"', '"icon": "javaa"'), encoding='utf-8')
        with self.assertRaises(SystemExit) as cm:
            builder.build(content_dir=content, out_dir=out)
        msg = str(cm.exception)
        self.assertIn('demo', msg)
        self.assertIn('javaa', msg)

    def test_missing_icon_stops_build_naming_module(self):
        content, out = fake_site([('01-one', 'one', LESSON_OK)])
        mj = content / 'modules.json'
        mj.write_text(mj.read_text(encoding='utf-8').replace(', "icon": "java"', ''), encoding='utf-8')
        with self.assertRaises(SystemExit) as cm:
            builder.build(content_dir=content, out_dir=out)
        msg = str(cm.exception)
        self.assertIn('demo', msg)
        self.assertIn('沒有填 icon', msg)

    def test_icons_inlined_once_per_page(self):
        content, out = fake_site([('01-one', 'one', LESSON_OK)])
        builder.build(content_dir=content, out_dir=out)
        for page in ('index.html', 'demo/index.html'):
            html = (out / page).read_text(encoding='utf-8')
            self.assertEqual(html.count('<symbol id="ic-java"'), 1, page)
            self.assertNotIn('__ICONS__', html, page)


class TestSections(unittest.TestCase):
    """本課小節目錄：從 <h3 class="head"> 自動產生，建置時補 id；有課中練習才列「課中練習」"""

    def test_heads_get_ids_and_titles(self):
        html, titles = builder.section_titles(
            '<h3 class="head">甲 <code>x</code></h3><p>a</p><h3 class="head">乙\n丙</h3>', 'l1')
        self.assertEqual(titles, ['甲 x', '乙 丙'])
        self.assertIn('<h3 class="head" id="l1-sec-1"><span>甲 <code>x</code></span></h3>', html)
        self.assertIn('<h3 class="head" id="l1-sec-2">', html)

    def test_toc_entries(self):
        L = {'slug': 'l1', 'sections': ['甲', '乙'], 'has_drill': True}
        self.assertEqual(builder.toc_entries(L),
                         [('l1-sec-1', '甲'), ('l1-sec-2', '乙'), ('l1-drill', '課中練習'), ('l1-quiz', '隨堂測驗')])
        L['has_drill'] = False
        self.assertEqual([t for _, t in builder.toc_entries(L)], ['甲', '乙', '隨堂測驗'])

    def test_built_page_has_toc_subs_scores_and_wrong_page(self):
        with_drill = LESSON_OK + DRILL_OK
        content, out = fake_site([('01-one', 'one', with_drill), ('02-two', 'two', LESSON_OK)])
        builder.build(content_dir=content, out_dir=out)
        html = (out / 'demo' / 'index.html').read_text(encoding='utf-8')
        # 課文裡的小節 id、課中練習 id、測驗 id
        self.assertIn('<h3 class="head" id="one-sec-1"><span>標題</span></h3>', html)
        self.assertIn('<div class="drill" id="one-drill"', html)
        self.assertNotIn('id="two-drill"', html)
        self.assertIn('<div class="quiz" id="one-quiz" data-quiz="one">', html)
        # 課首目錄：第一課有課中練習、第二課沒有
        self.assertIn('<details class="toc" open><summary>本課小節</summary><ol>'
                      '<li><a href="#" data-goto="one-sec-1">標題</a></li>'
                      '<li><a href="#" data-goto="one-drill">課中練習</a></li>'
                      '<li><a href="#" data-goto="one-quiz">隨堂測驗</a></li></ol></details>', html)
        self.assertIn('<li><a href="#" data-goto="two-sec-1">標題</a></li><li><a href="#" data-goto="two-quiz">隨堂測驗</a></li>', html)
        # 側欄：錯題區項目、每課的成績欄、每課的小節
        self.assertIn('href="#/wrong" data-nav="wrong"', html)
        self.assertIn('data-wrongcnt', html)
        self.assertIn('<span class="st" data-st="one"></span>', html)
        self.assertIn('<div class="subs" data-subs="one" hidden><a href="#" data-goto="one-sec-1">標題</a>', html)
        # 錯題區頁殼與課名表
        self.assertIn('<article id="pg-wrong" hidden>', html)
        self.assertIn('id="wrongBody"', html)
        self.assertIn('var TITLES={"one": "第 01-one 課", "two": "第 02-two 課"}', html)


class TestTitleSegments(unittest.TestCase):
    """標題在全形冒號後面分段，換行只發生在段與段之間（Tim：「五大句／型」這種斷行好醜）"""

    def test_split_after_colon(self):
        self.assertEqual(builder.title_html('詞性與句子骨架：五大句型'), '詞性與句子骨架：<wbr>五大句型')

    def test_no_colon_unchanged(self):
        self.assertEqual(builder.title_html('容器'), '容器')

    def test_markup_inside_left_alone(self):
        self.assertEqual(builder.title_html('<code>a</code>：b'), '<code>a</code>：b')

    def test_built_page_segments_lesson_and_section_titles(self):
        lesson = LESSON_OK.replace('<h3 class="head">標題</h3>', '<h3 class="head">甲：乙</h3>')
        content, out = fake_site([('01-one', 'one', lesson)])
        mj = content / 'demo' / 'module.json'
        mj.write_text(mj.read_text(encoding='utf-8').replace('"第 01-one 課"', '"前半：後半"'), encoding='utf-8')
        builder.build(content_dir=content, out_dir=out)
        html = (out / 'demo' / 'index.html').read_text(encoding='utf-8')
        self.assertIn('<h1 class="lt">前半：<wbr>後半</h1>', html)
        # 小節標題是 flex 排版（前面有小方塊）：文字一律包成一塊，換行記號才不會拆出間距，長標題在手機上也縮得下
        self.assertIn('<h3 class="head" id="one-sec-1"><span>甲：<wbr>乙</span></h3>', html)
        self.assertIn('data-goto="one-sec-1">甲：乙</a>', html)   # 目錄裡不用分段


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
        # 讀音拿掉；lang="ja" 留著，側欄與目錄的日文才會用日文字型
        self.assertEqual(titles, ['<span lang="ja">私は</span>的用法'])

    def test_section_title_drops_rt_with_attributes(self):
        html = '<h3 class="head"><ruby>私<rt class="x">わたし</rt></ruby></h3>'
        self.assertEqual(builder.section_titles(html, 'x')[1], ['私'])

    def test_desc_kana_needs_lang_in_ja_module(self):
        content, out = fake_site([('01-one', 'one', LESSON_OK)], {'lang': 'ja'})
        mj = content / 'demo' / 'module.json'
        m = json.loads(mj.read_text(encoding='utf-8'))
        m['lessons'][0]['desc'] = '教 です 的用法'
        mj.write_text(json.dumps(m, ensure_ascii=False), encoding='utf-8')
        with self.assertRaises(SystemExit) as cm:
            builder.build(content_dir=content, out_dir=out)
        self.assertIn('desc', str(cm.exception))

    def test_desc_ja_span_without_ruby_ok(self):
        # desc 是一行摘要，日文包 lang 就好，不要求標讀音
        content, out = fake_site([('01-one', 'one', LESSON_OK)], {'lang': 'ja'})
        mj = content / 'demo' / 'module.json'
        m = json.loads(mj.read_text(encoding='utf-8'))
        m['lessons'][0]['desc'] = '教 <span lang="ja">静かです</span> 的用法'
        mj.write_text(json.dumps(m, ensure_ascii=False), encoding='utf-8')
        builder.build(content_dir=content, out_dir=out)
