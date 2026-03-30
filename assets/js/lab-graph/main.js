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
    role: document.getElementById("lab-graph-role-filter"),
    topic: document.getElementById("lab-graph-topic-filter"),
    year: document.getElementById("lab-graph-year-filter"),
    focusDepth: document.getElementById("lab-graph-focus-depth"),
    modeButtons: Array.from(document.querySelectorAll("[data-graph-mode]")),
    actionButtons: Array.from(document.querySelectorAll("[data-graph-action]")),
  };

  fillSelect(
    controls.role,
    filterOptions.roles.map((item) => item.value),
    (value) => filterOptions.roles.find((item) => item.value === value)?.label || value,
  );
  fillSelect(controls.topic, filterOptions.topics);
  fillSelect(controls.year, filterOptions.years);

  const state = {
    mode: shell.dataset.defaultView || "people",
    search: "",
    role: "",
    topic: "",
    year: "",
    focusDepth: Number(shell.dataset.defaultFocusDepth || 1),
    minSharedPublications: Number(shell.dataset.initialMinSharedPublications || 1),
    isolatedNodeId: "",
  };

  const cy = window.cytoscape({
    container: canvas,
    elements: [],
    wheelSensitivity: 0.18,
    style: [
      {
        selector: "node",
        style: {
          "background-color": "#6c5ce7",
          label: "data(label)",
          color: "#f7f8ff",
          "text-wrap": "wrap",
          "text-max-width": 160,
          "font-size": 11,
          "text-valign": "bottom",
          "text-margin-y": 10,
          "overlay-opacity": 0,
          "border-width": 1.5,
          "border-color": "rgba(255,255,255,0.12)",
        },
      },
      {
        selector: 'node[type = "person"]',
        style: {
          shape: "ellipse",
          width: 62,
          height: 62,
          "background-color": "#6c5ce7",
          "background-image": "data(photo)",
          "background-fit": "cover",
          "background-clip": "none",
        },
      },
      {
        selector: 'node[type = "paper"]',
        style: {
          shape: "round-rectangle",
          width: 170,
          height: 78,
          "background-color": "#22306c",
          "border-color": "rgba(255,255,255,0.08)",
          "font-size": 10,
        },
      },
      {
        selector: "edge",
        style: {
          width: "mapData(weight, 1, 6, 1.2, 4.2)",
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
        selector: 'edge[relation = "authored"]',
        style: {
          "line-color": "rgba(98, 153, 255, 0.45)",
        },
      },
      {
        selector: ".is-muted",
        style: {
          opacity: 0.12,
        },
      },
      {
        selector: ".is-highlighted",
        style: {
          opacity: 1,
          "border-color": "#ffffff",
          "border-width": 2.5,
        },
      },
    ],
  });

  const runLayout = () => {
    cy.layout({
      name: "cose",
      animate: false,
      randomize: false,
      idealEdgeLength: state.mode === "hybrid" ? 150 : 110,
      nodeRepulsion: 9500,
      padding: 30,
      fit: true,
    }).run();
  };

  const applyIsolation = () => {
    cy.elements().removeClass("is-muted is-highlighted");

    if (!state.isolatedNodeId) return;

    const focal = cy.getElementById(state.isolatedNodeId);
    if (!focal || focal.empty()) return;

    const depth = Math.max(1, Number(state.focusDepth || 1));
    let visible = focal.closedNeighborhood();
    for (let hop = 1; hop < depth; hop += 1) {
      visible = visible.union(visible.neighborhood());
    }

    cy.elements().difference(visible).addClass("is-muted");
    visible.addClass("is-highlighted");
    cy.animate({ center: { eles: focal }, duration: 220 });
  };

  const renderGraph = () => {
    const elements = buildGraphElements(store, state.mode, state);
    cy.elements().remove();
    cy.add([...elements.nodes, ...elements.edges]);
    runLayout();
    applyIsolation();
    if (elements.nodes.length === 0) {
      details.innerHTML = `
        <div class="lab-graph-details-empty">
          <p class="lab-graph-details-kicker">Details</p>
          <h2>No nodes match the current filters</h2>
          <p>Relax one or more filters, clear isolation, or switch graph mode to explore a broader subgraph.</p>
        </div>
      `;
    }
  };

  const syncModeButtons = () => {
    controls.modeButtons.forEach((button) => {
      button.classList.toggle("is-active", button.dataset.graphMode === state.mode);
    });
  };

  controls.modeButtons.forEach((button) => {
    button.addEventListener("click", () => {
      state.mode = button.dataset.graphMode;
      state.isolatedNodeId = "";
      syncModeButtons();
      renderGraph();
    });
  });

  controls.search.addEventListener("input", (event) => {
    state.search = event.target.value.trim().toLowerCase();
    renderGraph();
  });

  controls.role.addEventListener("change", (event) => {
    state.role = event.target.value;
    renderGraph();
  });

  controls.topic.addEventListener("change", (event) => {
    state.topic = event.target.value;
    renderGraph();
  });

  controls.year.addEventListener("change", (event) => {
    state.year = event.target.value;
    renderGraph();
  });

  controls.focusDepth.addEventListener("change", (event) => {
    state.focusDepth = Number(event.target.value || 1);
    applyIsolation();
  });

  controls.actionButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const action = button.dataset.graphAction;
      if (action === "fit") {
        cy.fit(cy.elements(":visible"), 40);
      }
      if (action === "reset") {
        state.search = "";
        state.role = "";
        state.topic = "";
        state.year = "";
        state.isolatedNodeId = "";
        controls.search.value = "";
        controls.role.value = "";
        controls.topic.value = "";
        controls.year.value = "";
        controls.focusDepth.value = String(shell.dataset.defaultFocusDepth || 1);
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
    state.isolatedNodeId = node.id();
    applyIsolation();
    renderDetails(details, node, {
      center: () => cy.animate({ center: { eles: node }, duration: 220 }),
      isolate: () => {
        state.isolatedNodeId = node.id();
        applyIsolation();
      },
      clear: () => {
        state.isolatedNodeId = "";
        applyIsolation();
      },
    });
  });

  cy.on("tap", (event) => {
    if (event.target === cy) {
      state.isolatedNodeId = "";
      applyIsolation();
    }
  });

  syncModeButtons();
  renderGraph();
});
