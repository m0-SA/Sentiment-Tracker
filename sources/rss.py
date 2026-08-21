import calendar
import hashlib
from datetime import datetime, timezone

import feedparser


def rss_request(topic):

    feed_list = []
    feed_list.append(feedparser.parse("https://feeds.bbci.co.uk/news/world/rss.xml"))
    feed_list.append(feedparser.parse("https://feeds.bbci.co.uk/news/rss.xml"))

    now_tz = datetime.now(timezone.utc)
    print("RSS Request...")
    item_dicts = []

    for feed in feed_list:
        for item in feed.entries:
            if (
                topic.lower() in item.get("title").lower()
                or topic.lower() in item.get("summary").lower()
            ):
                st = item.get("published_parsed")
                timestamp = calendar.timegm(st)
                dt_utc = datetime.fromtimestamp(timestamp, tz=timezone.utc)

                itemData = {
                    "uniqueID": "BBC:"
                    + hashlib.sha256(item.get("link").encode()).hexdigest(),
                    "Title": item.get("title"),
                    "Source": item.get("link"),
                    "SourceType": "BBC RSS",
                    "Topic": topic,
                    "Content": item.get("summary"),
                    "publishDate": dt_utc,
                    "fetched": now_tz,
                }
                item_dicts.append(itemData)
    return item_dicts
