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
                "content": "You are analysing the general sentiment about a chosen topic for a dashboard. \n\n1. You will find up to five themes within the given items regarding the topic given. if there are few than five themes, return fewer. Each theme should be at most 5 words. The topic itself cannot be a theme. The strings within the themes list of strings is each theme. \n\n2. You then must summarize the collection of items for the topic chosen.  This summary is the overall narrative formed over the collection of items regarding the topic. The summary string contains this. Do not refer to items within summary, but instead as the 'data'. \n\n3. Finally, you extract up to five of what you determine are the most relevant comments from the collection of items. If there are few than five relevant comments, return fewer. The most relevant comments are the comments which represents the overall sentiment of the topic as well as themes you have identified. \nA. You must select text using ONLY direct quotes from the provided items. \nB. Do not rewrite, summarize, or paraphrase any words. Do not fix typos. Do not reword. Quote the comment completely word-for-word. \nC. Each representative comment object must contain the exact original ID and the quoted excerpt text. \nE. Do NOT repeat comments. \nD. NO MORE than five comments",
            },
            {"role": "user", "content": user_message},
        ],
        "max_tokens": 1024,
        "temperature": 0.3,
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "strict": True,
                "type": "object",
                "properties": {
                    "themes": {"type": "array", "items": {"type": "string"}},
                    "summary": {"type": "string"},
                    "representative_comments": {
                        "type": "array",
                        "maxItems": 5,
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
    result_response = result["result"]["response"]
    result_usage = result["result"]["usage"]

    return result_response, result_usage


def verify_comments(worker_data, database_items):
    verified_comments = []
    paraphrased_comments = []
    for comment in worker_data:
        for item in database_items:
            if comment["id"] == item["ID"]:
                if comment["excerpt"] in item["Content"]:
                    verified_comments.append(comment)
                    print("Comment Succeeded Verification")
                else:
                    paraphrased_comments.append(comment)
                    print("Comment Failed Verification")
                break

    return verified_comments, paraphrased_comments
