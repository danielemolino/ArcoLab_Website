---
layout: page
title: News
permalink: /news/
description: LinkedIn-sourced updates and announcements from Arco Lab.
nav: true
nav_order: 5
---

<section class="page-hero page-hero-news">
  <div class="page-hero-copy">
    <p class="page-hero-kicker">Updates</p>
    <h1>News</h1>
    <p class="page-hero-lead">
      Read the latest news from ArCo Lab, including research milestones, academic achievements, project updates, and activities across the group.
    </p>
    <div class="member-profile-links">
      <a class="about-hero-btn about-inline-btn news-linkedin-btn" href="https://www.linkedin.com/company/arco-unicampus/" target="_blank" rel="noopener">
        <i class="fa-brands fa-linkedin" aria-hidden="true"></i>
        <span>Follow us on LinkedIn!</span>
      </a>
      <a class="about-hero-btn about-hero-btn-secondary" href="/contact/">Get in touch <span aria-hidden="true">&rarr;</span></a>
    </div>
  </div>
</section>

<section class="news-feed-shell">
  {% assign news_items = site.data.news_feed | sort: "date" | reverse %}
  {% if news_items and news_items.size > 0 %}
    <div class="news-card-grid">
      {% for item in news_items limit: 6 %}
        <article class="news-card">
          {% if item.image_url != blank %}
            <div class="news-card-media">
              <img src="{{ item.image_url }}" alt="{{ item.title }}">
            </div>
          {% else %}
            <div class="news-card-media news-card-media-fallback" aria-hidden="true">
              <img src="{{ '/assets/branding/arco/symbol/logo_arco.svg' | relative_url }}" alt="">
            </div>
          {% endif %}
          <div class="news-card-meta">
            <span class="news-card-badge">{{ item.category }}</span>
            <time datetime="{{ item.date }}">{{ item.date | date: "%b %d, %Y" }}</time>
          </div>
          <h3>{{ item.title }}</h3>
          <p>{{ item.summary }}</p>
          <a class="news-card-link" href="{{ item.linkedin_url }}" target="_blank" rel="noopener">Open on LinkedIn <span aria-hidden="true">&rarr;</span></a>
        </article>
      {% endfor %}
    </div>

    {% if news_items.size > 6 %}
      <details class="news-more-details">
        <summary class="news-more-summary">Show more</summary>
        <div class="news-card-grid news-card-grid-more">
          {% for item in news_items offset: 6 %}
            <article class="news-card">
              {% if item.image_url != blank %}
                <div class="news-card-media">
                  <img src="{{ item.image_url }}" alt="{{ item.title }}">
                </div>
              {% else %}
                <div class="news-card-media news-card-media-fallback" aria-hidden="true">
                  <img src="{{ '/assets/branding/arco/symbol/logo_arco.svg' | relative_url }}" alt="">
                </div>
              {% endif %}
              <div class="news-card-meta">
                <span class="news-card-badge">{{ item.category }}</span>
                <time datetime="{{ item.date }}">{{ item.date | date: "%b %d, %Y" }}</time>
              </div>
              <h3>{{ item.title }}</h3>
              <p>{{ item.summary }}</p>
              <a class="news-card-link" href="{{ item.linkedin_url }}" target="_blank" rel="noopener">Open on LinkedIn <span aria-hidden="true">&rarr;</span></a>
            </article>
          {% endfor %}
        </div>
      </details>
    {% endif %}
  {% else %}
    <div class="contact-page-card">
      <p class="contact-page-card-kicker">No Updates Yet</p>
      <h2>News entries will appear here</h2>
      <p>Once the shared news sheet is populated, the latest LinkedIn-linked updates will be listed on this page automatically.</p>
    </div>
  {% endif %}
</section>
