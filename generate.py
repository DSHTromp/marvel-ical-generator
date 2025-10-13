import requests
from datetime import datetime
from ics import Calendar, Event

API_KEY = "YOUR_TMDB_API_KEY"  # vervang dit
SEARCH_URL = "https://api.themoviedb.org/3/discover/movie"
PARAMS = {
    "api_key": API_KEY,
    "with_companies": "420",  # Marvel Studios ID
    "sort_by": "release_date.asc",
    "primary_release_date.gte": datetime.now().strftime("%Y-%m-%d")
}

r = requests.get(SEARCH_URL, params=PARAMS)
data = r.json().get("results", [])

cal = Calendar()

for film in data:
    if not film.get("release_date"):
        continue
    e = Event()
    e.name = film["title"]
    e.begin = film["release_date"]
    e.description = film.get("overview", "")
    e.url = f"https://www.themoviedb.org/movie/{film['id']}"
    cal.events.add(e)

with open("marvel.ics", "w", encoding="utf-8") as f:
    f.writelines(cal)
