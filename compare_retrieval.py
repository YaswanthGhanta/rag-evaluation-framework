from evaluation_data import evaluation_cases
from reranker import rerank_policies
from semantic_retriever import retrieve_top_k

embedding_correct = 0
reranker_correct = 0
total_cases = len(evaluation_cases)

embedding_answerable_correct = 0
reranker_answerable_correct = 0
answerable_cases = 0

print("\n===== RETRIEVAL COMPARISON =====\n")

for case in evaluation_cases:

    question = case["question"]
    expected_policy = case["expected_policy"]
    category = case["category"]

    # ------------------------------------------
    # EMBEDDING RETRIEVAL
    # ------------------------------------------

    embedding_results = retrieve_top_k(question, k=3)

    embedding_top1 = embedding_results[0]
    embedding_policy = embedding_top1["policy"]
    embedding_policy_id = embedding_policy["id"]
    embedding_score = embedding_top1["score"]

    embedding_is_correct = (
        embedding_policy_id == expected_policy
    )

    # ------------------------------------------
    # RERANKER
    # ------------------------------------------

    reranked_results = rerank_policies(question, k=3)

    rerank_top1 = reranked_results[0]
    rerank_policy = rerank_top1["policy"]
    rerank_policy_id = rerank_policy["id"]
    rerank_score = rerank_top1["rerank_score"]

    top2_rerank_score = reranked_results[1]["rerank_score"]
    rerank_margin = rerank_score - top2_rerank_score

    rerank_is_correct = (
        rerank_policy_id == expected_policy
    )

    # ------------------------------------------
    # COUNTERS
    # ------------------------------------------

    if embedding_is_correct:
        embedding_correct += 1

    if rerank_is_correct:
        reranker_correct += 1

    if expected_policy is not None:

        answerable_cases += 1

        if embedding_is_correct:
            embedding_answerable_correct += 1

        if rerank_is_correct:
            reranker_answerable_correct += 1

    # ------------------------------------------
    # PRINT ONLY INTERESTING CASES
    # ------------------------------------------

    if embedding_policy_id != rerank_policy_id:

        print("=" * 70)
        print("QUESTION:", question)
        print("CATEGORY:", category)
        print("EXPECTED:", expected_policy)

        print(
            "EMBEDDING TOP-1:",
            embedding_policy_id,
            "| score:",
            round(embedding_score, 3),
            "| correct:",
            embedding_is_correct
        )

        print(
            "RERANK TOP-1:",
            rerank_policy_id,
            "| score:",
            round(rerank_score, 3),
            "| correct:",
            rerank_is_correct
        )

        print(
            "RERANK MARGIN:",
            round(rerank_margin, 3)
        )

        print()

embedding_accuracy = embedding_correct / total_cases
reranker_accuracy = reranker_correct / total_cases

embedding_answerable_accuracy = (
    embedding_answerable_correct / answerable_cases
)

reranker_answerable_accuracy = (
    reranker_answerable_correct / answerable_cases
)


print("\n===== SUMMARY =====")

print("Total Cases:", total_cases)
print("Cases With Expected Policy:", answerable_cases)

print("\n--- ALL CASES ---")

print(
    "Embedding Retrieval Accuracy:",
    embedding_accuracy
)

print(
    "Reranked Retrieval Accuracy:",
    reranker_accuracy
)

print("\n--- EXPECTED POLICY NOT NONE ---")

print(
    "Embedding Retrieval Accuracy:",
    embedding_answerable_accuracy
)

print(
    "Reranked Retrieval Accuracy:",
    reranker_answerable_accuracy
)
