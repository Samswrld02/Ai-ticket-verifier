# AI Ticket Verifier

Worker service that pulls ticket/email content from a Redis queue and validates it with an AI model (Gemini via an OpenAI-compatible API).

Built as an experimental worker setup: concurrent processing, graceful shutdown, and resilient Redis I/O.

## Architecture

```
Redis (ticket:events)
        │
        ▼
   Reader thread
   (BLPOP + retry)
        │
        ▼
 Internal queue (bounded)
        │
        ├──────────────┬──────────────┐
        ▼              ▼              ▼
    Worker 1       Worker 2   …   Worker N
        │              │              │
        └──────────────┴──────────────┘
                       │
                       ▼
                 AI client (Gemini)
              structured validation
```

**Flow**

1. A single **reader** runs `BLPOP` on Redis and pushes messages onto a bounded internal queue.
2. Multiple **workers** take messages from that queue and send them to the AI client.
3. If the internal queue is full, the message is kept locally and `put` is retried (no data loss).
4. On `SIGINT`/`SIGTERM`, workers receive a `STOP` signal and threads shut down cleanly.

## Design choices

| Choice                 | Why                                                |
| ---------------------- | -------------------------------------------------- |
| Reader / worker split  | Keep Redis I/O separate from slow AI calls         |
| Bounded internal queue | Absorb bursts without unbounded memory growth      |
| Timed `BLPOP` + `put`  | Periodically check the stop event                  |
| Retry on `queue.Full`  | Don't drop a message after it left Redis           |
| Redis retry + backoff  | Survive temporary connection issues                |
| Injected logger        | Avoid `print` spaghetti; easier to extend and test |

## Project structure

```
src/
├── ai_ticket_verifier/   # orchestration: start, reader, workers, signals
├── redis_connection/     # Redis client + read into internal queue
├── ai_client/            # Gemini/OpenAI client + structured response
├── logger/               # logging to stdout + file
└── config.py             # env-based configuration
```

## Requirements

- Python 3.14+
- [uv](https://github.com/astral-sh/uv)
- A running Redis instance
- Gemini API key

## Setup

```bash
# install dependencies
uv sync

# env file (not committed)
cp .env.example .env
```

Example `.env`:

```env
GEMINI_API_KEY=your_key_here
API_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_QUEUE=ticket:events
WORKERS=5
```

## Running

```bash
# start Redis (Docker example)
docker run -d --name redis -p 6379:6379 redis:alpine

# start the worker
cd src && uv run python -m ai_ticket_verifier.main
```

Push a test message onto the queue:

```bash
redis-cli LPUSH ticket:events "Paste sample email / ticket text here"
```

Logs go to stdout and `src/logger/logs/log.txt`.

## Status

**Work in progress.** Current focus: worker infrastructure (queue, concurrency, retries, shutdown).

Planned next:

- Push validation results back to Redis (or a response queue)
- Use host/port from config consistently in the Redis client
- Expand business rules / ticket domain logic

## Tech stack

- Python, threading
- Redis (`BLPOP`, retry/backoff)
- OpenAI SDK (Gemini-compatible endpoint)
- Pydantic (structured AI response)
- python-dotenv

## Author

Sam Al Jaboury — MBO Software Engineering (Noorderpoort)
