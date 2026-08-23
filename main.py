from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from insert import insert_articles
from scoring import aggregate_score, aggregate_score_all, append_scores
from sources.gnews import gnews_request
from sources.guardian import guardian_request
from sources.rss import rss_request

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
