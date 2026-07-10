<p align="center">
  <img src="assets/branding/arco/lockup/logo_arco.png" alt="ArCo Lab logo" width="220">
</p>

<h1 align="center">ArCo Lab Website</h1>

<p align="center">
  <strong>Applied AI research in medicine</strong><br>
  Universita Campus Bio-Medico di Roma
</p>

<p align="center">
  <a href="https://jekyllrb.com/">Jekyll</a> ·
  <a href="https://pages.github.com/">GitHub Pages</a> ·
  Static deployment
</p>

## About

This repository contains the public website of ArCo Lab, the Unit of Artificial Intelligence and Computer Systems at Universita Campus Bio-Medico di Roma.

The site is a static Jekyll website. It presents the lab's people, research projects, publications, educational activities, news, and contact information. It is designed to be hosted under the University's domain through the custom GitHub Actions deployment workflow.

## Website sections

- **Home** - Lab overview, research highlights, selected recent publications, projects, and team.
- **Team** - Researcher profiles, interests, biographies, and related publications.
- **Projects** - Active and completed research projects.
- **Publications** - Searchable publications with keyword, project, and year filters.
- **Education** - Courses and teaching activities.
- **News** - Editorial updates and research announcements.
- **Contact** - Lab contact details and institutional links.

## Repository structure

```text
_pages/                  Main pages and team profiles
_projects/               Project pages generated from the project sheet
_data/                   Generated site data
_bibliography/           Generated publication bibliography
assets/                  Published images, branding, styles, and scripts
scripts/                 Content synchronization and writeback scripts
shared/                  Local CSV sources and ignored configuration files
update_the_website/      Content update documentation
.github/workflows/       Build and deployment automation
```

## Local development

The supported local environment is Docker. Start the development server with:

```bash
docker compose up --build
```

The site is available at <http://localhost:8080>.

For a production-style build:

```bash
docker compose run --rm jekyll bundle exec jekyll build --trace
```

The generated site is written to `_site/`, which is ignored by Git.

## Updating content

Team, Projects, Publications, News, and Education are maintained through a separate private content-management workflow. The public repository contains only the generated website content and published assets.

Generated files should not be edited manually when the change belongs to the content workflow. Local service-account credentials, synchronization configuration, shared CSV sources, upload folders, and internal documentation are kept outside the public repository.

## Deployment

Pushing site changes to `main` triggers [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml). The workflow builds the Jekyll site and publishes the static artifact for GitHub Pages.

## Design and identity

The ArCo Lab visual identity is stored in [`assets/branding/arco/`](assets/branding/arco/). The main logo is used by the website and this README.
