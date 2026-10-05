import os

from google import genai
from dotenv import load_dotenv


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_ai_response(prompt):
    system_context = """
You are an AI assistant for a Smart Asset & Inventory Management System.

You can answer general questions using your normal knowledge.

When the user asks about information in this system, use only
information that is actually provided to you.

Do not invent or guess information about the user's system.

If the required system information is not available, clearly say
that the information is not available.
"""

    full_prompt = (
        system_context
        + "\n\nUser question:\n"
        + prompt
    )

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=full_prompt,
    )

    return interaction.output_text