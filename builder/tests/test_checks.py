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


def fake_site(lessons):
    """在暫存目錄造一個只有一個模組的假 content/。lessons 是 [(dir, slug, html), ...]。"""
    tmp = Path(tempfile.mkdtemp())
    content = tmp / 'content'
    mdir = content / 'demo'
    mdir.mkdir(parents=True)
    (content / 'modules.json').write_text(json.dumps(
        {'site_title': '測試站', 'site_intro': '介紹', 'modules': [{'id': 'demo', 'icon': '🧪'}]},
        ensure_ascii=False), encoding='utf-8')
    (mdir / 'module.json').write_text(json.dumps({
        'title': '示範模組', 'intro': '介紹', 'kick': 'DEMO', 'overview_intro': '總覽', 'footer_note': '註',
        'lessons': [{'dir': d, 'slug': s, 'title': '第 %s 課' % d, 'desc': '說明', 'mins': 5}
                    for d, s, _ in lessons]}, ensure_ascii=False), encoding='utf-8')
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
