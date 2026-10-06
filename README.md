# 🛠️ Central de Scripts e Automações Úteis

> Coleção modular de scripts e automações em Python, JavaScript/Node.js e Shell/PowerShell para resolver tarefas rotineiras e repetitivas de desenvolvimento.

![GitHub repo size](https://img.shields.io/github/repo-size/Anders0nlima/my-useful-scripts?color=blue)
![GitHub issues](https://img.shields.io/github/issues/Anders0nlima/my-useful-scripts?color=orange)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Anders0nlima/my-useful-scripts?color=green)
![Python](https://img.shields.io/badge/Python-3.13+-3776AB?logo=python&logoColor=white)
![NodeJS](https://img.shields.io/badge/Node.js-22+-339933?logo=node.js&logoColor=white)
![Shell](https://img.shields.io/badge/Shell-Bash%20%7C%20PowerShell-4EAA25?logo=gnu-bash&logoColor=white)

---

## 🎯 Proposta do Projeto

1. **Automações Práticas do Mundo Real:** Resolver pequenas dores do dia a dia (limpeza de arquivos, conversão de formatos, relatórios rápidos, chamadas de API, utilitários de repositório).
2. **Total Isolamento:** Cada automação é autocontida e funciona de forma independente, sem gerar acoplamento entre os scripts.
3. **Cultura DevOps / Open Source:** Todo novo script passa pelo ciclo completo de engenharia de software: **Issue** $\rightarrow$ **Branch** $\rightarrow$ **Commits Convencionais** $\rightarrow$ **Pull Request** $\rightarrow$ **Code Review & Merge**.

---

## 📁 Estrutura de Pastas

```text
my-useful-scripts/
├── .github/
│   ├── ISSUE_TEMPLATE/       # Templates padronizados para Issues
│   └── PULL_REQUEST_TEMPLATE.md # Template para Pull Requests
├── scripts/
│   ├── python/               # Scripts e automações em Python
│   ├── javascript/           # Scripts e automações em JavaScript / Node.js
│   └── shell/                # Scripts em Bash ou PowerShell
├── CONTRIBUTING.md           # Guia com fluxo de Branches, Commits e PRs
├── .editorconfig             # Padrões de formatação de código
├── .gitignore                # Arquivos ignorados pelo Git
└── README.md                 # Documentação principal
```

---

## 📚 Catálogo de Scripts

| Script | Linguagem | Categoria | Descrição | Caminho |
| :--- | :--- | :--- | :--- | :--- |
| *Em breve* | Python / Node / Shell | Utilitários | *Os primeiros scripts serão adicionados via Pull Requests dedicados.* | `scripts/` |

---

## 💡 Próximas Automações Planejadas (Roadmap de Issues)

Ideias para abertura de novas Issues e PRs no repositório:

- [ ] **Organizador de Downloads:** Agrupar arquivos em pastas por extensão (Imagens, PDFs, Vídeos, Documentos).
- [ ] **Limpador de Branches Locais:** Script Shell/PowerShell para remover branches do Git que já foram excluídas no repositório remoto.
- [ ] **Conversor de Imagens em Lote:** Otimização e conversão de PNG/JPEG para WebP.
- [ ] **Gerador de Dados de Teste:** Criar arquivos JSON/CSV com dados fictícios (nome, email, CPF, data).
- [ ] **Validador de Links em Markdown:** Percorrer arquivos `.md` e checar URLs quebradas com status HTTP 404.

---

## 🚀 Pré-requisitos

Para executar os scripts deste repositório, recomenda-se ter instalado:

- **Python 3.10+** (utilizado `python --version`)
- **Node.js 18+** (utilizado `node --version`)
- **Git** configurado localmente

---

## 🤝 Como Contribuir / Adicionar Novos Scripts

Cada novo script deve ser desenvolvido em uma branch isolada e submetido via Pull Request.

Consulte o nosso guia completo em [CONTRIBUTING.md](file:///c:/Projetos/my-useful-scripts/CONTRIBUTING.md) para conferir:
- Nomenclatura de branches (`feature/nome-do-script`)
- Padrão de commits (`feat: ...`, `fix: ...`)
- Como vincular a Issue ao Pull Request (`Closes #1`)

---

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.
