#!/usr/bin/env bash
# Remonta a base (dados/data.json) a partir dos PDFs em fontes/ e gera o index.html.
# Precisa de: pdftotext (poppler-utils), python3 e pdfplumber (pip install pdfplumber).
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p dados
cd dados
pdftotext -layout ../fontes/resolucao-cgibs-6-2026-regulamento-ibs.pdf reg.txt
python3 -I ../scripts/arts.py reg.txt reg_arts.json
pdftotext -layout ../fontes/lc-214-2025-atualizada.pdf lc.txt
python3 -I ../scripts/tables.py ../fontes/lc-214-2025-atualizada.pdf
python3 -I ../scripts/build.py
cd ..
python3 -I -c "
t=open('scripts/template.html').read(); d=open('dados/data.json').read().replace('</','<\\\\/')
open('index.html','w').write(t.replace('__DATA__',d))"
rm -f dados/reg.txt dados/lc.txt
echo "index.html gerado."
