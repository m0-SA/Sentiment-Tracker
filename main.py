import json

from insert import insert_articles
from sources.gnews import gnews_request
from sources.guardian import guardian_request

guardian_request_data = guardian_request("Climate Change")
gnews_request_data = gnews_request("Climate Change")

request_data = [guardian_request_data, gnews_request_data]

# with open("dataDump.json", "w") as file:
#    for item in gnews_request_data:
#        item["fetched"] = item["fetched"].isoformat()

#    json.dump(gnews_request_data, file, indent=4)

for x in request_data:
    insert_articles(x)
