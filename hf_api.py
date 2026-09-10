import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from huggingface_hub.errors import HfHubHTTPError, InferenceTimeoutError

load_dotenv()
client = InferenceClient(
    provider="hf-inference",
    api_key=os.environ["HF_TOKEN"],
)


def get_summary_sentiment(summary, model_number=1):
    match model_number:
        case 1:
            return get_summary_sentiment_mode_1(
                summary, "lxyuan/distilbert-base-multilingual-cased-sentiments-student"
            )
        case 2:
            return get_summary_sentiment_mode_1(
                summary, "cardiffnlp/twitter-roberta-base-sentiment-latest"
            )
        case _:
            return {"status": "failed", "detail": "Invalid model selection"}


def get_summary_sentiment_mode_1(summary, model_type):
    try:
        result = client.text_classification(
            summary,
            model=model_type,
        )
    except InferenceTimeoutError as timeout_err:
        print(f"Request Timed Out: {timeout_err}")
        return {
            "status": "failed",
            "detail": "Model is warming up, please try again shortly.",
        }

    except HfHubHTTPError as hf_err:
        print(f"Hugging Face API Error (Status {hf_err.response.status_code}):")
        print(f"Message: {hf_err.server_message}")
        return {
            "status": "failed",
            "detail": "Sentiment check failed. Please try again.",
        }

    except Exception as e:  # noqa: BLE001
        print(f"Unexpected error: {e}")
        return {
            "status": "failed",
            "detail": "Sentiment check failed. Please try again.",
        }

    negative = next(r.score for r in result if r.label.lower() == "negative")
    positive = next(r.score for r in result if r.label.lower() == "positive")
    neutral = next(r.score for r in result if r.label.lower() == "neutral")

    return {
        "status": "success",
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
    }


def get_sentiment_label(positive, negative, neutral):
    highest = max([positive, negative, neutral])
    if highest == positive:
        return "positive"
    elif highest == negative:
        return "negative"
    elif highest == neutral:
        return "neutral"
