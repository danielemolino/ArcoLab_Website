---
permalink: /assets/js/publications-filters.js
---

document.addEventListener("DOMContentLoaded", () => {
  const filtersRoot = document.getElementById("publications-keyword-filters");
  const publicationRows = Array.from(
    document.querySelectorAll(".publications ol.bibliography > li"),
  );

  if (!filtersRoot || publicationRows.length === 0) {
    return;
  }

  const keywordMap = new Map();

  publicationRows.forEach((item) => {
    const row = item.querySelector(".row[data-keywords]");
    if (!row) return;

    const keywords = (row.dataset.keywords || "")
      .split("|")
      .map((keyword) => keyword.trim())
      .filter(Boolean);

    keywords.forEach((keyword) => {
      const normalized = keyword.toLowerCase();
      if (!keywordMap.has(normalized)) {
        keywordMap.set(normalized, keyword);
      }
    });
  });

  if (keywordMap.size === 0) {
    return;
  }

  const title = document.createElement("p");
  title.className = "publications-keyword-title";
  title.textContent = "Filter by theme";
  filtersRoot.appendChild(title);

  const actions = document.createElement("div");
  actions.className = "publications-keyword-actions";
  filtersRoot.appendChild(actions);

  const activeKeywords = new Set();

  const render = () => {
    publicationRows.forEach((item) => {
      const row = item.querySelector(".row[data-keywords]");
      const keywords = ((row && row.dataset.keywords) || "")
        .split("|")
        .map((keyword) => keyword.trim().toLowerCase())
        .filter(Boolean);
      const matches =
        activeKeywords.size === 0 ||
        Array.from(activeKeywords).every((keyword) => keywords.includes(keyword));
      item.style.display = matches ? "" : "none";
    });

    Array.from(actions.querySelectorAll("button")).forEach((button) => {
      const isActive =
        button.dataset.keyword === ""
          ? activeKeywords.size === 0
          : activeKeywords.has(button.dataset.keyword);
      button.classList.toggle("is-active", isActive);
      button.setAttribute("aria-pressed", isActive ? "true" : "false");
    });
  };

  const createButton = (label, keyword = "") => {
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

  actions.appendChild(createButton("All", ""));

  Array.from(keywordMap.entries())
    .sort((a, b) => a[1].localeCompare(b[1]))
    .forEach(([normalized, label]) => {
      actions.appendChild(createButton(label, normalized));
    });

  render();
});
