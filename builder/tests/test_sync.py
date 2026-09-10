# -*- coding: utf-8 -*-
# sync.js 的檢查：語法正確、合併規則符合規格。用 node 跑；沒裝 node 就跳過。
import shutil, subprocess, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


@unittest.skipUnless(shutil.which('node'), '沒裝 node，跳過 JavaScript 檢查')
class TestSyncJs(unittest.TestCase):
    def test_syntax(self):
        subprocess.run(['node', '--check', str(ROOT / 'builder' / 'templates' / 'sync.js')],
                       check=True)

    def test_merge_rules(self):
        r = subprocess.run(['node', str(ROOT / 'builder' / 'tests' / 'test_merge.js')],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
