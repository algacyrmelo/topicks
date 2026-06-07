import csv
import random
import sys
from datetime import datetime


def pick_next_topic(topics: list[dict[str, str]]) -> dict[str, str]:
    random.seed()
    topic = random.choice(topics)
    return topic


def update_topic_done(topic: dict[str, str]) -> dict[str, str]:
    now = datetime.now()

    updated_topic = topic.copy()
    updated_topic["last_studied"] = now.strftime("%Y-%m-%d")
    updated_topic["current"] = ""
    return updated_topic


def main():
    args = [arg for arg in sys.argv if not arg.startswith("--")]
    if len(args) != 2:
        print("Usage: python3 main.py topics.csv [--done]")
        sys.exit(1)

    topics: list[dict[str, str]] = []

    filename = args[1]
    with open(filename, mode="r", encoding="utf-8", newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        curr_idx, curr_topic = -1, None
        for i, row in enumerate(reader):
            if row["current"] == "*":
                curr_idx, curr_topic = i, row
            topics.append(row)

    done = "--done" in sys.argv

    if curr_topic and not done:
        print(curr_topic)
        sys.exit(0)

    if curr_topic and curr_idx >= 0 and done:
        topics[curr_idx] = update_topic_done(curr_topic)

    if not curr_topic and curr_idx == -1:
        curr_topic = pick_next_topic(topics)
        for i in range(len(topics)):
            if topics[i] == curr_topic:
                topics[i]["current"] = "*"

    print(curr_topic)

    fieldnames = reader.fieldnames
    if fieldnames is None:
        raise Exception("CSV file has no headers")

    with open("topics.csv", mode="w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(topics)


main()
