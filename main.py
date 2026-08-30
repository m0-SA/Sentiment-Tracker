from fastapi import FastAPI
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from file import write_token_log
from insert import insert_articles
from scoring import (
    aggregate_score,
    aggregate_score_all,
    append_scores,
    get_source_types,
)
from sources.gnews import gnews_request
from sources.guardian import guardian_request
from sources.rss import rss_request
from trend import calc_trend, get_date_difference
from workers_ai import get_themes, verify_comments
from workers_message import build_item_block, build_user_message

app = FastAPI()


@app.post("/topics/{topic}/ingest")
def ingest(topic: str):
    topic = topic.title()
    request_functions = [guardian_request, gnews_request, rss_request]
    sid = SentimentIntensityAnalyzer()
    results = {}

    for func in request_functions:
        try:
            request_data = func(topic)
            for dictionary in request_data:
                append_scores(dictionary, sid)
            insert_articles(request_data)

            results[func.__name__] = {
                "Status": "Success",
                "Detail": "Successfully stored data",
            }
        except Exception as e:  # noqa: BLE001
            print(f"Failed to execute {func.__name__}: {e}")
            results[func.__name__] = {"Status": "Failed", "Detail": str(e)}
    return results


@app.get("/topics/{topic}/sentiment")
def sentiment(topic: str):
    topic = topic.title()
    source_types = get_source_types(topic)

    total_aggregate_score = aggregate_score_all(
        topic
    )  # overall aggregate score for topic
    sources_aggregate_score = {}
    for source in source_types:
        sources_aggregate_score.update({source: aggregate_score(topic, source)})
    result = {
        "Overall Aggregate Score": total_aggregate_score,
        "Score Per Source": sources_aggregate_score,
    }
    return result


@app.get("/topics/{topic}/trend")
def trend(topic: str):
    topic = topic.title()
    unit = get_date_difference(topic)
    if unit is None:
        return {"trend": [], "message": "Not enough data"}
    trend = calc_trend(topic, unit)
    return trend


@app.get("/topics/{topic}/analysis")
def analysis(topic: str):
    topic = topic.title()
    try:
        item_block, database_items = build_item_block(topic)
        user_message = build_user_message(topic, item_block)
        response, usage = get_themes(user_message)
        write_token_log(usage, topic)
        verified_comments, paraphrased_comments = verify_comments(
            response["representative_comments"], database_items
        )
    except Exception as e:  # noqa: BLE001
        print(f"Failed during analysis pipeline': {e}")
        return {"Status": "Failed", "Detail": str(e)}

    results = {
        "Themes": response["themes"],
        "Summary": response["summary"],
        "Verified Comments": verified_comments,
        "Paraphrased Comments": paraphrased_comments,
    }

    return results
