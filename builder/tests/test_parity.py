# -*- coding: utf-8 -*-
# 驗收：新工具組出來的 K8s 模組頁，逐課文字要跟 rescue/k8s-course.html 一致
# （總覽頁開場段落刻意改過措辭、測驗有補題，所以只比 13 課的文章與總覽的課程列表）
import re, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'builder'))
import build as builder

RESCUE = ROOT / 'rescue' / 'k8s-course.html'


def text_of(html):
    html = re.sub(r'<!--.*?-->', ' ', html, flags=re.S)
    html = re.sub(r'<[^>]+>', ' ', html)
    return re.sub(r'\s+', ' ', html).strip()


def article(html, slug):
    m = re.search(r'<article id="pg-%s"[^>]*>.*?</article>' % re.escape(slug), html, re.S)
    assert m, 'pg-%s not found' % slug
    return m.group(0)


@unittest.skipUnless(RESCUE.exists(), 'rescue/ 已刪，跳過一致性比對')
class TestParity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old = RESCUE.read_text(encoding='utf-8')
        out = Path(tempfile.mkdtemp()) / 'dist'
        builder.build(out_dir=out)
        cls.new = (out / 'k8s' / 'index.html').read_text(encoding='utf-8')
        _, mods = builder.load_site(ROOT / 'content')
        cls.k8s = [m for m in mods if m['id'] == 'k8s'][0]

    def test_all_13_lessons_match(self):
        for L in self.k8s['lessons']:
            with self.subTest(lesson=L['slug']):
                self.assertEqual(text_of(article(self.old, L['slug'])),
                                 text_of(article(self.new, L['slug'])))

    def test_overview_lesson_list_matches(self):
        pick = lambda h: re.search(r'<div class="lesson-list">.*?</div>', h, re.S).group(0)
        self.assertEqual(text_of(pick(article(self.old, 'ov'))),
                         text_of(pick(article(self.new, 'ov'))))


if __name__ == '__main__':
    unittest.main()
