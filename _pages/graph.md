---
layout: page
title: Graph
permalink: /graph/
description: Interactive graph view of Arco Lab researchers and selected publications.
nav: false
lab_graph: true
---

{% if site.lab_graph.enabled %}
{% include lab_graph/page.liquid %}
{% else %}

  <section class="page-hero page-hero-graph">
    <div class="page-hero-copy">
      <p class="page-hero-kicker">Lab Graph</p>
      <h1>Graph disabled</h1>
      <p class="page-hero-lead">
        The interactive graph module is currently disabled in the site configuration.
      </p>
    </div>
  </section>
{% endif %}
