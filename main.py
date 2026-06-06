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

        current_topic = None
        for row in reader:
            if row["current"] == "*":
                current_topic = row
            topics.append(row)

    done = "--done" in sys.argv

    if current_topic and not done:
        print(current_topic)
        sys.exit(0)

    if current_topic and done:
        for i in range(len(topics)):
            if topics[i] == current_topic:
                topics[i] = update_topic_done(current_topic)

    if not current_topic:
        current_topic = pick_next_topic(topics)
        for i in range(len(topics)):
            if topics[i] == current_topic:
                topics[i]["current"] = "*"

    print(current_topic)

    fieldnames = reader.fieldnames
    if fieldnames is None:
        raise Exception("CSV file has no headers")

    with open("topics.csv", mode="w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(topics)


main()
