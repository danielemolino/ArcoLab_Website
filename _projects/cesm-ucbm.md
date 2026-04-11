---
layout: page
title: CESM@UCBM
permalink: /projects/cesm-ucbm/
description: Deep generative modelling for virtual contrast enhancement in spectral mammography, supported by a publicly released in-house CESM dataset.
img: /assets/projects/cesm-vce.png
importance: 5
project_state: active
category: generative-medical-imaging
project_type: Clinical Application
status: Dataset and study available
timeline: 2021-2024 dataset programme
focus_areas:
  - Generative AI
  - Mammography
  - Dataset Curation
collaborators:
  - Università Campus Bio-Medico di Roma
  - Fondazione Policlinico Universitario Campus Bio-Medico
highlights:
  - Virtual contrast enhancement from low-energy images only, reducing reliance on contrast medium and double acquisition.
  - Public release of a 1138-image CESM dataset with imaging and clinical annotations.
  - Comparative evaluation of autoencoder, Pix2Pix, and CycleGAN approaches with radiologist assessment.
project_filter: cesm-ucbm
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
        CESM@UCBM studies virtual contrast enhancement in contrast-enhanced spectral mammography. The central technical goal is to generate synthetic recombined images from low-energy acquisitions only, preserving the clinical value of CESM while reducing the burden associated with contrast administration and higher radiation exposure.
      </p>
      <p>
        The project is also a data resource effort. It released a curated in-house dataset of 1138 CESM images collected at the Fondazione Policlinico Universitario Campus Bio-Medico, with acquisition metadata and lesion-related annotations that support reproducible research on generative models and breast imaging analysis.
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
