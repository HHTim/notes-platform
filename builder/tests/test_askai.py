# -*- coding: utf-8 -*-
# askai.js 的檢查：語法正確、純函式符合規格。用 node 跑；沒裝 node 就跳過。
import shutil, subprocess, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


@unittest.skipUnless(shutil.which('node'), '沒裝 node，跳過 JavaScript 檢查')
class TestAskAiJs(unittest.TestCase):
    def test_syntax(self):
        subprocess.run(['node', '--check', str(ROOT / 'builder' / 'templates' / 'askai.js')], check=True)

    def test_pure_functions(self):
        r = subprocess.run(['node', str(ROOT / 'builder' / 'tests' / 'test_askai.js')],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        # 非同步測試卡住時 node 會安靜結束、回 0；一定要看到最後那行才算跑完
        self.assertIn('問 AI 純函式測試全部通過', r.stdout, '測試沒有跑到最後')


if __name__ == '__main__':
    unittest.main()
