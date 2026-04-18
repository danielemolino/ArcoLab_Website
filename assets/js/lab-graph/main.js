import { buildGraphElements, collectFilterOptions, createGraphStore } from "./data.js";
import { createTooltip, fillSelect, positionTooltip, renderDetails, renderTooltip } from "./ui.js";

document.addEventListener("DOMContentLoaded", () => {
  const shell = document.querySelector(".lab-graph-shell");
  const canvas = document.getElementById("lab-graph-canvas");
  const details = document.getElementById("lab-graph-details");
  const dataScript = document.getElementById("lab-graph-data");

  if (!shell || !canvas || !details || !dataScript || typeof window.cytoscape === "undefined") {
    return;
  }

  const rawData = JSON.parse(dataScript.textContent);
  const store = createGraphStore(rawData);
  const filterOptions = collectFilterOptions(store);
  const tooltip = createTooltip();

  const controls = {
    search: document.getElementById("lab-graph-search"),
    linkMode: document.getElementById("lab-graph-link-filter"),
    topic: document.getElementById("lab-graph-topic-filter"),
    yearMin: document.getElementById("lab-graph-year-min"),
    yearMax: document.getElementById("lab-graph-year-max"),
    yearRangeSummary: document.getElementById("lab-graph-year-range-summary"),
    actionButtons: Array.from(document.querySelectorAll("[data-graph-action]")),
  };

  fillSelect(controls.topic, filterOptions.topics);
  const yearValues = filterOptions.years.map((value) => Number(value)).filter(Boolean);
  const minYear = Math.min(...yearValues);
  const maxYear = Math.max(...yearValues);
  const yearsAscending = [...yearValues].sort((a, b) => a - b).map(String);

  fillSelect(controls.yearMin, yearsAscending);
  fillSelect(controls.yearMax, yearsAscending);
  controls.yearMin.value = String(minYear);
  controls.yearMax.value = String(maxYear);

  const state = {
    mode: shell.dataset.defaultView || "papers",
    search: "",
    linkMode: "all",
    topic: "",
    yearMin: minYear,
    yearMax: maxYear,
    minSharedPublications: Number(shell.dataset.initialMinSharedPublications || 1),
    centeredNodeId: "",
  };

  const cy = window.cytoscape({
    container: canvas,
    elements: [],
    wheelSensitivity: 0.18,
    style: [
      {
        selector: "node",
        style: {
          "background-color": "#4d6bff",
          label: "",
          color: "#f7f8ff",
          "font-family": "Manrope, Segoe UI, sans-serif",
          "text-wrap": "none",
          "font-size": 8,
          "text-valign": "bottom",
          "text-halign": "center",
          "text-margin-y": 5,
          "text-outline-width": 3,
          "text-outline-color": "rgba(10, 15, 44, 0.96)",
          "overlay-opacity": 0,
          "border-width": 0.6,
          "border-color": "rgba(188, 197, 232, 0.3)",
        },
      },
      {
        selector: 'node[type = "paper"]',
        style: {
          shape: "ellipse",
          width: 18,
          height: 18,
          "background-color": "#22306c",
          "border-color": "rgba(188, 197, 232, 0.24)",
          "font-family": "Manrope, Segoe UI, sans-serif",
          "font-size": 8,
        },
      },
      {
        selector: "edge",
        style: {
          width: "mapData(weight, 1, 12, 1.1, 5.2)",
          "line-color": "rgba(164, 173, 214, 0.35)",
          "target-arrow-color": "rgba(164, 173, 214, 0.35)",
          "curve-style": "bezier",
          opacity: 0.8,
        },
      },
      {
        selector: 'edge[relation = "coauthor"]',
        style: {
          "line-color": "rgba(108, 92, 231, 0.55)",
        },
      },
      {
        selector: 'edge[relation = "topic"]',
        style: {
          "line-style": "dashed",
          "line-color": "rgba(84, 221, 167, 0.45)",
        },
      },
      {
        selector: 'edge[relation = "mixed"]',
        style: {
          "line-color": "rgba(117, 173, 255, 0.62)",
          opacity: 0.92,
        },
      },
    ],
  });

  const buildYearBandPositions = () => {
    const papers = cy.nodes().toArray();
    const years = [...new Set(papers.map((node) => String(node.data("year") || "")).filter(Boolean))].sort();
    const positions = {};
    const xGap = 170;
    const yGap = 170;

    years.forEach((year, yearIndex) => {
      const rowNodes = papers
        .filter((node) => String(node.data("year") || "") === year)
        .sort((a, b) => String(a.data("label") || "").localeCompare(String(b.data("label") || "")));

      const rowWidth = (rowNodes.length - 1) * xGap;
      rowNodes.forEach((node, nodeIndex) => {
        positions[node.id()] = {
          x: nodeIndex * xGap - rowWidth / 2,
          y: yearIndex * yGap,
        };
      });
    });

    if (state.centeredNodeId && positions[state.centeredNodeId]) {
      const focal = positions[state.centeredNodeId];
      Object.keys(positions).forEach((nodeId) => {
        positions[nodeId] = {
          x: positions[nodeId].x - focal.x,
          y: positions[nodeId].y - focal.y,
        };
      });
    }

    return positions;
  };

  const runLayout = () => {
    if (state.centeredNodeId) {
      cy.layout({
        name: "concentric",
        animate: false,
        fit: true,
        padding: 60,
        avoidOverlap: true,
        minNodeSpacing: 30,
        startAngle: -Math.PI / 2,
        sweep: 2 * Math.PI,
        concentric: (node) => {
          if (node.id() === state.centeredNodeId) return 10000;
          const focal = cy.getElementById(state.centeredNodeId);
          const edge = node.edgesWith(focal);
          if (edge && edge.length > 0) {
            return 500 + Number(edge[0].data("weight") || 0);
          }
          return 1;
        },
        levelWidth: () => 180,
      }).run();
      return;
    }

    cy.layout({
      name: "preset",
      positions: buildYearBandPositions(),
      animate: false,
      padding: 55,
      fit: true,
    }).run();
  };

  const renderGraph = () => {
    const elements = buildGraphElements(store, state.mode, state);
    cy.elements().remove();
    cy.add([...elements.nodes, ...elements.edges]);
    runLayout();

    if (elements.nodes.length === 0) {
      details.innerHTML = `
        <div class="lab-graph-details-empty">
          <p class="lab-graph-details-kicker">Details</p>
          <h2>No nodes match the current filters</h2>
          <p>Relax one or more filters to explore a broader publication subgraph.</p>
        </div>
      `;
    }
  };

  controls.search.addEventListener("input", (event) => {
    state.search = event.target.value.trim().toLowerCase();
    renderGraph();
  });

  controls.linkMode.addEventListener("change", (event) => {
    state.linkMode = event.target.value;
    renderGraph();
  });

  controls.topic.addEventListener("change", (event) => {
    state.topic = event.target.value;
    renderGraph();
  });

  const syncYearRange = (changed) => {
    let nextMin = Number(controls.yearMin.value);
    let nextMax = Number(controls.yearMax.value);

    if (changed === "min" && nextMin > nextMax) {
      nextMax = nextMin;
      controls.yearMax.value = String(nextMax);
    }

    if (changed === "max" && nextMax < nextMin) {
      nextMin = nextMax;
      controls.yearMin.value = String(nextMin);
    }

    state.yearMin = nextMin;
    state.yearMax = nextMax;
    controls.yearRangeSummary.textContent =
      nextMin === minYear && nextMax === maxYear
        ? "Showing all years"
        : `Showing papers from ${nextMin} to ${nextMax}`;
    renderGraph();
  };

  controls.yearMin.addEventListener("change", () => syncYearRange("min"));
  controls.yearMax.addEventListener("change", () => syncYearRange("max"));

  controls.actionButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const action = button.dataset.graphAction;
      if (action === "fit") {
        cy.fit(cy.elements(":visible"), 40);
      }
      if (action === "reset") {
        state.search = "";
        state.linkMode = "all";
        state.topic = "";
        state.yearMin = minYear;
        state.yearMax = maxYear;
        state.centeredNodeId = "";
        controls.yearMin.value = String(minYear);
        controls.yearMax.value = String(maxYear);
        controls.yearRangeSummary.textContent = "Showing all years";
        controls.search.value = "";
        controls.linkMode.value = "all";
        controls.topic.value = "";
        controls.yearMin.value = String(minYear);
        controls.yearMax.value = String(maxYear);
        controls.yearMinLabel.textContent = String(minYear);
        controls.yearMaxLabel.textContent = String(maxYear);
        renderGraph();
      }
    });
  });

  cy.on("mouseover", "node", (event) => {
    tooltip.hidden = false;
    tooltip.innerHTML = renderTooltip(event.target);
    positionTooltip(tooltip, event);
  });

  cy.on("mousemove", "node", (event) => {
    positionTooltip(tooltip, event);
  });

  cy.on("mouseout", "node", () => {
    tooltip.hidden = true;
  });

  cy.on("tap", "node", (event) => {
    const node = event.target;
    renderDetails(details, node, {
      center: () => {
        state.centeredNodeId = node.id();
        renderGraph();
      },
    });
  });

  cy.on("tap", (event) => {
    if (event.target === cy) {
      details.innerHTML = `
        <div class="lab-graph-details-empty">
          <p class="lab-graph-details-kicker">Details</p>
          <h2>Select a node</h2>
          <p>Hover a node for a quick preview or click it to inspect related papers, topics, venues, and outbound links.</p>
        </div>
      `;
    }
  });

  renderGraph();
});
