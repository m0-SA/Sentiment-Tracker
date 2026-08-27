import textwrap

from db import get_connection


def build_item_block(topic):
    data = {"topic": topic}

    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT ID, SourceType, Title, Content "
            "FROM mentionData "
            "WHERE Topic= %(topic)s AND SourceType = 'Guardian' ORDER BY publishDate DESC LIMIT 10",
            data,
        )
        items_guardian = cur.fetchall()

        cur.execute(
            "SELECT ID, SourceType, Title, Content "
            "FROM mentionData "
            "WHERE Topic = %(topic)s AND SourceType = 'GNews' ORDER BY publishDate DESC LIMIT 50 ",
            data,
        )
        items_gnews = cur.fetchall()

        cur.execute(
            "SELECT ID, SourceType, Title, Content "
            "FROM mentionData "
            "WHERE Topic = %(topic)s AND SourceType LIKE '%%RSS%%' ORDER BY publishDate DESC LIMIT 50",
            data,
        )
        items = cur.fetchall()

        items.extend(items_guardian)
        items.extend(items_gnews)

    results = "\n".join(
        f"[ID: {item_id}] Source: {source_type} | Title: {title} Content: {truncateContent(content, source_type)}"
        for item_id, source_type, title, content in items
    )

    return results


def build_user_message(topic, items_block):
    message = f"Topic: {topic} \n---BEGIN ITEMS---\n{items_block}\n---END ITEMS---"
    return message


def truncateContent(content, source_type):
    if source_type == "Guardian":
        content = textwrap.shorten(content, width=2000, placeholder="...")
        return content
    else:
        return content
