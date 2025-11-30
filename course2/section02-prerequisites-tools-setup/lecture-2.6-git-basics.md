# Lecture 2.6 – Git Basics for MLOps (Branching, PRs, Tags)

---

## Why Git Matters for MLOps

Git isn't just for software engineers. In MLOps, Git is essential for:

- **Tracking code changes**: Training scripts, configuration, pipelines
- **Collaboration**: Working with data scientists and engineers
- **Triggering CI/CD**: Commits trigger automated pipelines
- **Reproducibility**: "Which version of the code produced this model?"

Let's make sure you're comfortable with Git.

---

## Git Fundamentals Recap

If you already know Git, skim through this. If not, this is your crash course.

### What Is Git?

Git is a distributed version control system. It tracks changes to files over time.

Key concepts:
- **Repository (repo)**: A project tracked by Git
- **Commit**: A snapshot of changes
- **Branch**: A parallel line of development
- **Remote**: A copy of the repo on a server (GitHub, GitLab, etc.)

### Basic Workflow

```bash
# 1. Make changes to files
# 2. Stage changes
git add file.py

# 3. Commit changes
git commit -m "Add feature X"

# 4. Push to remote
git push origin main
```

---

## Essential Git Commands

Let me walk you through the commands you'll use daily.

### Starting a Project

```bash
# Initialize a new repo
git init

# Or clone an existing repo
git clone https://github.com/username/repo.git
```

### Checking Status

```bash
# See what's changed
git status

# See detailed changes
git diff

# See commit history
git log
git log --oneline --graph  # prettier view
```

### Making Commits

```bash
# Stage specific files
git add file1.py file2.py

# Stage all changes
git add .

# Commit with message
git commit -m "Fix bug in preprocessing"

# Stage and commit in one (only for tracked files)
git commit -am "Quick fix"
```

### Good Commit Messages

Bad:
```
git commit -m "fix"
git commit -m "update"
git commit -m "asdf"
```

Good:
```
git commit -m "Fix null handling in data preprocessing"
git commit -m "Add unit tests for model evaluation"
git commit -m "Update config to use new API endpoint"
```

Format: `<action> <what was changed>`

---

## Branching

Branches let you work on features without affecting the main code.

### Why Branch?

- Work on features in isolation
- Keep main branch stable
- Allow parallel development
- Enable code review before merging

### Branch Commands

```bash
# See all branches
git branch

# Create a new branch
git branch feature/add-preprocessing

# Switch to branch
git checkout feature/add-preprocessing

# Create and switch (shortcut)
git checkout -b feature/add-preprocessing

# Switch back to main
git checkout main

# Delete a branch
git branch -d feature/add-preprocessing
```

### Naming Conventions

Use consistent branch names:
- `feature/add-login` - New features
- `bugfix/fix-null-handling` - Bug fixes
- `experiment/try-xgboost` - Experiments
- `hotfix/critical-bug` - Urgent fixes

---

## Merging and Rebasing

### Merging

Combines changes from one branch into another:

```bash
# Switch to target branch
git checkout main

# Merge feature branch
git merge feature/add-preprocessing

# If there are conflicts, resolve them, then:
git add .
git commit -m "Merge feature/add-preprocessing"
```

### Handling Merge Conflicts

When Git can't automatically merge, you'll see:

```
<<<<<<< HEAD
your code here
=======
their code here
>>>>>>> feature-branch
```

To resolve:
1. Edit the file to keep what you want
2. Remove the conflict markers
3. Stage and commit

```bash
# After editing
git add conflicted_file.py
git commit -m "Resolve merge conflict"
```

### Rebasing (Advanced)

Rebase replays your commits on top of another branch:

```bash
# On your feature branch
git rebase main
```

Use rebase for cleaner history. Use merge for preserving history.

---

## Working with Remotes

### Remote Basics

```bash
# See remotes
git remote -v

# Add a remote
git remote add origin https://github.com/username/repo.git

# Fetch changes from remote
git fetch origin

# Pull changes (fetch + merge)
git pull origin main

# Push changes
git push origin main
```

### Pushing a New Branch

```bash
# Create and push a new branch
git checkout -b feature/my-feature
# ... make changes ...
git push -u origin feature/my-feature
# -u sets upstream, so next time just: git push
```

---

## Pull Requests (PRs)

Pull Requests are how teams review and merge code.

### The PR Workflow

1. Create a branch
2. Make changes and commit
3. Push branch to remote
4. Open a Pull Request
5. Team reviews
6. Address feedback
7. Merge

### Creating a PR (GitHub)

1. Push your branch:
   ```bash
   git push origin feature/my-feature
   ```

2. Go to GitHub
3. Click "Compare & pull request"
4. Add title and description
5. Request reviewers
6. Create PR

### PR Best Practices

- Keep PRs small (easier to review)
- Write clear descriptions
- Reference related issues
- Respond to feedback promptly
- Squash commits when merging (cleaner history)

### PR Description Template

```markdown
## What does this PR do?
Brief description of changes.

## How to test?
Steps to verify the changes work.

## Related issues
Closes #123

## Checklist
- [ ] Tests added
- [ ] Documentation updated
- [ ] Code formatted
```

---

## Tags and Releases

Tags mark specific points in history—great for versions.

### Creating Tags

```bash
# Create lightweight tag
git tag v1.0.0

# Create annotated tag (recommended)
git tag -a v1.0.0 -m "Release version 1.0.0"

# Tag a specific commit
git tag -a v1.0.0 abc1234 -m "Release version 1.0.0"
```

### Working with Tags

```bash
# List tags
git tag

# Show tag info
git show v1.0.0

# Push tags to remote
git push origin v1.0.0
git push origin --tags  # all tags

# Checkout a tag
git checkout v1.0.0
```

### Version Tagging for ML

In MLOps, we tag model releases:

```bash
# Model version tags
git tag -a model-v1.0.0 -m "First production model"
git tag -a model-v1.1.0 -m "Improved accuracy to 87%"

# Release tags
git tag -a release-2024-01-15 -m "January release"
```

---

## Git for MLOps: Specific Patterns

### Branch Strategy for ML Projects

```
main
├── develop          # Integration branch
├── feature/data-preprocessing
├── feature/model-training
├── experiment/try-transformer
└── release/v1.0
```

- **main**: Production-ready code
- **develop**: Integration of features
- **feature/**: New capabilities
- **experiment/**: ML experiments (might not merge)
- **release/**: Release preparation

### Commit Triggers for CI/CD

Set up your CI to trigger on:

```yaml
# .github/workflows/ci.yml
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  release:
    types: [published]
```

### What NOT to Commit

Never commit:
- Large data files (use DVC)
- Model files (use model registry)
- Secrets and credentials
- Local config files
- Virtual environment folders

Your `.gitignore` handles this.

---

## Common Git Scenarios

### Undo Last Commit (Not Pushed)

```bash
# Keep changes, undo commit
git reset --soft HEAD~1

# Discard changes and commit
git reset --hard HEAD~1
```

### Undo Last Commit (Already Pushed)

```bash
# Create a reverting commit
git revert HEAD
git push
```

### Discard Uncommitted Changes

```bash
# Discard changes to one file
git checkout -- file.py

# Discard all changes
git checkout -- .

# Remove untracked files
git clean -fd
```

### Stash Changes

Temporarily save changes:

```bash
# Stash changes
git stash

# List stashes
git stash list

# Apply stash
git stash pop  # apply and remove
git stash apply  # apply and keep
```

---

## Git Tools

### Git Aliases

Add to `~/.gitconfig`:

```ini
[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
    lg = log --oneline --graph --all
```

Now `git st` = `git status`.

### GUI Tools

- **GitHub Desktop**: Simple, free
- **GitKraken**: Powerful, visual
- **VS Code Git**: Built into VS Code
- **tig**: Terminal UI

### VS Code Integration

VS Code has built-in Git:
- Source Control panel (Ctrl+Shift+G)
- See changes inline
- Stage, commit, push from UI
- Compare changes visually

---

## Recap

Essential Git for MLOps:

**Daily commands**:
- `git status`, `git add`, `git commit`, `git push`, `git pull`

**Branching**:
- Create feature branches
- Merge when done
- Use consistent naming

**Collaboration**:
- Pull Requests for code review
- Keep PRs small and focused

**Versioning**:
- Tags for releases
- Semantic versioning (v1.0.0)

**Don't commit**:
- Large files, secrets, models, data

---

## What's Next

Now let's discuss how to follow along with this course if you only have a laptop—no cloud resources required.

---

**Next Lecture**: [2.7 – How to Follow Labs if You Only Have a Laptop](lecture-2.7-laptop-only-labs.md)
