from db import get_connection


def insert_weight(topic, weight):
    data = {"topic": topic, "weight": weight}
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO sourceWeights (topic, weight)"
            "VALUES (%(topic)s, %(weight)s)"
            "ON CONFLICT (topic) DO UPDATE SET weight = %(weight)s",
            data,
        )


def get_weight(topic):
    data = {"topic": topic}
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT weight FROM sourceWeights WHERE topic = %(topic)s",
            data,
        )
        weight = cur.fetchone()
        if weight is None:
            return 2
        return weight[0]


def remove_weight(topic):
    data = {"topic": topic}
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            "DELETE FROM sourceWeights WHERE topic = %(topic)s",
            data,
        )
