from context_judge import judge_context_sufficiency


remote_context = (
    "Remote Work. Employees may work remotely up to 2 days per week "
    "with prior approval from their manager. Remote work is not permitted "
    "during an employee's probation period."
)

expense_context = (
    "Expense Reimbursement. Employees must submit business expense "
    "claims within 30 days of the expense. Claims require receipts "
    "and manager approval."
)

parental_context = (
    "Parental Leave. Eligible employees are entitled to 12 weeks "
    "of paid parental leave following birth or adoption."
)


test_cases = [
    {
        "name": "conditional_answer",
        "question": "Am I allowed to work remotely?",
        "context": remote_context,
        "expected": "SUFFICIENT"
    },

    {
        "name": "material_condition",
        "question": (
            "If I have unused annual leave, can I work remotely "
            "two days per week with manager approval?"
        ),
        "context": remote_context,
        "expected": "INSUFFICIENT"
    },

    {
        "name": "incidental_background",
        "question": (
            "I currently work remotely. How many weeks of paid "
            "parental leave are eligible employees entitled to?"
        ),
        "context": parental_context,
        "expected": "SUFFICIENT"
    },

    {
        "name": "unstated_exclusion",
        "question": (
            "Can the company reimburse my personal vacation expenses?"
        ),
        "context": expense_context,
        "expected": "INSUFFICIENT"
    }
]


runs_per_case = 5


print("\n===== SUFFICIENCY RUBRIC TEST =====\n")


total_correct = 0
total_runs = 0


for case in test_cases:

    print("=" * 70)
    print("TYPE:", case["name"])
    print("QUESTION:", case["question"])
    print("EXPECTED:", case["expected"])
    print()

    correct_count = 0
    sufficient_count = 0
    insufficient_count = 0

    for run_number in range(1, runs_per_case + 1):

        result = judge_context_sufficiency(
            case["question"],
            case["context"]
        )

        correct = result == case["expected"]

        if result == "SUFFICIENT":
            sufficient_count += 1

        elif result == "INSUFFICIENT":
            insufficient_count += 1

        if correct:
            correct_count += 1

        total_correct += int(correct)
        total_runs += 1

        print(
            f"Run {run_number}: {result} | "
            f"Correct: {correct}"
        )

    print("\nCASE SUMMARY")
    print("SUFFICIENT:", sufficient_count)
    print("INSUFFICIENT:", insufficient_count)
    print("Accuracy:", correct_count / runs_per_case)

    print(
        "Stability:",
        max(sufficient_count, insufficient_count)
        / runs_per_case
    )

    print()


print("=" * 70)
print("OVERALL")
print("Total Judgments:", total_runs)
print("Correct Judgments:", total_correct)
print("Overall Accuracy:", total_correct / total_runs)
