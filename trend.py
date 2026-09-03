from db import get_connection


def get_date_difference(topic):

    data = {"topic": topic}

    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT MIN(publishDate) AS earliest_date, MAX(publishDate) AS latest_date "
            "FROM mentionData "
            "WHERE Topic = %(topic)s",
            data,
        )
        dates = cur.fetchone()

        earliest_time, latest_time = dates
        if latest_time == earliest_time:
            return None

        total_time_difference = latest_time - earliest_time
        days = total_time_difference.days

        if days > 180:
            return "month"
        elif days > 30:
            return "week"
        elif days > 1:
            return "day"
        else:
            return "hour"


def calc_trend(topic, unit):
    data = {"topic": topic, "unit": unit}

    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT date_trunc(%(unit)s, publishDate), SUM(CASE WHEN SourceType = 'Guardian' THEN compound*2 ELSE compound*1 END)/ SUM(CASE WHEN SourceType = 'Guardian' THEN 2 ELSE 1 END) "
            "FROM mentionData "
            "WHERE Topic = %(topic)s AND Compound IS NOT NULL "
            "GROUP BY date_trunc(%(unit)s, publishDate) "
            "ORDER By date_trunc(%(unit)s, publishDate) ",
            data,
        )
        response = cur.fetchall()
    result = []
    for trend in response:
        result.append({"date": trend[0].isoformat(), "score": trend[1]})

    return result
