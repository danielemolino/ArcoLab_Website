## Lab Graph

`Lab Graph` is an isolated, reversible module that adds an interactive network view to the site.

### What it includes

- `People Graph`
- `Paper Graph`
- optional `Hybrid Graph`

### Where it lives

- Page: [_pages/graph.md](/mnt/c/Users/danie/OneDrive/Desktop/Codice/lab-website/_pages/graph.md)
- Includes:
  - [_includes/lab_graph/page.liquid](/mnt/c/Users/danie/OneDrive/Desktop/Codice/lab-website/_includes/lab_graph/page.liquid)
  - [_includes/lab_graph/toolbar.liquid](/mnt/c/Users/danie/OneDrive/Desktop/Codice/lab-website/_includes/lab_graph/toolbar.liquid)
  - [_includes/lab_graph/legend.liquid](/mnt/c/Users/danie/OneDrive/Desktop/Codice/lab-website/_includes/lab_graph/legend.liquid)
  - [_includes/lab_graph/details_panel.liquid](/mnt/c/Users/danie/OneDrive/Desktop/Codice/lab-website/_includes/lab_graph/details_panel.liquid)
  - [_includes/lab_graph/raw_data.liquid](/mnt/c/Users/danie/OneDrive/Desktop/Codice/lab-website/_includes/lab_graph/raw_data.liquid)
- JS:
  - [assets/js/lab-graph/data.js](/mnt/c/Users/danie/OneDrive/Desktop/Codice/lab-website/assets/js/lab-graph/data.js)
  - [assets/js/lab-graph/ui.js](/mnt/c/Users/danie/OneDrive/Desktop/Codice/lab-website/assets/js/lab-graph/ui.js)
  - [assets/js/lab-graph/main.js](/mnt/c/Users/danie/OneDrive/Desktop/Codice/lab-website/assets/js/lab-graph/main.js)
- Styles:
  - [_sass/_lab-graph.scss](/mnt/c/Users/danie/OneDrive/Desktop/Codice/lab-website/_sass/_lab-graph.scss)

### Data source

Current graph data is derived from [_data/team.yml](/mnt/c/Users/danie/OneDrive/Desktop/Codice/lab-website/_data/team.yml), specifically:

- people metadata
- interests/topics
- selected publications attached to each team member

This keeps the feature independent from core site collections and avoids changing the existing publication model.

### Feature flag

Central flag in [_config.yml](/mnt/c/Users/danie/OneDrive/Desktop/Codice/lab-website/_config.yml):

```yml
lab_graph:
  enabled: true
```

Other optional switches:

- `show_in_nav`
- `enable_people`
- `enable_papers`
- `enable_hybrid`
- `default_view`

### Revert / disable

Fast disable:

1. set `lab_graph.enabled: false` in [_config.yml](/mnt/c/Users/danie/OneDrive/Desktop/Codice/lab-website/_config.yml)
2. rebuild the site

Complete rollback:

1. remove [_pages/graph.md](/mnt/c/Users/danie/OneDrive/Desktop/Codice/lab-website/_pages/graph.md)
2. remove [_includes/lab_graph](/mnt/c/Users/danie/OneDrive/Desktop/Codice/lab-website/_includes/lab_graph)
3. remove [assets/js/lab-graph](/mnt/c/Users/danie/OneDrive/Desktop/Codice/lab-website/assets/js/lab-graph)
4. remove [_sass/_lab-graph.scss](/mnt/c/Users/danie/OneDrive/Desktop/Codice/lab-website/_sass/_lab-graph.scss)
5. remove the `@use "lab-graph";` line from [assets/css/main.scss](/mnt/c/Users/danie/OneDrive/Desktop/Codice/lab-website/assets/css/main.scss)
6. remove the small conditional nav item in [_includes/header.liquid](/mnt/c/Users/danie/OneDrive/Desktop/Codice/lab-website/_includes/header.liquid)
7. remove the page-specific script include in [_includes/scripts.liquid](/mnt/c/Users/danie/OneDrive/Desktop/Codice/lab-website/_includes/scripts.liquid)

### Notes

- The graph uses Cytoscape loaded only on the graph page.
- No core routes or data files were renamed or moved.
- The current `Paper Graph` is based on selected publications already exposed in team data, which keeps the integration low-risk and easy to extend later.
