from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from policy_data import policies


model = SentenceTransformer("all-MiniLM-L6-v2")


policy_texts = []

for policy in policies:
    text = policy["topic"] + ". " + policy["content"]
    policy_texts.append(text)


policy_embeddings = model.encode(policy_texts)


def retrieve_policy_semantic(
    question,
    min_score=0.30,
    min_margin=0.08
):
    question_embedding = model.encode([question])

    similarities = cosine_similarity(
        question_embedding,
        policy_embeddings
    )[0]

    ranked_indexes = similarities.argsort()[::-1]

    best_index = ranked_indexes[0]
    second_index = ranked_indexes[1]

    best_score = float(similarities[best_index])
    second_score = float(similarities[second_index])

    margin = best_score - second_score

    if best_score < min_score:
        return None, best_score

    if margin < min_margin:
        return None, best_score

    return policies[best_index], best_score


"""def retrieve_policy_semantic(question):

    question_embedding = model.encode([question])

    similarities = cosine_similarity(
        question_embedding,
        policy_embeddings
    )[0]

    best_index = similarities.argmax()

    best_policy = policies[best_index]
    best_score = similarities[best_index]

    return best_policy, best_score"""


def retrieve_top_k(question, k=3):
    question_embedding = model.encode([question])

    similarities = cosine_similarity(
        question_embedding,
        policy_embeddings
    )[0]

    ranked_indexes = similarities.argsort()[::-1]

    results = []

    for index in ranked_indexes[:k]:
        results.append({
            "policy": policies[index],
            "score": float(similarities[index])
        })

    return results
