---
layout: page
title: VirtualScanner
full_title: Intelligenza Aumentata per democratizzare la diagnosi di polmonite
permalink: /projects/virtual-scanner/
description: Augmented intelligence platform for pneumonia diagnosis using generative AI to synthesise CT-like chest volumes from X-ray exams.
img: /assets/projects/virtual-scanner-pneumonia-xray.jpg
importance: 15
project_state: active
category: generative-medical-imaging
project_type: Applied Clinical AI
status: Intesa Sanpaolo proposal
timeline: 12 months
focus_areas:
  - Virtual Scanner
  - Pneumonia Diagnosis
  - Generative AI
collaborators:
  - Universita Campus Bio-Medico di Roma
  - Hospitals in Peru
highlights:
  - CT-like chest volume synthesis from X-ray exams to support pneumonia diagnosis.
  - Local deployment designed for settings with limited connectivity and no cloud dependency.
  - Training of clinical operators and evaluation of diagnostic impact in target hospitals.
project_filter: virtual-scanner
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
        VirtualScanner applies augmented intelligence to pneumonia diagnosis by generating CT-like chest volumes from standard X-ray acquisitions. The proposal targets hospitals in Peru, where the system is intended to support clinicians with limited infrastructure and no dependence on cloud services.
      </p>
      <p>
        The project material describes deployment in two hospitals, operator training, and an expected reduction of diagnostic errors through a local AI-assisted workflow.
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
