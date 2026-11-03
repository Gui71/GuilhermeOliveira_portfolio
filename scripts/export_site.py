"""Exporta apenas arquivos públicos aprovados para um diretório NOVO."""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_FILES = (
    'index.html', 'styles.css', 'script.js',
    'img/Guilherme.jpeg', 'img/favicon.ico', 'img/favicon-16x16.png',
    'img/favicon-32x32.png', 'img/apple-touch-icon.png',
    'img/android-chrome-192x192.png', 'img/android-chrome-512x512.png',
    'img/site.webmanifest',
)

def export(destination):
    destination = Path(destination).resolve()
    # Não sobrescrever um checkout, exportação antiga ou diretório do usuário.
    destination.mkdir(parents=True, exist_ok=False)
    for name in PUBLIC_FILES:
        source = ROOT / name
        if source.is_symlink():
            raise ValueError(f'Link simbólico não permitido: {name}')
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    print(f'Exportados {len(PUBLIC_FILES)} arquivos públicos para {destination}')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Uso: python3 scripts/export_site.py DIRETORIO_NOVO')
    export(sys.argv[1])
