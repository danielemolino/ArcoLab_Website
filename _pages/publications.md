---
layout: page
permalink: /publications/
title: Publications
description: Research outputs from Arco Lab.
nav: true
nav_order: 3
---

<section class="publications-intro">
  <p class="publications-intro-kicker">Research Outputs</p>
  <h1>Publications</h1>
  <p class="publications-intro-copy">
    Arco Lab publishes across medical imaging, multimodal learning, clinical prediction, and decision-support systems. Browse the bibliography below, search by keyword, and open the available DOI, PDF, and code links for each contribution.
  </p>
  <div class="publications-intro-actions">
    <a class="about-hero-btn about-hero-btn-primary about-inline-btn" href="{{ '/projects/' | relative_url }}">Explore projects</a>
    {% if site.lab_graph.enabled %}
      <a class="about-hero-btn publications-graph-btn" href="{{ '/graph/' | relative_url }}">
        <i class="fa-solid fa-share-nodes" aria-hidden="true"></i>
        <span>Open paper graph</span>
      </a>
    {% endif %}
    <a class="about-hero-btn about-hero-btn-secondary" href="{{ '/team/' | relative_url }}">Open researcher profiles <span aria-hidden="true">&rarr;</span></a>
  </div>
</section>

{% include bib_search.liquid %}

<div id="publications-keyword-filters" class="publications-keyword-filters"></div>
<div id="publications-project-filters" class="publications-keyword-filters"></div>
<div id="publications-year-filters" class="publications-keyword-filters"></div>

<div class="publications">
{% bibliography %}
</div>

<script>
  window.arcoProjectLabels = {
    {% assign sorted_projects = site.projects | sort: "title" %}
    {% for project in sorted_projects %}
      "{{ project.project_filter | default: project.slug | escape }}": "{{ project.title | escape }}"{% unless forloop.last %},{% endunless %}
    {% endfor %}
  };
</script>
<script src="{{ '/assets/js/publications-filters.js' | relative_url }}"></script>
