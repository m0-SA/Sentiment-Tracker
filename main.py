from insert import insert_articles
from sources.gnews import gnews_request
from sources.guardian import guardian_request
from sources.rss import rss_request

topic = "Climate Change"

request_functions = [guardian_request, gnews_request, rss_request]

for func in request_functions:
    try:
        request_data = func(topic)
        insert_articles(request_data)
    except Exception as e:  # noqa: BLE001
        print(f"Failed to execute {func.__name__}: {e}")
