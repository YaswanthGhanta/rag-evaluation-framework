from reranker import rerank_policies


test_questions = [

    # -----------------------------------
    # STRONG / CORRECT MATCHES
    # -----------------------------------

    {
        "question": "How many unused annual leave days can I carry forward?",
        "type": "correct_match"
    },

    {
        "question": "Do I need a medical certificate after three days of sick leave?",
        "type": "correct_match"
    },

    {
        "question": "Can employees work from home two days a week?",
        "type": "correct_match"
    },


    # -----------------------------------
    # OUT OF SCOPE
    # -----------------------------------

    {
        "question": "What is the employee dress code?",
        "type": "out_of_scope"
    },

    {
        "question": "What is the company's health insurance coverage?",
        "type": "out_of_scope"
    },

    {
        "question": "Does the company provide free meals to employees?",
        "type": "out_of_scope"
    },


    # -----------------------------------
    # CONFLICTING CUES
    # -----------------------------------

    {
        "question": "Can unused sick leave be carried forward to next year?",
        "type": "conflicting_cue"
    },

    {
        "question": "Can parental leave be carried forward to the next year?",
        "type": "conflicting_cue"
    },

    {
        "question": "Do I need manager approval to take sick leave?",
        "type": "conflicting_cue"
    }
]


for case in test_questions:

    question = case["question"]
    question_type = case["type"]

    results = rerank_policies(question, k=3)

    print("\n" + "=" * 70)
    print("TYPE:", question_type)
    print("QUESTION:", question)
    print("=" * 70)

    for rank, result in enumerate(results, start=1):

        policy = result["policy"]

        print(
            f"{rank}. "
            f"{policy['id']} - "
            f"{policy['topic']} | "
            f"embedding={result['embedding_score']:.3f} | "
            f"rerank={result['rerank_score']:.3f}"
        )

    # -----------------------------------
    # TOP-1 / TOP-2 MARGIN
    # -----------------------------------

    top1_score = results[0]["rerank_score"]
    top2_score = results[1]["rerank_score"]

    margin = top1_score - top2_score

    print(f"\nTOP-1 RERANK SCORE: {top1_score:.3f}")
    print(f"TOP-1 vs TOP-2 MARGIN: {margin:.3f}")
