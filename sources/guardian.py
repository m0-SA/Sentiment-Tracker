import os
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GUARDIAN_KEY")


def guardian_request(topic):
    params = {
        "q": topic,  #  search term
        "api-key": api_key,  #  developer key
        "page-size": 10,  # Items per page (max 200)
        "order-by": "newest",  # Order of items
        "show-fields": "bodyText",  # Returns full body text
    }

    response = requests.get("https://content.guardianapis.com/search", params=params)
    response.raise_for_status()
    now_tz = datetime.now(timezone.utc)
    print("Guardian Request...")

    data = response.json()
    item_dicts = []

    for item in data["response"]["results"]:
        itemData = {
            "uniqueID": "Guardian:" + item.get("id"),
            "Title": item.get("webTitle"),
            "Source": item.get("webUrl"),
            "SourceType": "Guardian",
            "Topic": topic,
            "Content": item["fields"].get("bodyText"),
            "publishDate": item.get("webPublicationDate"),
            "fetched": now_tz,
        }
        item_dicts.append(itemData)

    return item_dicts
