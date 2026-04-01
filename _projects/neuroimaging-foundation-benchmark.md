---
layout: page
title: Neuroimaging Foundation Benchmark
permalink: /projects/neuroimaging-foundation-benchmark/
description: Placeholder completed project on benchmark design, evaluation protocols, and foundation model assessment for neuroimaging tasks.
img: /assets/img/5.jpg
importance: 7
project_state: ended
category: benchmarking
project_type: Medical Imaging
status: Completed in December 2023
timeline: 2022-2023
team:
  - Ermanno Cordelli
  - Filippo Ruffini
focus_areas:
  - Neuroimaging
  - Foundation Models
  - Benchmarking
collaborators:
  - Università Campus Bio-Medico di Roma
  - Research imaging partners
highlights:
  - Placeholder direction on systematic benchmarking for foundation models.
  - Placeholder direction on reproducible evaluation design.
  - Placeholder direction on lessons transferred to later imaging projects.
project_filter: neuroimaging-foundation-benchmark
---

{% assign project_publications = site.data.publications | where_exp: "item", "item.projects contains page.project_filter" %}

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
        <a class="about-hero-btn about-hero-btn-primary about-inline-btn" href="/publications/?project={{ page.project_filter | url_encode }}">View Publications</a>
        <a class="about-hero-btn about-hero-btn-secondary" href="/projects/">Back to Projects <span aria-hidden="true">&rarr;</span></a>
      </div>
    </div>
  </div>

  <div class="project-profile-grid">
    <div class="project-profile-section">
      <h2>Overview</h2>
      <p>Placeholder copy for a completed project dedicated to benchmarking, comparative evaluation, and reporting protocols for neuroimaging and representation-learning models.</p>
      <p>Placeholder copy on how this line informed later work on robust validation and deployment realism.</p>
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
                  <a href="/publications/?project={{ page.project_filter | url_encode }}" class="btn btn-sm z-depth-0" role="button">Browse Publications</a>
                </div>
              </div>
            </div>
          </li>
        </ol>
      </div>
    {% endif %}
  </div>
</section>
