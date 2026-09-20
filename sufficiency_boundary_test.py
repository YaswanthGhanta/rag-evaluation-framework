from context_judge import judge_context_sufficiency


test_cases = [
    {
        "name": "conditional_policy_answer",
        "question": "Am I allowed to work remotely?",
        "context": (
            "Remote Work. Employees may work remotely up to 2 days per week "
            "with prior approval from their manager. Remote work is not permitted "
            "during an employee's probation period."
        ),
        "expected": "SUFFICIENT"
    },
    {
        "name": "unstated_exclusion",
        "question": "Can the company reimburse my personal vacation expenses?",
        "context": (
            "Expense Reimbursement. Employees must submit business expense "
            "claims within 30 days of the expense. Claims require receipts "
            "and manager approval."
        ),
        "expected": "INSUFFICIENT"
    }
]


runs = 5


print("\n===== SUFFICIENCY BOUNDARY TEST =====\n")


for case in test_cases:

    print("=" * 70)
    print("TYPE:", case["name"])
    print("QUESTION:", case["question"])
    print("EXPECTED:", case["expected"])
    print()

    correct_count = 0

    for run_number in range(1, runs + 1):

        result = judge_context_sufficiency(
            case["question"],
            case["context"]
        )

        correct = result == case["expected"]

        if correct:
            correct_count += 1

        print(
            f"Run {run_number}: {result} | "
            f"Correct: {correct}"
        )

    print(
        "\nAccuracy:",
        correct_count / runs
    )

    print()
