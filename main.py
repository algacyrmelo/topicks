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
    topic: dict[str, str] = random.choices(candidates, k=1)[0]
    return topic


def update_last_studied(topic: dict[str, str]) -> dict[str, str]:
    updated = topic.copy()
    now = datetime.now()
    updated["last_studied"] = now.strftime("%Y-%m-%d")
    return updated


def main():
    #rows = []
    with open("topics.csv", mode="r", encoding="utf-8", newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        candidates = list(filter(lambda row: row["last_studied"] == "", reader))
        # How can I handle the reader after being consumed?

        topic = pick_topic(candidates)
        topic = update_last_studied(topic)

        print(topic)


main()
