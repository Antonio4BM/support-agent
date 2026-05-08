from collections.abc import AsyncIterable

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain_ollama import OllamaLLM

app = FastAPI()

llm = OllamaLLM(
    model="gemma3:1b",
    base_url="http://ollama:11434"
)

@app.get("/chat", response_class=StreamingResponse)
def chat(message: str) -> AsyncIterable[str]:
    for chunk in llm.stream(message):
        yield chunk