---
layout: page
title: Clinical AI for Risk Stratification
permalink: /projects/clinical-risk-stratification/
description: Multimodal decision-support research for patient stratification, outcome prediction, and clinically grounded deployment pathways.
img: /assets/img/11.jpg
importance: 2
category: decision-support
project_type: Decision Support
status: Translational phase
timeline: 2024-present
team:
  - Paolo Soda
  - Valerio Guarrasi
focus_areas:
  - Clinical Data Analysis
  - Multimodal Learning
  - Outcome Prediction
collaborators:
  - Campus Bio-Medico University of Rome
  - Hospital and clinical partners
highlights:
  - Multimodal pipelines that integrate imaging, tabular, and longitudinal clinical information.
  - Outcome prediction models designed for robustness under real-world missingness and distribution shift.
  - Decision-support interfaces aligned with practical care pathways and human oversight.
related_publications:
  - A systematic review of intermediate fusion in multimodal deep learning for biomedical applications
  - A deep learning approach for overall survival prediction in lung cancer with missing values
  - A graph neural network-based model with out-of-distribution robustness for enhancing antiretroviral therapy outcome prediction for HIV-1
---

<section class="project-profile">
  <div class="project-profile-hero">
    <div class="project-profile-media">
      <img src="{{ page.img }}" alt="{{ page.title }}">
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
        <a class="about-hero-btn about-hero-btn-primary about-inline-btn" href="/publications/">View Publications</a>
        <a class="about-hero-btn about-hero-btn-secondary" href="/projects/">Back to Projects <span aria-hidden="true">&rarr;</span></a>
      </div>
    </div>
  </div>

  <div class="project-profile-grid">
    <div class="project-profile-section">
      <h2>Overview</h2>
      <p>
        This project line develops machine learning methods for clinically relevant risk stratification, combining multimodal evidence sources to support decision-making in complex medical settings. It focuses on model robustness, interpretability, and practical integration into translational research workflows.
      </p>
      <p>
        The programme spans data fusion, longitudinal modelling, and predictive analytics, with attention to deployment constraints such as missing values, heterogeneous cohorts, and human-in-the-loop decision support.
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
        <h3>Team</h3>
        <ul class="project-profile-list">
          {% for person in page.team %}
            {% assign team_member = site.data.team | where: "name", person | first %}
            <li>
              {% if team_member and team_member.profile_path %}
                <a href="{{ team_member.profile_path }}">{{ person }}</a>
              {% else %}
                {{ person }}
              {% endif %}
            </li>
          {% endfor %}
        </ul>
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
    <div class="about-publications-list">
      {% for publication in page.related_publications %}
        <article class="about-publication-item">
          <p class="about-publication-citation">
            <a href="/publications/">{{ publication }}</a>
          </p>
        </article>
      {% endfor %}
    </div>
  </div>
</section>
