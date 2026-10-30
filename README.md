# Consulta Reforma Tributária — Bonomi Contábil

Página pública de consulta (repositório `marquesbonomi/consulta-reforma`) dos benefícios de IBS e CBS por NCM, NBS ou atividade.

No ar em: **https://marquesbonomi.github.io/consulta-reforma/** (GitHub Pages, publica sozinho a cada mudança no `main`). Sem domínio próprio, por decisão do dono: não mexer no DNS do bonomi.com.br.

## Base legal usada
- LC 214/2025, texto atualizado com a LC 227/2026 (`fontes/lc-214-2025-atualizada.pdf`): anexos com NCM/NBS.
- Resolução CGIBS nº 6/2026, regulamento do IBS (`fontes/resolucao-cgibs-6-2026-regulamento-ibs.pdf`).
- Demais resoluções do CGIBS analisadas em `fontes/resolucoes/` (a lista e o efeito de cada uma estão em `NORMAS`, no fim de `scripts/build.py`, e na aba "Normas consideradas" da página).

## Como a página é montada
`scripts/montar.sh` lê os PDFs de `fontes/` e gera `dados/data.json` e `index.html`:
1. `tables.py` extrai as tabelas dos anexos da LC 214 (páginas 260 a 283 do PDF atual).
2. `arts.py` separa o regulamento em artigos (para mostrar o texto de cada benefício).
3. `build.py` junta tudo: anexos (tratamento, redução, artigos), atividades e regimes, lista de normas.
4. O resultado é embutido em `scripts/template.html` (a tela, com o logotipo) e vira o `index.html`.

## Quando sair norma nova
1. Colocar o PDF em `fontes/resolucoes/` (ou substituir a LC/regulamento em `fontes/` se for texto consolidado novo).
2. Ler a norma e decidir o efeito: muda lista de NCM/NBS, redução, alíquota, data de início, ou nada.
3. Ajustar `scripts/build.py` (entradas `add(...)`, `ANEXOS`, `NORMAS`) e, se a LC mudar de paginação, o intervalo de páginas em `scripts/tables.py`.
4. Rodar `scripts/montar.sh`, abrir o `index.html` e testar alguns códigos.
5. Commit no `main` = publicar.
