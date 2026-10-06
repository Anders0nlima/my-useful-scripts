# Contribution Guide & Git/GitHub Workflow

This repository is built to be modular: **each script or automation is treated as a completely isolated feature**.

Beyond collecting useful tools, this project is designed to practice real-world software engineering collaboration: creating **Issues**, developing in dedicated **Branches**, submitting **Pull Requests (PRs)**, and writing standardized commit messages.

---

## The Development Lifecycle (Step-by-Step)

```text
[1. Create Issue] ──> [2. Create Branch] ──> [3. Implement Script] ──> [4. Commit Changes] ──> [5. Push & Open PR] ──> [6. Merge to Main]
```

### 1. Create an Issue
Before writing code, open an Issue describing the problem and the proposed automation.
- On GitHub Web: **Issues** tab > **New Issue** > Select the **New Script / Automation** template.
- Note the generated issue number (e.g., `#1`).

---

### 2. Create a Dedicated Branch
Always branch off an up-to-date `main`. Never work directly on `main` for new features or fixes.

```bash
# 1. Ensure you are on the main branch and up to date
git checkout main
git pull origin main

# 2. Create and switch to a new branch (use a concise, descriptive name)
git checkout -b feature/script-name
# Example: git checkout -b feature/downloads-organizer
```

**Branch naming conventions:**
- New automations: `feature/<short-name>`
- Bug fixes: `fix/<short-name>`
- Documentation/Chores: `docs/<short-name>` or `chore/<short-name>`

---

### 3. Implement the Script
Place your script inside the appropriate directory according to its runtime/language:
- Python: `scripts/python/`
- Node.js / JavaScript: `scripts/javascript/`
- Shell / Bash / PowerShell: `scripts/shell/`

**Best Practices for each script:**
- Keep each script **self-contained** (standalone).
- Include clear usage instructions directly in the file header or docstring:
  - Purpose
  - Accepted arguments/flags
  - Practical execution examples
- If the script requires external dependencies, keep requirements minimal and clearly document installation instructions.

---

### 4. Commit with Conventional Commits
Write clear commit messages using the Conventional Commits format:
`<type>(<scope>): <imperative description>`

Examples:
- `feat(python): add automated downloads organizer script`
- `feat(node): add json to csv conversion script`
- `fix(shell): resolve permission issue in log backup script`
- `docs: update scripts table in README`

Terminal commands:
```bash
git status
git add scripts/python/my_script.py
git commit -m "feat(python): add downloads organizer script"
```

---

### 5. Push the Branch and Open a Pull Request (PR)

Push the branch to the remote repository:
```bash
git push -u origin feature/script-name
```

After pushing:
1. Go to your repository on GitHub (you will see the **Compare & pull request** banner).
2. Fill out the PR template sections.
3. **Important:** Link the issue in the PR description using `Closes #1` (replace `1` with your actual issue number). When the PR is merged, the issue will automatically close and update your GitHub stats!

---

### 6. Merge and Sync Locally
After merging the PR on GitHub:
```bash
# Switch back to local main
git checkout main

# Pull the merged changes from GitHub
git pull origin main

# (Optional) Delete the merged local branch
git branch -d feature/script-name
```

---

## Pro Tip: Using GitHub CLI (`gh`)
If you have the official GitHub CLI (`gh`) installed, you can execute this entire flow directly from your terminal:

```bash
# Create an issue from the terminal
gh issue create --title "feat: downloads organizer" --body "Script to organize downloads folder by extension."

# Create a pull request linked to the issue
gh pr create --title "feat(python): downloads organizer" --body "Closes #1"

# Merge the pull request
gh pr merge --squash --delete-branch
```
