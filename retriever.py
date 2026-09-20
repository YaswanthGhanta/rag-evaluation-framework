from policy_data import policies


def retrieve_policy(question):
    question = question.lower()

    keyword_map = {
        "Annual Leave": [
            "annual leave",
            "vacation",
            "unused leave",
            "carry forward"
        ],
        "Sick Leave": [
            "sick",
            "sick leave",
            "medical certificate"
        ],
        "Remote Work": [
            "remote",
            "work from home",
            "probation"
        ],
        "Parental Leave": [
            "parental",
            "birth",
            "adoption"
        ],
        "Expense Reimbursement": [
            "expense",
            "reimbursement",
            "receipt",
            "claim"
        ]
    }

    scores = {}

    for policy in policies:
        topic = policy["topic"]
        keywords = keyword_map[topic]

        score = 0

        for keyword in keywords:
            if keyword in question:
                score = score + 1

        scores[topic] = score

    highest_score = max(scores.values())

    if highest_score == 0:
        return None

    winners = []

    for topic, score in scores.items():
        if score == highest_score:
            winners.append(topic)

    if len(winners) > 1:
        return None

    winning_topic = winners[0]

    for policy in policies:
        if policy["topic"] == winning_topic:
            return policy

    return None
