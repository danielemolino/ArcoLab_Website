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
</section>

{% include bib_search.liquid %}

<div id="publications-keyword-filters" class="publications-keyword-filters"></div>

<div class="publications">
{% bibliography %}
</div>

<script src="{{ '/assets/js/publications-filters.js' | relative_url }}"></script>
