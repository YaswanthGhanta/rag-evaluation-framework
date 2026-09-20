import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)


def generate_strict_answer(question, context):

    prompt = f"""
You are an HR policy assistant.

Answer the user's question using ONLY the provided policy context.

Rules:
1. Every factual claim must be explicitly stated in the context
   or directly logically entailed by it.
2. Do not add assumptions.
3. Do not use outside knowledge.
4. If the context answers only part of the question, answer only
   the supported part and clearly say what the policy does not specify.
5. Do not invent consequences, exceptions, procedures, or rules
   that are not provided.

QUESTION:
{question}

POLICY CONTEXT:
{context}

Give a concise answer.
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

    return response.choices[0].message.content
