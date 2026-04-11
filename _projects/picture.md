---
layout: page
title: PICTURE
permalink: /projects/picture/
description: AI-driven prediction of pathological complete response after neoadjuvant therapies in non-small cell lung cancer through multimodal data fusion.
img: /assets/projects/picture-overview.png
importance: 2
project_state: active
category: multimodal-clinical-ai
project_type: Clinical Application
status: Through December 2026
timeline: 2023-2026
focus_areas:
  - Pathological Response Prediction
  - Multimodal Learning
  - Explainable AI
collaborators:
  - Università Campus Bio-Medico di Roma
  - Università degli Studi di Torino
  - Università degli Studi di Cassino
highlights:
  - Fusion of radiology, histology, cytology, molecular data, and electronic health records.
  - Prediction of pathological complete response before surgery in NSCLC.
  - Robust and explainable multimodal deep learning pipelines, including transfer toward chemoimmunotherapy settings.
project_filter: picture
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
        PICTURE addresses one of the central questions in contemporary lung oncology: whether pathological complete response after neoadjuvant treatment can be predicted before surgical resection. The project assumes that a multimodal view of the patient offers a more faithful representation of treatment response than any single data source taken in isolation.
      </p>
      <p>
        The project develops AI systems that integrate radiology imaging, histology, cytology, molecular data, and electronic health records to support pre-surgical decision-making in NSCLC. Alongside predictive performance, PICTURE emphasizes robustness, explainability, and the possibility of transferring learned models toward chemoimmunotherapy scenarios.
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
