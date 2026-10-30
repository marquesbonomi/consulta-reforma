# Consulta Reforma Tributária — regras para o Claude

Página pública da Bonomi Contábil para clientes consultarem benefícios de IBS/CBS.
Falar em português, direto. Público é cliente: linguagem simples, sem jargão interno.

- Qualquer commit no `main` publica o site (GitHub Pages). Testar antes.
- Norma nova chega como PDF/zip na conversa: seguir "Quando sair norma nova" do README.
  Sempre registrar a norma em `NORMAS` (build.py), mesmo quando não tem efeito.
- Nunca inventar item, código ou percentual: tudo tem que sair do texto da norma, com o artigo citado.
- Alíquotas padrão da tela (em `scripts/template.html`): CBS 11,32% e IBS 0,1%.
- Nada de dado de cliente, senha ou token neste repositório (ele é público).
- CNAE e regras por atividade da NBS são ligações por afinidade (`CNAE_MAP`/`NBS_MAP` no build.py), não tabela oficial: a tela avisa isso. Ao mudar, citar o artigo que justifica.
