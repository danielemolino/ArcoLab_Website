import { highlightSearchTerm } from "./highlight-search-term.js";

document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("bibsearch");
  if (!searchInput) return;

  const normalizeText = (value) => (value || "").toLowerCase().replace(/\s+/g, " ").trim();

  // actual bibsearch logic
  const filterItems = (searchTerm) => {
    document.querySelectorAll(".bibliography, .unloaded").forEach((element) => element.classList.remove("unloaded"));

    const bibliographyItems = document.querySelectorAll(".bibliography > li");
    const normalizedSearchTerm = normalizeText(searchTerm);
    const searchTokens = normalizedSearchTerm.split(" ").filter(Boolean);

    bibliographyItems.forEach((element) => {
      const row = element.querySelector(".row[data-search-text]");
      const searchableText = normalizeText(row?.dataset.searchText || element.innerText);
      const matches = searchTokens.length === 0 || searchTokens.every((token) => searchableText.includes(token));
      if (!matches) {
        element.classList.add("unloaded");
      }
    });

    if (CSS.highlights && normalizedSearchTerm !== "") {
      highlightSearchTerm({
        search: normalizedSearchTerm,
        selector: ".bibliography > li .title, .bibliography > li .author, .bibliography > li .periodical, .bibliography > li .publication-keywords",
      });
    }

    document.querySelectorAll("h2.bibliography").forEach(function (element) {
      let iterator = element.nextElementSibling; // get next sibling element after h2, which can be h3 or ol
      let hideFirstGroupingElement = true;
      // iterate until next group element (h2), which is already selected by the querySelectorAll(-).forEach(-)
      while (iterator && iterator.tagName !== "H2") {
        if (iterator.tagName === "OL") {
          const ol = iterator;
          const unloadedSiblings = ol.querySelectorAll(":scope > li.unloaded");
          const totalSiblings = ol.querySelectorAll(":scope > li");

          if (unloadedSiblings.length === totalSiblings.length) {
            ol.previousElementSibling.classList.add("unloaded"); // Add the '.unloaded' class to the previous grouping element (e.g. year)
            ol.classList.add("unloaded"); // Add the '.unloaded' class to the OL itself
          } else {
            hideFirstGroupingElement = false; // there is at least some visible entry, don't hide the first grouping element
          }
        }
        iterator = iterator.nextElementSibling;
      }
      // Add unloaded class to first grouping element (e.g. year) if no item left in this group
      if (hideFirstGroupingElement) {
        element.classList.add("unloaded");
      }
    });
  };

  const updateInputField = () => {
    const params = new URLSearchParams(window.location.search);
    const queryValue = (params.get("search") || "").trim();
    const hashValue = decodeURIComponent(window.location.hash.substring(1));
    const value = queryValue || hashValue;
    searchInput.value = value;
    filterItems(value.toLowerCase());
  };

  // Sensitive search. Only start searching if there's been no input for 300 ms
  let timeoutId;
  searchInput.addEventListener("input", function () {
    clearTimeout(timeoutId); // Clear the previous timeout
    const searchTerm = this.value;
    timeoutId = setTimeout(() => filterItems(searchTerm), 300);
  });

  window.addEventListener("hashchange", updateInputField); // Update the filter when the hash changes
  window.addEventListener("popstate", updateInputField);

  updateInputField(); // Update filter when page loads
});
