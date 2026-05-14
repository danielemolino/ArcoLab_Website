---
layout: page
title: IDEA
full_title: AI-powered Digital Twin for next-generation lung cancer care
permalink: /projects/idea/
description: Digital twin research for next-generation lung cancer diagnosis, virtual treatment, and decision support.
img: /assets/img/7.jpg
importance: 13
project_state: active
category: digital-twins
project_type: Research Project
status: Project proposal
timeline: 24 months
grant_number: Horizon Europe Cluster 1 Health D3/D4/D5
focus_areas:
  - Digital Twin
  - Lung Cancer Care
  - Clinical Decision Support
collaborators:
  - Unit of Computer Systems and Bioinformatics, UCBM
  - Radiation Oncology, UCBM
  - Diagnostic Imaging, UCBM
  - Bioethics and Humanities, UCBM
highlights:
  - Radiological digital twins for lung cancer diagnosis and treatment decision support.
  - Virtual scanning and virtual treatments for patient-specific clinical scenarios.
  - Data interfaces, security, explainability, fairness, and ethical analysis.
project_filter: idea
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
        IDEA proposes AI-powered digital twins for next-generation lung cancer care. The project combines imaging, treatment information, data security, explainability, and ethics to support clinical decision-making for non-small cell lung cancer.
      </p>
      <p>
        The technical programme covers radiological digital twins, virtual scans, virtual treatments, and AI methods that can support diagnosis and therapy planning while accounting for data governance and clinical usability.
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
