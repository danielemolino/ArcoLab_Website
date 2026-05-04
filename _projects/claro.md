---
layout: page
title: CLARO
permalink: /projects/claro/
description: A collaborative multi-source radiopathomics project for personalized oncology in non-small cell lung cancer.
img: /assets/img/10.jpg
importance: 4
project_state: ended
category: personalized-oncology
project_type: Clinical Application
status: 16 April 2019 - in progress
timeline: 16 April 2019 - present
scientific_manager: Prof. Sara Ramella
coordinating_institution: Oncological Radiotherapy, Campus Bio-Medico University
focus_areas:
  - RadioPathomics
  - Personalized Oncology
  - Decision Support
collaborators:
  - Oncological Radiotherapy, Campus Bio-Medico University
  - Bioinformatics Systems Engineering, UCBM
  - Diagnostic imaging, UCBM
  - Medical Oncology, UCBM
  - Medical Oncology, University of Turin - AOU S. Luigi Gonzaga Orbassano, Italy
highlights:
  - Imaging characteristics specific to lung cancer used as biomarkers for response prediction.
  - Multimodal analysis of radiological and anatomo-pathological images with clinical information.
  - Quantitative biomarker signatures for therapy selection in stage III-IV non-small cell lung cancer.
official_page: https://www.unicampus.it/progetto-di-ricerca/claro-a-collaborative-multi-sources-radiopathomics-approach-for-personalized-oncology-in-non-small-cell-lung-cancer/
project_filter: claro
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
        <a class="about-hero-btn about-hero-btn-secondary" href="{{ page.official_page }}" target="_blank" rel="noopener">Official Project Page <span aria-hidden="true">&rarr;</span></a>
        <a class="about-hero-btn about-hero-btn-secondary" href="{{ '/projects/' | relative_url }}">Back to Projects <span aria-hidden="true">&rarr;</span></a>
      </div>
    </div>
  </div>

  <div class="project-profile-grid">
    <div class="project-profile-section">
      <h2>Overview</h2>
      <p>
        CLARO was born from a collaborative project between the Faculties of Medicine and Surgery and Engineering, with the aim of identifying imaging characteristics specific to lung cancer and using them as biomarkers to predict response to oncological therapies.
      </p>
      <p>
        The project combines radiological and anatomo-pathological images with other clinical information to build personalized image-analysis models for stage III-IV non-small cell lung cancer. The goal is to convert heterogeneous medical data into a single and interpretable biomarker signature to support precision medicine.
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
        <h3>Scientific Manager</h3>
        <p>{{ page.scientific_manager }}</p>
      </div>
      <div class="project-profile-panel-block">
        <h3>Coordinating Institution</h3>
        <p>{{ page.coordinating_institution }}</p>
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
