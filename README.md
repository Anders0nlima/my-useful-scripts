# Useful Scripts & Automations Hub

> A modular collection of lightweight scripts and automations written in Python, JavaScript/Node.js, and Shell/PowerShell to solve everyday developer tasks.

![GitHub repo size](https://img.shields.io/github/repo-size/Anders0nlima/my-useful-scripts?color=blue)
![GitHub issues](https://img.shields.io/github/issues/Anders0nlima/my-useful-scripts?color=orange)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Anders0nlima/my-useful-scripts?color=green)
![Python](https://img.shields.io/badge/Python-3.13+-3776AB?logo=python&logoColor=white)
![NodeJS](https://img.shields.io/badge/Node.js-22+-339933?logo=node.js&logoColor=white)
![Shell](https://img.shields.io/badge/Shell-Bash%20%7C%20PowerShell-4EAA25?logo=gnu-bash&logoColor=white)

---

## Project Goals

1. **Practical Real-World Automations:** Solve repetitive daily chores (file reorganization, data transformations, quick reports, API utilities, git cleanup).
2. **Full Isolation:** Every script is self-contained and operates independently without coupling to other scripts.
3. **Open Source & DevOps Best Practices:** Every new script follows the complete engineering workflow: **Issue** $\rightarrow$ **Branch** $\rightarrow$ **Conventional Commits** $\rightarrow$ **Pull Request** $\rightarrow$ **Review & Merge**.

---

## Directory Structure

```text
my-useful-scripts/
├── .github/
│   ├── ISSUE_TEMPLATE/          # Standardized issue templates
│   └── PULL_REQUEST_TEMPLATE.md # Pull request template
├── scripts/
│   ├── python/                  # Python utilities & automations
│   ├── javascript/              # JavaScript / Node.js utilities
│   └── shell/                   # Shell / Bash / PowerShell scripts
├── CONTRIBUTING.md              # Workflow guide for Branches, Commits, and PRs
├── .editorconfig                # Editor and code style standards
├── .gitignore                   # Ignored files and patterns
└── README.md                    # Main documentation
```

---

## Scripts Catalog

| Script | Language | Category | Description | Path |
| :--- | :--- | :--- | :--- | :--- |
| **Downloads Organizer** | Python 3 | File Management | Organizes files into categorized folders (`Documents`, `Images`, `Archives`, `Media`, `Executables`) by extension. Supports `--dry-run` and collision-safe renaming. | [`scripts/python/downloads_organizer.py`](scripts/python/downloads_organizer.py) |
| **Image Compressor** | Python 3 | Media Optimization | Batch compresses images for the web with quality control, optional WebP conversion, and aspect-ratio resizing. | [`scripts/python/image_compressor.py`](scripts/python/image_compressor.py) |

---

## Planned Automations (Roadmap)

Ideas for upcoming Issues and Pull Requests:

- [x] **Downloads Organizer:** Sort files into categorized folders by extension (Images, Docs, PDFs, Videos, Installers). *(Implemented in #1)*
- [x] **Image Compressor:** Batch optimize and compress images for web using Pillow. *(Implemented in #2)*
- [ ] **Git Local Branch Cleaner:** Shell / PowerShell script to prune local branches that have been deleted on the remote.
- [ ] **Mock Data Generator:** Generate JSON / CSV files with mock test data (names, emails, dates).
- [ ] **Markdown Broken Links Checker:** Scan markdown files and detect broken HTTP links (e.g., 404 responses).

---

## Prerequisites

To run scripts from this repository, ensure you have installed:

- **Python 3.10+** (`python --version`)
- **Node.js 18+** (`node --version`)
- **Git** configured locally

---

## How to Contribute / Add New Scripts

Every new script must be developed in an isolated branch and submitted through a Pull Request.

Check out our complete step-by-step guide in [CONTRIBUTING.md](file:///c:/Projetos/my-useful-scripts/CONTRIBUTING.md) for:
- Branch naming guidelines (`feature/<script-name>`)
- Commit message conventions (`feat: ...`, `fix: ...`)
- Linking Issues to Pull Requests (`Closes #1`)

---

## License

Distributed under the MIT License. See `LICENSE` for more information.
