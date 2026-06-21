import os, requests

api_key = os.getenv("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")
if not api_key:
    raise SystemExit("Set OPENAI_API_KEY environment variable first")

headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
payload = {"model":"gpt-4o-mini","messages":[{"role":"user","content":"hello"}],"max_tokens":10}

r = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=10)
print(r.status_code, r.text)