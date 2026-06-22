import datetime as dt


def pick_topic_by_highest_score(topics: list[dict[str, str]]) -> dict[str, str]:
    curr_pick = {}
    highest_score = -float("inf")

    for topic in topics:
        curr_score = score_topic(topic)
        if curr_score > highest_score:
            curr_pick = topic
            highest_score = curr_score

    return curr_pick


def score_topic(topic: dict[str, str]) -> float:
    # Review cycles goes from 1 to 4 and it's current value
    # affects the likelihood for a topic to be picked.
    cycle_days = {"1": 3, "2": 7, "3": 15, "4": 30}

    last_studied_str = topic["last_studied"]
    # If topic was never studied, give it high priority
    # by returning an arbitrary big score.
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


def display_topics(topics: list[dict[str, str]], curr_topic: dict[str, str] | None):
    if curr_topic is not None:
        last_studied = curr_topic["last_studied"] or "Not studied"
        print(f"▶ {curr_topic['name']}")
        print(f"  Subject:       {curr_topic['subject']}")
        print(f"  Cycle:         {curr_topic['review_cycle']}")
        print(f"  Last studied: {last_studied}")
    else:
        for topic in topics:
            last_studied = topic["last_studied"] or "—"
            print(
                f"  {topic['name']} ({topic['subject']}) — cycle {topic['review_cycle']}, last studied: {last_studied}"
            )
