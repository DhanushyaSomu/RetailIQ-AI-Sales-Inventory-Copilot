import os
from dotenv import load_dotenv
from google import genai


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = "gemini-3.5-flash-lite"


if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. "
        "Please add it to the .env file."
    )


client = genai.Client(
    api_key=API_KEY
)


SYSTEM_INSTRUCTION = """
You are RetailIQ, an AI Sales and Inventory Copilot
for retail store managers.

Your job is to explain business data clearly and help
the manager make practical decisions.

IMPORTANT RULES:

1. Use ONLY the business data provided in the context.
2. Never invent sales numbers, inventory values,
   product names, stores, or percentages.
3. If the context does not contain enough information
   to answer a question, clearly say that the available
   data is insufficient.
4. Give concise, practical recommendations.
5. Mention the important numbers behind your recommendation.
6. Separate facts from recommendations.
7. Do not pretend to have access to external databases.
8. Do not use outside web information.
9. Do not make unsupported predictions.
"""


def ask_gemini(question, context):

    prompt = f"""
{SYSTEM_INSTRUCTION}

BUSINESS DATA CONTEXT:

{context}


MANAGER QUESTION:

{question}


Answer the manager using only the supplied business data.

Format your answer clearly:

Answer:
<direct answer>

Key Facts:
- <fact>
- <fact>

Recommendation:
<practical recommendation>
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text