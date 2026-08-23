from db import get_connection


def append_scores(data_dict, sid):
    if data_dict.get("Content") is None:
        data_dict.update(
            {
                "positive": None,
                "negative": None,
                "neutral": None,
                "compound": None,
            }
        )
        return data_dict

    content = data_dict["Title"] + " - " + data_dict["Content"]

    sentiment_dict = sid.polarity_scores(content)

    data_dict.update(
        {
            "positive": sentiment_dict["pos"],
            "negative": sentiment_dict["neg"],
            "neutral": sentiment_dict["neu"],
            "compound": sentiment_dict["compound"],
        }
    )

    return data_dict


def aggregate_score_all(topic):

    data = {"topic": topic}

    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT SUM(CASE WHEN SourceType = 'Guardian' THEN compound*2 ELSE compound*1 END)/ SUM(CASE WHEN SourceType = 'Guardian' THEN 2 ELSE 1 END) "
            "FROM mentionData "
            "WHERE Topic = %(topic)s AND Compound IS NOT NULL ",
            data,
        )
        all_sources = cur.fetchone()

        return all_sources[0]


def aggregate_score(topic, source_type):

    data = {"topic": topic, "source_type": source_type}

    with get_connection() as conn, conn.cursor() as cur:
        if "RSS".lower() in source_type.lower():
            cur.execute(
                "SELECT AVG(Compound) "
                "FROM mentionData "
                "WHERE Topic = %(topic)s  AND SourceType LIKE '%%RSS%%' AND Compound IS NOT NULL ",
                data,
            )
        else:
            cur.execute(
                "SELECT AVG(Compound) "
                "FROM mentionData "
                "WHERE Topic = %(topic)s AND SourceType = %(source_type)s AND Compound IS NOT NULL ",
                data,
            )

        all_sources = cur.fetchone()

        return all_sources[0]
