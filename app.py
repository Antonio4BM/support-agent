import re
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
    buffer = ""
    for chunk in llm.stream(message):
        buffer += chunk

        while True:
            match = re.search(r"^(.+?[.!?])(\s|$)", buffer, re.DOTALL)
            if not match:
                break
            
            sentence = match.group(1).strip()
            buffer = buffer[match.end():]
            yield sentence
            
    if buffer.strip():
        yield buffer.strip()
