from insert import insert_articles
from sources.gnews import gnews_request
from sources.guardian import guardian_request
from sources.rss import rss_request

topic = "Climate Change"
guardian_request_data = guardian_request(topic)
gnews_request_data = gnews_request(topic)
rss_request_data = rss_request(topic)

request_data = [guardian_request_data, gnews_request_data, rss_request_data]


for x in request_data:
    insert_articles(x)
