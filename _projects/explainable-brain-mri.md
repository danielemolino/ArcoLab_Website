---
layout: page
title: Explainable AI for Brain MRI Analysis
permalink: /projects/explainable-brain-mri/
description: Translational research on trustworthy neuroimaging AI for quantitative analysis, uncertainty estimation, and clinical interpretability.
img: /assets/img/10.jpg
importance: 1
category: medical-imaging
project_type: Medical Imaging
status: Ongoing
timeline: 2024-present
team:
  - Paolo Soda
  - Valerio Guarrasi
focus_areas:
  - Brain MRI
  - Explainability
  - Trustworthy AI
collaborators:
  - Campus Bio-Medico University of Rome
  - Clinical imaging partners
highlights:
  - Robust modelling pipelines for structural and multimodal MRI analysis.
  - Interpretable representations to support clinical understanding and trust.
  - Validation strategies focused on generalization, uncertainty, and translational usability.
related_publications:
  - Multimodal explainability via latent shift applied to COVID-19 stratification
  - LatentAugment: Data Augmentation via Guided Manipulation of GAN's Latent Space
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
        <a class="about-hero-btn about-hero-btn-primary about-inline-btn" href="/team/">Meet the Team</a>
        <a class="about-hero-btn about-hero-btn-secondary" href="/projects/">Back to Projects <span aria-hidden="true">&rarr;</span></a>
      </div>
    </div>
  </div>

  <div class="project-profile-grid">
    <div class="project-profile-section">
      <h2>Overview</h2>
      <p>
        This project investigates clinically meaningful artificial intelligence for brain MRI analysis, combining representation learning, multimodal modelling, and explainability-aware evaluation. The goal is to support diagnostic and prognostic workflows with systems that remain technically robust while being intelligible to clinical stakeholders.
      </p>
      <p>
        The work integrates methodological research on data efficiency and interpretability with application-driven validation on imaging tasks where reliability and transparency are essential for translational adoption.
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
