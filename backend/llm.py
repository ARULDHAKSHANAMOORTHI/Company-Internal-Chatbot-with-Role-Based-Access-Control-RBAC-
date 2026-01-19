
# import google.generativeai as genai
# import os

# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# MODEL_NAME = "models/gemini-pro-latest"


# model = genai.GenerativeModel(MODEL_NAME)


# def llm_answer(prompt: str) -> str:
#     response = model.generate_content(
#         prompt,
#         generation_config={
#             "temperature": 0.3,
#             "max_output_tokens": 512
#         }
#     )
#     return response.text


import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY not set")

# Initialize Gemini client
client = genai.Client(api_key=API_KEY)

# Use a model that is AVAILABLE in your account
MODEL_NAME = "models/gemini-flash-lite-latest"


def generate_answer(prompt: str) -> str:
    """
    Generate answer using Gemini LLM
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text.strip()



