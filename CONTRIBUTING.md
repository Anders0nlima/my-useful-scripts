# 🤝 Guia de Contribuição e Fluxo Git / GitHub

Este repositório foi projetado para ser modular: **cada automação é tratada como uma funcionalidade (feature) independente**.

Além de construir ferramentas úteis, o fluxo deste projeto simula as melhores práticas de engenharia de software usadas no mercado: abertura de **Issues**, desenvolvimento em **Branches**, submissão de **Pull Requests (PRs)** e commits padronizados.

---

## 🧭 O Ciclo de Desenvolvimento (Passo a Passo)

```
[1. Criar Issue] ──> [2. Criar Branch] ──> [3. Desenvolver Script] ──> [4. Fazer Commit] ──> [5. Push & Abrir PR] ──> [6. Merge na Main]
```

### 1. Criar a Issue
Antes de codificar, abra uma Issue descrevendo o problema e o script que será criado.
- Pelo GitHub Web: Aba **Issues** > **New Issue** > Selecione o template **Novo Script / Automação**.
- Anote o número da Issue criada (ex: `#1`).

---

### 2. Criar uma Branch dedicada
Sempre crie uma nova branch a partir da `main` atualizada. Nunca trabalhe direto na `main` para novas features.

```bash
# 1. Garanta que está na branch main e atualizado
git checkout main
git pull origin main

# 2. Crie e mude para a nova branch (use um nome descritivo)
git checkout -b feature/nome-do-script
# Exemplo: git checkout -b feature/organizador-downloads
```

**Padrão de nomenclatura de branches:**
- Novas automações: `feature/<nome-curto>`
- Correção de bugs: `fix/<nome-curto>`
- Documentação ou ajustes: `docs/<nome-curto>` ou `chore/<nome-curto>`

---

### 3. Desenvolver o Script
Coloque o seu script no diretório adequado de acordo com a linguagem:
- Python: `scripts/python/`
- Node.js / JavaScript: `scripts/javascript/`
- Shell / Bash / PowerShell: `scripts/shell/`

**Boas práticas para cada script:**
- Mantenha o script **autossuficiente** (standalone).
- Inclua documentação no próprio cabeçalho do arquivo explicando:
  - Objetivo
  - Parâmetros aceitos
  - Exemplo prático de execução
- Se houver dependências externas (ex: biblioteca Python), documente ou mantenha um `requirements.txt` específico na pasta do script se for um script mais complexo.

---

### 4. Commitar com Conventional Commits
Use mensagens de commit claras e padronizadas no formato:
`<tipo>(<escopo>): <descrição no imperativo>`

Exemplos:
- `feat(python): adiciona script para organizacao automatica de downloads`
- `feat(node): adiciona script para conversao de json para csv`
- `fix(shell): corrige erro de permissao no backup de logs`
- `docs: atualiza tabela de scripts no README`

Comandos no terminal:
```bash
git status
git add scripts/python/meu_script.py
git commit -m "feat(python): adiciona script para organizacao de downloads"
```

---

### 5. Enviar a Branch e Abrir o Pull Request (PR)

Envie a branch para o repositório remoto:
```bash
git push -u origin feature/nome-do-script
```

Após o push:
1. Acesse o GitHub no seu navegador (o GitHub exibirá um botão verde **Compare & pull request**).
2. No corpo do PR, preencha as seções do template.
3. **Importante:** Vincule a issue adicionando no corpo: `Closes #1` (substitua pelo número da sua issue). Assim que o PR for aprovado e mesclado, a Issue será fechada automaticamente, computando suas estatísticas no GitHub!

---

### 6. Merge e Sincronização Local
Após mergear o PR no GitHub:
```bash
# Volte para a main local
git checkout main

# Baixe as alterações mescladas do GitHub
git pull origin main

# (Opcional) Delete a branch local que já foi mesclada
git branch -d feature/nome-do-script
```

---

## ⚡ Dica Bônus: Usando a GitHub CLI (`gh`)
Se você instalar a ferramenta oficial do GitHub no terminal (`gh`), poderá fazer todo esse fluxo sem abrir o navegador:

```bash
# Criar uma issue direto pelo terminal
gh issue create --title "feat: organizador de downloads" --body "Script para organizar pasta por extensões."

# Criar um PR direto pelo terminal
gh pr create --title "feat(python): organizador de downloads" --body "Closes #1"

# Fazer merge do PR pelo terminal
gh pr merge --squash --delete-branch
```
