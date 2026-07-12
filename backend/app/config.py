from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./smart_ecommerce.db"
    frontend_origin: str = "http://127.0.0.1:5173"

    gemini_api_key: str | None = None
    openai_api_key: str |None = None

    hf_asr_space: str = "TonmoyKroos/asr"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()