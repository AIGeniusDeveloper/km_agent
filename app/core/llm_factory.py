from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import get_settings

settings = get_settings()

def get_llm(temperature: float = 0.0, model_name: str = "gemini-1.5-flash-001"):
    """
    Factory function to create a Gemini LLM instance.
    Defaults to Flash for speed, but can be overridden.
    """
    return ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=temperature
    )
