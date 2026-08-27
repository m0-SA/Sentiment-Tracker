import os

import requests
from dotenv import load_dotenv

load_dotenv()
account_id = os.getenv("ACCOUNT_ID")
model_name = "@cf/meta/llama-3.1-8b-instruct-fast"
workers_token = os.getenv("CLOUDFLARE_AI_TOKEN")
account_url = (
    f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model_name}"
)


def get_themes(user_message):

    request_message = {
        "messages": [
            {
                "role": "system",
                "content": "You are analysing the general sentiment about a chosen topic for a dashboard. You will find up to five themes within the given items regarding the topic given. if there are few than five themes, return fewer. The  strings within the themes list of strings is each theme. You then must summarize the collection of items for the topic chosen.  This summary is the overall narrative formed over the collection of items regarding the topic. The summary string contains this. Finally, you extract up to five of what you determine are the most relevant comments from the collection of items. If there are few than five relevant comments, return fewer. The most relevant comments are the comments which represents the overall sentiment of the topic as well as themes you have identified. You cannot paraphrase. Quote the relevant comment exactly. Each representative comment object must contain the exact original ID and the quoted excerpt text.",
            },
            {"role": "user", "content": user_message},
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "type": "object",
                "properties": {
                    "themes": {"type": "array", "items": {"type": "string"}},
                    "summary": {"type": "string"},
                    "representative_comments": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "excerpt": {"type": "string"},
                            },
                            "required": ["id", "excerpt"],
                        },
                    },
                },
                "required": ["themes", "summary", "representative_comments"],
            },
        },
    }
    response = requests.post(
        account_url,
        headers={"Authorization": f"Bearer {workers_token}"},
        json=request_message,
    )
    result = response.json()
    return result
