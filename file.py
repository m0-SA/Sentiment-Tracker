import csv
import json
import os
from datetime import datetime, timezone


def dump_json(file_name, response):
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(response, file, indent=4, ensure_ascii=False)


def write_token_log(usage, topic):
    usage_rows = [
        datetime.now(timezone.utc),
        topic,
        usage.get("prompt_tokens", 0),
        usage.get("completion_tokens", 0),
        usage.get("total_tokens", 0),
        usage.get("neurons", 0),
    ]
    usage_csv = "token_log.csv"
    usage_csv_exists = os.path.isfile(usage_csv)

    with open(usage_csv, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not usage_csv_exists:
            writer.writerow(
                [
                    "Log Time",
                    "Topic",
                    "Prompt Tokens",
                    "Completion Tokens",
                    "Total Tokens",
                    "Neurons",
                ]
            )

        writer.writerow(usage_rows)
