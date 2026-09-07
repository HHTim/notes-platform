# -*- coding: utf-8 -*-
# content/ 的格式檢查：檔案齊全、來源註記、不含樣式、換色乾淨、測驗格式
import json, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / 'content'


def load_modules():
    site = json.loads((CONTENT / 'modules.json').read_text(encoding='utf-8'))
    mods = []
    for entry in site['modules']:
        mod = json.loads((CONTENT / entry['id'] / 'module.json').read_text(encoding='utf-8'))
        mod['id'] = entry['id']
        mods.append(mod)
    return site, mods


class TestContent(unittest.TestCase):
    def test_modules_json(self):
        site, mods = load_modules()
        self.assertTrue(site['site_title'])
        for mod in mods:
            for key in ('title', 'intro', 'kick', 'overview_intro', 'footer_note', 'lessons'):
                self.assertIn(key, mod, mod['id'])

    def test_lesson_files(self):
        _, mods = load_modules()
        for mod in mods:
            for L in mod['lessons']:
                ldir = CONTENT / mod['id'] / L['dir']
                html = (ldir / 'lesson.html').read_text(encoding='utf-8')
                with self.subTest(lesson=str(ldir)):
                    self.assertTrue(html.startswith('<!-- 來源：'), '第一行要是來源註解')
                    self.assertNotIn('<style', html, '內容檔不准帶樣式')
                    for old in ('var(--teal', 'var(--amber', 'var(--brass'):
                        self.assertNotIn(old, html, '換色沒換乾淨：' + old)
                    self.assertIn('class="learn"', html)
                    self.assertIn('class="keys"', html)
                    self.assertTrue((ldir / 'quiz.json').exists())

    def test_quiz_format(self):
        _, mods = load_modules()
        for mod in mods:
            for L in mod['lessons']:
                qf = CONTENT / mod['id'] / L['dir'] / 'quiz.json'
                qs = json.loads(qf.read_text(encoding='utf-8'))['questions']
                with self.subTest(lesson=str(qf)):
                    # 任務 3 補完題後把下限改成 5（規格：每課 5〜10 題）
                    self.assertTrue(3 <= len(qs) <= 10, '目前 %d 題' % len(qs))
                    for q in qs:
                        self.assertTrue(q['q'].strip())
                        self.assertTrue(q['exp'].strip())
                        self.assertGreaterEqual(len(q['opts']), 3)
                        self.assertTrue(all(o.strip() for o in q['opts']))

    def test_k8s_migration_details(self):
        _, mods = load_modules()
        k8s = [m for m in mods if m['id'] == 'k8s'][0]
        self.assertEqual(len(k8s['lessons']), 13)
        read = lambda d: (CONTENT / 'k8s' / d / 'lesson.html').read_text(encoding='utf-8')
        # 修字有帶到、圖有搬對位子（對應 rescue/build_spa.py 的加工）
        self.assertIn('第 9 課要講的 Service 背後的執行者', read('07-cluster-brain'))
        self.assertIn('（v1.24，2022 年）', read('06-pod-node'))
        self.assertIn('Gateway API', read('10-ingress'))
        self.assertIn('Kubernetes 的核心迴圈', read('05-why-k8s'))
        self.assertNotIn('Kubernetes 的核心迴圈', read('08-deployment'))
        self.assertIn('ReplicaSet', read('08-deployment'))


if __name__ == '__main__':
    unittest.main()
