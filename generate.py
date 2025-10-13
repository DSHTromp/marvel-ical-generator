import os
import requests
from datetime import datetime
from ics import Calendar, Event

API_KEY = os.getenv("TMDB_API_KEY")  # komt uit GitHub Secret
SEARCH_URL = "https://api.themoviedb.org/3/discover/movie"
PARAMS = {
    "api_key": API_KEY,
    "with_companies": "420",  # Marvel Studios ID op TMDB
    "sort_by": "release_date.asc",
    "primary_release_date.gte": datetime.now().strftime("%Y-%m-%d")
}

print("Fetching Marvel movies...")
response = requests.get(SEARCH_URL, params=PARAMS)
data = response.json().get("results", [])

cal = Calendar()

for film in data:
    release = film.get("release_date")
    if not release:
        continue
    e = Event()
    e.name = film["title"]
    e.begin = release
    e.description = film.get("overview", "")
    e.url = f"https://www.themoviedb.org/movie/{film['id']}"
    cal.events.add(e)

print(f"Adding {len(cal.events)} events to calendar...")

with open("marvel.ics", "w", encoding="utf-8") as f:
    f.writelines(cal)

print("marvel.ics created successfully!")
