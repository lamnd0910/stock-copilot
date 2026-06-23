from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    gemini_api_key: str = ""
    embed_model: str = "bkai-foundation-models/vietnamese-bi-encoder"
    top_k: int = 5
    model_config = {"env_file": ".env"}

settings = Settings()