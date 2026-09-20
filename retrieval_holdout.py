from semantic_retriever import retrieve_top_k
holdout_cases = [

    # ==========================================
    # RELEVANT POLICY EXISTS
    # ==========================================

    {
        "question": "What is the maximum number of vacation days I can move into next year?",
        "expected_policy": "HR001",
        "type": "policy_exists"
    },

    {
        "question": "What documentation is required for a prolonged sickness absence?",
        "expected_policy": "HR002",
        "type": "policy_exists"
    },

    {
        "question": "Are employees in their probation period eligible to work from home?",
        "expected_policy": "HR003",
        "type": "policy_exists"
    },

    {
        "question": "How long is the paid leave provided after adopting a child?",
        "expected_policy": "HR004",
        "type": "policy_exists"
    },

    {
        "question": "Is a receipt required when submitting a work-related expense?",
        "expected_policy": "HR005",
        "type": "policy_exists"
    },

    {
        "question": "What happens if I have more than five unused vacation days?",
        "expected_policy": "HR001",
        "type": "policy_exists"
    },

    {
        "question": "I have been absent because of illness for several working days. What certificate do I need?",
        "expected_policy": "HR002",
        "type": "policy_exists"
    },

    {
        "question": "How often can an employee work away from the office each week?",
        "expected_policy": "HR003",
        "type": "policy_exists"
    },

    {
        "question": "Does adoption qualify an employee for paid parental leave?",
        "expected_policy": "HR004",
        "type": "policy_exists"
    },

    {
        "question": "Is there a deadline for filing an employee business expense?",
        "expected_policy": "HR005",
        "type": "policy_exists"
    },


    # ==========================================
    # NO RELEVANT POLICY EXISTS
    # ==========================================

    {
        "question": "What are the standard office working hours?",
        "expected_policy": None,
        "type": "no_policy"
    },

    {
        "question": "Does the company provide dental insurance?",
        "expected_policy": None,
        "type": "no_policy"
    },

    {
        "question": "What laptop will I receive when I join?",
        "expected_policy": None,
        "type": "no_policy"
    },

    {
        "question": "Is there a company shuttle service for employees?",
        "expected_policy": None,
        "type": "no_policy"
    },

    {
        "question": "How frequently are employee performance reviews conducted?",
        "expected_policy": None,
        "type": "no_policy"
    },

    {
        "question": "What is the notice period for resignation?",
        "expected_policy": None,
        "type": "no_policy"
    },

    {
        "question": "Are employees given a joining bonus?",
        "expected_policy": None,
        "type": "no_policy"
    },

    {
        "question": "What parking facilities are available at the office?",
        "expected_policy": None,
        "type": "no_policy"
    },

    {
        "question": "Does the company offer training programs for employees?",
        "expected_policy": None,
        "type": "no_policy"
    },

    {
        "question": "What are the rules for employee promotions?",
        "expected_policy": None,
        "type": "no_policy"
    }
]


policy_scores = []
no_policy_scores = []

policy_correct = 0


print("\n===== HOLDOUT RETRIEVAL TEST =====\n")


for case in holdout_cases:

    question = case["question"]
    expected_policy = case["expected_policy"]
    case_type = case["type"]

    results = retrieve_top_k(question, k=3)

    top1 = results[0]

    retrieved_policy = top1["policy"]["id"]
    score = top1["score"]

    if case_type == "policy_exists":

        policy_scores.append(score)

        if retrieved_policy == expected_policy:
            policy_correct += 1

    else:
        no_policy_scores.append(score)

    print("=" * 70)
    print("QUESTION:", question)
    print("TYPE:", case_type)
    print("EXPECTED POLICY:", expected_policy)
    print("TOP-1 POLICY:", retrieved_policy)
    print("TOP-1 SCORE:", round(score, 3))


def show_summary(name, scores):

    print(f"\n{name}")
    print("Cases:", len(scores))
    print("Minimum:", round(min(scores), 3))
    print("Maximum:", round(max(scores), 3))
    print(
        "Average:",
        round(sum(scores) / len(scores), 3)
    )


print("\n\n===== HOLDOUT SUMMARY =====")

show_summary(
    "POLICY EXISTS",
    policy_scores
)

show_summary(
    "NO POLICY EXISTS",
    no_policy_scores
)


print(
    "\nPolicy Selection Accuracy:",
    policy_correct / len(policy_scores)
)
