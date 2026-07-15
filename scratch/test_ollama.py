import requests
payload = {
    "model": "qwen2.5:14b",
    "messages": [
        {"role": "user", "content": "Say hello in Spanish"}
    ],
    "temperature": 0.2
}
try:
    resp = requests.post("http://localhost:11434/v1/chat/completions", json=payload, timeout=30)
    print("Status:", resp.status_code)
    print("JSON:", resp.json())
except Exception as e:
    print("Error:", e)
