import requests
import time

payload = {
    "model": "qwen2.5:14b",
    "messages": [
        {"role": "user", "content": "Say hello in Spanish"}
    ],
    "temperature": 0.2
}

print("[+] Sending request with 180s timeout...")
start_time = time.time()
try:
    resp = requests.post("http://localhost:11434/v1/chat/completions", json=payload, timeout=180)
    duration = time.time() - start_time
    print(f"[+] Status: {resp.status_code} (took {duration:.2f}s)")
    print("JSON:", resp.json())
except Exception as e:
    duration = time.time() - start_time
    print(f"[-] Error after {duration:.2f}s: {e}")
