import os
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GNEWS_KEY")


def gnews_request(topic):
    params = {
        "apikey": api_key,  #  developer key
        "q": topic,  #  search term
        "max": 10,  # max result
        "lang": "en",  # returns english articles
    }

    response = requests.get("https://gnews.io/api/v4/search", params=params)
    response.raise_for_status()
    now_tz = datetime.now(timezone.utc)
    print("GNews Request...")

    data = response.json()
    item_dicts = []
    for item in data["articles"]:
        itemData = {
            "uniqueID": "GNews:" + item.get("id"),
            "Title": item.get("title"),
            "Source": item.get("url"),
            "SourceType": "GNews",
            "Topic": topic,
            "Content": item.get("content"),
            "publishDate": item.get("publishedAt"),
            "fetched": now_tz,
        }
        item_dicts.append(itemData)

    return item_dicts
