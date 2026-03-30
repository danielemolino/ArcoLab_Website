---
layout: page
title: Projects
permalink: /projects/
description: Research projects and applied AI initiatives at Arco Lab.
nav: true
nav_order: 2
---

<section class="page-hero page-hero-projects">
  <div class="page-hero-copy">
    <p class="page-hero-kicker">Research Portfolio</p>
    <h1>Projects</h1>
    <p class="page-hero-lead">
      Arco Lab develops projects spanning medical imaging, multimodal clinical data analysis, and decision-support systems. Each project page gathers the core context, involved researchers, and related outputs in a format ready to scale to larger funded initiatives.
    </p>
    <div class="member-profile-links">
      <a class="about-hero-btn about-hero-btn-primary about-inline-btn" href="/team/">Meet the team</a>
      <a class="about-hero-btn about-hero-btn-secondary" href="/contact/">Discuss a collaboration <span aria-hidden="true">&rarr;</span></a>
    </div>
  </div>
  <aside class="page-hero-panel">
    <div class="page-hero-metric">
      <span class="page-hero-metric-value">{{ site.projects | size }}</span>
      <span class="page-hero-metric-label">Structured project pages</span>
    </div>
    <div class="page-hero-metric">
      <span class="page-hero-metric-value">Translational</span>
      <span class="page-hero-metric-label">From methods to clinical deployment</span>
    </div>
  </aside>
</section>

{% assign sorted_projects = site.projects | sort: "importance" %}
{% if sorted_projects.size > 0 %}
  <div class="about-project-grid">
    {% for project in sorted_projects %}
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
          <div class="about-project-story-strip">
            <span>Challenge</span>
            <span>Approach</span>
            <span>Outputs</span>
          </div>
          <h3>{{ project.title }}</h3>
          <p>{{ project.description }}</p>
          <div class="about-project-meta">
            {% if project.team %}
              <span><i class="fa-regular fa-user"></i> {{ project.team | size }} team members</span>
            {% endif %}
            {% if project.timeline %}
              <span><i class="fa-regular fa-calendar"></i> {{ project.timeline }}</span>
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
{% else %}
  <p>No projects are available yet.</p>
{% endif %}
