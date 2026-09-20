from evaluation_data import evaluation_cases
from rag_pipeline import run_rag_pipeline


total_cases = len(evaluation_cases)

retrieval_correct = 0
sufficiency_correct = 0

generated_answers = 0
first_pass_grounded = 0

retry_used = 0
retry_recovered = 0


# -----------------------------------
# SUFFICIENCY CONFUSION MATRIX
# -----------------------------------

true_positive = 0
false_positive = 0
true_negative = 0
false_negative = 0


# -----------------------------------
# STORE ALL EVALUATION RESULTS
# -----------------------------------

evaluation_results = []


# -----------------------------------
# CATEGORY / SLICE METRICS
# -----------------------------------

category_stats = {}


for case in evaluation_cases:

    question = case["question"]
    expected_policy = case["expected_policy"]
    expected_sufficiency = case["expected_sufficiency"]
    category = case["category"]

    result = run_rag_pipeline(question)

    retrieved_policy = result["retrieved_policy"]
    accepted_policy = result["accepted_policy"]

    actual_sufficiency = result["sufficiency"]

    generated_answer = result["generated_answer"]
    first_groundedness = result["groundedness"]

    retry_answer = result["retry_answer"]
    retry_groundedness = result["retry_groundedness"]

    final_answer = result["final_answer"]

    # -----------------------------------
    # RETRIEVAL ACCURACY
    # -----------------------------------

    retrieval_pass = (
        retrieved_policy == expected_policy
    )

    if retrieval_pass:
        retrieval_correct += 1

    # -----------------------------------
    # SUFFICIENCY ACCURACY
    # -----------------------------------

    sufficiency_pass = (
        actual_sufficiency == expected_sufficiency
    )

    if sufficiency_pass:
        sufficiency_correct += 1

    # -----------------------------------
    # SUFFICIENCY CONFUSION MATRIX
    # -----------------------------------

    if (
        expected_sufficiency == "INSUFFICIENT"
        and actual_sufficiency == "INSUFFICIENT"
    ):
        true_positive += 1
        sufficiency_classification = "TP"

    elif (
        expected_sufficiency == "SUFFICIENT"
        and actual_sufficiency == "INSUFFICIENT"
    ):
        false_positive += 1
        sufficiency_classification = "FP"

    elif (
        expected_sufficiency == "SUFFICIENT"
        and actual_sufficiency == "SUFFICIENT"
    ):
        true_negative += 1
        sufficiency_classification = "TN"

    elif (
        expected_sufficiency == "INSUFFICIENT"
        and actual_sufficiency == "SUFFICIENT"
    ):
        false_negative += 1
        sufficiency_classification = "FN"

    # -----------------------------------
    # FIRST-PASS GROUNDEDNESS
    # -----------------------------------

    if generated_answer is not None:
        generated_answers += 1

        if first_groundedness == "PASS":
            first_pass_grounded += 1

    # -----------------------------------
    # RETRY METRICS
    # -----------------------------------

    if retry_answer is not None:
        retry_used += 1

        if retry_groundedness == "PASS":
            retry_recovered += 1

    # -----------------------------------
    # CATEGORY / SLICE METRICS
    # -----------------------------------

    if category not in category_stats:

        category_stats[category] = {
            "total": 0,
            "retrieval_correct": 0,
            "sufficiency_correct": 0
        }

    category_stats[category]["total"] += 1

    if retrieval_pass:
        category_stats[category]["retrieval_correct"] += 1

    if sufficiency_pass:
        category_stats[category]["sufficiency_correct"] += 1

    # -----------------------------------
    # STORE THIS TEST RESULT
    # -----------------------------------

    test_result = {
        "question": question,
        "category": category,

        "expected_policy": expected_policy,
        "retrieved_policy": retrieved_policy,
        "accepted_policy": accepted_policy,
        "retrieval_pass": retrieval_pass,

        "expected_sufficiency": expected_sufficiency,
        "actual_sufficiency": actual_sufficiency,
        "sufficiency_pass": sufficiency_pass,
        "sufficiency_classification": sufficiency_classification,

        "first_groundedness": first_groundedness,

        "retry_used": retry_answer is not None,
        "retry_groundedness": retry_groundedness,

        "final_answer": final_answer
    }

    evaluation_results.append(test_result)


# -----------------------------------
# CALCULATE OVERALL METRICS
# -----------------------------------

retrieval_accuracy = (
    retrieval_correct / total_cases
)

sufficiency_accuracy = (
    sufficiency_correct / total_cases
)


if generated_answers > 0:

    first_pass_groundedness_rate = (
        first_pass_grounded / generated_answers
    )

    retry_usage_rate = (
        retry_used / generated_answers
    )

else:

    first_pass_groundedness_rate = 0
    retry_usage_rate = 0


if retry_used > 0:

    retry_recovery_rate = (
        retry_recovered / retry_used
    )

else:

    retry_recovery_rate = 0


# -----------------------------------
# PRECISION
# -----------------------------------

if true_positive + false_positive > 0:

    insufficient_precision = (
        true_positive
        / (true_positive + false_positive)
    )

else:

    insufficient_precision = 0


# -----------------------------------
# RECALL
# -----------------------------------

if true_positive + false_negative > 0:

    insufficient_recall = (
        true_positive
        / (true_positive + false_negative)
    )

else:

    insufficient_recall = 0


# -----------------------------------
# PRINT INDIVIDUAL RESULTS
# -----------------------------------

print()
print("===== INDIVIDUAL RESULTS =====")


for result in evaluation_results:

    print()
    print("QUESTION:", result["question"])
    print("CATEGORY:", result["category"])

    print(
        "RETRIEVAL:",
        result["retrieval_pass"]
    )

    if not result["retrieval_pass"]:

        print(
            "EXPECTED POLICY:",
            result["expected_policy"]
        )

        print(
            "RETRIEVED POLICY:",
            result["retrieved_policy"]
        )

    print(
        "SUFFICIENCY:",
        result["sufficiency_pass"]
    )

    print(
        "CLASSIFICATION:",
        result["sufficiency_classification"]
    )

    print(
        "FIRST GROUNDEDNESS:",
        result["first_groundedness"]
    )

    print(
        "RETRY USED:",
        result["retry_used"]
    )

    print("------------------------------")


# -----------------------------------
# PRINT OVERALL SUMMARY
# -----------------------------------

print()
print("===== EVALUATION SUMMARY =====")

print("Total Cases:", total_cases)

print()
print("Retrieval Accuracy:", retrieval_accuracy)
print("Sufficiency Accuracy:", sufficiency_accuracy)

print()
print(
    "First-Pass Groundedness Rate:",
    first_pass_groundedness_rate
)

print(
    "Retry Usage Rate:",
    retry_usage_rate
)

print(
    "Retry Recovery Rate:",
    retry_recovery_rate
)


# -----------------------------------
# PRINT CONFUSION MATRIX
# -----------------------------------

print()
print("===== SUFFICIENCY CONFUSION MATRIX =====")

print("True Positive:", true_positive)
print("False Positive:", false_positive)
print("True Negative:", true_negative)
print("False Negative:", false_negative)

print()
print(
    "Insufficient-Context Precision:",
    insufficient_precision
)

print(
    "Insufficient-Context Recall:",
    insufficient_recall
)


# -----------------------------------
# PRINT CATEGORY / SLICE RESULTS
# -----------------------------------

print()
print("===== CATEGORY / SLICE ANALYSIS =====")


for category, stats in category_stats.items():

    category_total = stats["total"]

    category_retrieval_accuracy = (
        stats["retrieval_correct"]
        / category_total
    )

    category_sufficiency_accuracy = (
        stats["sufficiency_correct"]
        / category_total
    )

    print()
    print("CATEGORY:", category)

    print(
        "Cases:",
        category_total
    )

    print(
        "Retrieval Accuracy:",
        category_retrieval_accuracy
    )

    print(
        "Sufficiency Accuracy:",
        category_sufficiency_accuracy
    )

    print("------------------------------")


"""from evaluation_data import evaluation_cases
from rag_pipeline import run_rag_pipeline


total_cases = len(evaluation_cases)

retrieval_correct = 0
sufficiency_correct = 0

generated_answers = 0
first_pass_grounded = 0

retry_used = 0
retry_recovered = 0


# -----------------------------------
# SUFFICIENCY CONFUSION MATRIX
# -----------------------------------

true_positive = 0
false_positive = 0
true_negative = 0
false_negative = 0


# -----------------------------------
# STORE ALL EVALUATION RESULTS
# -----------------------------------

evaluation_results = []


for case in evaluation_cases:

    question = case["question"]
    expected_policy = case["expected_policy"]
    expected_sufficiency = case["expected_sufficiency"]
    category = case["category"]

    result = run_rag_pipeline(question)

    retrieved_policy = result["retrieved_policy"]
    accepted_policy = result["accepted_policy"]

    actual_sufficiency = result["sufficiency"]

    generated_answer = result["generated_answer"]
    first_groundedness = result["groundedness"]

    retry_answer = result["retry_answer"]
    retry_groundedness = result["retry_groundedness"]

    final_answer = result["final_answer"]

    # -----------------------------------
    # RETRIEVAL ACCURACY
    # -----------------------------------

    retrieval_pass = (
        retrieved_policy == expected_policy
    )

    if retrieval_pass:
        retrieval_correct += 1

    # -----------------------------------
    # SUFFICIENCY ACCURACY
    # -----------------------------------

    sufficiency_pass = (
        actual_sufficiency == expected_sufficiency
    )

    if sufficiency_pass:
        sufficiency_correct += 1

    # -----------------------------------
    # SUFFICIENCY CONFUSION MATRIX
    # -----------------------------------

    if (
        expected_sufficiency == "INSUFFICIENT"
        and actual_sufficiency == "INSUFFICIENT"
    ):
        true_positive += 1
        sufficiency_classification = "TP"

    elif (
        expected_sufficiency == "SUFFICIENT"
        and actual_sufficiency == "INSUFFICIENT"
    ):
        false_positive += 1
        sufficiency_classification = "FP"

    elif (
        expected_sufficiency == "SUFFICIENT"
        and actual_sufficiency == "SUFFICIENT"
    ):
        true_negative += 1
        sufficiency_classification = "TN"

    elif (
        expected_sufficiency == "INSUFFICIENT"
        and actual_sufficiency == "SUFFICIENT"
    ):
        false_negative += 1
        sufficiency_classification = "FN"

    # -----------------------------------
    # FIRST-PASS GROUNDEDNESS
    # -----------------------------------

    if generated_answer is not None:
        generated_answers += 1

        if first_groundedness == "PASS":
            first_pass_grounded += 1

    # -----------------------------------
    # RETRY METRICS
    # -----------------------------------

    if retry_answer is not None:
        retry_used += 1

        if retry_groundedness == "PASS":
            retry_recovered += 1

    # -----------------------------------
    # STORE THIS TEST RESULT
    # -----------------------------------

    test_result = {
        "question": question,
        "category": category,

        "expected_policy": expected_policy,
        "retrieved_policy": retrieved_policy,
        "accepted_policy": accepted_policy,
        "retrieval_pass": retrieval_pass,

        "expected_sufficiency": expected_sufficiency,
        "actual_sufficiency": actual_sufficiency,
        "sufficiency_pass": sufficiency_pass,
        "sufficiency_classification": sufficiency_classification,

        "first_groundedness": first_groundedness,

        "retry_used": retry_answer is not None,
        "retry_groundedness": retry_groundedness,

        "final_answer": final_answer
    }

    evaluation_results.append(test_result)


# -----------------------------------
# CALCULATE METRICS
# -----------------------------------

retrieval_accuracy = (
    retrieval_correct / total_cases
)

sufficiency_accuracy = (
    sufficiency_correct / total_cases
)


if generated_answers > 0:

    first_pass_groundedness_rate = (
        first_pass_grounded / generated_answers
    )

    retry_usage_rate = (
        retry_used / generated_answers
    )

else:

    first_pass_groundedness_rate = 0
    retry_usage_rate = 0


if retry_used > 0:

    retry_recovery_rate = (
        retry_recovered / retry_used
    )

else:

    retry_recovery_rate = 0


if true_positive + false_positive > 0:

    insufficient_precision = (
        true_positive
        / (true_positive + false_positive)
    )

else:

    insufficient_precision = 0


if true_positive + false_negative > 0:

    insufficient_recall = (
        true_positive
        / (true_positive + false_negative)
    )

else:

    insufficient_recall = 0


# -----------------------------------
# PRINT INDIVIDUAL RESULTS
# -----------------------------------

print()
print("===== INDIVIDUAL RESULTS =====")


for result in evaluation_results:

    print()
    print("QUESTION:", result["question"])
    print("CATEGORY:", result["category"])

    print(
        "RETRIEVAL:",
        result["retrieval_pass"]
    )

    print(
        "SUFFICIENCY:",
        result["sufficiency_pass"]
    )

    print(
        "CLASSIFICATION:",
        result["sufficiency_classification"]
    )

    print(
        "FIRST GROUNDEDNESS:",
        result["first_groundedness"]
    )

    print(
        "RETRY USED:",
        result["retry_used"]
    )

    print("------------------------------")


# -----------------------------------
# PRINT SUMMARY
# -----------------------------------

print()
print("===== EVALUATION SUMMARY =====")

print("Total Cases:", total_cases)

print()
print("Retrieval Accuracy:", retrieval_accuracy)
print("Sufficiency Accuracy:", sufficiency_accuracy)

print()
print(
    "First-Pass Groundedness Rate:",
    first_pass_groundedness_rate
)

print(
    "Retry Usage Rate:",
    retry_usage_rate
)

print(
    "Retry Recovery Rate:",
    retry_recovery_rate
)


print()
print("===== SUFFICIENCY CONFUSION MATRIX =====")

print("True Positive:", true_positive)
print("False Positive:", false_positive)
print("True Negative:", true_negative)
print("False Negative:", false_negative)

print()
print(
    "Insufficient-Context Precision:",
    insufficient_precision
)

print(
    "Insufficient-Context Recall:",
    insufficient_recall
)"""


"""from evaluation_data import evaluation_cases
from rag_pipeline import run_rag_pipeline


total_cases = len(evaluation_cases)

retrieval_correct = 0
sufficiency_correct = 0

generated_answers = 0
first_pass_grounded = 0

retry_used = 0
retry_recovered = 0


# -----------------------------------
# SUFFICIENCY CONFUSION MATRIX
# -----------------------------------

true_positive = 0
false_positive = 0
true_negative = 0
false_negative = 0


for case in evaluation_cases:

    question = case["question"]
    expected_policy = case["expected_policy"]
    expected_sufficiency = case["expected_sufficiency"]

    result = run_rag_pipeline(question)

    retrieved_policy = result["retrieved_policy"]
    accepted_policy = result["accepted_policy"]

    actual_sufficiency = result["sufficiency"]

    generated_answer = result["generated_answer"]
    first_groundedness = result["groundedness"]

    retry_answer = result["retry_answer"]
    retry_groundedness = result["retry_groundedness"]

    final_answer = result["final_answer"]

    # -----------------------------------
    # RETRIEVAL ACCURACY
    # -----------------------------------

    if retrieved_policy == expected_policy:
        retrieval_correct += 1

    # -----------------------------------
    # SUFFICIENCY ACCURACY
    # -----------------------------------

    if actual_sufficiency == expected_sufficiency:
        sufficiency_correct += 1

    # -----------------------------------
    # SUFFICIENCY CONFUSION MATRIX
    #
    # We treat INSUFFICIENT as POSITIVE.
    # -----------------------------------

    if (
        expected_sufficiency == "INSUFFICIENT"
        and actual_sufficiency == "INSUFFICIENT"
    ):
        true_positive += 1

    elif (
        expected_sufficiency == "SUFFICIENT"
        and actual_sufficiency == "INSUFFICIENT"
    ):
        false_positive += 1

    elif (
        expected_sufficiency == "SUFFICIENT"
        and actual_sufficiency == "SUFFICIENT"
    ):
        true_negative += 1

    elif (
        expected_sufficiency == "INSUFFICIENT"
        and actual_sufficiency == "SUFFICIENT"
    ):
        false_negative += 1

    # -----------------------------------
    # FIRST-PASS GROUNDEDNESS
    # -----------------------------------

    if generated_answer is not None:
        generated_answers += 1

        if first_groundedness == "PASS":
            first_pass_grounded += 1

    # -----------------------------------
    # RETRY METRICS
    # -----------------------------------

    if retry_answer is not None:
        retry_used += 1

        if retry_groundedness == "PASS":
            retry_recovered += 1

    # -----------------------------------
    # PRINT EACH TEST CASE
    # -----------------------------------

    print()
    print("QUESTION:", question)

    print("EXPECTED POLICY:", expected_policy)
    print("RETRIEVED POLICY:", retrieved_policy)
    print("ACCEPTED POLICY:", accepted_policy)

    print("EXPECTED SUFFICIENCY:", expected_sufficiency)
    print("ACTUAL SUFFICIENCY:", actual_sufficiency)

    print("FIRST GROUNDEDNESS:", first_groundedness)

    print("RETRY USED:", retry_answer is not None)
    print("RETRY GROUNDEDNESS:", retry_groundedness)

    print("FINAL ANSWER:", final_answer)

    print("------------------------------")


# -----------------------------------
# CALCULATE METRICS
# -----------------------------------

retrieval_accuracy = (
    retrieval_correct / total_cases
)

sufficiency_accuracy = (
    sufficiency_correct / total_cases
)


if generated_answers > 0:
    first_pass_groundedness_rate = (
        first_pass_grounded / generated_answers
    )

    retry_usage_rate = (
        retry_used / generated_answers
    )
else:
    first_pass_groundedness_rate = 0
    retry_usage_rate = 0


if retry_used > 0:
    retry_recovery_rate = (
        retry_recovered / retry_used
    )
else:
    retry_recovery_rate = 0


# -----------------------------------
# INSUFFICIENT-CONTEXT PRECISION
# -----------------------------------

if true_positive + false_positive > 0:

    insufficient_precision = (
        true_positive
        / (true_positive + false_positive)
    )

else:
    insufficient_precision = 0


# -----------------------------------
# INSUFFICIENT-CONTEXT RECALL
# -----------------------------------

if true_positive + false_negative > 0:

    insufficient_recall = (
        true_positive
        / (true_positive + false_negative)
    )

else:
    insufficient_recall = 0


# -----------------------------------
# PRINT SUMMARY
# -----------------------------------

print()
print("===== EVALUATION SUMMARY =====")

print("Total Cases:", total_cases)

print()
print("Retrieval Accuracy:", retrieval_accuracy)

print("Sufficiency Accuracy:", sufficiency_accuracy)

print()
print("First-Pass Groundedness Rate:", first_pass_groundedness_rate)

print("Retry Usage Rate:", retry_usage_rate)

print("Retry Recovery Rate:", retry_recovery_rate)


print()
print("===== SUFFICIENCY CONFUSION MATRIX =====")

print("True Positive:", true_positive)
print("False Positive:", false_positive)
print("True Negative:", true_negative)
print("False Negative:", false_negative)


print()
print("Insufficient-Context Precision:", insufficient_precision)

print("Insufficient-Context Recall:", insufficient_recall)"""
