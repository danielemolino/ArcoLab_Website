const normalizeText = (value) =>
  String(value || "")
    .toLowerCase()
    .replace(/\s+/g, " ")
    .trim();

const slug = (value) =>
  normalizeText(value)
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");

const uniq = (values) => [...new Set((values || []).filter(Boolean))];

const intersect = (a, b) => a.filter((value) => b.includes(value));

export function createGraphStore(rawData) {
  const people = (rawData.people || []).map((person) => ({
    ...person,
    interests: uniq(person.interests || []),
    publications: (person.publications || []).map((publication) => ({
      ...publication,
      topics: uniq(person.interests || []),
    })),
  }));

  const paperMap = new Map();

  people.forEach((person) => {
    person.publications.forEach((publication) => {
      const paperId = publication.id || slug(`${publication.title}-${publication.year}`);
      const existing = paperMap.get(paperId) || {
        id: paperId,
        type: "paper",
        title: publication.title,
        year: publication.year,
        venue: publication.venue,
        doiUrl: publication.doiUrl,
        url: publication.url,
        pdf: publication.pdf,
        code: publication.code,
        website: publication.website,
        authors: [],
        authorIds: [],
        topics: [],
      };

      existing.authors = uniq([...existing.authors, person.name]);
      existing.authorIds = uniq([...existing.authorIds, person.id]);
      existing.topics = uniq([...(existing.topics || []), ...(person.interests || [])]);
      paperMap.set(paperId, existing);
    });
  });

  const papers = Array.from(paperMap.values()).sort((a, b) => String(b.year).localeCompare(String(a.year)));

  return { people, papers };
}

const matchesSearch = (payload, query) => {
  if (!query) return true;
  const haystack = normalizeText(
    [
      payload.name,
      payload.title,
      payload.roleLabel,
      payload.groupLabel,
      payload.venue,
      ...(payload.interests || []),
      ...(payload.topics || []),
      ...(payload.authors || []),
    ].join(" "),
  );

  return query
    .split(" ")
    .filter(Boolean)
    .every((token) => haystack.includes(token));
};

const personPassesFilters = (person, filters) => {
  if (filters.role && person.role !== filters.role) return false;
  if (filters.topic && !(person.interests || []).includes(filters.topic)) return false;
  if (filters.year) {
    const hasYear = (person.publications || []).some((publication) => String(publication.year) === String(filters.year));
    if (!hasYear) return false;
  }
  return matchesSearch(person, filters.search);
};

const paperPassesFilters = (paper, filters) => {
  if (filters.topic && !(paper.topics || []).includes(filters.topic)) return false;
  if (filters.year && String(paper.year) !== String(filters.year)) return false;
  return matchesSearch(paper, filters.search);
};

function buildPeopleElements(store, filters) {
  const visiblePeople = store.people.filter((person) => personPassesFilters(person, filters));
  const nodes = visiblePeople.map((person) => ({
    data: {
      id: `person:${person.id}`,
      entityId: person.id,
      type: "person",
      label: person.name,
      subtitle: person.title,
      role: person.role,
      roleLabel: person.roleLabel,
      groupLabel: person.groupLabel,
      topics: person.interests || [],
      photo: person.photo,
      profilePath: person.profilePath,
      publicationCount: person.publicationCount || (person.publications || []).length,
      email: person.email,
      externalUrl: person.externalUrl,
      scholarUrl: person.scholarUrl,
      orcidUrl: person.orcidUrl,
      githubUrl: person.githubUrl,
      linkedinUrl: person.linkedinUrl,
    },
  }));

  const edges = [];
  for (let i = 0; i < visiblePeople.length; i += 1) {
    for (let j = i + 1; j < visiblePeople.length; j += 1) {
      const source = visiblePeople[i];
      const target = visiblePeople[j];
      const sourcePubIds = new Set((source.publications || []).map((publication) => publication.id));
      const targetPubIds = new Set((target.publications || []).map((publication) => publication.id));
      const sharedPublicationIds = [...sourcePubIds].filter((id) => targetPubIds.has(id));
      const sharedTopics = intersect(source.interests || [], target.interests || []);

      if (
        sharedPublicationIds.length < (filters.minSharedPublications || 1) &&
        sharedTopics.length === 0
      ) {
        continue;
      }

      edges.push({
        data: {
          id: `edge:person:${source.id}:${target.id}`,
          source: `person:${source.id}`,
          target: `person:${target.id}`,
          relation: sharedPublicationIds.length > 0 ? "coauthor" : "topic",
          label:
            sharedPublicationIds.length > 0
              ? `${sharedPublicationIds.length} shared paper${sharedPublicationIds.length > 1 ? "s" : ""}`
              : `${sharedTopics.length} shared topic${sharedTopics.length > 1 ? "s" : ""}`,
          weight: sharedPublicationIds.length * 2 + sharedTopics.length,
          sharedPublicationIds,
          sharedTopics,
        },
      });
    }
  }

  return { nodes, edges };
}

function buildPaperElements(store, filters) {
  const visiblePapers = store.papers.filter((paper) => paperPassesFilters(paper, filters));
  const nodes = visiblePapers.map((paper) => ({
    data: {
      id: `paper:${paper.id}`,
      entityId: paper.id,
      type: "paper",
      label: paper.title,
      year: paper.year,
      venue: paper.venue,
      authors: paper.authors,
      topics: paper.topics,
      doiUrl: paper.doiUrl,
      url: paper.url,
      pdf: paper.pdf,
      code: paper.code,
      website: paper.website,
    },
  }));

  const edges = [];
  for (let i = 0; i < visiblePapers.length; i += 1) {
    for (let j = i + 1; j < visiblePapers.length; j += 1) {
      const source = visiblePapers[i];
      const target = visiblePapers[j];
      const sharedAuthors = intersect(source.authorIds || [], target.authorIds || []);
      const sharedTopics = intersect(source.topics || [], target.topics || []);

      if (sharedAuthors.length === 0 && sharedTopics.length === 0) continue;

      edges.push({
        data: {
          id: `edge:paper:${source.id}:${target.id}`,
          source: `paper:${source.id}`,
          target: `paper:${target.id}`,
          relation: sharedAuthors.length > 0 ? "coauthor" : "topic",
          label:
            sharedAuthors.length > 0
              ? `${sharedAuthors.length} shared author${sharedAuthors.length > 1 ? "s" : ""}`
              : `${sharedTopics.length} shared topic${sharedTopics.length > 1 ? "s" : ""}`,
          weight: sharedAuthors.length * 2 + sharedTopics.length,
          sharedAuthors,
          sharedTopics,
        },
      });
    }
  }

  return { nodes, edges };
}

function buildHybridElements(store, filters) {
  const peopleElements = buildPeopleElements(store, filters);
  const paperElements = buildPaperElements(store, filters);

  const visiblePersonIds = new Set(peopleElements.nodes.map((node) => node.data.entityId));
  const visiblePaperIds = new Set(paperElements.nodes.map((node) => node.data.entityId));

  const authoredEdges = [];
  store.people.forEach((person) => {
    if (!visiblePersonIds.has(person.id)) return;
    (person.publications || []).forEach((publication) => {
      if (!visiblePaperIds.has(publication.id)) return;
      authoredEdges.push({
        data: {
          id: `edge:authored:${person.id}:${publication.id}`,
          source: `person:${person.id}`,
          target: `paper:${publication.id}`,
          relation: "authored",
          label: "authored by",
          weight: 1,
        },
      });
    });
  });

  return {
    nodes: [...peopleElements.nodes, ...paperElements.nodes],
    edges: [...peopleElements.edges, ...paperElements.edges, ...authoredEdges],
  };
}

export function collectFilterOptions(store) {
  const roleMap = new Map();
  store.people.forEach((person) => {
    if (person.role && person.roleLabel && !roleMap.has(person.role)) {
      roleMap.set(person.role, person.roleLabel);
    }
  });

  return {
    roles: Array.from(roleMap.entries())
      .map(([value, label]) => ({ value, label }))
      .sort((a, b) => a.label.localeCompare(b.label)),
    topics: uniq([
      ...store.people.flatMap((person) => person.interests || []),
      ...store.papers.flatMap((paper) => paper.topics || []),
    ]).sort(),
    years: uniq(store.papers.map((paper) => String(paper.year || "")))
      .filter(Boolean)
      .sort((a, b) => b.localeCompare(a)),
  };
}

export function buildGraphElements(store, mode, filters) {
  if (mode === "papers") return buildPaperElements(store, filters);
  if (mode === "hybrid") return buildHybridElements(store, filters);
  return buildPeopleElements(store, filters);
}
