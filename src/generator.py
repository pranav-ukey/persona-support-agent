from google import genai

from src.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_response(user_query, persona, context):
    if persona == "Technical Expert":
        persona_instruction = """
You are a Senior Systems Engineer.

Provide:
- root cause analysis
- detailed explanations
- technical terminology
- step-by-step troubleshooting
"""

    elif persona == "Frustrated User":
        persona_instruction = """
You are a compassionate customer support specialist.

Start by acknowledging the user's frustration.

Use:
- simple language
- bullet points
- actionable troubleshooting steps

Avoid:
- emotional counseling
- phrases like 'take a deep breath'
- generic encouragement

Focus on helping solve the problem.
"""

    else:
        persona_instruction = """
You are a business relationship manager.

Provide:
- concise response
- business impact
- estimated resolution guidance

Avoid technical jargon.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=f"""
        Knowledge Base Context:

        {context}

        User Query:

        {user_query}

        Answer only using the information provided above.
        If the answer is not present, say that the issue should be escalated to a human support agent.
        """,
            config={
                "system_instruction": persona_instruction,
                "temperature": 0.2
            }
        )

        return response.text

    except Exception:
        return (
            "The AI service is temporarily unavailable.\n\n"
            "Possible reasons:\n"
            "- Gemini API quota exceeded.\n"
            "- Gemini servers are busy.\n\n"
            "Please try again later."
        )