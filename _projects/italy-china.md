---
layout: page
title: Italy-China (2023-2025)
permalink: /projects/italy-china/
description: Bilateral research programme on trustworthy multimodal AI for COVID-19 risk analysis, explainability, and robust validation across imaging and clinical data.
img: /assets/img/6.jpg
importance: 3
project_state: ended
category: clinical-ai
project_type: Collaborative Research
status: Completed in December 2025
timeline: 2023-2025
focus_areas:
  - COVID-19 Prognosis
  - Trustworthy AI
  - Multimodal Learning
collaborators:
  - Università Campus Bio-Medico di Roma
  - Shenzhen University
highlights:
  - Multimodal signatures for severe COVID-19 outcomes using imaging and clinical variables.
  - Explainable AI methods for risk factor analysis and transparent prognostic modelling.
  - Bilateral collaboration joining chest X-ray and chest CT expertise with robust validation protocols.
project_filter: italy-china
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
        The Italy-China programme focused on trustworthy next-generation precision medicine for COVID-19, combining chest X-ray, chest CT, and clinical information to identify patients at risk of severe outcomes. The technical core of the project was multimodal deep learning for richer joint representations under limited and heterogeneous biomedical data.
      </p>
      <p>
        Beyond pure prediction, the programme addressed explainability, counterfactual reasoning, and human-understandable concepts to make AI outputs more useful to physicians, patients, and regulators. The collaboration joined ArCo’s work on multimodal learning and explainable AI with complementary expertise in deep networks and CT-driven risk analysis.
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
