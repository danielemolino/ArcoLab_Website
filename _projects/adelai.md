---
layout: page
title: "ADELAI"
full_title: "Alzheimer’s DiseasE Longitudinal study with Artificial Intelligence"
permalink: "/projects/adelai/"
description: "ADELAI collects longitudinal data from patients with dementia during routine neurological assessments. The collected data include clinical history, neurological examinations, neuropsychological test results, and patients’ written and spoken responses to structured questions. Digital interaction data, including keystroke press and release timing, are also acquired. These heterogeneous data are used to develop and evaluate AI models capable of identifying patterns associated with cognitive impairment and disease progression, with the long-term goal of enabling continuous, non-invasive monitoring approaches."
img: "/assets/projects/adelai.png"
project_state: "active"
project_type: "Technology Transfer"
timeline: "2025"
grant_number: ""
official_page: ""
focus_areas:
  - "Missing Modalities"
  - "Multimodal Telemonitoring"
  - "Neurodegenerative Disease"
collaborators:
  - "Università Campus Bio-Medico di Roma"
  - "Fondazione Policlinico Universitàrio Campus Bio-Medico"
highlights:
  - "Development and validation of artificial intelligence methods for dementia, with a focus on multimodal learning, missing modalities, longitudinal disease modeling, early diagnosis, prognosis, and non-invasive patient monitoring. Research activities include the integration of clinical, neuropsychological, speech, and keystroke dynamics data, as well as the exploration of machine learning, deep learning, and foundation models."
project_filter: "adelai"
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
        {% if page.official_page and page.official_page != '' %}
          <a class="about-hero-btn about-hero-btn-secondary" href="{{ page.official_page }}" target="_blank" rel="noopener">Official Project Page <span aria-hidden="true">&rarr;</span></a>
        {% endif %}
        <a class="about-hero-btn about-hero-btn-secondary" href="{{ '/projects/' | relative_url }}">Back to Projects <span aria-hidden="true">&rarr;</span></a>
      </div>
    </div>
  </div>

  <div class="project-profile-grid">
    <div class="project-profile-section">
      <h2>Overview</h2>
      <p>ADELAI is a longitudinal study aimed at collecting real-world clinical and behavioral data from patients with dementia. The study investigates the potential of artificial intelligence to support the diagnosis, prognosis, and longitudinal monitoring of cognitive decline through non-invasive and multimodal data collected during routine neurological visits.</p>
    </div>

    <aside class="project-profile-panel">
      {% if page.timeline and page.timeline != '' %}
        <div class="project-profile-panel-block">
          <h3>Timeline</h3>
          <p>{{ page.timeline }}</p>
        </div>
      {% endif %}
      {% if page.grant_number and page.grant_number != '' %}
        <div class="project-profile-panel-block">
          <h3>Grant</h3>
          <p>{{ page.grant_number }}</p>
        </div>
      {% endif %}
      {% if page.collaborators and page.collaborators != empty %}
        <div class="project-profile-panel-block">
          <h3>Collaborators</h3>
          <ul class="project-profile-list">
            {% for organization in page.collaborators %}
              <li>{{ organization }}</li>
            {% endfor %}
          </ul>
        </div>
      {% endif %}
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
