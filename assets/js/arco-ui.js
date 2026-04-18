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
    ".project-profile-panel",
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
      rootMargin: "0px 0px -8% 0px",
    }
  );

  revealTargets.forEach((element) => observer.observe(element));

  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const projectRails = Array.from(document.querySelectorAll(".about-project-rail"));

  projectRails.forEach((rail) => {
    const originalCards = Array.from(rail.children);
    const cardCount = originalCards.length;
    if (cardCount < 4 || cardCount % 2 !== 0) return;

    const getRailMetrics = () => {
      const setSize = cardCount / 2;
      const firstOriginal = rail.children[0];
      const firstDuplicate = rail.children[setSize];
      if (!firstOriginal || !firstDuplicate) {
        return { setWidth: rail.scrollWidth / 2 };
      }

      return {
        setWidth: firstDuplicate.offsetLeft - firstOriginal.offsetLeft,
      };
    };

    let isDragging = false;
    let dragStartX = 0;
    let dragStartScroll = 0;

    const normalizeRailScroll = () => {
      const { setWidth } = getRailMetrics();
      if (setWidth <= 0) return;
      if (rail.scrollLeft >= setWidth) rail.scrollLeft -= setWidth;
      if (rail.scrollLeft < 0) rail.scrollLeft += setWidth;
    };

    rail.addEventListener(
      "wheel",
      (event) => {
        if (Math.abs(event.deltaY) <= Math.abs(event.deltaX)) return;
        event.preventDefault();
        rail.scrollLeft += event.deltaY;
        normalizeRailScroll();
      },
      { passive: false }
    );

    rail.addEventListener("mousedown", (event) => {
      isDragging = true;
      dragStartX = event.clientX;
      dragStartScroll = rail.scrollLeft;
      rail.classList.add("is-dragging");
      event.preventDefault();
    });

    window.addEventListener("mousemove", (event) => {
      if (!isDragging) return;
      const delta = event.clientX - dragStartX;
      rail.scrollLeft = dragStartScroll - delta;
      normalizeRailScroll();
    });

    window.addEventListener("mouseup", () => {
      if (!isDragging) return;
      isDragging = false;
      rail.classList.remove("is-dragging");
    });

    rail.addEventListener("scroll", normalizeRailScroll, { passive: true });

    const controls = rail.parentElement?.querySelectorAll("[data-project-rail-direction]");
    controls?.forEach((control) => {
      control.addEventListener("click", () => {
        const step = Math.max(rail.clientWidth * 0.82, 360);
        const direction = control.dataset.projectRailDirection === "prev" ? -1 : 1;
        rail.scrollBy({
          left: direction * step,
          behavior: prefersReducedMotion ? "auto" : "smooth",
        });
      });
    });
  });
})();
