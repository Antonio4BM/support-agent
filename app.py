from fastapi import FastAPI
from langchain_ollama import OllamaLLM

app = FastAPI()

llm = OllamaLLM(
    model="gemma3:1b",
    base_url="http://ollama:11434"
)

@app.get("/chat")
def chat(message: str):
    return {"message": llm.invoke(message)}