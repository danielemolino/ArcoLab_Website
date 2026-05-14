---
layout: page
title: FAIR Spoke 3
full_title: Resilient AI
permalink: /projects/fair-spoke-3/
description: FAIR research line on robust AI methods for noisy, incomplete, and inconsistent real-world data.
img: /assets/projects/fair-preview.jpg
importance: 10
project_state: ended
category: artificial-intelligence
project_type: National Partnership Spoke
status: PNRR programme
timeline: 2023-2025
official_page: https://fondazione-fair.it/en/spoke/spoke-3-resilient-ai/
focus_areas:
  - Resilient AI
  - Robust Multimodal Learning
  - Adversarial Robustness
collaborators:
  - Fondazione FAIR
  - Consiglio Nazionale delle Ricerche
  - Universita Campus Bio-Medico di Roma
highlights:
  - Data augmentation strategies for incomplete or poorly representative real-world data.
  - Robust and resilient algorithms, including resistance to external and malicious attacks.
  - Validation and operation of AI systems that must work with in-the-wild data.
project_filter: fair-spoke-3
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
        FAIR Spoke 3 focuses on resilient AI: models and software that remain effective when trained and deployed on real-world data that are noisy, incomplete, inconsistent, or limited. The spoke studies techniques for robustness, data augmentation, validation, and operation in challenging environments.
      </p>
      <p>
        ArCo's local activity connects these goals with biomedical AI, multimodal representation learning, missing modalities, adversarial robustness, fairness, and precision medicine case studies.
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
