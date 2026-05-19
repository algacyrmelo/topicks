import csv
import random
from datetime import datetime

SUBJECT_WEIGHTS = {
    "lingua_portuguesa": 12,
    "arquitetura_sistema_informacao": 30,
    "arquitetura_infra": 20,
    "seguranca_cibernetica": 20,
}


def pick_topic(candidates: list[dict[str, str]]) -> dict[str, str]:
    random.seed(42)
    topic: dict[str, str] = random.choice(candidates)
    return topic


def update_last_studied(topic: dict[str, str]) -> dict[str, str]:
    updated_topic = topic.copy()
    now = datetime.now()
    updated_topic["last_studied"] = now.strftime("%Y-%m-%d")
    return updated_topic


def main():
    rows: list[dict[str, str]] = []
    with open("topics.csv", mode="r", encoding="utf-8", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append(row)

    candidates = list(filter(lambda row: row["last_studied"] == "", rows))
    topic = pick_topic(candidates)

    updated_topic = update_last_studied(topic)
    for i in range(len(rows)):
        if rows[i] == topic:
            rows[i] = updated_topic

    fieldnames = reader.fieldnames
    if fieldnames is None:
        raise Exception("CSV file has no headers")

    with open("topics.csv", mode="w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(updated_topic)


main()
