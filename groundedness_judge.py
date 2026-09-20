import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def judge_groundedness(question, context, answer):

    prompt = f"""
You are an AI Trust Assurance evaluator.

Evaluate whether every material claim in the ANSWER is supported by the provided CONTEXT.

QUESTION:
{question}

CONTEXT:
{context}

ANSWER:
{answer}

Rules:
- PASS if all material claims in the answer are supported by the context.
- FAIL if the answer adds, invents, contradicts, or assumes any material information not supported by the context.

Return exactly one word:

PASS

or

FAIL
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

    result = response.choices[0].message.content.strip()

    return result
