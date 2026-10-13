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
        for name in ('index.html', 'style.css', 'course.js', 'favicon.svg'):
            self.assertTrue((self.out / name).exists(), name)
        for mod in self.mods:
            self.assertTrue((self.out / mod['id'] / 'index.html').exists(), mod['id'])

    def test_module_page_k8s(self):
        html = (self.out / 'k8s' / 'index.html').read_text(encoding='utf-8')
        k8s = [m for m in self.mods if m['id'] == 'k8s'][0]
        # 側邊欄：總覽 + 錯題區 + 每課
        self.assertEqual(html.count('data-nav='), len(k8s['lessons']) + 2)
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
        self.assertIn('<link rel="icon" type="image/svg+xml" href="../favicon.svg">', html)
        self.assertIn('../course.js', html)
        # 頂欄：回首頁連結與模組下拉選單，選單有全部模組
        self.assertIn('href="../"', html)
        self.assertEqual(html.count('<option'), len(self.mods))
        # 每課的小節目錄與側欄小節都在；錯題區頁殼在
        for L in k8s['lessons']:
            self.assertIn('data-subs="%s"' % L['slug'], html)
            self.assertIn('data-goto="%s-quiz"' % L['slug'], html)
        self.assertIn('<article id="pg-wrong" hidden>', html)

    def test_no_company_terms(self):
        for page in self.out.rglob('*.html'):
            text_lower = page.read_text(encoding='utf-8').lower()
            self.assertNotIn('kpi', text_lower, str(page))

    def test_progress_key_per_module(self):
        js = (self.out / 'course.js').read_text(encoding='utf-8')
        self.assertIn("'notes-progress:'+MODULE", js)
        self.assertNotIn('k8s-course-done', js)

    def test_sidebar_progress_and_hint(self):
        for mid in ('k8s', 'database'):
            html = (self.out / mid / 'index.html').read_text(encoding='utf-8')
            self.assertIn('id="sideProg"', html, mid)
            self.assertIn('id="syncHint"', html, mid)
            self.assertIn('進度只存在這台裝置', html, mid)

    def test_course_js_hooks(self):
        js = (self.out / 'course.js').read_text(encoding='utf-8')
        self.assertIn('window.NotesCourse', js)
        self.assertIn('notes:progress-saved', js)
        self.assertIn('sideProg', js)
        for s in ('NotesQuiz.afterQuiz', 'NotesQuiz.afterPractice', 'NotesQuiz.remove', 'NotesQuiz.active',
                  "'#/wrong'", 'data-goto', 'IntersectionObserver', '_last'):
            self.assertIn(s, js, s)

    def test_home_page(self):
        html = (self.out / 'index.html').read_text(encoding='utf-8')
        self.assertIn(self.site['site_title'], html)
        for mod in self.mods:
            self.assertIn('href="%s/"' % mod['id'], html)
            self.assertIn('<use href="#ic-%s"/>' % mod['icon'], html)
            self.assertIn(mod['title'], html)
            self.assertIn('data-stat="%s"' % mod['id'], html)
            self.assertIn('共 %d 課' % len(mod['lessons']), html)
        self.assertIn('style.css', html)
        self.assertIn('<link rel="icon" type="image/svg+xml" href="favicon.svg">', html)
        self.assertIn('viewport', html)

    EMOJI = re.compile('[\U0001F300-\U0001FAFF\u2600-\u27BF\U0001F1E6-\U0001F1FF]')

    def test_no_emoji_in_templates_and_chrome(self):
        """樣板、建置工具、首頁、模組頁的外殼（去掉課文）都不能有 emoji 或 ✓ ✗ ☰ 這類符號"""
        for f in (ROOT / 'builder' / 'templates').iterdir():
            self.assertIsNone(self.EMOJI.search(f.read_text(encoding='utf-8')), f.name)
        self.assertIsNone(self.EMOJI.search((ROOT / 'builder' / 'build.py').read_text(encoding='utf-8')))
        self.assertIsNone(self.EMOJI.search((self.out / 'index.html').read_text(encoding='utf-8')))
        shell = re.sub(r'<article id="pg-[a-z0-9-]+".*?</article>', '',
                       (self.out / 'english' / 'index.html').read_text(encoding='utf-8'), flags=re.S)
        self.assertIsNone(self.EMOJI.search(shell))

    def test_new_palette_only(self):
        css = (self.out / 'style.css').read_text(encoding='utf-8')
        css = re.sub(r'\[(?:fill|stroke)="#[0-9A-Fa-f]{6}"\]', '', css)   # 示意圖對應規則的選擇器要寫出舊色號才抓得到，不算使用
        for old in ('#F7F0E3', '#B5730F', '#5E7A9B', 'Chivo'):
            self.assertNotIn(old, css, old)
        for new in ('#233831', '#DEE5DD', '#A9D9C7', '#C5E0D7', '#F29F80', '#F2CEAE', '#FBC580'):
            self.assertIn(new, css, new)
        for page in ('index.html', 'english/index.html'):
            self.assertNotIn('Chivo', (self.out / page).read_text(encoding='utf-8'), page)

    def test_formula_wraps_readably(self):
        """公式／流程那一行很多課都很長（最長三百多字），等寬字太寬會在句子中間斷行，要用一般字、靠左"""
        css = (self.out / 'style.css').read_text(encoding='utf-8')
        rule = re.search(r'p\.formula\{[^}]*\}', css).group(0)
        self.assertNotIn('var(--mono)', rule)
        self.assertIn('text-align:left', rule)

    def test_every_css_variable_used_in_content_is_defined(self):
        """課文的示意圖用 var(--名稱) 上色；樣式檔沒定義的名稱會讓圖整塊變黑（2026-10-13 改版踩過）"""
        css = (self.out / 'style.css').read_text(encoding='utf-8')
        defined = set(re.findall(r'(--[a-z0-9-]+)\s*:', css))
        used = set()
        for f in (ROOT / 'content').rglob('lesson.html'):
            html = re.sub(r'<pre.*?</pre>|<code>.*?</code>', '', f.read_text(encoding='utf-8'), flags=re.S)   # 程式碼範例裡的字不算
            used |= set(re.findall(r'var\((--[a-z0-9-]+)', html))
        self.assertEqual(sorted(used - defined), [])

    def test_dark_theme_overrides_every_color(self):
        """暗色要把亮色定義的每個顏色變數都換掉，漏一個就會出現亮底白字這種看不到的組合"""
        css = (self.out / 'style.css').read_text(encoding='utf-8')
        light = re.search(r':root\{(.*?)\}', css, re.S).group(1)
        colors = set(re.findall(r'(--[a-z0-9-]+):#', light))
        dark = re.search(r':root\[data-theme="dark"\]\{(.*?)\}', css, re.S)
        self.assertIsNotNone(dark)
        self.assertEqual(sorted(colors - set(re.findall(r'(--[a-z0-9-]+):', dark.group(1)))), [])
        # 規則裡不能再寫死白字，要用 --on-ink（深色按鈕上的字）
        rules = css[css.index('}') + 1:]
        # 答對、答錯選項的字母圓點底色是亮的薄荷、桃橘，字要用深色
        self.assertIn('.opt.right .l,.dopts li.right .l{background:var(--mint);color:var(--on-ink)}', css)
        self.assertNotIn('color:#FFFFFF', rules)

    def test_figures_hardcoded_old_colors_are_remapped(self):
        """課文示意圖裡寫死的舊配色（白底、古銅、灰藍、舊墨色），樣式要逐一改成新色系的變數"""
        css = (self.out / 'style.css').read_text(encoding='utf-8')
        found = set()
        for f in (ROOT / 'content').rglob('lesson.html'):
            found |= set(re.findall(r'((?:fill|stroke)="#[0-9A-Fa-f]{6}")', f.read_text(encoding='utf-8')))
        for attr in found:
            self.assertIn('figure svg [%s]' % attr, css, attr)

    def test_theme_switch_fades(self):
        """按開關時顏色要漸變（Tim：不然眼睛不舒服）；只在切換那一下，開頁不漸變；系統要求減少動態效果時不漸變"""
        css = (self.out / 'style.css').read_text(encoding='utf-8')
        rule = re.search(r'\.theme-fade[^{]*\{[^}]*\}', css)
        self.assertIsNotNone(rule)
        for prop in ('background-color', 'color', 'border-color', 'fill', 'stroke'):
            self.assertIn(prop, rule.group(0))
        self.assertRegex(css, r'prefers-reduced-motion:reduce\)\{[^}]*\.theme-fade')
        js = (self.out / 'theme.js').read_text(encoding='utf-8')
        self.assertIn("classList.add('theme-fade')", js)
        self.assertIn("classList.remove('theme-fade')", js)

    def test_theme_toggle_on_every_page(self):
        self.assertTrue((self.out / 'theme.js').exists())
        for page, src in (('index.html', 'theme.js'), ('english/index.html', '../theme.js')):
            html = (self.out / page).read_text(encoding='utf-8')
            head = html[:html.index('</head>')]
            self.assertIn('<script src="%s"></script>' % src, head, page)   # 放在 head，開頁不會先閃一下亮色
            self.assertIn('id="themeBtn"', html, page)
        icons = (ROOT / 'builder' / 'templates' / 'icons.svg').read_text(encoding='utf-8')
        for name in ('ic-moon', 'ic-sun'):
            self.assertIn('<symbol id="%s"' % name, icons)

    def test_hidden_attribute_wins_over_display(self):
        """成績卡、按鈕列這些用 display:flex 的元素，加了 hidden 也要真的消失"""
        css = (self.out / 'style.css').read_text(encoding='utf-8')
        self.assertIn('[hidden]{display:none!important}', css)

    def test_home_resume_and_cards(self):
        html = (self.out / 'index.html').read_text(encoding='utf-8')
        for i in ('id="resume"', 'id="resumeIcon"', 'id="resumeMod"', 'id="resumeLesson"'):
            self.assertIn(i, html, i)
        for mod in self.mods:
            self.assertIn('data-card="%s"' % mod['id'], html)
            self.assertIn('data-bar="%s"' % mod['id'], html)
        self.assertNotIn(self.site['site_intro'], html)   # 長介紹不再放首頁

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
        for page in ('k8s/index.html', 'index.html'):
            html = (out / page).read_text(encoding='utf-8')
            self.assertNotIn('firebasejs', html, page)
            self.assertNotIn('FIREBASE_CONFIG', html, page)
            self.assertNotIn('sync.js', html, page)
        self.assertFalse((out / 'sync.js').exists())

    def test_on_with_config(self):
        out = build_variant(self.CFG)
        for mid in ('k8s', 'database'):
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
        # 首頁也要能登入登出：同一段 SDK，sync.js 走同層路徑；且要在首頁自己的 script（開 NotesHome 掛勾）之後
        home = (out / 'index.html').read_text(encoding='utf-8')
        self.assertIn('var FIREBASE_CONFIG=', home)
        self.assertIn('<script src="sync.js"></script>', home)
        self.assertIn('id="syncHint"', home)
        self.assertLess(home.index('window.NotesHome='), home.index('<script src="sync.js">'))

    def test_placeholder_never_leaks(self):
        for out in (build_variant(None), build_variant(self.CFG)):
            for page in out.rglob('*.html'):
                self.assertNotIn('__SYNC__', page.read_text(encoding='utf-8'), str(page))


if __name__ == '__main__':
    unittest.main()
