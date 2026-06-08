from pydantic import BaseSettings

class Settings(BaseSettings):

    app_name: str = "Agent API"
    model_name: str
    model_base_url: str