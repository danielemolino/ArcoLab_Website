---
layout: page
permalink: /team/
title: Team
description: Research staff and collaborators at Arco Lab.
nav: true
nav_order: 1
---

The Arco Lab team brings together expertise in artificial intelligence, biomedical engineering, and clinically grounded computational research.

{% assign team_members = site.data.team | sort: "order" %}
<div class="about-team-grid">
  {% for member in team_members %}
    <article
      class="about-team-card about-team-card-clickable"
      onclick="window.location.href='{{ member.profile_path }}'"
      onkeydown="if(event.key === 'Enter'){ window.location.href='{{ member.profile_path }}'; }"
      role="link"
      tabindex="0"
      aria-label="View {{ member.name }} profile"
    >
      <img src="{{ member.photo }}" alt="{{ member.name }}">
      <div class="about-team-body">
        <h3>{{ member.name }}</h3>
        {% if member.title %}
          <p class="about-team-role">{{ member.title }}</p>
        {% endif %}
        {% if member.subtitle %}
          <p class="about-team-bio">{{ member.subtitle }}</p>
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
          <a class="about-team-action-link" href="{{ member.profile_path }}" aria-label="View profile" onclick="event.stopPropagation()"><i class="fa-solid fa-user"></i></a>
          <a class="about-team-action-link" href="{{ member.external_url }}" aria-label="Official profile" onclick="event.stopPropagation()"><i class="fa-solid fa-up-right-from-square"></i></a>
          <a class="about-team-action-link" href="/publications/" aria-label="Publications" onclick="event.stopPropagation()"><i class="fa-solid fa-book-open"></i></a>
          {% if member.email %}
            <a class="about-team-action-link" href="mailto:{{ member.email }}" aria-label="Email" onclick="event.stopPropagation()"><i class="fa-regular fa-envelope"></i></a>
          {% else %}
            <a class="about-team-action-link" href="/contact/" aria-label="Contact" onclick="event.stopPropagation()"><i class="fa-regular fa-envelope"></i></a>
          {% endif %}
        </div>
        <span class="about-team-profile-link">View profile <span aria-hidden="true">&rarr;</span></span>
      </div>
    </article>
  {% endfor %}
</div>
