# -*- coding: utf-8 -*-
# 讀 content/ 全部，組出整個平台到 dist/（每次整站重建，不做增量）
import json, re, shutil
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# 不需要關閉標籤的元素（HTML 規格叫 void 元素），配對檢查時跳過
VOID_TAGS = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
             'link', 'meta', 'param', 'source', 'track', 'wbr'}


class TagBalanceChecker(HTMLParser):
    """開閉標籤要一一配對。多一個 </article> 會把該課的測驗、導覽擠到文章外面，瀏覽器不會報錯，
    所以在建置時抓。錯誤存在 self.errors，每筆是一句人看得懂的話。"""

    def __init__(self):
        super().__init__()
        self.stack = []      # 還沒關閉的 (標籤名, 行號)
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID_TAGS:
            self.stack.append((tag, self.getpos()[0]))

    def handle_startendtag(self, tag, attrs):
        pass   # <path/> 這種自己關閉的寫法，開與閉在同一處，不上堆疊

    def handle_endtag(self, tag):
        if tag in VOID_TAGS:
            return
        line = self.getpos()[0]
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()
        elif self.stack:
            self.errors.append('第 %d 行的 </%s> 對不上——此時還沒關閉的是第 %d 行的 <%s>'
                               % (line, tag, self.stack[-1][1], self.stack[-1][0]))
        else:
            self.errors.append('第 %d 行的 </%s> 沒有對應的開頭標籤' % (line, tag))

    def close(self):
        super().close()
        for tag, line in self.stack:
            self.errors.append('第 %d 行的 <%s> 沒有關閉' % (line, tag))


def check_tag_balance(html, where):
    """where 是給人看的位置，例如 k8s/07-cluster-brain/lesson.html。不平衡就中止建置。"""
    p = TagBalanceChecker()
    p.feed(html)
    p.close()
    if p.errors:
        raise SystemExit('建置中止：%s 的標籤沒配對\n  ' % where + '\n  '.join(p.errors))


class DrillChecker(HTMLParser):
    """課中練習 <div class="drill">：選項在 <ul class="dopts"> 的 <li>，正解那個帶 data-ok，
    解析是 <p class="dexp">。正解不是剛好一個、沒有解析、選項不是 2〜5 個，就記一筆錯誤。"""

    def __init__(self):
        super().__init__()
        self.errors = []
        self.depth = 0       # 進到 drill 之後的 div 層數；0 表示不在 drill 裡
        self.cur = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        classes = (a.get('class') or '').split()
        if tag == 'div' and self.depth == 0 and 'drill' in classes:
            self.depth = 1
            self.cur = {'line': self.getpos()[0], 'opts': 0, 'ok': 0, 'exp': False}
            return
        if self.depth == 0:
            return
        if tag == 'div':
            self.depth += 1
        elif tag == 'li':
            self.cur['opts'] += 1
            if 'data-ok' in a:
                self.cur['ok'] += 1
        elif tag == 'p' and 'dexp' in classes:
            self.cur['exp'] = True

    def handle_endtag(self, tag):
        if self.depth and tag == 'div':
            self.depth -= 1
            if self.depth == 0:
                d = self.cur
                if d['ok'] != 1:
                    self.errors.append('第 %d 行的練習題正解有 %d 個，要剛好 1 個（在那個 <li> 加 data-ok）'
                                       % (d['line'], d['ok']))
                if not d['exp']:
                    self.errors.append('第 %d 行的練習題沒有解析（<p class="dexp">）' % d['line'])
                if not 2 <= d['opts'] <= 5:
                    self.errors.append('第 %d 行的練習題有 %d 個選項，要 2〜5 個' % (d['line'], d['opts']))


def drill_errors(html):
    p = DrillChecker()
    p.feed(html)
    p.close()
    return p.errors


def load_templates(tpl_dir):
    names = ('style.css', 'course.js', 'sync.js', 'module.html', 'home.html', 'favicon.svg')
    return {n: (tpl_dir / n).read_text(encoding='utf-8') for n in names if (tpl_dir / n).exists()}


SLUG_RE = re.compile(r'^[a-z0-9-]+$')   # 要跟 course.js 的路由 /^#\/lesson\/([a-z0-9-]+)$/ 一致


def check_slugs(mods):
    """slug 全站唯一、只含小寫英數與連字號。撞名會讓頁面裡的 QUIZ 字典後者蓋前者；
    不合法的 slug 路由不認，那一課永遠開不到。不合就中止建置並說是哪幾課。"""
    seen = {}
    errors = []
    for mod in mods:
        for L in mod['lessons']:
            where = '%s/%s' % (mod['id'], L['dir'])
            slug = L['slug']
            if not SLUG_RE.match(slug):
                errors.append('%s 的 slug「%s」不合法：只能用小寫英文字母、數字、連字號' % (where, slug))
            if slug in seen:
                errors.append('%s 與 %s 的 slug 撞名，都叫「%s」' % (seen[slug], where, slug))
            else:
                seen[slug] = where
    if errors:
        raise SystemExit('建置中止：課程 slug 有問題\n  ' + '\n  '.join(errors))


def load_site(content_dir):
    site = json.loads((content_dir / 'modules.json').read_text(encoding='utf-8'))
    mods = []
    for entry in site['modules']:
        mdir = content_dir / entry['id']
        mod = json.loads((mdir / 'module.json').read_text(encoding='utf-8'))
        mod['id'], mod['icon'] = entry['id'], entry['icon']
        for L in mod['lessons']:
            ldir = mdir / L['dir']
            L['html'] = (ldir / 'lesson.html').read_text(encoding='utf-8')
            check_tag_balance(L['html'], '%s/%s/lesson.html' % (entry['id'], L['dir']))
            errs = drill_errors(L['html'])
            if errs:
                raise SystemExit('建置中止：%s/%s/lesson.html 的課中練習有問題\n  ' % (entry['id'], L['dir'])
                                 + '\n  '.join(errs))
            L['quiz'] = json.loads((ldir / 'quiz.json').read_text(encoding='utf-8'))['questions']
            L['assets'] = ldir / 'assets'
        mods.append(mod)
    check_slugs(mods)
    fb = content_dir / 'firebase.json'
    site['firebase'] = json.loads(fb.read_text(encoding='utf-8')) if fb.exists() else None
    return site, mods


def sidebar_html(mod):
    out = ['  <a href="#/" data-nav="ov" class="ov">📖&nbsp; 課綱總覽</a>\n']
    group = None
    for i, L in enumerate(mod['lessons']):
        if L.get('group') and L['group'] != group:
            group = L['group']
            out.append('  <div class="group">%s</div>\n' % group)
        out.append('  <a href="#/lesson/%s" data-nav="%s"><span class="n">%d.</span>'
                   '<span>%s</span><span class="tick" data-tick hidden>✓</span></a>\n'
                   % (L['slug'], L['slug'], i + 1, L['title']))
    return ''.join(out)


def intro_html(intro):
    """總覽開場：一個字串是一段；陣列裡的字串各成一段，巢狀陣列變成列點。"""
    if isinstance(intro, str):
        intro = [intro]
    out = []
    for block in intro:
        if isinstance(block, list):
            out.append('<ul class="ov-points">\n%s</ul>\n' % ''.join('<li>%s</li>\n' % x for x in block))
        else:
            out.append('<p>%s</p>\n' % block)
    return ''.join(out)


def overview_html(mod):
    o = ['<article id="pg-ov">\n<div class="ov-hero">\n<p class="kick">%s</p>\n<h1>%s</h1>\n'
         % (mod['kick'], mod['title'])]
    o.append(intro_html(mod['overview_intro']))
    o.append('<p class="ov-progress" id="ovProgress"></p>\n</div>\n<div class="lesson-list">\n')
    for i, L in enumerate(mod['lessons']):
        o.append('<a href="#/lesson/%s"><span class="n">%d</span><span class="tt"><b>%s</b>'
                 '<span>%s</span></span><span class="done" data-ovtick="%s" hidden>✓</span>'
                 '<span class="mins">%d 分</span></a>\n'
                 % (L['slug'], i + 1, L['title'], L['desc'], L['slug'], L['mins']))
    o.append('</div>\n<footer class="site">%s</footer>\n</article>\n' % mod['footer_note'])
    return ''.join(o)


def article_html(mod, i, L):
    N = len(mod['lessons'])
    a = ['<article id="pg-%s" hidden>\n' % L['slug']]
    a.append('<p class="crumb"><a href="#/">課綱總覽</a> › 第 %d 課 / 共 %d 課</p>\n' % (i + 1, N))
    a.append('<h1 class="lt">%s</h1>\n' % L['title'])
    a.append('<div class="meta"><span class="chip g">第 %d 課 / 共 %d 課</span>'
             '<span class="chip">約 %d 分鐘</span></div>\n' % (i + 1, N, L['mins']))
    a.append('<p class="sub">%s</p>\n' % L['desc'])
    a.append(L['html'] + '\n')   # 「讀完這課你會」框、內文、「重點整理」框都在 lesson.html 裡
    a.append('<div class="quiz" data-quiz="%s"></div>\n' % L['slug'])
    a.append('<nav class="pager">')
    if i > 0:
        P = mod['lessons'][i - 1]
        a.append('<a href="#/lesson/%s"><span class="dir">← 上一課</span><span class="t">%s</span></a>'
                 % (P['slug'], P['title']))
    if i < N - 1:
        Nx = mod['lessons'][i + 1]
        a.append('<a class="next" href="#/lesson/%s"><span class="dir">下一課 →</span>'
                 '<span class="t">%s</span></a>' % (Nx['slug'], Nx['title']))
    else:
        a.append('<a class="next" href="#/"><span class="dir">回到</span><span class="t">課綱總覽</span></a>')
    a.append('</nav>\n</article>\n')
    return ''.join(a)


def modsel_html(mods, current_id):
    return ''.join('<option value="%s"%s>%s %s</option>'
                   % (m['id'], ' selected' if m['id'] == current_id else '', m['icon'], m['title'])
                   for m in mods)


def sync_html(firebase, prefix):
    """登入同步那一段 <script>：Firebase 設定＋SDK＋sync.js。首頁與模組頁都用，差在 sync.js 的相對路徑。
    沒有 content/firebase.json 就整段不放（規格：同步是可選功能）。"""
    if not firebase:
        return ''
    sdk = 'https://www.gstatic.com/firebasejs/10.14.1/firebase-%s-compat.js'
    return ('<script>var FIREBASE_CONFIG=%s;</script>\n' % json.dumps(firebase).replace('</', '<\\/')
            + ''.join('<script src="%s"></script>\n' % (sdk % part) for part in ('app', 'auth', 'firestore'))
            + '<script src="%ssync.js"></script>' % prefix)


def render_module_page(mod, mods, tpl, firebase=None):
    quiz = {L['slug']: L['quiz'] for L in mod['lessons']}
    slugs = [L['slug'] for L in mod['lessons']]
    data = ('var MODULE=%s;\nvar QUIZ=%s;\nvar SLUGS=%s;'
            % (json.dumps(mod['id']), json.dumps(quiz, ensure_ascii=False),
               json.dumps(slugs, ensure_ascii=False)))
    data = data.replace('</', '<\\/')   # 防護：測驗文字若含 </ 之類的字，不會提前把嵌入的 <script> 截斷
    sync = sync_html(firebase, '../')
    arts = [overview_html(mod)] + [article_html(mod, i, L) for i, L in enumerate(mod['lessons'])]
    page = tpl['module.html']
    for key, val in (('__TITLE__', mod['title']), ('__MODSEL__', modsel_html(mods, mod['id'])),
                     ('__SIDEBAR__', sidebar_html(mod)), ('__ARTICLES__', ''.join(arts)),
                     ('__DATA__', data), ('__SYNC__', sync)):
        page = page.replace(key, val)
    return page


def render_home_page(site, mods, tpl, firebase=None):
    side = ''.join('  <a href="%s/"><span class="n">%s</span><span>%s</span></a>\n'
                   % (m['id'], m['icon'], m['title']) for m in mods)
    cards = ''.join(
        '<a class="mod-card" href="%s/"><span class="icon">%s</span><b>%s</b>'
        '<span>%s</span><span class="stats"><span data-stat="%s"></span> · 共 %d 課</span></a>\n'
        % (m['id'], m['icon'], m['title'], m['intro'], m['id'], len(m['lessons']))
        for m in mods)
    mods_js = json.dumps([{'id': m['id'], 'count': len(m['lessons'])} for m in mods],
                         ensure_ascii=False)
    page = tpl['home.html']
    for key, val in (('__SITE_TITLE__', site['site_title']), ('__SITE_INTRO__', site['site_intro']),
                     ('__SIDEBAR__', side), ('__CARDS__', cards), ('__MODS__', mods_js),
                     ('__SYNC__', sync_html(firebase, ''))):
        page = page.replace(key, val)
    return page


def build(content_dir=None, tpl_dir=None, out_dir=None):
    content_dir = content_dir or ROOT / 'content'
    tpl_dir = tpl_dir or ROOT / 'builder' / 'templates'
    out_dir = out_dir or ROOT / 'dist'
    site, mods = load_site(content_dir)
    tpl = load_templates(tpl_dir)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    (out_dir / 'style.css').write_text(tpl['style.css'], encoding='utf-8')
    (out_dir / 'course.js').write_text(tpl['course.js'], encoding='utf-8')
    (out_dir / 'favicon.svg').write_text(tpl['favicon.svg'], encoding='utf-8')   # 網站圖示：分頁、書籤、手機主畫面都用它
    if site['firebase']:
        (out_dir / 'sync.js').write_text(tpl['sync.js'], encoding='utf-8')
    (out_dir / 'index.html').write_text(render_home_page(site, mods, tpl, site['firebase']), encoding='utf-8')
    for mod in mods:
        d = out_dir / mod['id']
        d.mkdir()
        (d / 'index.html').write_text(render_module_page(mod, mods, tpl, site['firebase']),
                                      encoding='utf-8')
        for L in mod['lessons']:
            if L['assets'].is_dir():   # 規格：每課的圖放自己的 assets/；建置時搬到 assets/<課資料夾>/
                shutil.copytree(L['assets'], d / 'assets' / L['dir'])
    print('built →', out_dir)


if __name__ == '__main__':
    build()
