"""
Gemini configuration for the Agentic AI DB system.
Simple setup for using Google's Gemini model.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()


def get_gemini_model(model_name: str = "gemini-1.5-flash") -> ChatGoogleGenerativeAI:
    """
    Get a configured Gemini model instance.

    Args:
        model_name: Gemini model to use (default: gemini-1.5-flash)

    Returns:
        Configured ChatGoogleGenerativeAI instance
    """
    # Get API key from environment
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not found in environment variables. "
            "Please set it in your .env file or environment."
        )

    # Create and configure the model
    model = ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=api_key,
        temperature=0.1,  # Low temperature for consistent results
        max_output_tokens=2048,  # Reasonable output limit
        convert_system_message_to_human=True  # Gemini compatibility
    )

    return model


def get_gemini_pro_model() -> ChatGoogleGenerativeAI:
    """Get Gemini Pro model (good for complex reasoning)."""
    return get_gemini_model("gemini-1.5-pro")


def get_gemini_flash_model() -> ChatGoogleGenerativeAI:
    """Get Gemini Flash model (fast and efficient)."""
    return get_gemini_model("gemini-1.5-flash")


# Available Gemini models
AVAILABLE_MODELS = {
    "gemini-1.5-flash": "Fast and efficient, good for most tasks",
    "gemini-1.5-pro": "More capable, better for complex reasoning",
    "gemini-1.0-pro": "Previous generation, still capable"
}

