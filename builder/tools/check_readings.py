#!/usr/bin/env python3
"""審查用：把日文模組裡我們標的讀音，跟 SudachiPy（日文斷詞程式，會把句子切成詞並查出讀音）比對。
不是建置的一部分。對不上不一定是我們錯（例如「私」辭典讀わたくし），要逐條人工確認。
需要 SudachiPy；這台電腦的系統 Python 不給直接 pip install，裝在獨立環境：
  python3 -m venv ~/.cache/notes-sudachi && ~/.cache/notes-sudachi/bin/pip install sudachipy sudachidict_core
  ~/.cache/notes-sudachi/bin/python builder/tools/check_readings.py <課的資料夾>"""
import json, re, sys
from html.parser import HTMLParser
from pathlib import Path

VOID = {'br', 'img', 'wbr', 'hr', 'input', 'meta', 'link', 'source'}


class _Units(HTMLParser):
    """每個最外層 lang="ja" 元素收成一句：(行號, 原文, 讀音版)。原文去掉 <rt>；讀音版把 <ruby> 換成 <rt> 的假名。"""

    def __init__(self):
        super().__init__()
        self.stack, self.out, self.cur = [], [], None   # stack 每層 (tag, 是日文, 在 ruby 裡, 在 rt 裡)

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        ja, ruby, rt = self.stack[-1][1:] if self.stack else (False, False, False)
        lang = dict(attrs).get('lang')
        if lang is not None:
            ja = lang.lower().startswith('ja')
        if tag == 'li' and self.cur is not None:      # 選項清單：每個選項各算一句
            if self.cur[1]:
                self.out.append((self.cur[0], self.cur[1], self.cur[2]))
            self.cur = None
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
    """片假名轉平假名，只留平假名與長音「ー」（標點、空格、括號都拿掉）"""
    s = ''.join(chr(ord(c) - 0x60) if 'ァ' <= c <= 'ヶ' else c for c in s)
    return re.sub(r'[^ぁ-ゖー]', '', s)


def clean(text):
    """送進斷詞程式前拿掉英文字母、符號與空格（數字留著，「3人」要讀成さんにん）：程式會把 Ａ、〜、／ 讀成「きごう」，跟我們的讀音對不上"""
    return re.sub(r'[A-Za-zＡ-Ｚａ-ｚ〜～／/：:→←＿★（）()「」『』、。？！…・\s　]', '', text)


def compare(us, read_fn):
    bad = []
    for line, plain, ours in us:
        theirs = hira(read_fn(plain))
        if hira(ours) != theirs:
            bad.append((line, plain, hira(ours), theirs))
    return bad


# 斷詞辭典的讀法跟日常／教材的讀法不同、但我們的標法是對的：照詞覆蓋，免得每句都被列出來。
# 林＝課裡的台灣人姓，音讀りん（日本姓はやし不會出現在課裡）。
USUAL = {'私': 'わたし', '林': 'りん', '日本': 'にほん', '明日': 'あした'}


def sudachi_reader():
    from sudachipy import dictionary, tokenizer
    tok = dictionary.Dictionary().create() if not hasattr(dictionary.Dictionary, "tokenizer") else dictionary.Dictionary().tokenizer()
    mode = tokenizer.Tokenizer.SplitMode.C
    return lambda text: ''.join(USUAL.get(m.surface(), m.reading_form()) for m in (tok.tokenize(clean(text), mode) if clean(text) else []))


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
