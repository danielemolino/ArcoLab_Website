---
layout: page
title: "Cyber ACN"
full_title: "Sicurezza dei dati medici: strumenti di Intelligenza Artificiale Generativa per la condivisione e l'anonimizzazione sicura dei dati"
permalink: "/projects/cyber-acn/"
description: "Generative AI research for secure medical data sharing, anonymisation, synthetic datasets, and adversarial robustness."
img: "/assets/projects/cybersecurity-health-data.png"
project_state: "active"
project_type: "Cybersecurity Research"
timeline: ""
grant_number: ""
official_page: ""
focus_areas:
  - "Synthetic Medical Data"
  - "Privacy-Preserving AI"
  - "Cybersecurity"
collaborators:
  - "Bracco Imaging"
  - "Eustema"
  - "Centro Diagnostico Italiano"
  - "Fondazione Policlinico Universitario Campus Bio-Medico"
highlights:
  - "Generative models for synthetic medical datasets that support secure sharing."
  - "Adversarial training, penetration testing, and model hardening against cyber threats."
  - "Differential privacy and benchmark workflows for privacy-preserving medical AI."
project_filter: "cyber-acn"
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
      <p>Cyber ACN studies secure medical data sharing through generative artificial intelligence. The project material focuses on synthetic medical data, anonymisation, and robust AI pipelines that can support collaboration while reducing exposure of sensitive data.</p>
      <p>The research plan includes adversarial robustness, model hardening, penetration testing, differential privacy, and benchmarks for evaluating the security of generative medical AI systems.</p>
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
