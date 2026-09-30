# Repository Agent

## Purpose

Maintain a clean, reproducible, and well-structured repository.

## Repository Principles

- One topic per directory.
- Each topic is runnable independently.
- Keep dependencies minimal.
- Prefer simple layouts over deep nesting.
- Generated figures belong in results/figures/.
- Each topic contains its own README.md.

```text
XpX-topic-name/
├── README.md
├── src/
│   └── main.py
├── results/
│   └── figures/
└── requirements.txt
```

## Git Workflow

Small commits.

Commit message style:

feat: add gaussian process regression
fix: correct covariance implementation
docs: update topic readme
refactor: simplify plotting code

Commit working states.
Avoid large mixed-purpose commits.

## Branches

Default branch: main

Use temporary branches for larger work:

feature/gp-regression
feature/bayesian-linear-regression

Merge back into main after validation.

## GitHub Practices

Required files:

readme.md
.gitignore

Prefer Markdown for documentation.
Keep repository homepage and description updated.

## Continuous Integration

Every push should:

- create Python environment
- install requirements
- run scripts
- fail on errors

Prefer GitHub Actions.
Keep workflows simple.

## Documentation

Each topic README should contain:
- 
- objective
- theory reference
- implementation overview
- generated results
- key takeaways

Keep explanations concise.

## Command Line

Prefer command-line operations over GUI tools.

Useful commands:

git status
git add .
git commit -m "message"
git push
git pull

tree
find
grep

## Reproducibility

Pin dependencies when needed.

Use fixed random seed:

seed = 0

Generated figures should be reproducible from source code.

## Goal

Create a repository that remains clean, reproducible, and well-structured.