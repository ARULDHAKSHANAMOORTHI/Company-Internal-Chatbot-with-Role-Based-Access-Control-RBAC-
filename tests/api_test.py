

from google import genai
import os

# Load API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyBIvhV_QAcaxxVILERG-27PGc-xdjkYdew"

# Create Gemini client
gemini_client = genai.Client()

# Test generation
response = gemini_client.models.generate_content(
    model="models/gemini-flash-lite-latest",
    contents="Say hello in one line"
)

print(response.text)
