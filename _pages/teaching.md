---
layout: page
permalink: /education/
title: Education
description: Teaching activities and courses delivered by Arco Lab members.
nav: true
nav_order: 4
---

<section class="page-hero page-hero-education">
  <div class="page-hero-copy">
    <p class="page-hero-kicker">Teaching</p>
    <h1>Education</h1>
    <p class="page-hero-lead">
      Arco Lab contributes to teaching activities in artificial intelligence, biomedical engineering, intelligent systems, and related computational methods at Università Campus Bio-Medico di Roma.
    </p>
    <div class="member-profile-links">
      <a class="about-hero-btn about-hero-btn-primary about-inline-btn" href="/team/">Meet the instructors</a>
      <a class="about-hero-btn about-hero-btn-secondary" href="/contact/">Academic inquiries <span aria-hidden="true">&rarr;</span></a>
    </div>
  </div>
  <aside class="page-hero-panel">
    <div class="page-hero-metric">
      <span class="page-hero-metric-value">{{ site.data.education_courses | size }}</span>
      <span class="page-hero-metric-label">Course entries</span>
    </div>
    <div class="page-hero-metric">
      <span class="page-hero-metric-value">AI + Engineering</span>
      <span class="page-hero-metric-label">Educational focus across data, learning, and intelligent systems</span>
    </div>
  </aside>
</section>

<section class="about-section education-courses-section">
  <div class="about-section-heading">
    <h2>Courses</h2>
    <p class="about-section-kicker">Current Teaching Portfolio</p>
    <p class="about-section-copy">
      Each course card summarizes the teaching activity, the degree program, credits, and the instructional team without requiring a separate page for every entry.
    </p>
  </div>
  {% include courses.liquid %}
</section>
