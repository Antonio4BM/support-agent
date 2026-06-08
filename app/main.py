import re
from collections.abc import AsyncIterable

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import Settings

settings = Settings()

app = FastAPI(title=settings.app_name)

llm = OllamaLLM(
    model=settings.model_name,
    base_url=settings.model_base_url
)

template = """"
you are a helpful assistant that can answer questions and help with tasks.

Return you response in plain text ommitting asterisks and other formatting.

user message: {message}
"""

prompt = ChatPromptTemplate.from_template(template)

chain = prompt | llm

@app.get("/chat", response_class=StreamingResponse)
def chat(message: str) -> AsyncIterable[str]:
    buffer = ""
    for chunk in chain.stream({"message": message}):
        buffer += chunk
        buffer = re.sub(r"([.!?])([A-Z])", r"\1 \2", buffer)

        while True:
            match = re.search(r"^(.+?[.!?])(\s|$)", buffer, re.DOTALL)
            if not match:
                break
            
            sentence = match.group(1).strip()
            buffer = buffer[match.end():]
            yield sentence + " "
            
    if buffer.strip():
        yield buffer.strip()
