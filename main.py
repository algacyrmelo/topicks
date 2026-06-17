import csv
import datetime as dt
import sys


def get_topic_score(topic: dict[str, str]) -> float:
    # Review cycles goes from 1 to 4 and it's current value
    # affects the likelihood for a topic to be picked
    cycle_days = {"1": 3, "2": 7, "3": 15, "4": 30}

    last_studied_str = topic["last_studied"]
    # If topic was never studied, give it priority by
    # returning an arbitrary big score
    if last_studied_str == "":
        return 100.0

    last_studied = dt.datetime.strptime(last_studied_str, "%Y-%m-%d")

    review_cycle = topic["review_cycle"]

    due_date = last_studied + dt.timedelta(days=cycle_days[review_cycle])

    now = dt.datetime.now()
    time_since_last_studied = now - last_studied

    delay = now - due_date

    score = (time_since_last_studied.days / cycle_days[review_cycle]) + delay.days
    return score


def pick_next_topic(topics: list[dict[str, str]]) -> dict[str, str]:
    curr_pick = {}
    highest_score = -float("inf")

    for topic in topics:
        curr_score = get_topic_score(topic)
        if curr_score > highest_score:
            curr_pick = topic
            highest_score = curr_score

    return curr_pick


def update_topic_done(topic: dict[str, str]) -> dict[str, str]:
    updated_topic = topic.copy()

    now = dt.date.today()
    updated_topic["last_studied"] = now.strftime("%Y-%m-%d")

    updated_topic["current"] = ""

    curr_cycle = updated_topic["review_cycle"]
    next_cycle = int(curr_cycle) + 1
    if next_cycle > 4:
        next_cycle = 1
    updated_topic["review_cycle"] = str(next_cycle)

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

        curr_i, curr_topic = -1, None
        for i, row in enumerate(reader):
            if row["current"] == "*":
                curr_i, curr_topic = i, row
            topics.append(row)

    done: bool = "--done" in sys.argv

    if curr_topic and curr_i >= 0 and done:
        topics[curr_i] = update_topic_done(curr_topic)

    if not curr_topic and curr_i == -1:
        curr_topic = pick_next_topic(topics)
        for i in range(len(topics)):
            if topics[i] == curr_topic:
                topics[i]["current"] = "*"

    for topic in topics:
        print(f"{topic['name']}{topic['current']}")

    fieldnames = reader.fieldnames
    if fieldnames is None:
        raise Exception("CSV file has no headers")

    with open(filename, mode="w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(topics)


main()
