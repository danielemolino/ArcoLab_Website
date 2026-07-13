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
      <a class="about-hero-btn about-inline-btn news-linkedin-btn" href="https://www.linkedin.com/company/arco-unicampus/" target="_blank" rel="noopener">
        <i class="fa-brands fa-linkedin" aria-hidden="true"></i>
        <span>Follow us on LinkedIn!</span>
      </a>
    </div>

  </div>
</section>

<section class="about-section about-section-flagship">
  <div class="about-flagship-panel">
    <div class="about-flagship-copy">
      <p class="about-section-kicker">Research Areas</p>
      <h2>Research areas from intelligent methods to real-world translation</h2>
    </div>

    <div class="about-focus-grid">
      <article class="about-focus-card about-focus-card-research-area">
        <div class="about-focus-visual about-focus-visual-pink">
          <i class="fa-solid fa-brain"></i>
        </div>
        <div class="about-focus-body">
          <h3>Artificial Intelligence</h3>
          <p>
            We develop AI methods for multimodal data, generative modelling, time-series analysis, and decision support, with attention to robustness, interpretability, and explainability.
          </p>
          <div class="about-focus-tags">
            <span>Generative AI</span>
            <span>Multimodal AI</span>
            <span>Deep Learning</span>
          </div>
        </div>
      </article>

      <article class="about-focus-card about-focus-card-research-area">
        <div class="about-focus-visual about-focus-visual-green">
          <i class="fa-solid fa-microchip"></i>
        </div>
        <div class="about-focus-body">
          <h3>Computer Systems</h3>
          <p>
            We design and optimize computing systems that bring intelligence close to sensors and devices, including embedded platforms, IoT architectures, edge computing, and performance-aware AI deployment.
          </p>
          <div class="about-focus-tags">
            <span>Embedded Systems</span>
            <span>Edge AI</span>
            <span>IoT</span>
          </div>
        </div>
      </article>

      <article class="about-focus-card about-focus-card-research-area">
        <div class="about-focus-visual about-focus-visual-cyan">
          <i class="fa-solid fa-wave-square"></i>
        </div>
        <div class="about-focus-body">
          <h3>Control & Dynamical Systems</h3>
          <p>
            We develop control and estimation methods for networked and dynamical systems, including distributed filtering, consensus algorithms, nonlinear dynamics modelling, and adaptive biomedical control.
          </p>
          <div class="about-focus-tags">
            <span>Networked Control</span>
            <span>Distributed Estimation</span>
            <span>Dynamical Systems</span>
          </div>
        </div>
      </article>

      <article class="about-focus-card about-focus-card-research-area">
        <div class="about-focus-visual about-focus-visual-blue">
          <i class="fa-solid fa-layer-group"></i>
        </div>
        <div class="about-focus-body">
          <h3>Applications</h3>
          <p>
            We apply AI and system-level methods across healthcare, industrial processes, agriculture, and data-intensive domains, focusing on reliability, interpretability, and measurable real-world impact.
          </p>
          <div class="about-focus-tags">
            <span>Clinical AI</span>
            <span>Agriculture</span>
            <span>Industry 4.0</span>
          </div>
        </div>
      </article>

      <article class="about-focus-card about-focus-card-research-area about-focus-card-translation">
        <div class="about-focus-visual about-focus-visual-amber">
          <i class="fa-solid fa-arrows-turn-to-dots"></i>
        </div>
        <div class="about-focus-body">
          <h3>Translation</h3>
          <p>
            We support the translation of research into operational solutions, working with companies, institutions, and clinical partners to prototype, validate, and deploy data-driven technologies.
          </p>
          <div class="about-focus-tags">
            <span>Technology Transfer</span>
            <span>Prototyping</span>
            <span>Validation</span>
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

{% assign featured_projects = site.data.projects | where: "project_state", "active" | sort: "title" %}

  <div class="about-project-rail-shell">
    <div class="about-project-rail" aria-label="Active research projects">
      {% for project in featured_projects %}
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
            <h3>{{ project.title }}</h3>
            <p>{{ project.full_title | default: project.title }}</p>
            <div class="about-project-meta">
              {% if project.collaborators %}
                <span><i class="fa-regular fa-handshake"></i> {{ project.collaborators | size }} collaborators</span>
              {% endif %}
              {% if project.timeline %}
                {% assign clean_timeline = project.timeline | remove: " dataset programme" | remove: " Dataset Programme" %}
                <span><i class="fa-regular fa-calendar"></i> {{ clean_timeline }}</span>
              {% endif %}
            </div>
            <a class="about-project-link" href="{{ project.url | relative_url }}" onclick="event.stopPropagation()">Open project page <span aria-hidden="true">&rarr;</span></a>
          </div>
        </article>
      {% endfor %}
    </div>
  </div>
  <div class="about-project-rail-controls" aria-label="Project portfolio and scroll controls">
    <button type="button" class="about-project-rail-control about-project-rail-control-left" data-project-rail-direction="prev" aria-label="Scroll projects left">
      <span class="about-project-rail-arrow about-project-rail-arrow-left" aria-hidden="true">
        <svg viewBox="0 0 24 24" focusable="false" aria-hidden="true">
          <path d="M14.5 5.5L8 12l6.5 6.5" />
        </svg>
      </span>
    </button>
    <a class="about-hero-btn about-hero-btn-primary about-inline-btn about-project-rail-main" href="{{ '/projects/' | relative_url }}">
      <i class="fa-solid fa-diagram-project"></i>
      <span>Open Project Portfolio</span>
    </a>
    <button type="button" class="about-project-rail-control about-project-rail-control-right" data-project-rail-direction="next" aria-label="Scroll projects right">
      <span class="about-project-rail-arrow about-project-rail-arrow-right" aria-hidden="true">
        <svg viewBox="0 0 24 24" focusable="false" aria-hidden="true">
          <path d="M9.5 5.5L16 12l-6.5 6.5" />
        </svg>
      </span>
    </button>
  </div>
</section>

<section class="about-section about-section-alt">
  <div class="about-split about-split-reverse">
    <div class="about-split-copy">
      <h2>Meet the Research Group</h2>
      <p>
        ArCo Lab is built on multidisciplinary collaboration among computer engineers, biomedical engineers, data scientists, postdocs, PhD students, researchers, and professors, combining methodological depth with clinical and applied perspectives.
      </p>
      <a class="about-hero-btn about-hero-btn-primary about-inline-btn" href="{{ '/team/' | relative_url }}">
        <span>Open Team Page</span>
        <i class="fa-solid fa-arrow-right"></i>
      </a>
    </div>
    <div class="about-split-media">
      {% assign home_team_photo = site.static_files | where: "path", "/assets/team_photos/arco.jpg" | first %}
      {% if home_team_photo %}
        <img src="{{ '/assets/team_photos/arco.jpg' | relative_url }}" alt="ArCo Lab team">
      {% else %}
        <img src="{{ '/assets/team_photos/arco_lab_group.jpg' | relative_url }}" alt="ArCo Lab team">
      {% endif %}
    </div>
  </div>
</section>

<section class="about-section about-section-last">
  <div class="about-section-heading">
    <h2>Recent Publications</h2>
  </div>

{% include recent_publications.liquid %}

  <div class="about-section-actions">
    <a class="about-hero-btn about-hero-btn-primary about-inline-btn" href="{{ '/publications/' | relative_url }}">
      <i class="fa-solid fa-book-open"></i>
      <span>View Publications</span>
    </a>
  </div>

</section>
