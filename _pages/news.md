---
layout: page
title: News
permalink: /news/
description: News and announcements from Arco Lab.
nav: true
nav_order: 5
---

<section class="page-hero page-hero-news">
  <div class="page-hero-copy">
    <p class="page-hero-kicker">Updates</p>
    <h1>News</h1>
    <p class="page-hero-lead">
      Arco Lab news is organized by milestone type, from accepted papers and invited talks to grants, awards, and open opportunities.
    </p>
    <div class="member-profile-links">
      <a class="about-hero-btn about-hero-btn-primary about-inline-btn" href="/publications/">Browse publications</a>
      <a class="about-hero-btn about-hero-btn-secondary" href="/contact/">Get in touch <span aria-hidden="true">&rarr;</span></a>
    </div>
  </div>
  <aside class="page-hero-panel">
    <div class="page-hero-metric">
      <span class="page-hero-metric-value">{{ site.news | size }}</span>
      <span class="page-hero-metric-label">Current updates</span>
    </div>
    <div class="page-hero-metric">
      <span class="page-hero-metric-value">5</span>
      <span class="page-hero-metric-label">Tracked categories</span>
    </div>
  </aside>
</section>

{% assign category_sections = "Paper Accepted|Accepted papers and preprints,Grant|Funded initiatives and project wins,Award|Recognition and distinctions,Talk|Invited talks and seminars,Open Position|Open calls and recruiting" | split: "," %}

{% for section in category_sections %}
{% assign parts = section | split: "|" %}
{% assign category_name = parts[0] %}
{% assign category_description = parts[1] %}
{% assign category_items = site.news | where: "category", category_name | sort: "date" | reverse %}
{% if category_items.size > 0 %}
<section class="news-category-group">
  <div class="news-category-heading">
    <div>
      <p class="team-role-kicker">News Category</p>
      <h2>{{ category_name }}</h2>
      <p>{{ category_description }}</p>
    </div>
    <span class="team-role-count">{{ category_items.size }}</span>
  </div>

  <div class="news-card-grid">
    {% for item in category_items %}
    <article class="news-card">
      <div class="news-card-meta">
        <span class="news-card-badge">{{ item.category }}</span>
        <time datetime="{{ item.date | date_to_xmlschema }}">{{ item.date | date: "%b %d, %Y" }}</time>
      </div>
      <h3>
        {% if item.inline %}
        {{ item.title }}
        {% else %}
        <a href="{{ item.url | relative_url }}">{{ item.title }}</a>
        {% endif %}
      </h3>
      {% if item.summary %}
      <p>{{ item.summary }}</p>
      {% else %}
      <p>{{ item.excerpt | strip_html | truncate: 180 }}</p>
      {% endif %}
      {% unless item.inline %}
      <a class="news-card-link" href="{{ item.url | relative_url }}">Open update <span aria-hidden="true">&rarr;</span></a>
      {% endunless %}
    </article>
    {% endfor %}
  </div>
</section>
{% endif %}
{% endfor %}
