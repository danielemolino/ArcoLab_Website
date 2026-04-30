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
  const meta = `${data.venue || "Publication"}${data.year ? `, ${data.year}` : ""}`;
  return `
    <p class="lab-graph-tooltip-kicker">Paper</p>
    <strong>${data.fullTitle || data.label}</strong>
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
  if (data.doiUrl) {
    links.push(
      `<a class="btn btn-sm z-depth-0 publication-cta publication-cta-read" href="${data.doiUrl}">READ THE PAPER</a>`,
    );
  }
  if (data.pdf) links.push(`<a class="btn btn-sm z-depth-0" href="${data.pdf}">PDF</a>`);
  if (data.code) {
    links.push(
      `<a class="btn btn-sm z-depth-0 publication-cta publication-cta-code" href="${data.code}">Code</a>`,
    );
  }
  if (data.website) {
    links.push(
      `<a class="btn btn-sm z-depth-0 publication-cta publication-cta-website" href="${data.website}">Website</a>`,
    );
  }

  panel.innerHTML = `
    <div class="lab-graph-details-card">
      <p class="lab-graph-details-kicker">Paper node</p>
      <h2>${data.fullTitle || data.label}</h2>
      <p class="lab-graph-details-meta">${data.venue || "Publication"}${data.year ? `, ${data.year}` : ""}</p>
      ${(data.topics || []).length ? `<div class="lab-graph-details-tags">${data.topics.map((topic) => `<span>${topic}</span>`).join("")}</div>` : ""}
      ${(data.authors || []).length ? `<p class="lab-graph-details-copy"><strong>Authors:</strong> ${data.authors.join(", ")}</p>` : ""}
      <div class="lab-graph-details-actions">
        <button type="button" class="lab-graph-button" data-detail-action="center">Center node</button>
      </div>
      ${links.length ? `<div class="lab-graph-details-links">${links.join("")}</div>` : ""}
    </div>
  `;

  panel.querySelector('[data-detail-action="center"]')?.addEventListener("click", actions.center);
}
