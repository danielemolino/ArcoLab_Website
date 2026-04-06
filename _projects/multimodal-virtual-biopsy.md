---
layout: page
title: Multimodal Virtual Biopsy
permalink: /projects/multimodal-virtual-biopsy/
description: Placeholder project on multimodal virtual biopsy pipelines for clinically interpretable prediction and synthetic data support.
img: /assets/img/9.jpg
importance: 3
project_state: active
category: multimodal-clinical-ai
project_type: Clinical Application
status: Through September 2028
timeline: 2025-2028
team:
  - Paolo Soda
  - Aurora Rofena
  - Camillo Maria Caruso
focus_areas:
  - Multimodal Learning
  - Virtual Biopsy
  - Predictive Modelling
collaborators:
  - Università Campus Bio-Medico di Roma
  - Clinical oncology partners
highlights:
  - Placeholder direction on fusing imaging, pathology, and clinical variables.
  - Placeholder direction on interpretable prediction pipelines for translational workflows.
  - Placeholder direction on synthetic data support for robust validation.
project_filter: multimodal-virtual-biopsy
---

{% assign project_publications = site.data.publications | where_exp: "item", "item.projects contains page.project_filter" %}

<section class="project-profile">
  <div class="project-profile-hero">
    <div class="project-profile-media">
      <img src="{{ page.img | relative_url }}" alt="{{ page.title }}">
    </div>
    <div class="project-profile-copy">
      <p class="project-profile-kicker">{{ page.project_type }}</p>
      <h1>{{ page.title }}</h1>
      <p class="project-profile-lead">{{ page.description }}</p>
      <div class="project-profile-tags">
        {% for item in page.focus_areas %}
          <span>{{ item }}</span>
        {% endfor %}
      </div>
      <div class="member-profile-links">
        <a class="about-hero-btn about-hero-btn-primary about-inline-btn" href="{{ '/publications/' | relative_url }}?project={{ page.project_filter | url_encode }}">View Publications</a>
        <a class="about-hero-btn about-hero-btn-secondary" href="{{ '/projects/' | relative_url }}">Back to Projects <span aria-hidden="true">&rarr;</span></a>
      </div>
    </div>
  </div>

  <div class="project-profile-grid">
    <div class="project-profile-section">
      <h2>Overview</h2>
      <p>Placeholder copy for a project page centred on multimodal virtual biopsy, combining heterogeneous clinical evidence into clinically meaningful prediction and stratification workflows.</p>
      <p>Placeholder copy on bridging methodological modelling with translational scenarios where interpretability, robustness, and cross-modal consistency are essential.</p>
    </div>

    <aside class="project-profile-panel">
      <div class="project-profile-panel-block">
        <h3>Status</h3>
        <p>{{ page.status }}</p>
      </div>
      <div class="project-profile-panel-block">
        <h3>Timeline</h3>
        <p>{{ page.timeline }}</p>
      </div>
      <div class="project-profile-panel-block">
        <h3>Collaborators</h3>
        <ul class="project-profile-list">
          {% for organization in page.collaborators %}
            <li>{{ organization }}</li>
          {% endfor %}
        </ul>
      </div>
    </aside>
  </div>

  <div class="project-profile-section">
    <h2>Research Directions</h2>
    <ul class="project-profile-list">
      {% for item in page.highlights %}
        <li>{{ item }}</li>
      {% endfor %}
    </ul>
  </div>

  <div class="project-profile-section">
    <h2>Related Publications</h2>
    {% if project_publications and project_publications != empty %}
      {% include publication_cards.liquid publications=project_publications %}
    {% else %}
      <div class="publications project-related-publications">
        <ol class="bibliography">
          <li>
            <div class="row">
              <div class="col-sm-10">
                <div class="title">Project-linked publications</div>
                <div class="periodical">No publications are linked to this project yet. Once project tags are assigned in the publications workflow, related outputs will appear here automatically.</div>
                <div class="links">
                  <a href="{{ '/publications/' | relative_url }}?project={{ page.project_filter | url_encode }}" class="btn btn-sm z-depth-0" role="button">Browse Publications</a>
                </div>
              </div>
            </div>
          </li>
        </ol>
      </div>
    {% endif %}
  </div>
</section>
