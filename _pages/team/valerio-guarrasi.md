---
layout: page
title: Valerio Guarrasi
permalink: /team/valerio-guarrasi/
description: Full profile and recent publications of Valerio Guarrasi.
---

{% assign member = site.data.team | where: "slug", "valerio-guarrasi" | first %}

<section class="member-profile">
  <div class="member-profile-hero">
    <div class="member-profile-media">
      <img src="{{ member.photo | relative_url }}" alt="{{ member.name }}">
    </div>
    <div class="member-profile-copy">
      <p class="member-profile-kicker">{{ member.role_label }}</p>
      <h1>{{ member.name }}</h1>
      <p class="member-profile-role">{{ member.title }}</p>
      <p class="member-profile-bio">{{ member.bio }}</p>
      <div class="member-profile-tags">
        {% for interest in member.interests %}
          <span>{{ interest }}</span>
        {% endfor %}
      </div>
      <div class="member-profile-links">
        <a class="member-profile-link-btn member-profile-link-btn-scholar" href="{{ member.scholar_url }}"><i class="fa-solid fa-graduation-cap"></i><span>Google Scholar</span></a>
        <a class="member-profile-link-btn member-profile-link-btn-orcid" href="{{ member.orcid_url }}"><i class="fa-solid fa-id-badge"></i><span>ORCID</span></a>
        <a class="member-profile-link-btn member-profile-link-btn-linkedin" href="{{ member.linkedin_url }}"><i class="fa-brands fa-linkedin-in"></i><span>LinkedIn</span></a>
        <a class="member-profile-link-btn member-profile-link-btn-publications" href="{{ '/publications/' | relative_url }}?search={{ member.name | url_encode }}"><i class="fa-solid fa-book-open"></i><span>Browse Publications</span></a>
        <a class="member-profile-link-btn member-profile-link-btn-back" href="{{ '/team/' | relative_url }}"><i class="fa-solid fa-arrow-left"></i><span>Back to Team</span></a>
      </div>
    </div>
  </div>

  <div class="member-profile-section">
    <h2>Recent Publications</h2>
    {% if member.recent_publications and member.recent_publications != empty %}
      {% include member_selected_publications.liquid %}
    {% else %}
      <p class="member-profile-footnote">Recent publications will appear here when this member is matched to the bibliography workflow.</p>
    {% endif %}

    {% if member.scholar_url and member.scholar_url contains 'scholar.google.' %}
      <p class="member-profile-footnote">
        Full publication list:
        <a href="{{ member.scholar_url }}">{{ member.scholar_url }}</a>
      </p>
    {% else %}
      <p class="member-profile-footnote">
        Browse all indexed publications for this author:
        <a href="/publications/?search=Valerio%20Guarrasi">/publications/?search=Valerio Guarrasi</a>
      </p>
    {% endif %}
  </div>
</section>
