
import sqlite3
import requests
from bs4 import BeautifulSoup

DB_PATH = "retrieval_data.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS retrieval_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            title TEXT,
            description TEXT,
            url TEXT
        )
    """)
    conn.commit()
    conn.close()

def scrape_retrieval_data():
    """
    Simple scraper for Stevens Creek Chevrolet retrieval_data.
    (Replace selectors as needed when testing against real site)
    """
    url = "https://www.stevenscreekchevy.com"
    resp = requests.get(url, timeout=15)
    soup = BeautifulSoup(resp.text, "html.parser")

    retrieval_data = []
    for offer in soup.select(".vehicle-card"):  # placeholder selector
        title = offer.select_one(".vehicle-title").get_text(strip=True) if offer.select_one(".vehicle-title") else "Unknown"
        desc = offer.get_text(" ", strip=True)
        link = offer.find("a")["href"] if offer.find("a") else url
        retrieval_data.append(("vehicle", title, desc, link))

    store_retrieval_data(retrieval_data)

def store_retrieval_data(retrieval_data):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executemany(
        "INSERT INTO retrieval_data (category, title, description, url) VALUES (?, ?, ?, ?)",
        retrieval_data
    )
    conn.commit()
    conn.close()
