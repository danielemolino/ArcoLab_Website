# Agent Guidelines for ArCo Lab Website

This repository contains the ArCo Lab static website for Universita Campus Bio-Medico di Roma.

## Working rules

- Inspect the existing implementation before changing it.
- Treat the repository as a dirty worktree. Do not revert unrelated user changes.
- Use `rg` and `rg --files` for searches.
- Use `apply_patch` for manual edits.
- Preserve the current ArCo visual identity and static GitHub Pages architecture.
- Keep secrets and local sync configuration out of Git.
- Use `relative_url` for links and asset paths rendered by Liquid templates.

## Main paths

- `_pages/`: main pages and team profiles
- `_projects/`: project pages
- `_data/`: generated YAML data
- `_bibliography/`: generated BibTeX bibliography
- `assets/`: published images, branding, styles, and scripts
- `scripts/`: Google Sheets and Drive synchronization scripts
- `shared/`: local CSV sources, uploads, and ignored configuration
- `update_the_website/`: content update documentation
- `.github/workflows/deploy.yml`: build and deployment workflow

## Content workflow

Team, Projects, Publications, News, and Education are synchronized from shared Google Sheets and Drive folders. Do not edit generated files manually when a change belongs in a source Sheet or upload folder.

The collaborator-facing guide is [`update_the_website/ARCO_LAB_CONTENT_UPDATE_GUIDE.md`](update_the_website/ARCO_LAB_CONTENT_UPDATE_GUIDE.md). The technical workflow overview is [`update_the_website/README.md`](update_the_website/README.md).

## Validation

Use Docker for local builds:

```bash
docker compose up --build
docker compose run --rm jekyll bundle exec jekyll build --trace
```

Before finishing, run `git diff --check` and inspect relevant generated output. Do not commit `_site/`, credentials, ignored sync configuration, or local upload folders.
