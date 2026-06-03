---
layout: page
permalink: /team/
title: Team
description: Research staff and collaborators at Arco Lab.
nav: true
nav_order: 1
---

<section class="page-hero page-hero-team">
  <div class="page-hero-copy">
    <p class="page-hero-kicker">People</p>
    <h1>Team</h1>
    <p class="page-hero-lead">
      Arco Lab brings together researchers working across artificial intelligence, biomedical engineering, and clinically grounded computational research. Each profile collects current roles, research interests, and selected outputs.
    </p>
    <div class="member-profile-links">
      <a class="about-hero-btn about-hero-btn-primary about-inline-btn" href="{{ '/contact/' | relative_url }}">Get in touch</a>
      <a class="about-hero-btn about-hero-btn-secondary" href="{{ '/publications/' | relative_url }}">Browse publications <span aria-hidden="true">&rarr;</span></a>
    </div>
  </div>
  <aside class="page-hero-panel">
    <div class="page-hero-metric">
      <span class="page-hero-metric-value">{{ site.data.team | size }}</span>
      <span class="page-hero-metric-label">Current profiles</span>
    </div>
  </aside>
</section>

{% assign team_members = site.data.team | sort: "order" %}
{% assign role_sections = "pi|PI,senior_staff|Senior Staff,researchers|Researchers,phd|PhD" | split: "," %}

{% for section in role_sections %}
{% assign parts = section | split: "|" %}
{% assign role_key = parts[0] %}
{% assign role_label = parts[1] %}
{% assign section_members = team_members | where: "role", role_key %}
{% if section_members.size > 0 %}

<section class="team-role-group">
  <div class="team-role-heading">
    <div>
      <h2>{{ role_label }}</h2>
    </div>
    <span class="team-role-count">{{ section_members.size }}</span>
  </div>

  <div class="about-team-grid">
    {% for member in section_members %}
    <article
      class="about-team-card about-team-card-clickable"
      onclick="window.location.href='{{ member.profile_path | relative_url }}'"
      onkeydown="if(event.key === 'Enter'){ window.location.href='{{ member.profile_path | relative_url }}'; }"
      role="link"
      tabindex="0"
      aria-label="View {{ member.name }} profile"
    >
      <img src="{{ member.photo | relative_url }}" alt="{{ member.name }}">
      <div class="about-team-body">
        <div class="about-team-card-header">
          <span class="about-team-role-badge">{{ member.role_label }}</span>
        </div>
        <h3>{{ member.name }}</h3>
        {% if member.affiliation %}
        <p class="about-team-role">{{ member.affiliation }}</p>
        {% elsif member.title %}
        <p class="about-team-role">{{ member.title }}</p>
        {% endif %}
        <div class="about-team-links">
          {% if member.scholar_url and member.scholar_url contains 'scholar.google.' %}
          <a class="about-team-action-link" href="{{ member.scholar_url }}" aria-label="Google Scholar" title="Google Scholar" onclick="event.preventDefault(); event.stopPropagation(); window.location.href=this.href;"><i class="fa-solid fa-graduation-cap"></i></a>
          {% endif %}
          <a class="about-team-action-link" href="{{ '/publications/' | relative_url }}?search={{ member.name | url_encode }}" aria-label="Filter publications by {{ member.name }}" title="Publications by {{ member.name }}" onclick="event.preventDefault(); event.stopPropagation(); window.location.href=this.href;"><i class="fa-solid fa-book-open"></i></a>
          {% if member.email %}
          <a class="about-team-action-link" href="mailto:{{ member.email }}" aria-label="Email {{ member.name }}" title="Email {{ member.name }}" onclick="event.preventDefault(); event.stopPropagation(); window.location.href=this.href;"><i class="fa-regular fa-envelope"></i></a>
          {% else %}
          <a class="about-team-action-link" href="{{ '/contact/' | relative_url }}" aria-label="Contact" title="Contact" onclick="event.preventDefault(); event.stopPropagation(); window.location.href=this.href;"><i class="fa-regular fa-envelope"></i></a>
          {% endif %}
        </div>
        <span class="about-team-profile-link">Open profile <span aria-hidden="true">&rarr;</span></span>
      </div>
    </article>
    {% endfor %}
  </div>
</section>
{% endif %}
{% endfor %}

{% assign alumni_members = team_members | where: "role", "phd_alumni" %}
{% if alumni_members.size > 0 %}

<section class="team-role-group team-alumni-group">
  <details class="team-alumni-details">
    <summary class="team-alumni-summary">View PhD Alumni</summary>
    <div class="team-role-heading">
      <div>
        <h2>PhD Alumni</h2>
      </div>
      <span class="team-role-count">{{ alumni_members.size }}</span>
    </div>

    <div class="about-team-grid">
      {% for member in alumni_members %}
      <article
        class="about-team-card about-team-card-clickable"
        onclick="window.location.href='{{ member.profile_path | relative_url }}'"
        onkeydown="if(event.key === 'Enter'){ window.location.href='{{ member.profile_path | relative_url }}'; }"
        role="link"
        tabindex="0"
        aria-label="View {{ member.name }} profile"
      >
        <img src="{{ member.photo | relative_url }}" alt="{{ member.name }}">
        <div class="about-team-body">
          <div class="about-team-card-header">
            <span class="about-team-role-badge">{{ member.role_label }}</span>
          </div>
          <h3>{{ member.name }}</h3>
          {% if member.affiliation %}
          <p class="about-team-role">{{ member.affiliation }}</p>
          {% elsif member.title %}
          <p class="about-team-role">{{ member.title }}</p>
          {% endif %}
          <div class="about-team-links">
            {% if member.scholar_url and member.scholar_url contains 'scholar.google.' %}
            <a class="about-team-action-link" href="{{ member.scholar_url }}" aria-label="Google Scholar" title="Google Scholar" onclick="event.preventDefault(); event.stopPropagation(); window.location.href=this.href;"><i class="fa-solid fa-graduation-cap"></i></a>
            {% endif %}
            <a class="about-team-action-link" href="{{ '/publications/' | relative_url }}?search={{ member.name | url_encode }}" aria-label="Filter publications by {{ member.name }}" title="Publications by {{ member.name }}" onclick="event.preventDefault(); event.stopPropagation(); window.location.href=this.href;"><i class="fa-solid fa-book-open"></i></a>
            {% if member.email %}
            <a class="about-team-action-link" href="mailto:{{ member.email }}" aria-label="Email {{ member.name }}" title="Email {{ member.name }}" onclick="event.preventDefault(); event.stopPropagation(); window.location.href=this.href;"><i class="fa-regular fa-envelope"></i></a>
            {% endif %}
          </div>
          <span class="about-team-profile-link">Open profile <span aria-hidden="true">&rarr;</span></span>
        </div>
      </article>
      {% endfor %}
    </div>

  </details>
</section>
{% endif %}
