from db import get_connection


def insert_articles(request_data):
    with get_connection() as conn, conn.cursor() as cur:
        cur.executemany(
            "INSERT INTO mentionData (UniqueID, Title, Source, SourceType, Topic, Content, publishDate, fetched, positive, negative, neutral, compound)"
            "VALUES (%(uniqueID)s, %(Title)s, %(Source)s, %(SourceType)s, %(Topic)s, %(Content)s, %(publishDate)s, %(fetched)s, %(positive)s, %(negative)s, %(neutral)s, %(compound)s)"
            "ON CONFLICT (UniqueID) DO NOTHING",
            request_data,
        )
