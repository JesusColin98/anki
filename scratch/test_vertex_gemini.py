import sys
from google import genai
from google.genai import types

def test_gemini():
    try:
        # Use Vertex AI mode
        client = genai.Client(
            vertexai=True,
            project="384412501694",
            location="us-central1"
        )
        print("Client initialized successfully.")
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Say hello in Spanish"
        )
        print("Response text:", response.text)
    except Exception as e:
        print("Error calling Gemini:", e)

if __name__ == "__main__":
    test_gemini()
