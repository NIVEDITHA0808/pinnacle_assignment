
import re
import sqlite3

DB_PATH = "retrieval_data.db"

def search_retrieval_data(query: str, limit: int = 3):
    """
    Simple keyword-based retriever.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT title, description, url FROM retrieval_data")
    rows = cur.fetchall()
    conn.close()

    # naive keyword matching
    q_terms = set(re.findall(r"\w+", query.lower()))
    scored = []
    for title, desc, url in rows:
        text = (title + " " + desc).lower()
        overlap = len([t for t in q_terms if t in text])
        if overlap > 0:
            scored.append((overlap, title, desc, url))

    # sort by overlap
    scored.sort(reverse=True, key=lambda x: x[0])
    results = [
        f"{title}\n{desc}\nMore info: {url}"
        for _, title, desc, url in scored[:limit]
    ]
    return "\n\n".join(results) if results else "No current specials matched your query."
