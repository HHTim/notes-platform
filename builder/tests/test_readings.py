# -*- coding: utf-8 -*-
# 讀音比對程式的純函式部分；真的斷詞要裝 SudachiPy，這裡用假的讀音函式，不用裝
import sys, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'builder' / 'tools'))
import check_readings as cr


class TestReadings(unittest.TestCase):
    def test_units_split_base_and_reading(self):
        u = cr.units('<p>中文</p>\n<p lang="ja"><ruby>食<rt>た</rt></ruby>べる</p>')
        self.assertEqual(u, [(2, '食べる', 'たべる')])

    def test_hira_and_strip_symbols(self):
        self.assertEqual(cr.hira('コーヒー（　　）を、ください。'), 'こーひーをください')

    def test_compare_reports_mismatch_only(self):
        u = [(1, '私です', 'わたしです'), (2, '学生', 'がくせ')]
        fake = {'私です': 'ワタシデス', '学生': 'ガクセイ'}.get
        self.assertEqual(cr.compare(u, fake), [(2, '学生', 'がくせ', 'がくせい')])
