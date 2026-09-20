import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def judge_context_sufficiency(question, context):

    prompt = f"""
You are evaluating whether the provided HR policy context contains enough
information to answer the user's question reliably.

QUESTION:
{question}

CONTEXT:
{context}

Classify the context as SUFFICIENT or INSUFFICIENT.

Follow this decision procedure:

1. Identify the user's core information request.

2. Identify any conditions, constraints, exceptions, or qualifications in the
   user's question that materially affect the requested answer.

3. Distinguish material conditions from incidental background information.
   Incidental background may be ignored only when it does not affect what must
   be established to answer the question.

4. Check whether the context provides the information needed to answer the core
   request AND any material conditions relevant to that request.

5. A conditional answer is still a valid answer.
   If the context itself provides the applicable policy rule and the relevant
   conditions or exceptions, return SUFFICIENT even if the user's personal
   circumstances are unknown.

6. Do not ignore a condition stated by the user merely because the remaining
   part of the question can be answered from the context. If answering the
   question requires knowing how that condition affects the policy outcome,
   the context must address that relationship.

7. Do not infer unstated permissions, prohibitions, exclusions, eligibility
   rules, or other policy conclusions merely because the context discusses a
   related or narrower category.

8. Do not use outside knowledge or invent missing policy rules.

9. Return INSUFFICIENT if any information material to answering the user's
   actual question is missing from the context.

Otherwise, return SUFFICIENT.

Return exactly one word:

SUFFICIENT

or

INSUFFICIENT
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
