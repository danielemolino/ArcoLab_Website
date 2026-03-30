export function createTooltip() {
  const tooltip = document.createElement("div");
  tooltip.className = "lab-graph-tooltip";
  tooltip.hidden = true;
  document.body.appendChild(tooltip);
  return tooltip;
}

export function positionTooltip(tooltip, event) {
  const clientX = event.originalEvent?.clientX ?? 24;
  const clientY = event.originalEvent?.clientY ?? 24;
  tooltip.style.left = `${clientX + 18}px`;
  tooltip.style.top = `${clientY + 18}px`;
}

export function renderTooltip(node) {
  const data = node.data();
  const meta =
    data.type === "paper"
      ? `${data.venue || "Publication"}${data.year ? `, ${data.year}` : ""}`
      : data.roleLabel || "";
  return `
    <p class="lab-graph-tooltip-kicker">${data.type === "paper" ? "Paper" : "Person"}</p>
    <strong>${data.label}</strong>
    <p>${meta}</p>
  `;
}

export function fillSelect(select, values, formatter = (value) => value) {
  const current = select.value;
  while (select.options.length > 1) select.remove(1);
  values.forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = formatter(value);
    select.appendChild(option);
  });
  select.value = current;
}

export function renderDetails(panel, node, actions) {
  const data = node.data();
  const links = [];
  if (data.profilePath) links.push(`<a class="lab-graph-detail-link" href="${data.profilePath}">Open profile</a>`);
  if (data.externalUrl) links.push(`<a class="lab-graph-detail-link" href="${data.externalUrl}">Official page</a>`);
  if (data.scholarUrl) links.push(`<a class="lab-graph-detail-link" href="${data.scholarUrl}">Google Scholar</a>`);
  if (data.doiUrl) links.push(`<a class="lab-graph-detail-link" href="${data.doiUrl}">DOI</a>`);
  if (data.pdf) links.push(`<a class="lab-graph-detail-link" href="${data.pdf}">PDF</a>`);
  if (data.code) links.push(`<a class="lab-graph-detail-link" href="${data.code}">Code</a>`);
  if (data.website) links.push(`<a class="lab-graph-detail-link" href="${data.website}">Website</a>`);

  panel.innerHTML = `
    <div class="lab-graph-details-card">
      <p class="lab-graph-details-kicker">${data.type === "paper" ? "Paper node" : "Person node"}</p>
      <h2>${data.label}</h2>
      ${
        data.type === "paper"
          ? `<p class="lab-graph-details-meta">${data.venue || "Publication"}${data.year ? `, ${data.year}` : ""}</p>`
          : `<p class="lab-graph-details-meta">${data.roleLabel || ""}${data.title ? ` · ${data.title}` : ""}</p>`
      }
      ${
        (data.topics || []).length
          ? `<div class="lab-graph-details-tags">${data.topics
              .map((topic) => `<span>${topic}</span>`)
              .join("")}</div>`
          : ""
      }
      ${
        (data.authors || []).length
          ? `<p class="lab-graph-details-copy"><strong>Authors:</strong> ${data.authors.join(", ")}</p>`
          : ""
      }
      ${
        data.publicationCount
          ? `<p class="lab-graph-details-copy"><strong>Selected publications:</strong> ${data.publicationCount}</p>`
          : ""
      }
      <div class="lab-graph-details-actions">
        <button type="button" class="lab-graph-button" data-detail-action="center">Center node</button>
        <button type="button" class="lab-graph-button" data-detail-action="isolate">Isolate neighborhood</button>
        <button type="button" class="lab-graph-button" data-detail-action="clear">Clear isolation</button>
      </div>
      ${links.length ? `<div class="lab-graph-details-links">${links.join("")}</div>` : ""}
    </div>
  `;

  panel.querySelector('[data-detail-action="center"]')?.addEventListener("click", actions.center);
  panel.querySelector('[data-detail-action="isolate"]')?.addEventListener("click", actions.isolate);
  panel.querySelector('[data-detail-action="clear"]')?.addEventListener("click", actions.clear);
}
