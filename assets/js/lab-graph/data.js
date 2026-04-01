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

const STOP_WORDS = new Set([
  "a",
  "an",
  "and",
  "for",
  "from",
  "in",
  "of",
  "on",
  "the",
  "to",
  "via",
  "with",
]);

const titleAcronym = (title) => {
  const tokens = String(title || "")
    .replace(/[^A-Za-z0-9 ]+/g, " ")
    .split(/\s+/)
    .map((token) => token.trim())
    .filter(Boolean)
    .filter((token) => !STOP_WORDS.has(token.toLowerCase()));

  return tokens
    .slice(0, 3)
    .map((token) => token[0]?.toUpperCase() || "")
    .join("") || "P";
};

const shortPaperLabelBase = (paper) => {
  const firstAuthor = String((paper.authors || [])[0] || "")
    .trim()
    .split(/\s+/)
    .filter(Boolean)
    .pop() || "Paper";
  const cleanSurname = firstAuthor.replace(/[^A-Za-z0-9]/g, "") || "Paper";
  const surname = cleanSurname.charAt(0).toUpperCase() + cleanSurname.slice(1).toLowerCase();
  const year = String(paper.year || "").slice(-2) || "00";
  const acronym = titleAcronym(paper.title);
  return `${surname}${year}-${acronym}`;
};

export function createGraphStore(rawData) {
  const papers = (rawData.papers || [])
    .map((paper) => ({
      ...paper,
      id: paper.id || slug(`${paper.title}-${paper.year}`),
      authors: uniq(paper.authors || []),
      authorIds: uniq((paper.authorIds || []).map((author) => normalizeText(author))),
      firstAuthorId: normalizeText((paper.authors || [])[0] || ""),
      topics: uniq((paper.topics || []).map((topic) => normalizeText(topic)).filter(Boolean)),
    }))
    .sort((a, b) => String(b.year).localeCompare(String(a.year)));

  const labelCounts = new Map();
  papers.forEach((paper) => {
    const base = shortPaperLabelBase(paper);
    const count = (labelCounts.get(base) || 0) + 1;
    labelCounts.set(base, count);
    paper.shortLabel = count === 1 ? base : `${base}-${count}`;
  });

  return { papers };
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

const paperPassesFilters = (paper, filters) => {
  if (filters.topic && !(paper.topics || []).includes(filters.topic)) return false;
  const paperYear = Number(paper.year || 0);
  if (filters.yearMin && paperYear < Number(filters.yearMin)) return false;
  if (filters.yearMax && paperYear > Number(filters.yearMax)) return false;
  return matchesSearch(paper, filters.search);
};

function buildPaperElements(store, filters) {
  const visiblePapers = store.papers.filter((paper) => paperPassesFilters(paper, filters));
  const nodes = visiblePapers.map((paper) => ({
    data: {
      id: `paper:${paper.id}`,
      entityId: paper.id,
      type: "paper",
      label: paper.shortLabel,
      fullTitle: paper.title,
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
      const linkMode = filters.linkMode || "all";
      const useAuthors = linkMode === "all" || linkMode === "authors";
      const useTopics = linkMode === "all" || linkMode === "keywords";
      const activeSharedAuthors = useAuthors ? sharedAuthors : [];
      const activeSharedTopics = useTopics ? sharedTopics : [];

      if (activeSharedAuthors.length === 0 && activeSharedTopics.length === 0) continue;

      const firstAuthorShared =
        !!source.firstAuthorId &&
        !!target.firstAuthorId &&
        source.firstAuthorId === target.firstAuthorId &&
        activeSharedAuthors.includes(source.firstAuthorId);

      const authorScore = activeSharedAuthors.reduce((score, authorId) => {
        const isFirstAuthor = authorId === source.firstAuthorId || authorId === target.firstAuthorId;
        return score + (isFirstAuthor ? 3 : 1.25);
      }, 0);

      const multiAuthorBonus = activeSharedAuthors.length > 1 ? (activeSharedAuthors.length - 1) * 1.4 : 0;
      const topicScore =
        activeSharedTopics.length > 0 ? activeSharedTopics.length * 1.3 + Math.max(0, activeSharedTopics.length - 1) * 0.9 : 0;
      const totalWeight = Number((authorScore + multiAuthorBonus + topicScore).toFixed(2));

      let relation = "topic";
      if (activeSharedAuthors.length > 0 && activeSharedTopics.length > 0) relation = "mixed";
      else if (activeSharedAuthors.length > 0) relation = "coauthor";

      edges.push({
        data: {
          id: `edge:paper:${source.id}:${target.id}`,
          source: `paper:${source.id}`,
          target: `paper:${target.id}`,
          relation,
          label: [
            activeSharedAuthors.length > 0 ? `${activeSharedAuthors.length} shared author${activeSharedAuthors.length > 1 ? "s" : ""}` : "",
            activeSharedTopics.length > 0 ? `${activeSharedTopics.length} shared keyword${activeSharedTopics.length > 1 ? "s" : ""}` : "",
          ]
            .filter(Boolean)
            .join(" · "),
          weight: totalWeight,
          sharedAuthors: activeSharedAuthors,
          sharedTopics: activeSharedTopics,
          firstAuthorShared,
        },
      });
    }
  }

  return { nodes, edges };
}

export function collectFilterOptions(store) {
  return {
    topics: uniq(store.papers.flatMap((paper) => paper.topics || [])).sort(),
    years: uniq(store.papers.map((paper) => String(paper.year || "")))
      .filter(Boolean)
      .sort((a, b) => b.localeCompare(a)),
  };
}

export function buildGraphElements(store, _mode, filters) {
  return buildPaperElements(store, filters);
}
