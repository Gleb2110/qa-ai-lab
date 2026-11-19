import time
from concurrent.futures import ThreadPoolExecutor, wait
import requests
import psycopg2

TARGET_URL = "http://localhost:9090/api/v1/query?query=up"
TOTAL_REQUESTS = 200
THREADS = 10

def send_request(_):
    t0 = time.perf_counter()
    r = requests.get(TARGET_URL, timeout=5)
    r.raise_for_status()
    return (time.perf_counter() - t0) * 1000  # ms

start_all = time.perf_counter()
with ThreadPoolExecutor(max_workers=THREADS) as pool:
    futures = [pool.submit(send_request, i) for i in range(TOTAL_REQUESTS)]
    wait(futures)
    latencies = sorted(f.result() for f in futures)
total_time = time.perf_counter() - start_all

rps = round(TOTAL_REQUESTS / total_time, 2)
p50 = round(latencies[int(TOTAL_REQUESTS * 0.50)], 2)
p95 = round(latencies[int(TOTAL_REQUESTS * 0.95)], 2)
p99 = round(latencies[int(TOTAL_REQUESTS * 0.99)], 2)

conn = psycopg2.connect(
    host="localhost", port=5432, dbname="shop_db", user="qa_user", password="qa_password"
)
with conn, conn.cursor() as cur:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS public.perf_runs (
            id SERIAL PRIMARY KEY,
            created_at TIMESTAMP DEFAULT NOW(),
            total_requests INT,
            rps FLOAT,
            p50_ms FLOAT,
            p95_ms FLOAT,
            p99_ms FLOAT
        );
    """)
    cur.execute(
        "INSERT INTO public.perf_runs (total_requests, rps, p50_ms, p95_ms, p99_ms) VALUES (%s, %s, %s, %s, %s);",
        (TOTAL_REQUESTS, rps, p50, p95, p99),
    )
conn.close()
print(f"Done! RPS={rps}, p50={p50}ms, p95={p95}ms, p99={p99}ms")
