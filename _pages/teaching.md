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
      Arco Lab contributes to teaching activities in artificial intelligence, biomedical engineering, intelligent systems, and related computational methods at Campus Bio-Medico University of Rome.
    </p>
    <div class="member-profile-links">
      <a class="about-hero-btn about-hero-btn-primary about-inline-btn" href="/team/">Meet the instructors</a>
      <a class="about-hero-btn about-hero-btn-secondary" href="/contact/">Academic inquiries <span aria-hidden="true">&rarr;</span></a>
    </div>
  </div>
  <aside class="page-hero-panel">
    <div class="page-hero-metric">
      <span class="page-hero-metric-value">{{ site.teachings | size }}</span>
      <span class="page-hero-metric-label">Course entries</span>
    </div>
    <div class="page-hero-metric">
      <span class="page-hero-metric-value">AI + Engineering</span>
      <span class="page-hero-metric-label">Educational focus across data, learning, and intelligent systems</span>
    </div>
  </aside>
</section>

<section class="contact-page-grid education-grid">
  <article class="contact-page-card">
    <p class="contact-page-card-kicker">Course Areas</p>
    <h2>Topics taught by the lab</h2>
    <p>Current teaching activities span machine learning, data science, biomedical engineering, and intelligent systems.</p>
  </article>
  <article class="contact-page-card">
    <p class="contact-page-card-kicker">Academic Role</p>
    <h2>Research-informed teaching</h2>
    <p>Courses are aligned with the lab’s work in applied AI for medicine, bridging methodological foundations and real biomedical applications.</p>
  </article>
</section>

<section class="about-section education-courses-section">
  <div class="about-section-heading">
    <h2>Courses</h2>
    <p class="about-section-kicker">Current Teaching Portfolio</p>
    <p class="about-section-copy">
      This section can grow over time with courses, teaching responsibilities, and educational resources linked to the lab.
    </p>
  </div>
  {% include courses.liquid %}
</section>
