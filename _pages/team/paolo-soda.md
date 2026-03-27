---
layout: page
title: Paolo Soda
permalink: /team/paolo-soda/
description: Full profile and selected publications of Paolo Soda.
---

{% assign member = site.data.team | where: "slug", "paolo-soda" | first %}

<section class="member-profile">
  <div class="member-profile-hero">
    <div class="member-profile-media">
      <img src="{{ member.photo }}" alt="{{ member.name }}">
    </div>
    <div class="member-profile-copy">
      <p class="member-profile-kicker">Principal Investigator</p>
      <h1>{{ member.name }}</h1>
      <p class="member-profile-role">{{ member.title }}</p>
      {% if member.subtitle %}
        <p class="member-profile-subtitle">{{ member.subtitle }}</p>
      {% endif %}
      {% if member.visiting_role %}
        <p class="member-profile-subtitle">{{ member.visiting_role }}</p>
      {% endif %}
      <p class="member-profile-bio">{{ member.bio }}</p>
      <div class="member-profile-tags">
        {% for interest in member.interests %}
          <span>{{ interest }}</span>
        {% endfor %}
      </div>
      <div class="member-profile-links">
        <a class="about-hero-btn about-hero-btn-primary about-inline-btn" href="{{ member.external_url }}">Official Profile</a>
        <a class="about-hero-btn about-hero-btn-secondary" href="/team/">Back to Team <span aria-hidden="true">&rarr;</span></a>
      </div>
    </div>
  </div>

  <div class="member-profile-section">
    <h2>Selected Publications</h2>
    <div class="publications member-profile-publications">
      {% bibliography --group_by none --query @*[selected=true && author ^= Soda] %}
    </div>
    {% if member.publications_url %}
      <p class="member-profile-footnote">
        Full publication list:
        <a href="{{ member.publications_url }}">{{ member.publications_url }}</a>
      </p>
    {% endif %}
  </div>
</section>
