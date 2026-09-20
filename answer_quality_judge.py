import os
from groq import Groq


# Create the Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def judge_answer_quality(question, context, answer):

    prompt = f"""
You are evaluating the quality of an answer produced by a RAG system.

QUESTION:
{question}

CONTEXT:
{context}

ANSWER:
{answer}

Evaluate the answer on TWO dimensions:

1. RELEVANCE
Does the answer directly address the user's actual question?

Return PASS if it directly answers the question.
Return FAIL if it avoids, misunderstands, or answers a different question.

2. COMPLETENESS
Does the answer include all material information from the context
needed to adequately answer the question?

Return PASS if the important information needed to answer the question
is included.

Return FAIL if important information needed to answer the question
is omitted.

Do not require unrelated details from the context.

Return EXACTLY:

RELEVANCE: PASS or FAIL
COMPLETENESS: PASS or FAIL
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    raw_result = response.choices[0].message.content.strip()

    relevance = None
    completeness = None

    for line in raw_result.splitlines():

        line = line.strip()

        if line.startswith("RELEVANCE:"):
            relevance = line.split(":", 1)[1].strip()

        elif line.startswith("COMPLETENESS:"):
            completeness = line.split(":", 1)[1].strip()

    return {
        "relevance": relevance,
        "completeness": completeness
    }


# Everything below this point runs ONLY when
# answer_quality_judge.py is executed directly.
#
# It will NOT run when judge_answer_quality()
# is imported into another Python file.

if __name__ == "__main__":

    # ---------------------------------------------------------
    # TEST 1:
    # Relevance and completeness controlled tests
    # ---------------------------------------------------------

    context = """
Employees may work remotely up to 2 days per week with prior
manager approval. Remote work is not permitted during probation.
"""

    question = """
Can a new employee on probation work remotely?
"""

    test_answers = [

        {
            "type": "good",
            "answer": """
No. Remote work is not permitted during probation.
""",
            "expected_relevance": "PASS",
            "expected_completeness": "PASS"
        },

        {
            "type": "wrong_focus",
            "answer": """
Employees may work remotely up to two days per week with
prior manager approval.
""",
            "expected_relevance": "FAIL",
            "expected_completeness": "FAIL"
        },

        {
            "type": "unsupported_extra",
            "answer": """
No. Employees on probation cannot work remotely because
they must first complete a six-month probation period.
""",
            "expected_relevance": "PASS",
            "expected_completeness": "PASS"
        }

    ]

    print("\n===== ANSWER QUALITY JUDGE TEST =====\n")

    for test in test_answers:

        result = judge_answer_quality(
            question,
            context,
            test["answer"]
        )

        print("=" * 70)
        print("TYPE:", test["type"])

        print(
            "EXPECTED RELEVANCE:",
            test["expected_relevance"]
        )

        print(
            "EXPECTED COMPLETENESS:",
            test["expected_completeness"]
        )

        print("\nJUDGE RESULT:")
        print("RELEVANCE:", result["relevance"])
        print("COMPLETENESS:", result["completeness"])

        print()

    # ---------------------------------------------------------
    # TEST 2:
    # Specifically test relevance vs completeness
    # ---------------------------------------------------------

    print("\n===== RELEVANT VS COMPLETE TEST =====\n")

    expense_context = """
Employees must submit business expense claims within 30 days
of the expense, attach receipts, and obtain manager approval.
"""

    expense_question = """
How do I claim reimbursement for a work expense?
"""

    expense_answers = [

        {
            "type": "complete_answer",
            "answer": """
Submit the expense claim within 30 days, attach the receipt,
and obtain manager approval.
""",
            "expected_relevance": "PASS",
            "expected_completeness": "PASS"
        },

        {
            "type": "relevant_but_incomplete",
            "answer": """
Submit the expense claim within 30 days.
""",
            "expected_relevance": "PASS",
            "expected_completeness": "FAIL"
        }

    ]

    for test in expense_answers:

        result = judge_answer_quality(
            expense_question,
            expense_context,
            test["answer"]
        )

        print("=" * 70)
        print("TYPE:", test["type"])

        print(
            "EXPECTED RELEVANCE:",
            test["expected_relevance"]
        )

        print(
            "EXPECTED COMPLETENESS:",
            test["expected_completeness"]
        )

        print("\nJUDGE RESULT:")
        print("RELEVANCE:", result["relevance"])
        print("COMPLETENESS:", result["completeness"])

        print()
