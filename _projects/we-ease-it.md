---
layout: page
title: We-ease-it
permalink: /projects/we-ease-it/
description: Hospital 4.0 telemonitoring platform for frail patients, combining home-life data, hospital information systems, and AI-driven predictive models.
img: /assets/projects/we-ease-it-model.png
importance: 6
project_state: ended
category: digital-health
project_type: Clinical Application
status: Completed in May 2024
timeline: 2021-2024
focus_areas:
  - Telemonitoring
  - Digital Health
  - Predictive Modelling
collaborators:
  - Università Campus Bio-Medico di Roma
  - Fondazione Policlinico Universitario Campus Bio-Medico
highlights:
  - Hospital 4.0 service for intelligent telemonitoring of frail, chronic, and oncologic patients.
  - Integration of daily-life signals with hospital information systems through an M-shaped platform architecture.
  - Personalized predictive models for COPD, heart failure, and non-small cell lung cancer.
project_filter: we-ease-it
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
        We-ease-it aimed to build an intelligent Hospital 4.0 service for telemonitoring frail patients outside the hospital while keeping care pathways tightly connected to institutional information systems. The project addressed an increasingly urgent healthcare problem: supporting chronic, elderly, and vulnerable patients without relying only on conventional in-hospital workflows.
      </p>
      <p>
        The technical programme combined home monitoring, hospital data integration, and AI-driven data mining to build personalized predictive models of disease evolution. The platform architecture followed an M-shaped model, with a horizontal core and disease-specific vertical modules, and targeted COPD, heart failure, and NSCLC as primary use cases.
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
