
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def create_gemini_model(api_key=None, model_name="gemini-pro"):
    if not api_key:
        api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not found. Please set it in environment or pass as parameter.")

    model = ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=api_key,
        temperature=0.1,
        convert_system_message_to_human=True
    )
    return model


def get_gemini_model():
    return create_gemini_model()
