import json

from db import get_connection
from sources.guardian import guardian_request

guardian_request_data = guardian_request("Climate Change")
# with open("dataDump.json", "w") as file:
#    for item in guardian_request_data:
#        item["fetched"] = item["fetched"].isoformat()

#    json.dump(guardian_request_data, file, indent=4)

with get_connection() as conn, conn.cursor() as cur:
    cur.executemany(
        "INSERT INTO mentionData (UniqueID, Title, Source, SourceType, Topic, Content, publishDate, fetched)"
        "VALUES (%(uniqueID)s, %(Title)s, %(Source)s, %(SourceType)s, %(Topic)s, %(Content)s, %(publishDate)s, %(fetched)s)"
        "ON CONFLICT (UniqueID) DO NOTHING",
        guardian_request_data,
    )
    print("Guardian Items Added...")
    conn.commit()
