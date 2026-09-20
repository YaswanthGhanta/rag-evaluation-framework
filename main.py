from rag_pipeline import run_rag_pipeline


questions = [
    "Do I need a medical certificate after three days of sick leave?",
    "Can I carry forward sick leave into next year?",
    "What happens to my leftover holidays at the end of the year?"
]


for question in questions:

    result = run_rag_pipeline(question)

    print()
    print("QUESTION:", result["question"])
    print("POLICY:", result["policy"])
    print("SUFFICIENCY:", result["sufficiency"])

    print()
    print("FIRST GENERATED ANSWER:")
    print(result["generated_answer"])

    print("FIRST GROUNDEDNESS:")
    print(result["groundedness"])

    print()
    print("RETRY ANSWER:")
    print(result["retry_answer"])

    print("RETRY GROUNDEDNESS:")
    print(result["retry_groundedness"])

    print()
    print("FINAL USER ANSWER:")
    print(result["final_answer"])

    print("------------------------------")


"""from rag_pipeline import run_rag_pipeline


questions = [
    "Do I need a medical certificate after three days of sick leave?",
    "Can I carry forward sick leave into next year?",
    "What happens to my leftover holidays at the end of the year?"
]


for question in questions:

    result = run_rag_pipeline(question)

    print()
    print("QUESTION:", result["question"])
    print("POLICY:", result["policy"])
    print("SUFFICIENCY:", result["sufficiency"])
    print("ANSWER:", result["answer"])
    print("GROUNDEDNESS:", result["groundedness"])
    print("------------------------------")"""

"""from rag_pipeline import run_rag_pipeline


questions = [
    "Do I need a medical certificate after three days of sick leave?",
    "Can I carry forward sick leave into next year?",
    "What happens to my leftover holidays at the end of the year?"
]


for question in questions:

    result = run_rag_pipeline(question)

    print()
    print("QUESTION:", result["question"])
    print("POLICY:", result["policy"])
    print("SUFFICIENCY:", result["sufficiency"])
    print("ANSWER STATUS:", result["answer"])
    print("------------------------------")"""


"""from reranker import rerank_policies


questions = [
    "What happens to my leftover holidays at the end of the year?",
    "Can I work from another country while on vacation?",
    "How many public holidays are there this year?",
    "Can I carry forward sick leave into next year?"
]


for question in questions:

    print()
    print("QUESTION:", question)

    results = rerank_policies(question)

    for rank, result in enumerate(results, start=1):

        policy = result["policy"]

        print(
            rank,
            policy["id"],
            "-",
            policy["topic"],
            "- embedding:",
            round(result["embedding_score"], 3),
            "- rerank:",
            round(result["rerank_score"], 3)
        )

    print("------------------------------")"""

"""from semantic_retriever import retrieve_policy_semantic
from unseen_test_data import unseen_test_cases


passed = 0
failed = 0

false_negatives = 0
false_positives = 0
wrong_retrievals = 0


for test in unseen_test_cases:

    question = test["question"]
    expected = test["expected_policy"]

    policy, score = retrieve_policy_semantic(question)

    if policy is None:
        actual = None
    else:
        actual = policy["id"]

    if actual == expected:
        passed += 1

    else:
        failed += 1

        if expected is not None and actual is None:
            failure_type = "False Negative"
            false_negatives += 1

        elif expected is None and actual is not None:
            failure_type = "False Positive"
            false_positives += 1

        else:
            failure_type = "Wrong Retrieval"
            wrong_retrievals += 1

        print()
        print("FAILURE")
        print("Question:", question)
        print("Expected:", expected)
        print("Actual:", actual)
        print("Top score:", round(float(score), 3))
        print("Failure type:", failure_type)


total = len(unseen_test_cases)
accuracy = passed / total


print()
print("===== UNSEEN EVALUATION =====")
print("Total tests:", total)
print("Passed:", passed)
print("Failed:", failed)
print("Accuracy:", round(accuracy, 3))
print("False negatives:", false_negatives)
print("False positives:", false_positives)
print("Wrong retrievals:", wrong_retrievals)"""


"""from semantic_retriever import retrieve_policy_semantic
from test_data import test_cases


passed = 0
failed = 0

false_negatives = 0
false_positives = 0
wrong_retrievals = 0


for test in test_cases:

    question = test["question"]
    expected = test["expected_policy"]

    policy, score = retrieve_policy_semantic(question)

    if policy is None:
        actual = None
    else:
        actual = policy["id"]

    if actual == expected:
        status = "PASS"
        passed += 1

    else:
        status = "FAIL"
        failed += 1

        if expected is not None and actual is None:
            failure_type = "False Negative"
            false_negatives += 1

        elif expected is None and actual is not None:
            failure_type = "False Positive"
            false_positives += 1

        else:
            failure_type = "Wrong Retrieval"
            wrong_retrievals += 1

        print()
        print("FAILURE")
        print("Question:", question)
        print("Expected:", expected)
        print("Actual:", actual)
        print("Top score:", round(float(score), 3))
        print("Failure type:", failure_type)


total = len(test_cases)
accuracy = passed / total


print()
print("===== SEMANTIC RETRIEVER WITH THRESHOLDS =====")
print("Total tests:", total)
print("Passed:", passed)
print("Failed:", failed)
print("Accuracy:", round(accuracy, 3))
print("False negatives:", false_negatives)
print("False positives:", false_positives)
print("Wrong retrievals:", wrong_retrievals)"""


"""from semantic_retriever import retrieve_policy_semantic
from test_data import test_cases


passed = 0
failed = 0

false_negatives = 0
false_positives = 0
wrong_retrievals = 0


for test in test_cases:

    question = test["question"]
    expected = test["expected_policy"]

    policy, score = retrieve_policy_semantic(question)

    actual = policy["id"]

    if actual == expected:
        status = "PASS"
        passed += 1

    else:
        status = "FAIL"
        failed += 1

        if expected is not None and actual is None:
            failure_type = "False Negative"
            false_negatives += 1

        elif expected is None and actual is not None:
            failure_type = "False Positive"
            false_positives += 1

        else:
            failure_type = "Wrong Retrieval"
            wrong_retrievals += 1

        print()
        print("FAILURE")
        print("Question:", question)
        print("Expected:", expected)
        print("Actual:", actual)
        print("Similarity:", round(float(score), 3))
        print("Failure type:", failure_type)


total = len(test_cases)
accuracy = passed / total


print()
print("===== SEMANTIC RETRIEVER =====")
print("Total tests:", total)
print("Passed:", passed)
print("Failed:", failed)
print("Accuracy:", round(accuracy, 3))
print("False negatives:", false_negatives)
print("False positives:", false_positives)
print("Wrong retrievals:", wrong_retrievals)"""


"""from semantic_retriever import retrieve_policy_semantic

question = "What happens to my leftover holidays at the end of the year?"

policy, score = retrieve_policy_semantic(question)

print("Question:", question)
print("Retrieved policy:", policy["id"])
print("Topic:", policy["topic"])
print("Similarity score:", score)"""


"""from retriever import retrieve_policy
from test_data import test_cases


passed = 0
failed = 0

for test in test_cases:

    question = test["question"]
    expected = test["expected_policy"]

    result = retrieve_policy(question)

    if result is None:
        actual = None
    else:
        actual = result["id"]

    if actual == expected:
        status = "PASS"
        passed = passed + 1
    else:
        status = "FAIL"
        failed = failed + 1

    print("Question:", question)
    print("Expected:", expected)
    print("Actual:", actual)
    print("Status:", status)
    print("------------------------------")


total = len(test_cases)

accuracy = passed / total

print("Total tests:", total)
print("Passed:", passed)
print("Failed:", failed)
print("Accuracy:", accuracy)"""


"""from retriever import retrieve_policy
from test_data import test_cases


passed = 0
failed = 0

false_negatives = 0
false_positives = 0
wrong_retrievals = 0

for test in test_cases:

    question = test["question"]
    expected = test["expected_policy"]

    result = retrieve_policy(question)

    if result is None:
        actual = None
    else:
        actual = result["id"]

    if actual == expected:
        status = "PASS"
        passed += 1

    else:
        status = "FAIL"
        failed += 1

        if expected is not None and actual is None:
            failure_type = "False Negative"
            false_negatives += 1

        elif expected is None and actual is not None:
            failure_type = "False Positive"
            false_positives += 1

        else:
            failure_type = "Wrong Retrieval"
            wrong_retrievals += 1

        print("FAILURE")
        print("Question:", question)
        print("Expected:", expected)
        print("Actual:", actual)
        print("Failure type:", failure_type)
        print("------------------------------")


total = len(test_cases)
accuracy = passed / total

print()
print("===== EVALUATION SUMMARY =====")
print("Total tests:", total)
print("Passed:", passed)
print("Failed:", failed)
print("Accuracy:", accuracy)

print("False negatives:", false_negatives)
print("False positives:", false_positives)
print("Wrong retrievals:", wrong_retrievals)"""
