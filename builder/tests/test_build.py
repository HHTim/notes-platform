# -*- coding: utf-8 -*-
# 建置結果檢查：檔案齊、模組頁的側邊欄／文章／測驗資料都組對
import json, re, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'builder'))
import build as builder


class TestBuild(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = Path(tempfile.mkdtemp()) / 'dist'
        builder.build(out_dir=cls.out)
        cls.site, cls.mods = builder.load_site(ROOT / 'content')

    def test_output_files(self):
        for name in ('index.html', 'style.css', 'course.js'):
            self.assertTrue((self.out / name).exists(), name)
        for mod in self.mods:
            self.assertTrue((self.out / mod['id'] / 'index.html').exists(), mod['id'])

    def test_module_page_k8s(self):
        html = (self.out / 'k8s' / 'index.html').read_text(encoding='utf-8')
        k8s = [m for m in self.mods if m['id'] == 'k8s'][0]
        # 側邊欄：總覽 + 13 課
        self.assertEqual(html.count('data-nav='), len(k8s['lessons']) + 1)
        # 分組標題四個都在
        for g in ('歷史：為什麼會有容器', 'DOCKER：一台機器上的事', 'K8S：由小到大', '判斷'):
            self.assertIn(g, html)
        # 每課一篇文章
        for L in k8s['lessons']:
            self.assertIn('<article id="pg-%s"' % L['slug'], html)
        # 測驗資料整包嵌進頁面，抽查第一課第一題
        self.assertIn(json.dumps(k8s['lessons'][0]['quiz'][0]['q'], ensure_ascii=False), html)
        self.assertIn("var MODULE=\"k8s\"", html)
        # 共用樣式與腳本用相對路徑
        self.assertIn('../style.css', html)
        self.assertIn('../course.js', html)
        # 頂欄：回首頁連結與模組下拉選單，選單有全部模組
        self.assertIn('href="../"', html)
        self.assertEqual(html.count('<option'), len(self.mods))

    def test_no_company_terms(self):
        for page in self.out.rglob('*.html'):
            self.assertNotIn('KPI', page.read_text(encoding='utf-8'), str(page))

    def test_progress_key_per_module(self):
        js = (self.out / 'course.js').read_text(encoding='utf-8')
        self.assertIn("'notes-progress:'+MODULE", js)
        self.assertNotIn('k8s-course-done', js)


if __name__ == '__main__':
    unittest.main()
