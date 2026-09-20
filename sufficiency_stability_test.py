from context_judge import judge_context_sufficiency


question = "Am I allowed to work remotely?"


context_versions = {

    # A: Exact context used by the real RAG pipeline
    "A_exact_production": (
        "Remote Work. Employees may work remotely up to 2 days per week "
        "with prior approval from their manager. Remote work is not permitted "
        "during an employee's probation period."
    ),

    # B: Remove only the topic heading
    "B_no_heading": (
        "Employees may work remotely up to 2 days per week "
        "with prior approval from their manager. Remote work is not permitted "
        "during an employee's probation period."
    ),

    # C: Keep heading, but change approval wording
    "C_changed_approval_wording": (
        "Remote Work. Employees may work remotely up to 2 days per week "
        "with prior manager approval. Remote work is not permitted "
        "during an employee's probation period."
    ),

    # D: Remove heading AND change approval wording
    "D_no_heading_changed_wording": (
        "Employees may work remotely up to 2 days per week "
        "with prior manager approval. Remote work is not permitted "
        "during an employee's probation period."
    )
}


runs_per_version = 5


print("\n===== CONTEXT PERTURBATION TEST =====\n")


for version_name, context in context_versions.items():

    sufficient_count = 0
    insufficient_count = 0

    print("=" * 70)
    print("VERSION:", version_name)
    print("CONTEXT:", context)
    print()

    for run_number in range(1, runs_per_version + 1):

        result = judge_context_sufficiency(
            question,
            context
        )

        if result == "SUFFICIENT":
            sufficient_count += 1

        elif result == "INSUFFICIENT":
            insufficient_count += 1

        print(
            f"Run {run_number}: {result}"
        )

    sufficient_rate = (
        sufficient_count / runs_per_version
    )

    insufficient_rate = (
        insufficient_count / runs_per_version
    )

    stability_rate = (
        max(
            sufficient_count,
            insufficient_count
        )
        / runs_per_version
    )

    print("\nSUMMARY")

    print(
        "SUFFICIENT:",
        sufficient_count
    )

    print(
        "INSUFFICIENT:",
        insufficient_count
    )

    print(
        "SUFFICIENT Rate:",
        sufficient_rate
    )

    print(
        "INSUFFICIENT Rate:",
        insufficient_rate
    )

    print(
        "Stability Rate:",
        stability_rate
    )

    print()
