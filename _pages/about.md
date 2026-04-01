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
      Arco Lab advances applied artificial intelligence for medicine at Università Campus Bio-Medico di Roma, with research spanning medical imaging, clinical data analysis, and decision support systems.
    </p>

    <div class="about-hero-actions">
      <a class="about-hero-btn about-hero-btn-primary" href="/team/">
        <i class="fa-solid fa-users"></i>
        <span>Meet the Team</span>
      </a>
      <a class="about-hero-btn about-hero-btn-primary" href="/publications/">
        <i class="fa-solid fa-book-open"></i>
        <span>View Publications</span>
      </a>
      <a class="about-hero-btn about-hero-btn-primary" href="/projects/">
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

<section class="about-section about-section-featured-project">
  <div class="about-featured-project-panel">
    <div class="about-featured-project-copy">
      <p class="about-section-kicker">Featured Project Lens</p>
      <h2>Designing multimodal systems that stay useful under real clinical constraints</h2>
      <p class="about-section-copy">
        Our project portfolio focuses on models that combine data modalities, remain interpretable to domain experts, and preserve performance when data quality, missing values, or deployment conditions change.
      </p>
      <div class="about-featured-project-points">
        <span><i class="fa-solid fa-wave-square"></i> Multimodal inputs</span>
        <span><i class="fa-solid fa-shield-heart"></i> Robust evaluation</span>
        <span><i class="fa-solid fa-user-doctor"></i> Clinical usability</span>
      </div>
      <a class="about-hero-btn about-hero-btn-primary about-inline-btn" href="/projects/">
        <span>Open Project Portfolio</span>
        <i class="fa-solid fa-arrow-right"></i>
      </a>
    </div>
    <div class="about-featured-project-stack">
      <article class="about-featured-project-card">
        <span class="about-featured-project-step">Clinical Challenge</span>
        <h3>Fragmented and heterogeneous medical data</h3>
        <p>Real healthcare workflows rarely offer clean, balanced, single-modality datasets.</p>
      </article>
      <article class="about-featured-project-card">
        <span class="about-featured-project-step">Arco Approach</span>
        <h3>Joint modelling, explainability, and robustness</h3>
        <p>We design methods that stay intelligible and reliable while handling complexity.</p>
      </article>
    </div>
  </div>
</section>

<section class="about-section">
  <div class="about-section-heading">
    <h2>Active Research Projects</h2>
  </div>

  {% assign featured_projects = site.projects | sort: "importance" %}
  <div class="about-project-rail" aria-label="Active research projects">
    {% for project in featured_projects limit: 5 %}
      <article
        class="about-project-card about-project-card-clickable"
        onclick="window.location.href='{{ project.url }}'"
        onkeydown="if(event.key === 'Enter'){ window.location.href='{{ project.url }}'; }"
        role="link"
        tabindex="0"
        aria-label="View {{ project.title }} project"
      >
        <img src="{{ project.img }}" alt="{{ project.title }}">
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
          <a class="about-project-link" href="{{ project.url }}" onclick="event.stopPropagation()">Open project page <span aria-hidden="true">&rarr;</span></a>
        </div>
      </article>
    {% endfor %}
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
      <a class="about-hero-btn about-hero-btn-primary about-inline-btn" href="/team/">
        <span>Open Team Page</span>
        <i class="fa-solid fa-arrow-right"></i>
      </a>
    </div>
    <div class="about-split-media">
      <img src="/assets/img/12.jpg" alt="Team presentation placeholder">
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
