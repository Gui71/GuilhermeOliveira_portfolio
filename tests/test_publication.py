"""Valida a fronteira entre arquivos locais e publicação estática."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class PublicationTest(unittest.TestCase):
    def test_export_contains_only_approved_public_files(self):
        with tempfile.TemporaryDirectory() as temp:
            dest = Path(temp) / 'site'
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/export_site.py'), str(dest)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            files = {str(p.relative_to(dest)) for p in dest.rglob('*') if p.is_file()}
            self.assertIn('index.html', files)
            self.assertIn('img/Guilherme.jpeg', files)
            self.assertIn('script.js', files)
            self.assertFalse(any(p.startswith(('video/', 'curriculo_referencia/', '.git/', '.codex/')) for p in files))
            self.assertFalse(any(p.endswith(('.md', '.docx', '.pdf', '.mp4')) for p in files))
            self.assertNotIn('img/sorteio2.png', files)
            self.assertNotIn('img/portfolio-prev.png', files)

if __name__ == '__main__':
    unittest.main()
