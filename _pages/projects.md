---
layout: page
title: Projects
permalink: /projects/
description: Research projects and applied AI initiatives at Arco Lab.
nav: true
nav_order: 2
---

Arco Lab develops research initiatives spanning medical imaging, multimodal clinical data analysis, and decision-support systems, with each project page collecting the core context, team, and related outputs.

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
          <a class="about-project-link" href="{{ project.url }}" onclick="event.stopPropagation()">Open project <span aria-hidden="true">&rarr;</span></a>
        </div>
      </article>
    {% endfor %}
  </div>
{% else %}
  <p>No projects are available yet.</p>
{% endif %}
