import json

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from insert import insert_articles
from scoring import aggregate_score, aggregate_score_all, append_scores
from sources.gnews import gnews_request
from sources.guardian import guardian_request
from sources.rss import rss_request
from workers_ai import get_themes, verify_comments
from workers_message import build_item_block, build_user_message

topic = "Climate Change"

request_functions = [guardian_request, gnews_request, rss_request]

sid = SentimentIntensityAnalyzer()
sources = []

for func in request_functions:
    try:
        request_data = func(topic)

        for dictionary in request_data:
            source_type = dictionary.get("SourceType")
            if "rss" in source_type.lower() and "rss" not in sources:
                sources.append("rss")
            elif source_type not in sources:
                sources.append(dictionary.get("SourceType"))

            append_scores(dictionary, sid)

        insert_articles(request_data)
    except Exception as e:  # noqa: BLE001
        print(f"Failed to execute {func.__name__}: {e}")

total_aggregate_score = aggregate_score_all(topic)
sources_aggregate_score = {}
for source in sources:
    sources_aggregate_score.update({source: aggregate_score(topic, source)})

item_block, database_items = build_item_block(topic)
user_message = build_user_message(topic, item_block)
response = get_themes(user_message)
verified_comments = verify_comments(response["representative_comments"], database_items)

print(verified_comments)

with open("dumptext.json", "w", encoding="utf-8") as file:
    json.dump(response, file, indent=4, ensure_ascii=False)
