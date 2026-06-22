import csv
import sys
from pathlib import Path

from topick import display_topics, pick_topic_by_highest_score, update_topic_done


def main():
    # Validate count of provided arguments.
    args = [arg for arg in sys.argv if not arg.startswith("--")]
    if len(args) != 2:
        print("Usage: python3 main.py file.csv [--done]")
        sys.exit(1)

    # Init command options.
    topic_done: bool = "--done" in sys.argv

    # Validate filepath argument.
    filepath = Path(args[1])
    if not filepath.exists() or not filepath.is_file():
        print("Error: Invalid filepath.")
        sys.exit(1)

    # Read csv data into memory.
    topics: list[dict[str, str]] = []
    with open(filepath, mode="r", encoding="utf-8", newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        fieldnames = reader.fieldnames
        if fieldnames is None:
            print("Error: Missing CSV headers.")
            sys.exit(1)

        curr_i, curr_topic = -1, None
        for i, row in enumerate(reader):
            if row["current"] == "*":
                curr_i, curr_topic = i, row
            topics.append(row)

    # Mark current topic as done.
    if curr_topic is not None and curr_i >= 0 and topic_done:
        topics[curr_i] = update_topic_done(curr_topic)
        curr_topic = None

    # Pick the highest score's topic.
    if curr_topic is None and curr_i == -1 and not topic_done:
        curr_topic = pick_topic_by_highest_score(topics)

        for i in range(len(topics)):
            if topics[i] == curr_topic:
                topics[i]["current"] = "*"
                break

    display_topics(topics, curr_topic)

    # Write current topics data back to disk.
    with open(filepath, mode="w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(topics)


main()
