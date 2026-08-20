import json

from sources.guardian import guardian_request

i = guardian_request("Climate Change")
with open("dataDump.json", "w") as file:
    for x in i:
        x["fetched"] = x["fetched"].isoformat()

    json.dump(i, file, indent=4)
