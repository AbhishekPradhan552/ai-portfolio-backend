import os
import httpx
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


class AIServiceError(Exception):
    pass


async def ask_ai(messages: list) -> str:
    if not OPENROUTER_API_KEY:
        raise AIServiceError("OpenRouter API key not configured.")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": messages,
        "temperature": 0.2,
    }

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(
                OPENROUTER_URL,
                headers=headers,
                json=payload,
            )

        response.raise_for_status()

        data = response.json()

        choices = data.get("choices")
        if not choices:
            raise AIServiceError("No choices returned from OpenRouter.")

        message = choices[0].get("message")
        if not message or "content" not in message:
            raise AIServiceError("Invalid response structure from OpenRouter.")

        return message["content"]

    except httpx.TimeoutException:
        raise AIServiceError("AI request timed out.")

    except httpx.HTTPStatusError as e:
        raise AIServiceError(
            f"OpenRouter returned error {e.response.status_code}: {e.response.text}"
        )

    except Exception as e:
        raise AIServiceError(f"Unexpected AI service error: {str(e)}")