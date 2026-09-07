# -*- coding: utf-8 -*-
# 讀 content/ 全部，組出整個平台到 dist/（每次整站重建，不做增量）
import json, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_templates(tpl_dir):
    names = ('style.css', 'course.js', 'module.html', 'home.html')
    return {n: (tpl_dir / n).read_text(encoding='utf-8') for n in names if (tpl_dir / n).exists()}


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
            L['quiz'] = json.loads((ldir / 'quiz.json').read_text(encoding='utf-8'))['questions']
            L['assets'] = ldir / 'assets'
        mods.append(mod)
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


def overview_html(mod):
    o = ['<article id="pg-ov">\n<div class="ov-hero">\n<p class="kick">%s</p>\n<h1>%s</h1>\n'
         % (mod['kick'], mod['title'])]
    o.append('<p>%s</p>\n' % mod['overview_intro'])
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


def render_module_page(mod, mods, tpl):
    quiz = {L['slug']: L['quiz'] for L in mod['lessons']}
    slugs = [L['slug'] for L in mod['lessons']]
    data = ('var MODULE=%s;\nvar QUIZ=%s;\nvar SLUGS=%s;'
            % (json.dumps(mod['id']), json.dumps(quiz, ensure_ascii=False),
               json.dumps(slugs, ensure_ascii=False)))
    data = data.replace('</', '<\\/')   # 防護：測驗文字若含 </ 之類的字，不會提前把嵌入的 <script> 截斷
    arts = [overview_html(mod)] + [article_html(mod, i, L) for i, L in enumerate(mod['lessons'])]
    page = tpl['module.html']
    for key, val in (('__TITLE__', mod['title']), ('__MODSEL__', modsel_html(mods, mod['id'])),
                     ('__SIDEBAR__', sidebar_html(mod)), ('__ARTICLES__', ''.join(arts)),
                     ('__DATA__', data)):
        page = page.replace(key, val)
    return page


def render_home_page(site, mods, tpl):
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
                     ('__SIDEBAR__', side), ('__CARDS__', cards), ('__MODS__', mods_js)):
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
    (out_dir / 'index.html').write_text(render_home_page(site, mods, tpl), encoding='utf-8')
    for mod in mods:
        d = out_dir / mod['id']
        d.mkdir()
        (d / 'index.html').write_text(render_module_page(mod, mods, tpl), encoding='utf-8')
        for L in mod['lessons']:
            if L['assets'].is_dir():   # 規格：每課的圖放自己的 assets/；建置時搬到 assets/<課資料夾>/
                shutil.copytree(L['assets'], d / 'assets' / L['dir'])
    print('built →', out_dir)


if __name__ == '__main__':
    build()
