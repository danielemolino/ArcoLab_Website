---
permalink: /assets/js/publications-filters.js
---

document.addEventListener("DOMContentLoaded", () => {
  const keywordFiltersRoot = document.getElementById("publications-keyword-filters");
  const projectFiltersRoot = document.getElementById("publications-project-filters");
  const yearFiltersRoot = document.getElementById("publications-year-filters");
  const projectLabelsScript = document.getElementById("arco-project-labels");
  const publicationRows = Array.from(
    document.querySelectorAll(".publications ol.bibliography > li"),
  );

  if (publicationRows.length === 0) {
    return;
  }

  const keywordMap = new Map();
  const projectMap = new Map();
  const yearMap = new Map();
  let projectLabels = {};
  if (projectLabelsScript) {
    try {
      projectLabels = JSON.parse(projectLabelsScript.textContent || "{}");
    } catch (error) {
      projectLabels = {};
    }
  }
  if (Object.keys(projectLabels).length === 0 && typeof window !== "undefined" && window.arcoProjectLabels) {
    projectLabels = window.arcoProjectLabels;
  }

  publicationRows.forEach((item) => {
    const row = item.querySelector(".row[data-search-text]");
    const keywords = ((row && row.dataset.keywords) || "")
      .split("|")
      .map((keyword) => keyword.trim())
      .filter(Boolean);

    keywords.forEach((keyword) => {
      const normalized = keyword.toLowerCase();
      if (!keywordMap.has(normalized)) {
        keywordMap.set(normalized, keyword);
      }
    });

    const projects = ((row && row.dataset.projects) || "")
      .split("|")
      .map((project) => project.trim())
      .filter(Boolean);

    projects.forEach((project) => {
      const normalized = project.toLowerCase();
      const label = projectLabels[project] || projectLabels[normalized];
      if (!projectMap.has(normalized)) {
        projectMap.set(normalized, label || project);
      }
    });

    const year = ((row && row.dataset.year) || "").trim();
    if (year && !yearMap.has(year)) {
      yearMap.set(year, year);
    }
  });

  if (keywordMap.size === 0 && projectMap.size === 0 && yearMap.size === 0) {
    return;
  }

  const activeKeywords = new Set();
  const activeProjects = new Set();
  const activeYears = new Set();

  const keywordActions = document.createElement("div");
  keywordActions.className = "publications-keyword-actions";
  const projectActions = document.createElement("div");
  projectActions.className = "publications-keyword-actions";
  const yearActions = document.createElement("div");
  yearActions.className = "publications-keyword-actions";

  const render = () => {
    publicationRows.forEach((item) => {
      const row = item.querySelector(".row[data-search-text]");
      const keywords = ((row && row.dataset.keywords) || "")
        .split("|")
        .map((keyword) => keyword.trim().toLowerCase())
        .filter(Boolean);
      const projects = ((row && row.dataset.projects) || "")
        .split("|")
        .map((project) => project.trim().toLowerCase())
        .filter(Boolean);
      const year = ((row && row.dataset.year) || "").trim();
      const keywordMatches =
        activeKeywords.size === 0 ||
        Array.from(activeKeywords).every((keyword) => keywords.includes(keyword));
      const projectMatches =
        activeProjects.size === 0 ||
        Array.from(activeProjects).every((project) => projects.includes(project));
      const yearMatches =
        activeYears.size === 0 || Array.from(activeYears).every((value) => value === year);
      item.style.display = keywordMatches && projectMatches && yearMatches ? "" : "none";
    });

    Array.from(keywordActions.querySelectorAll("button")).forEach((button) => {
      const isActive =
        button.dataset.keyword === ""
          ? activeKeywords.size === 0
          : activeKeywords.has(button.dataset.keyword);
      button.classList.toggle("is-active", isActive);
      button.setAttribute("aria-pressed", isActive ? "true" : "false");
    });

    Array.from(projectActions.querySelectorAll("button")).forEach((button) => {
      const isActive =
        button.dataset.project === ""
          ? activeProjects.size === 0
          : activeProjects.has(button.dataset.project);
      button.classList.toggle("is-active", isActive);
      button.setAttribute("aria-pressed", isActive ? "true" : "false");
    });

    Array.from(yearActions.querySelectorAll("button")).forEach((button) => {
      const isActive =
        button.dataset.year === ""
          ? activeYears.size === 0
          : activeYears.has(button.dataset.year);
      button.classList.toggle("is-active", isActive);
      button.setAttribute("aria-pressed", isActive ? "true" : "false");
    });
  };

  const createKeywordButton = (label, keyword = "") => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "publications-keyword-chip";
    button.dataset.keyword = keyword;
    button.textContent = label;
    button.addEventListener("click", () => {
      if (keyword === "") {
        activeKeywords.clear();
      } else if (activeKeywords.has(keyword)) {
        activeKeywords.delete(keyword);
      } else {
        activeKeywords.add(keyword);
      }
      render();
    });
    return button;
  };

  const createProjectButton = (label, project = "") => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "publications-keyword-chip";
    button.dataset.project = project;
    button.textContent = label;
    button.addEventListener("click", () => {
      if (project === "") {
        activeProjects.clear();
      } else if (activeProjects.has(project)) {
        activeProjects.delete(project);
      } else {
        activeProjects.add(project);
      }
      render();
    });
    return button;
  };

  const createYearButton = (label, year = "") => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "publications-keyword-chip";
    button.dataset.year = year;
    button.textContent = label;
    button.addEventListener("click", () => {
      if (year === "") {
        activeYears.clear();
      } else if (activeYears.has(year)) {
        activeYears.delete(year);
      } else {
        activeYears.clear();
        activeYears.add(year);
      }
      render();
    });
    return button;
  };

  if (keywordFiltersRoot && keywordMap.size > 0) {
    const title = document.createElement("p");
    title.className = "publications-keyword-title";
    title.textContent = "Filter by theme";
    keywordFiltersRoot.appendChild(title);
    keywordFiltersRoot.appendChild(keywordActions);
    keywordActions.appendChild(createKeywordButton("All", ""));
    Array.from(keywordMap.entries())
      .sort((a, b) => a[1].localeCompare(b[1]))
      .forEach(([normalized, label]) => {
        keywordActions.appendChild(createKeywordButton(label, normalized));
      });
  }

  if (projectFiltersRoot && projectMap.size > 0) {
    const title = document.createElement("p");
    title.className = "publications-keyword-title";
    title.textContent = "Filter by project";
    projectFiltersRoot.appendChild(title);
    projectFiltersRoot.appendChild(projectActions);
    projectActions.appendChild(createProjectButton("All", ""));
    Array.from(projectMap.entries())
      .sort((a, b) => a[1].localeCompare(b[1]))
      .forEach(([normalized, label]) => {
        projectActions.appendChild(createProjectButton(label, normalized));
      });
  }

  if (yearFiltersRoot && yearMap.size > 0) {
    const title = document.createElement("p");
    title.className = "publications-keyword-title";
    title.textContent = "Filter by year";
    yearFiltersRoot.appendChild(title);
    yearFiltersRoot.appendChild(yearActions);
    yearActions.appendChild(createYearButton("All", ""));
    Array.from(yearMap.keys())
      .sort((a, b) => Number(b) - Number(a))
      .forEach((year) => {
        yearActions.appendChild(createYearButton(year, year));
      });
  }

  const params = new URLSearchParams(window.location.search);
  const initialProject = (params.get("project") || "").trim().toLowerCase();
  const initialYear = (params.get("year") || "").trim();
  if (initialProject && projectMap.has(initialProject)) {
    activeProjects.add(initialProject);
  }
  if (initialYear && yearMap.has(initialYear)) {
    activeYears.add(initialYear);
  }

  render();
});
