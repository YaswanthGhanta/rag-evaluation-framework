from sentence_transformers import CrossEncoder

from semantic_retriever import retrieve_top_k


reranker_model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L6-v2"
)


def rerank_policies(question, k=3):
    candidates = retrieve_top_k(question, k)

    pairs = []

    for candidate in candidates:
        policy = candidate["policy"]

        policy_text = (
            policy["topic"]
            + ". "
            + policy["content"]
        )

        pairs.append(
            [question, policy_text]
        )

    rerank_scores = reranker_model.predict(pairs)

    reranked_results = []

    for i in range(len(candidates)):
        reranked_results.append({
            "policy": candidates[i]["policy"],
            "embedding_score": candidates[i]["score"],
            "rerank_score": float(rerank_scores[i])
        })

    reranked_results.sort(
        key=lambda item: item["rerank_score"],
        reverse=True
    )

    return reranked_results
