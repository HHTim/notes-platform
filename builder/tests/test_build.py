# -*- coding: utf-8 -*-
# 建置結果檢查：檔案齊、模組頁的側邊欄／文章／測驗資料都組對
import json, re, shutil, sys, tempfile, unittest
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
            text_lower = page.read_text(encoding='utf-8').lower()
            self.assertNotIn('kpi', text_lower, str(page))

    def test_progress_key_per_module(self):
        js = (self.out / 'course.js').read_text(encoding='utf-8')
        self.assertIn("'notes-progress:'+MODULE", js)
        self.assertNotIn('k8s-course-done', js)

    def test_sidebar_progress_and_hint(self):
        for mid in ('k8s', 'redis'):
            html = (self.out / mid / 'index.html').read_text(encoding='utf-8')
            self.assertIn('id="sideProg"', html, mid)
            self.assertIn('id="syncHint"', html, mid)
            self.assertIn('進度只存在這台裝置', html, mid)

    def test_course_js_hooks(self):
        js = (self.out / 'course.js').read_text(encoding='utf-8')
        self.assertIn('window.NotesCourse', js)
        self.assertIn('notes:progress-saved', js)
        self.assertIn('sideProg', js)

    def test_home_page(self):
        html = (self.out / 'index.html').read_text(encoding='utf-8')
        self.assertIn(self.site['site_title'], html)
        for mod in self.mods:
            self.assertIn('href="%s/"' % mod['id'], html)
            self.assertIn(mod['icon'], html)
            self.assertIn(mod['title'], html)
            self.assertIn('data-stat="%s"' % mod['id'], html)
            self.assertIn('共 %d 課' % len(mod['lessons']), html)
        self.assertIn('style.css', html)
        self.assertIn('viewport', html)

    def test_fixnote_styles(self):
        css = (self.out / 'style.css').read_text(encoding='utf-8')
        self.assertIn('mark.fixnote', css)
        self.assertIn('attr(data-note)', css)   # 提示文字來自 data-note，純 CSS 不用 JavaScript
        self.assertIn('a.fixsrc', css)


def build_variant(firebase_cfg):
    """複製 content/ 到暫存區，依參數放或拿掉 firebase.json，建置後回傳 dist 路徑。"""
    tmp = Path(tempfile.mkdtemp())
    content = tmp / 'content'
    shutil.copytree(ROOT / 'content', content)
    fb = content / 'firebase.json'
    if firebase_cfg is None:
        if fb.exists():
            fb.unlink()
    else:
        fb.write_text(json.dumps(firebase_cfg), encoding='utf-8')
    out = tmp / 'dist'
    builder.build(content_dir=content, out_dir=out)
    return out


class TestFirebaseInjection(unittest.TestCase):
    CFG = {'apiKey': 'test-key', 'authDomain': 'test.firebaseapp.com', 'projectId': 'test'}

    def test_off_without_config(self):
        out = build_variant(None)
        html = (out / 'k8s' / 'index.html').read_text(encoding='utf-8')
        self.assertNotIn('firebasejs', html)
        self.assertNotIn('FIREBASE_CONFIG', html)
        self.assertNotIn('sync.js', html)
        self.assertFalse((out / 'sync.js').exists())

    def test_on_with_config(self):
        out = build_variant(self.CFG)
        for mid in ('k8s', 'redis'):
            html = (out / mid / 'index.html').read_text(encoding='utf-8')
            self.assertIn('var FIREBASE_CONFIG=', html, mid)
            self.assertIn('"apiKey": "test-key"', html, mid)
            for part in ('firebase-app-compat.js', 'firebase-auth-compat.js',
                         'firebase-firestore-compat.js'):
                self.assertIn('https://www.gstatic.com/firebasejs/10.14.1/' + part, html, mid)
            self.assertIn('<script src="../sync.js"></script>', html, mid)
            # 順序：course.js 要先於 sync.js（sync.js 依賴 NotesCourse）
            self.assertLess(html.index('course.js'), html.index('sync.js'), mid)
        self.assertTrue((out / 'sync.js').exists())
        home = (out / 'index.html').read_text(encoding='utf-8')
        self.assertNotIn('firebasejs', home)

    def test_placeholder_never_leaks(self):
        for out in (build_variant(None), build_variant(self.CFG)):
            for page in out.rglob('*.html'):
                self.assertNotIn('__SYNC__', page.read_text(encoding='utf-8'), str(page))


if __name__ == '__main__':
    unittest.main()
