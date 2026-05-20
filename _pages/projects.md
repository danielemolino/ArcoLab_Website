---
layout: page
title: Projects
permalink: /projects/
description: Research projects and applied AI initiatives at Arco Lab.
nav: true
nav_order: 2
---

{% assign sorted_projects = site.data.projects | sort: "title" %}
{% assign active_projects = sorted_projects | where: "project_state", "active" %}
{% assign ended_projects = sorted_projects | where: "project_state", "ended" %}

<section class="page-hero page-hero-projects">
  <div class="page-hero-copy">
    <p class="page-hero-kicker">Research Portfolio</p>
    <h1>Projects</h1>
    <p class="page-hero-lead">
      Arco Lab develops projects spanning medical imaging, multimodal clinical data analysis, and decision-support systems. Each project page gathers the core context, involved researchers, and related outputs in a format ready to scale to larger funded initiatives.
    </p>
    <div class="member-profile-links">
      <a class="about-hero-btn about-hero-btn-primary about-inline-btn" href="{{ '/team/' | relative_url }}">Meet the team</a>
      <a class="about-hero-btn about-hero-btn-secondary" href="{{ '/contact/' | relative_url }}">Discuss a collaboration <span aria-hidden="true">&rarr;</span></a>
    </div>
  </div>
  <aside class="page-hero-panel">
    <div class="page-hero-metric">
      <span class="page-hero-metric-value">{{ active_projects | size }}</span>
      <span class="page-hero-metric-label">Active projects</span>
    </div>
  </aside>
</section>

{% if active_projects.size > 0 %}

  <section class="about-section">
    <div class="about-section-heading">
      <h2>Active Projects</h2>
      <p class="about-section-kicker">Current Research Lines</p>
    </div>
    <div class="about-project-grid">
      {% for project in active_projects %}
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
  </section>
{% endif %}

{% if ended_projects.size > 0 %}

  <section class="about-section about-section-last">
    <div class="about-section-heading">
      <h2>Completed Projects</h2>
      <p class="about-section-kicker">Completed Initiatives</p>
    </div>
    <div class="about-project-grid">
      {% for project in ended_projects %}
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
  </section>
{% endif %}

{% if active_projects.size == 0 and ended_projects.size == 0 %}

  <p>No projects are available yet.</p>
{% endif %}
