---
layout: page
title: MISE
full_title: Piattaforma per la Medicina di Precisione. Intelligenza Artificiale e Diagnostica Clinica Integrata
permalink: /projects/mise/
description: Collaborative platform for precision medicine, federated learning, and integrated clinical diagnostics.
img: /assets/projects/mise-ai-overview.png
importance: 8
project_state: ended
category: precision-medicine
project_type: Industrial Research
status: Completed programme
timeline: 36 months
focus_areas:
  - Precision Medicine
  - Federated Learning
  - Clinical Data Integration
collaborators:
  - Bracco Imaging
  - Orobix
  - INNOMED
  - Istituto Italiano di Tecnologia
  - Universita Campus Bio-Medico di Roma
highlights:
  - Federated learning methods for distributed clinical research across multiple data holders.
  - Consensus models that can be trained without centralising sensitive clinical data.
  - Integration of AI algorithms with clinical applications for precision medicine workflows.
project_filter: mise
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
        MISE develops a collaborative technological platform for precision medicine and integrated clinical diagnostics. The project focuses on distributed clinical data aggregation, standardised information sharing, and AI methods that can learn from multiple clinical sources while preserving data locality.
      </p>
      <p>
        ArCo's contribution is centred on the integration of AI algorithms and clinical applications, with emphasis on federated learning, model-parameter sharing, and consensus models for clinical research.
      </p>
    </div>

    <aside class="project-profile-panel">
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
