# Support Chatbot

A streaming chat API backed by a local LLM via [Ollama](https://ollama.com/). The service accepts user messages over HTTP and streams the model response back sentence by sentence, using LangChain to orchestrate prompts and inference.

## Features

- **FastAPI HTTP API** — single `/chat` endpoint for conversational queries
- **Local LLM inference** — uses Ollama with a configurable model (default: `gemma3:1b`)
- **Streaming responses** — output is streamed to the client as complete sentences rather than raw token chunks
- **Plain-text replies** — the system prompt instructs the model to omit markdown and other formatting
- **Docker Compose setup** — runs the API and Ollama as separate services on a shared network

## Architecture

```
Client  →  chat-api (FastAPI, port 8000)  →  Ollama (port 11434)
```

| Service   | Role                                      |
|-----------|-------------------------------------------|
| `chat-api` | FastAPI app; builds prompts and streams LLM output |
| `ollama`   | Serves the language model locally         |

The API buffers incoming LLM chunks, normalizes spacing after sentence-ending punctuation, and yields one sentence at a time so clients receive readable, incremental updates.

## Prerequisites

- Docker and Docker Compose
- An external Docker network named `agent-network` (required by `docker-compose.yaml`):

  ```bash
  docker network create agent-network
  ```

## Configuration

Environment variables are loaded from `.env`:

| Variable          | Description                          | Example                    |
|-------------------|--------------------------------------|----------------------------|
| `MODEL_NAME`      | Ollama model to use                  | `gemma3:1b`                |
| `MODEL_BASE_URL`  | Ollama API base URL                  | `http://ollama:11434`      |

When running locally outside Docker, point `MODEL_BASE_URL` at your Ollama instance (e.g. `http://localhost:11434`).

## Running with Docker Compose

```bash
docker compose up --build
```

The API is available at `http://localhost:8000`.

## API

### `GET /chat`

Send a user message and receive a streamed plain-text response.

**Query parameters**

| Parameter | Type   | Description        |
|-----------|--------|--------------------|
| `message` | string | The user's message |

**Example**

```bash
curl -N "http://localhost:8000/chat?message=Hello%2C%20how%20are%20you%3F"
```

The response is streamed as `text/plain`, with each sentence emitted as it becomes complete.

## Local development

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the API (with Ollama reachable at the configured `MODEL_BASE_URL`):

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

A small test script is included to exercise the streaming endpoint:

```bash
python test_stream.py
```

## Project structure

```
support-chatbot/
├── app/
│   ├── main.py           # FastAPI app, LangChain chain, streaming /chat endpoint
│   └── core/
│       └── config.py     # Settings (app name, model name, Ollama URL)
├── docker-compose.yaml   # Ollama + chat-api services
├── Dockerfile.api        # Python 3.12 API image
├── Dockerfile.ollama     # Ollama image with gemma3:1b pre-pulled
├── requirements.txt
└── test_stream.py        # Async client example for the streaming endpoint
```
