from context_judge import judge_context_sufficiency


question = (
    "If I have unused annual leave, can I work remotely "
    "two days per week with manager approval?"
)

context = (
    "Remote Work. Employees may work remotely up to 2 days per week "
    "with prior approval from their manager. Remote work is not permitted "
    "during an employee's probation period."
)

expected = "INSUFFICIENT"

runs = 10

sufficient_count = 0
insufficient_count = 0
correct_count = 0


print("\n===== MATERIAL CONDITION STABILITY TEST =====\n")

print("QUESTION:")
print(question)

print("\nCONTEXT:")
print(context)

print("\nEXPECTED:")
print(expected)

print("\n" + "=" * 70)


for run_number in range(1, runs + 1):

    result = judge_context_sufficiency(
        question,
        context
    )

    if result == "SUFFICIENT":
        sufficient_count += 1

    elif result == "INSUFFICIENT":
        insufficient_count += 1

    if result == expected:
        correct_count += 1

    print(
        f"Run {run_number}: {result} | "
        f"Correct: {result == expected}"
    )


print("\n===== SUMMARY =====")

print("Total Runs:", runs)
print("SUFFICIENT:", sufficient_count)
print("INSUFFICIENT:", insufficient_count)

print(
    "SUFFICIENT Rate:",
    sufficient_count / runs
)

print(
    "INSUFFICIENT Rate:",
    insufficient_count / runs
)

print(
    "Accuracy:",
    correct_count / runs
)

print(
    "Stability Rate:",
    max(sufficient_count, insufficient_count) / runs
)
