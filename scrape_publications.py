import requests
import pandas as pd


AUTHOR_NAME = "Paolo Soda"
OUT_CSV = "paolo_soda_openalex_publications.csv"


def get_json(url, params=None):
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.json()


# 1. Cerca autore su OpenAlex
authors_url = "https://api.openalex.org/authors"

authors_data = get_json(authors_url, params={
    "search": AUTHOR_NAME,
    "per-page": 10
})

candidates = authors_data.get("results", [])

print("\nCandidati trovati:\n")

for i, a in enumerate(candidates, start=1):
    affiliations = []

    for aff in a.get("affiliations", []):
        inst = aff.get("institution", {})
        if inst.get("display_name"):
            affiliations.append(inst["display_name"])

    print(f"{i}. {a.get('display_name')}")
    print(f"   OpenAlex ID: {a.get('id')}")
    print(f"   Works count: {a.get('works_count')}")
    print(f"   Citations: {a.get('cited_by_count')}")
    print(f"   Affiliations: {', '.join(affiliations[:3])}")
    print()


choice = int(input("Seleziona il numero corretto dell'autore: "))
author_id = candidates[choice - 1]["id"].replace("https://openalex.org/", "")

print(f"\nAutore selezionato: {candidates[choice - 1]['display_name']}")
print(f"ID OpenAlex: {author_id}")


# 2. Scarica tutti i lavori associati all'autore
works_url = "https://api.openalex.org/works"

cursor = "*"
rows = []

while cursor:
    data = get_json(works_url, params={
        "filter": f"authorships.author.id:{author_id}",
        "sort": "publication_year:desc",
        "per-page": 200,
        "cursor": cursor
    })

    for w in data.get("results", []):
        source = (
            w.get("primary_location", {})
             .get("source", {}) or {}
        )

        authors = []
        for auth in w.get("authorships", []):
            author = auth.get("author", {})
            if author.get("display_name"):
                authors.append(author["display_name"])

        rows.append({
            "title": w.get("title"),
            "year": w.get("publication_year"),
            "publication_date": w.get("publication_date"),
            "type": w.get("type"),
            "venue": source.get("display_name"),
            "doi": w.get("doi"),
            "openalex_url": w.get("id"),
            "cited_by_count": w.get("cited_by_count"),
            "authors": "; ".join(authors),
        })

    cursor = data.get("meta", {}).get("next_cursor")

    if not data.get("results"):
        break

    print(f"Scaricati finora: {len(rows)}")


df = pd.DataFrame(rows)

df = df.drop_duplicates(subset=["title", "year", "doi"])

df.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")

print(f"\nCompletato. Pubblicazioni salvate: {len(df)}")
print(f"File creato: {OUT_CSV}")