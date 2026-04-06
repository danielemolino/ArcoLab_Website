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
    <div class="page-hero-metric">
      <span class="page-hero-metric-value">AI + Medicine</span>
      <span class="page-hero-metric-label">Interdisciplinary research focus</span>
    </div>
  </aside>
</section>

{% assign team_members = site.data.team | sort: "order" %}
{% assign role_sections = "pi|Principal Investigator,researcher|Researchers,collaborator|Collaborators,postdoc|Post Doc,phd|PhD Candidate" | split: "," %}

{% for section in role_sections %}
{% assign parts = section | split: "|" %}
{% assign role_key = parts[0] %}
{% assign role_label = parts[1] %}
{% assign section_members = team_members | where: "role", role_key %}
{% if section_members.size > 0 %}
<section class="team-role-group">
  <div class="team-role-heading">
    <div>
      <p class="team-role-kicker">People</p>
      <h2>{{ role_label }}</h2>
    </div>
    <span class="team-role-count">{{ section_members.size }}</span>
  </div>

  <div class="about-team-grid">
    {% for member in section_members %}
    <article
      class="about-team-card about-team-card-clickable"
      onclick="window.location.href='{{ member.profile_path }}'"
      onkeydown="if(event.key === 'Enter'){ window.location.href='{{ member.profile_path }}'; }"
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
        {% if member.title %}
        <p class="about-team-role">{{ member.title }}</p>
        {% endif %}
        <p class="about-team-bio">{{ member.short_bio | default: member.bio }}</p>
        {% if member.interests %}
        <div class="about-team-tags">
          {% for interest in member.interests limit: 3 %}
          <span>{{ interest }}</span>
          {% endfor %}
        </div>
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

<section class="team-role-group team-alumni-group">
  <details class="team-alumni-details">
    <summary class="team-alumni-summary">View PhD Alumni</summary>
    <div class="team-role-heading">
      <div>
        <p class="team-role-kicker">People</p>
        <h2>PhD Alumni</h2>
      </div>
      <span class="team-role-count">4</span>
    </div>

    <div class="about-team-grid">
      <article class="about-team-card">
        <img src="{{ '/assets/img/prof_pic_color.png' | relative_url }}" alt="Placeholder PhD alumnus">
        <div class="about-team-body">
          <div class="about-team-card-header">
            <span class="about-team-role-badge">PhD Alumni</span>
          </div>
          <h3>Placeholder Alumna One</h3>
          <p class="about-team-role">Former PhD Candidate in Artificial Intelligence</p>
          <p class="about-team-bio">Placeholder content for a completed PhD profile that can later include thesis topic, current position, and period in the lab.</p>
        </div>
      </article>

      <article class="about-team-card">
        <img src="{{ '/assets/img/prof_pic_color.png' | relative_url }}" alt="Placeholder PhD alumnus">
        <div class="about-team-body">
          <div class="about-team-card-header">
            <span class="about-team-role-badge">PhD Alumni</span>
          </div>
          <h3>Placeholder Alumnus Two</h3>
          <p class="about-team-role">Former PhD Candidate in Biomedical Engineering</p>
          <p class="about-team-bio">Placeholder content for a former doctoral researcher, ready to be replaced by real alumni information and current affiliation.</p>
        </div>
      </article>

      <article class="about-team-card">
        <img src="{{ '/assets/img/prof_pic_color.png' | relative_url }}" alt="Placeholder PhD alumnus">
        <div class="about-team-body">
          <div class="about-team-card-header">
            <span class="about-team-role-badge">PhD Alumni</span>
          </div>
          <h3>Placeholder Alumna Three</h3>
          <p class="about-team-role">Former PhD Candidate in Applied AI</p>
          <p class="about-team-bio">Placeholder content for a past lab member whose profile can later highlight thesis area, collaborations, and current destination.</p>
        </div>
      </article>

      <article class="about-team-card">
        <img src="{{ '/assets/img/prof_pic_color.png' | relative_url }}" alt="Placeholder PhD alumnus">
        <div class="about-team-body">
          <div class="about-team-card-header">
            <span class="about-team-role-badge">PhD Alumni</span>
          </div>
          <h3>Placeholder Alumnus Four</h3>
          <p class="about-team-role">Former PhD Candidate in Clinical AI</p>
          <p class="about-team-bio">Placeholder content for a completed PhD path, intended as a temporary entry until real alumni records are added.</p>
        </div>
      </article>
    </div>
  </details>
</section>
