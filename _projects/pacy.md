---
layout: page
title: "PACY"
full_title: "Pro-Active Cybersecurity"
permalink: "/projects/pacy/"
description: "AI-driven web application for identifying cyber vulnerabilities and recommending real-time mitigation strategies for SMEs."
img: "/assets/projects/pacy-google-org.jpg"
project_state: "active"
project_type: "Google.org Impact Challenge"
timeline: "2024-2026"
grant_number: "Google.org Grant Proposal"
official_page: "https://impactchallenge.withgoogle.com/techforsocialgood/funding/politecnico-milano-e-campus-biomedico-roma"
focus_areas:
  - "Cybersecurity"
  - "SME Support"
  - "AI Decision Support"
collaborators:
  - "Google.org"
  - "Politecnico di Milano"
  - "Universita Campus Bio-Medico di Roma"
highlights:
  - "AI-driven web app for identifying cyber vulnerabilities and gaps."
  - "Real-time mitigation recommendations for SMEs facing digital threats."
  - "Integration with cybersecurity education and hands-on support activities."
project_filter: "pacy"
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
      <p>PACY is the Pro-Active Cybersecurity platform developed in the context of the Google.org Impact Challenge: Tech for Social Good 2023. The initiative joins Politecnico di Milano and Universita Campus Bio-Medico di Roma to support SMEs with AI-based cybersecurity assistance.</p>
      <p>The platform identifies cyber vulnerabilities, highlights protection gaps, and recommends real-time mitigation strategies. The local proposal also describes Operational Technology cybersecurity assessment through time-varying Bayesian models and decision-support methods.</p>
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
