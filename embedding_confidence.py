from evaluation_data import evaluation_cases
from semantic_retriever import retrieve_top_k


policy_exists_scores = []
no_policy_scores = []

category_scores = {}


print("\n===== EMBEDDING CONFIDENCE ANALYSIS =====\n")


for case in evaluation_cases:

    question = case["question"]
    expected_policy = case["expected_policy"]
    category = case["category"]

    # Get semantic retrieval results
    results = retrieve_top_k(question, k=3)

    top1 = results[0]

    retrieved_policy = top1["policy"]["id"]
    top1_score = top1["score"]

    # ------------------------------------------
    # STORE BY WHETHER A POLICY EXISTS
    # ------------------------------------------

    if expected_policy is None:
        no_policy_scores.append(top1_score)
    else:
        policy_exists_scores.append(top1_score)

    # ------------------------------------------
    # STORE BY CATEGORY
    # ------------------------------------------

    if category not in category_scores:
        category_scores[category] = []

    category_scores[category].append(top1_score)

    # ------------------------------------------
    # PRINT INDIVIDUAL CASE
    # ------------------------------------------

    print("=" * 70)
    print("QUESTION:", question)
    print("CATEGORY:", category)
    print("EXPECTED POLICY:", expected_policy)
    print("EMBEDDING TOP-1:", retrieved_policy)
    print("TOP-1 SCORE:", round(top1_score, 3))
# ==================================================
# SUMMARY FUNCTIONS
# ==================================================


def print_score_summary(name, scores):

    print(f"\n{name}")

    print("Cases:", len(scores))

    print(
        "Minimum:",
        round(min(scores), 3)
    )

    print(
        "Maximum:",
        round(max(scores), 3)
    )

    print(
        "Average:",
        round(sum(scores) / len(scores), 3)
    )


print("\n\n===== POLICY EXISTENCE ANALYSIS =====")

print_score_summary(
    "POLICY EXISTS",
    policy_exists_scores
)

print_score_summary(
    "NO POLICY EXISTS",
    no_policy_scores
)


print("\n\n===== CATEGORY SCORE ANALYSIS =====")

for category, scores in category_scores.items():

    print_score_summary(
        category,
        scores
    )
