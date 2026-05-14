---
layout: page
title: LUMINATE
full_title: "Advancing Lung Cancer Screening: Artificial Intelligence, Multimodal Imaging and Cutting-Edge Technologies for Early Detection and Characterization"
permalink: /projects/luminate/
description: Multimodal lung cancer screening research using low-dose CT, low-dose FDG PET/CT, and AI risk prediction.
img: /assets/img/8.jpg
importance: 14
project_state: active
category: lung-cancer-screening
project_type: PNRR Research Project
status: Project code PNRR-MCNT2-2023-12377755
timeline: 24 months
grant_number: PNRR-MCNT2-2023-12377755
focus_areas:
  - Lung Cancer Screening
  - Multimodal Imaging
  - Risk Prediction
collaborators:
  - Ospedale San Raffaele Milano
  - Universita Campus Bio-Medico di Roma
  - University of Calabria
  - Ruggi d'Aragona
highlights:
  - Early detection and characterisation of suspicious lung nodules.
  - AI models for lung cancer risk prediction from clinical and imaging data.
  - Integration of low-dose CT and low-dose FDG PET/CT in screening workflows.
project_filter: luminate
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
        LUMINATE addresses lung cancer screening through artificial intelligence, multimodal imaging, and technologies for early detection and characterisation. The project combines low-dose CT, low-dose FDG PET/CT, and clinical information to improve risk assessment.
      </p>
      <p>
        The UCBM engineering unit contributes AI models for predicting lung cancer risk using clinical and imaging data, within a multi-centre project coordinated by Ospedale San Raffaele.
      </p>
    </div>

    <aside class="project-profile-panel">
      <div class="project-profile-panel-block">
        <h3>Timeline</h3>
        <p>{{ page.timeline }}</p>
      </div>
      <div class="project-profile-panel-block">
        <h3>Grant</h3>
        <p>{{ page.grant_number }}</p>
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
