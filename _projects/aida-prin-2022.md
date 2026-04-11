---
layout: page
title: AIDA - PRIN 2022
permalink: /projects/aida-prin-2022/
description: Explainable multimodal deep learning for personalized oncology, with a focus on robust fusion, missing modalities, and clinical validation in non-small cell lung cancer.
img: /assets/projects/aida-visual.jpg
importance: 1
project_state: active
category: multimodal-clinical-ai
project_type: Clinical Application
status: Through December 2026
timeline: 2023-2026
focus_areas:
  - Multimodal Deep Learning
  - Explainable AI
  - Personalized Oncology
collaborators:
  - Università Campus Bio-Medico di Roma
  - Hospital oncology partners
highlights:
  - Multimodal representation learning across radiomics, pathomics, and electronic health records.
  - Explainable AI methods for attention, counterfactual reasoning, and user-facing clinical transparency.
  - Prospective validation in non-small cell lung cancer with comparison against conventional clinical markers.
project_filter: aida-prin-2022
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
      <p>
        AIDA develops explainable multimodal deep learning for healthcare scenarios where single-modality pipelines are not enough. The project investigates when and how to fuse heterogeneous evidence, how to learn stronger shared representations, and how to maintain robustness when data are incomplete or some modalities are missing.
      </p>
      <p>
        The translational application is personalized oncology in non-small cell lung cancer, where radiomic, pathomic, and electronic health record data are combined to predict response, relapse, progression-free survival, and overall survival. The project also studies clinical trust through explainability mechanisms designed for physicians and domain experts.
      </p>
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
