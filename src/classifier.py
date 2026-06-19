import json
from google import genai
from google.genai import types

from src.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)


def classify_persona(user_message):
    system_instruction = """
You are a customer persona classifier.

Classify the user into exactly one persona:

1. Technical Expert
2. Frustrated User
3. Business Executive

Return the output in JSON format.
"""

    response_schema = {
        "type": "OBJECT",
        "properties": {
            "persona": {
                "type": "STRING",
                "enum": [
                    "Technical Expert",
                    "Frustrated User",
                    "Business Executive"
                ]
            },
            "confidence": {
                "type": "NUMBER"
            },
            "reasoning": {
                "type": "STRING"
            }
        },
        "required": [
            "persona",
            "confidence",
            "reasoning"
        ]
    }

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            response_schema=response_schema,
            temperature=0.1
        )
    )

    return json.loads(response.text)