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
