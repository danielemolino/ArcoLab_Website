# ArCo Lab Coding Instructions

## Project

This is a customized Jekyll website for ArCo Lab at Universita Campus Bio-Medico di Roma. It is deployed as a static GitHub Pages artifact through `.github/workflows/deploy.yml`.

The public sections are Home, Team, Projects, Publications, Education, News, and Contact. Graph is accessed from Publications and is focused on papers.

## Before editing

- Inspect the relevant templates, data files, scripts, and existing styles.
- Check `git status --short` and preserve unrelated worktree changes.
- Search with `rg` before adding new files or duplicate logic.
- Prefer stable static-site solutions over runtime services or unnecessary dependencies.

## Content sources

Team, Projects, Publications, News, and Education use shared Google Sheets and Drive upload folders. The synchronization scripts are in `scripts/`; the operational notes are in `update_the_website/`.

Generated files include `_data/*.yml`, `_projects/*.md`, `_pages/team/*.md`, `_bibliography/papers.bib`, and published assets. Change the source Sheet or synchronization script rather than manually editing generated output.

Local credentials and `shared/*_sync.json` files are ignored. Never expose service-account JSON files, local CSVs, or upload folders in the public site.

## Implementation conventions

- Keep Jekyll paths compatible with both local development and the final custom domain.
- Use `relative_url` in Liquid for local links and images.
- Preserve the current ArCo typography, colors, responsive layout, and footer behavior unless the task requests a redesign.
- Keep filenames and slugs stable once they are used by content sources.
- Add short comments only for non-obvious logic.

## Build and checks

The supported environment is Docker:

```bash
docker compose up --build
docker compose run --rm jekyll bundle exec jekyll build --trace
```

Also run:

```bash
git diff --check
```

Do not include `_site/`, ignored credentials, local sync configuration, or upload sources in commits.
