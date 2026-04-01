(() => {
  const root = document.documentElement;
  root.classList.add("has-arco-ui");
  root.setAttribute("data-palette-variant", "current-refined");

  const navbar = document.getElementById("navbar");
  const updateNavbar = () => {
    if (!navbar) return;
    navbar.classList.toggle("is-scrolled", window.scrollY > 18);
  };

  updateNavbar();
  window.addEventListener("scroll", updateNavbar, { passive: true });

  const progress = document.createElement("div");
  progress.className = "arco-scroll-progress";
  document.body.appendChild(progress);

  const updateProgress = () => {
    const scrollable = document.documentElement.scrollHeight - window.innerHeight;
    const ratio = scrollable > 0 ? Math.min(window.scrollY / scrollable, 1) : 0;
    progress.style.transform = `scaleX(${ratio})`;
  };

  updateProgress();
  window.addEventListener("scroll", updateProgress, { passive: true });

  const selectors = [
    ".page-hero",
    ".about-stat-card",
    ".about-flagship-panel",
    ".about-focus-card",
    ".about-split",
    ".about-team-card",
    ".about-project-card",
    ".about-publication-item",
    ".publications-intro",
    ".publications-keyword-filters",
    ".publications ol.bibliography li",
    ".contact-page-hero",
    ".contact-page-grid > *",
    ".member-profile-hero",
    ".member-profile-section",
    ".project-profile-hero",
    ".project-profile-section",
    ".project-profile-panel"
  ];

  const revealTargets = selectors.flatMap((selector) => Array.from(document.querySelectorAll(selector)));
  revealTargets.forEach((element, index) => {
    element.classList.add("arco-reveal");
    element.style.setProperty("--arco-reveal-delay", `${Math.min(index % 6, 5) * 60}ms`);
  });

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      });
    },
    {
      threshold: 0.14,
      rootMargin: "0px 0px -8% 0px"
    }
  );

  revealTargets.forEach((element) => observer.observe(element));
})();
