---
layout: page
title: "BISTOURY"
full_title: "3D-guided roBotIc Surgery based on advanced navigaTiOn systems and aUgmented viRtual realitY"
permalink: "/projects/bistoury/"
description: "AI, augmented virtual reality, and navigation methods for 3D-guided robotic surgery."
img: "/assets/projects/bistoury-overview.png"
project_state: "ended"
project_type: "Cascade Funding Project"
timeline: "2024-2025"
grant_number: "HEAL Italia Spoke 2 - Intelligent Health"
official_page: "https://www.healitalia.eu/intelligent-health/"
focus_areas:
  - "Robotic Surgery"
  - "Augmented Virtual Reality"
  - "3D Reconstruction"
collaborators:
  - "Universita Campus Bio-Medico di Roma"
  - "Teleconsys"
  - "Fondazione Policlinico Universitario Campus Bio-Medico"
highlights:
  - "Preoperative 3D model reconstruction from CT and MRI scans."
  - "Intraoperative 3D reconstruction and alignment of the surgical scene."
  - "AI-enabled augmented virtual reality for perception, navigation, and surgeon support."
project_filter: "bistoury"
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
      <p>BISTOURY proposes an integrated system for robotic surgery based on minimally invasive robotic surgery, augmented virtual reality, and AI methods. The goal is to enhance the surgeon&#x27;s perception of anatomical structures and provide intraoperative support for decision-making and navigation.</p>
      <p>The project combines preoperative 3D model reconstruction, intraoperative scene reconstruction, alignment, visual instructions, haptic feedback, and compatibility with robotic surgical systems.</p>
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
