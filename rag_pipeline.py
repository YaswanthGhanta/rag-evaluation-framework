from reranker import rerank_policies
from context_judge import judge_context_sufficiency
from generator import generate_answer
from strict_generator import generate_strict_answer
from groundedness_judge import judge_groundedness


def run_rag_pipeline(question):

    # STEP 1: Retrieve and rerank policies
    reranked_results = rerank_policies(question, k=3)

    best_result = reranked_results[0]
    best_policy = best_result["policy"]

    retrieved_policy = best_policy["id"]

    context = (
        best_policy["topic"]
        + ". "
        + best_policy["content"]
    )

    # STEP 2: Check context sufficiency
    sufficiency = judge_context_sufficiency(
        question,
        context
    )

    # STEP 3: If context is insufficient, reject the policy
    if sufficiency == "INSUFFICIENT":
        return {
            "question": question,
            "retrieved_policy": retrieved_policy,
            "accepted_policy": None,
            "context": context,
            "sufficiency": sufficiency,
            "generated_answer": None,
            "groundedness": None,
            "retry_answer": None,
            "retry_groundedness": None,
            "final_answer": (
                "I don't have enough policy information "
                "to answer this question reliably."
            )
        }

    # Policy is accepted because context is sufficient
    accepted_policy = retrieved_policy

    # STEP 4: Generate first answer
    generated_answer = generate_answer(
        question,
        context
    )

    # STEP 5: Evaluate groundedness
    groundedness = judge_groundedness(
        question,
        context,
        generated_answer
    )

    # STEP 6: If first answer passes, return it
    if groundedness == "PASS":
        return {
            "question": question,
            "retrieved_policy": retrieved_policy,
            "accepted_policy": accepted_policy,
            "context": context,
            "sufficiency": sufficiency,
            "generated_answer": generated_answer,
            "groundedness": groundedness,
            "retry_answer": None,
            "retry_groundedness": None,
            "final_answer": generated_answer
        }

    # STEP 7: Retry with stricter generator
    retry_answer = generate_strict_answer(
        question,
        context
    )

    # STEP 8: Evaluate retry groundedness
    retry_groundedness = judge_groundedness(
        question,
        context,
        retry_answer
    )

    # STEP 9: Final guardrail decision
    if retry_groundedness == "PASS":
        final_answer = retry_answer
    else:
        final_answer = (
            "I can't provide a reliable answer from "
            "the available policy information."
        )

    return {
        "question": question,
        "retrieved_policy": retrieved_policy,
        "accepted_policy": accepted_policy,
        "context": context,
        "sufficiency": sufficiency,
        "generated_answer": generated_answer,
        "groundedness": groundedness,
        "retry_answer": retry_answer,
        "retry_groundedness": retry_groundedness,
        "final_answer": final_answer
    }


"""from reranker import rerank_policies
from context_judge import judge_context_sufficiency
from generator import generate_answer
from groundedness_judge import judge_groundedness


def run_rag_pipeline(question):

    # STEP 1: Retrieve and rerank policies
    reranked_results = rerank_policies(question, k=3)

    best_result = reranked_results[0]
    best_policy = best_result["policy"]

    context = (
        best_policy["topic"]
        + ". "
        + best_policy["content"]
    )

    # STEP 2: Check whether context is sufficient
    sufficiency = judge_context_sufficiency(
        question,
        context
    )

    if sufficiency == "INSUFFICIENT":
        return {
            "question": question,
            "policy": None,
            "context": context,
            "sufficiency": sufficiency,
            "generated_answer": None,
            "groundedness": None,
            "final_answer": "I don't have enough policy information to answer this question reliably."
        }

    # STEP 3: Generate answer
    generated_answer = generate_answer(
        question,
        context
    )

    # STEP 4: Evaluate groundedness
    groundedness = judge_groundedness(
        question,
        context,
        generated_answer
    )

    # STEP 5: Guardrail
    if groundedness == "FAIL":
        final_answer = (
            "I can't provide a reliable answer from the available "
            "policy information."
        )
    else:
        final_answer = generated_answer

    # STEP 6: Return evaluation trace
    return {
        "question": question,
        "policy": best_policy["id"],
        "context": context,
        "sufficiency": sufficiency,
        "generated_answer": generated_answer,
        "groundedness": groundedness,
        "final_answer": final_answer
    }"""


"""from reranker import rerank_policies
from context_judge import judge_context_sufficiency
from generator import generate_answer
from groundedness_judge import judge_groundedness


def run_rag_pipeline(question):

    reranked_results = rerank_policies(question, k=3)

    best_result = reranked_results[0]

    best_policy = best_result["policy"]

    context = (
        best_policy["topic"]
        + ". "
        + best_policy["content"]
    )

    sufficiency = judge_context_sufficiency(
        question,
        context
    )

    if sufficiency == "INSUFFICIENT":
        return {
            "question": question,
            "policy": None,
            "context": context,
            "sufficiency": sufficiency,
            "answer": None,
            "groundedness": None
        }

    answer = generate_answer(
        question,
        context
    )

    groundedness = judge_groundedness(
        question,
        context,
        answer
    )

    return {
        "question": question,
        "policy": best_policy["id"],
        "context": context,
        "sufficiency": sufficiency,
        "answer": answer,
        "groundedness": groundedness
    }"""
