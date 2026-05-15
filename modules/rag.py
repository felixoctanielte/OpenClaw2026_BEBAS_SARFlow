from pathlib import Path

import yaml


def load_rag_sources(config_path: str) -> list[dict]:
    with open(config_path, "r", encoding="utf-8") as f:
        sources = yaml.safe_load(f) or []

    docs = []
    for source in sources:
        path = Path(source["path"])
        if path.is_dir():
            for child in sorted(path.glob("*.md")):
                text = child.read_text(encoding="utf-8")
                docs.append(
                    {
                        **source,
                        "id": f"{source['id']}:{child.stem}",
                        "path": str(child),
                        "text": text,
                        "metadata": _parse_frontmatter(text),
                    }
                )
        else:
            text = path.read_text(encoding="utf-8") if path.exists() else ""
            docs.append({**source, "text": text, "metadata": _parse_frontmatter(text)})
    return docs


def search_rag(docs: list[dict], query: str, limit: int = 3) -> list[dict]:
    query_terms = [term.lower() for term in query.split() if len(term) > 3]
    scored = []
    for doc in docs:
        text = doc.get("text", "")
        lower = text.lower()
        score = sum(lower.count(term) for term in query_terms)
        if score <= 0:
            continue
        snippet = _best_snippet(text, query_terms)
        scored.append({"id": doc["id"], "score": score, "snippet": snippet})
    scored.sort(key=lambda item: item["score"], reverse=True)
    return scored[:limit]


def _best_snippet(text: str, query_terms: list[str]) -> str:
    paragraphs = [part.strip() for part in text.split("\n\n") if part.strip()]
    if not paragraphs:
        return ""
    best = max(paragraphs, key=lambda part: sum(part.lower().count(term) for term in query_terms))
    compact = " ".join(best.split())
    return compact[:220] + ("..." if len(compact) > 220 else "")


def _parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    try:
        parsed = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return {}
    return parsed if isinstance(parsed, dict) else {}

