import time
from openai import OpenAI

client = OpenAI(
    base_url="http://192.168.64.1:11434/v1",
    api_key="ollama",
)

prompt = "Write 3 short negative test cases for a login API endpoint. Be concise."

t0 = time.perf_counter()
stream = client.chat.completions.create(
    model="qwen3:8b",
    messages=[{"role": "user", "content": prompt}],
    stream=True,
)

ttft = None
tokens = 0
for chunk in stream:
    if chunk.choices and chunk.choices[0].delta.content:
        if ttft is None:
            ttft = (time.perf_counter() - t0) * 1000  # ms
        tokens += 1

total_time = time.perf_counter() - t0
tps = round(tokens / total_time, 2)

print(f"TTFT (Time To First Token): {round(ttft, 2)} ms")
print(f"Total time: {round(total_time, 2)} s | Tokens: {tokens} | Speed: {tps} tokens/sec")
