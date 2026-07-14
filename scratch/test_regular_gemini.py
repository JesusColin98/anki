from google import genai

def test_gemini():
    try:
        # Try regular API client
        client = genai.Client()
        print("Regular Client initialized.")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Say hello in Spanish"
        )
        print("Regular Client Response:", response.text)
    except Exception as e:
        print("Regular Client Error:", e)

if __name__ == "__main__":
    test_gemini()
