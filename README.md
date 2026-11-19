# QA AI & Performance Lab

Локальный изолированный стенд для практики использования AI-агентов (Cline + MCP) в задачах QA и профилирования производительности локальных LLM.

## Архитектура стенда
* **Host (macOS / Apple Silicon):** Нативный запуск `Ollama` (`Qwen3`) с использованием GPU (Metal) для работы с моделями без передачи данных во внешние облака.
* **Isolated Linux VM (Ubuntu ARM64):** Изолированный тестовый контур на базе `Docker Compose`:
  * **PostgreSQL 16** — хранение метрик прогонов и проверка работы AI-агента с БД через MCP.
  * **Prometheus + Grafana** — целевой сервис для генерации нагрузки и мониторинга.
* **AI Agent & MCP:** `VS Code (Remote-SSH)` + `Cline` + `@modelcontextprotocol/server-postgres` (режим `read-only` для безопасной валидации данных).

## Состав проекта
* `docker-compose.yml` — инфраструктура стенда (PostgreSQL, Prometheus, Grafana).
* `perf_test.py` — многопоточный нагрузочный скрипт (Python `ThreadPoolExecutor`), замеряющий `RPS`, `p50`, `p95`, `p99` latency API Prometheus с сохранением результатов в PostgreSQL.
* `llm_perf.py` — профилировщик LLM-эндпоинта через `OpenAI SDK` (`stream=True`) для замера **TTFT (Time To First Token)** и **Throughput (tokens/sec)**.

## Быстрый старт
1. Поднять инфраструктуру:
   ```bash
   docker compose up -d
   ```
2. Создать виртуальное окружение и поставить зависимости:
   ```bash
   python3 -m venv .venv
   .venv/bin/pip install requests psycopg2-binary openai
   ```
3. Запустить нагрузочный тест API или бенчмарк LLM:
   ```bash
   .venv/bin/python perf_test.py
   .venv/bin/python llm_perf.py
   ```
