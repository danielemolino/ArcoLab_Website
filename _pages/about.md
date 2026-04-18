---
layout: about
title: Home
permalink: /
subtitle:

selected_papers: false # includes a list of papers marked as "selected={true}"
social: false # includes social icons at the bottom of the page

announcements:
  enabled: false # includes a list of news items
  scrollable: true # adds a vertical scroll bar if there are more than 3 news items
  limit: 5 # leave blank to include all the news in the `_news` folder

latest_posts:
  enabled: false
  scrollable: true # adds a vertical scroll bar if there are more than 3 new posts items
  limit: 3 # leave blank to include all the blog posts
---

<section class="about-hero">
  <div class="about-hero-inner">
    <div class="about-hero-title-shell">
      <img class="about-hero-logo-static" src="{{ '/assets/branding/arco/lockup/logo_arco_cb.png' | relative_url }}" alt="ArCo Lab">
    </div>

    <p class="about-hero-lead">
      ArCo at Università Campus Bio-Medico di Roma specializes in artificial intelligence research, with applications spanning medicine, industrial and environmental monitoring, energy management, and digital twins. Established in 2004, the lab develops AI-driven methodologies including multimodal learning, AI resilience, and computer vision, with a strong focus on oncology, connected health, medical records, and biomedical signals.
    </p>

    <div class="about-hero-actions">
      <a class="about-hero-btn about-hero-btn-primary" href="{{ '/team/' | relative_url }}">
        <i class="fa-solid fa-users"></i>
        <span>Meet the Team</span>
      </a>
      <a class="about-hero-btn about-hero-btn-primary" href="{{ '/publications/' | relative_url }}">
        <i class="fa-solid fa-book-open"></i>
        <span>View Publications</span>
      </a>
      <a class="about-hero-btn about-hero-btn-primary" href="{{ '/projects/' | relative_url }}">
        <i class="fa-solid fa-diagram-project"></i>
        <span>Explore Projects</span>
      </a>
    </div>

  </div>
</section>

<section class="about-section about-section-flagship">
  <div class="about-flagship-panel">
    <div class="about-flagship-copy">
      <p class="about-section-kicker">Research Areas</p>
      <h2>Research areas spanning method design, clinical translation, and industrial impact</h2>
      <p class="about-section-copy">
        ArCo Lab develops applied artificial intelligence across a connected pipeline: foundational model design, clinically grounded validation, and deployment-oriented solutions for industrial and agricultural settings.
      </p>
    </div>

    <div class="about-focus-grid">
      <article class="about-focus-card about-focus-card-research-area">
        <div class="about-focus-visual about-focus-visual-pink">
          <i class="fa-solid fa-brain"></i>
          <span class="about-focus-status">Core Area</span>
        </div>
        <div class="about-focus-body">
          <h3>Generative and Deep Learning Architecture for Medical Image Synthesis and Analysis</h3>
          <p>
            Placeholder copy: this area covers model design for image synthesis, reconstruction, multimodal representation learning, and analysis pipelines aimed at robust biomedical imaging workflows.
          </p>
          <div class="about-focus-tags">
            <span>Generative AI</span>
            <span>Medical Imaging</span>
            <span>Deep Architectures</span>
          </div>
        </div>
      </article>

      <article class="about-focus-card about-focus-card-research-area">
        <div class="about-focus-visual about-focus-visual-green">
          <i class="fa-solid fa-user-doctor"></i>
          <span class="about-focus-status">Clinical Area</span>
        </div>
        <div class="about-focus-body">
          <h3>Clinical Application</h3>
          <p>
            Placeholder copy: this area focuses on decision support, multimodal clinical modelling, outcome prediction, and translational validation in real healthcare pathways and patient-facing contexts.
          </p>
          <div class="about-focus-tags">
            <span>Clinical AI</span>
            <span>Decision Support</span>
            <span>Validation</span>
          </div>
        </div>
      </article>

      <article class="about-focus-card about-focus-card-research-area">
        <div class="about-focus-visual about-focus-visual-blue">
          <i class="fa-solid fa-industry"></i>
          <span class="about-focus-status">Applied Area</span>
        </div>
        <div class="about-focus-body">
          <h3>Industrial Application</h3>
          <p>
            Placeholder copy: this area extends lab methods toward industrial use cases, including monitoring, predictive systems, and agriculture-oriented applications where data-driven automation must remain reliable and interpretable.
          </p>
          <div class="about-focus-tags">
            <span>Industry 4.0</span>
            <span>Agriculture</span>
            <span>Applied AI</span>
          </div>
        </div>
      </article>
    </div>

  </div>
</section>

<section class="about-section about-section-projects">
  <div class="about-section-heading">
    <h2>Active Research Projects</h2>
  </div>

{% assign featured_projects = site.projects | where: "project_state", "active" | sort: "importance" %}

  <div class="about-project-rail-shell">
    <button type="button" class="about-project-rail-control about-project-rail-control-left" data-project-rail-direction="prev" aria-label="Scroll projects left">
      <span class="about-project-rail-arrow about-project-rail-arrow-left" aria-hidden="true"></span>
    </button>
    <div class="about-project-rail" aria-label="Active research projects">
      {% assign featured_projects_limited = featured_projects | slice: 0, 5 %}
      {% for project in featured_projects_limited %}
        <article
          class="about-project-card about-project-card-clickable"
          onclick="window.location.href='{{ project.url | relative_url }}'"
          onkeydown="if(event.key === 'Enter'){ window.location.href='{{ project.url | relative_url }}'; }"
          role="link"
          tabindex="0"
          aria-label="View {{ project.title }} project"
        >
          <img src="{{ project.img | relative_url }}" alt="{{ project.title }}">
          <div class="about-project-body">
            {% if project.project_type %}
              <span class="about-project-badge">{{ project.project_type }}</span>
            {% endif %}
            <h3>{{ project.title }}</h3>
            <p>{{ project.description }}</p>
            <div class="about-project-meta">
              {% if project.collaborators %}
                <span><i class="fa-regular fa-handshake"></i> {{ project.collaborators | size }} collaborators</span>
              {% endif %}
              {% if project.status %}
                <span><i class="fa-regular fa-clock"></i> {{ project.status }}</span>
              {% endif %}
            </div>
            <a class="about-project-link" href="{{ project.url | relative_url }}" onclick="event.stopPropagation()">Open project page <span aria-hidden="true">&rarr;</span></a>
          </div>
        </article>
      {% endfor %}
      {% for project in featured_projects_limited %}
        <article
          class="about-project-card about-project-card-clickable"
          onclick="window.location.href='{{ project.url | relative_url }}'"
          onkeydown="if(event.key === 'Enter'){ window.location.href='{{ project.url | relative_url }}'; }"
          role="link"
          tabindex="0"
          aria-label="View {{ project.title }} project"
          aria-hidden="true"
        >
          <img src="{{ project.img | relative_url }}" alt="{{ project.title }}">
          <div class="about-project-body">
            {% if project.project_type %}
              <span class="about-project-badge">{{ project.project_type }}</span>
            {% endif %}
            <h3>{{ project.title }}</h3>
            <p>{{ project.description }}</p>
            <div class="about-project-meta">
              {% if project.collaborators %}
                <span><i class="fa-regular fa-handshake"></i> {{ project.collaborators | size }} collaborators</span>
              {% endif %}
              {% if project.status %}
                <span><i class="fa-regular fa-clock"></i> {{ project.status }}</span>
              {% endif %}
            </div>
            <a class="about-project-link" href="{{ project.url | relative_url }}" onclick="event.stopPropagation()">Open project page <span aria-hidden="true">&rarr;</span></a>
          </div>
        </article>
      {% endfor %}
    </div>
    <button type="button" class="about-project-rail-control about-project-rail-control-right" data-project-rail-direction="next" aria-label="Scroll projects right">
      <span class="about-project-rail-arrow about-project-rail-arrow-right" aria-hidden="true"></span>
    </button>
  </div>
  <div class="about-project-rail-controls" aria-label="Project portfolio link">
    <a class="about-hero-btn about-hero-btn-primary about-inline-btn about-project-rail-main" href="{{ '/projects/' | relative_url }}">
      <i class="fa-solid fa-diagram-project"></i>
      <span>Open Project Portfolio</span>
    </a>
  </div>
</section>

<section class="about-section about-section-alt">
  <div class="about-split about-split-reverse">
    <div class="about-split-copy">
      <h2>Meet the Research Group</h2>
      <p>
        Placeholder copy: ArCo Lab brings together researchers working across artificial intelligence, medicine, engineering, and data-driven decision systems, building a group that spans methodological research, clinical translation, and applied innovation.
      </p>
      <ul class="about-feature-list">
        <li>Placeholder copy on interdisciplinary collaboration across technical and biomedical expertise.</li>
        <li>Placeholder copy on shared research directions, project work, and scientific exchange inside the lab.</li>
        <li>Placeholder copy on training, mentorship, and the growth of PhD students, postdocs, and researchers.</li>
      </ul>
      <a class="about-hero-btn about-hero-btn-primary about-inline-btn" href="{{ '/team/' | relative_url }}">
        <span>Open Team Page</span>
        <i class="fa-solid fa-arrow-right"></i>
      </a>
    </div>
    <div class="about-split-media">
      <img src="{{ '/assets/img/12.jpg' | relative_url }}" alt="Team presentation placeholder">
    </div>
  </div>
</section>

<section class="about-section about-section-last">
  <div class="about-section-heading">
    <h2>Recent Publications</h2>
    <p class="about-section-kicker">Latest Research Outputs</p>
    <p class="about-section-copy">
      This section shows the three most recent publications according to the global bibliography ordering, which is currently sorted by publication year in descending order.
    </p>
  </div>

{% include recent_publications.liquid %}

</section>
