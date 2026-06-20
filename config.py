from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Telegram
    BOT_TOKEN: str = Field(..., env="BOT_TOKEN")
    WEBAPP_URL: str = Field("https://localhost:5173", env="WEBAPP_URL")

    # xAI Grok
    XAI_API_KEY: str = Field(..., env="XAI_API_KEY")
    GROK_MODEL: str = Field("grok-4.3", env="GROK_MODEL")

    # Database
    DATABASE_URL: str = Field(
        "postgresql+asyncpg://postgres:postgres@localhost:5432/ideafarm",
        env="DATABASE_URL"
    )

    # Redis
    REDIS_URL: str = Field("redis://localhost:6379/0", env="REDIS_URL")

    # Security
    SECRET_KEY: str = Field("change-this-in-production", env="SECRET_KEY")

    # App
    ENV: str = Field("development", env="ENV")
    DEBUG: bool = Field(True, env="DEBUG")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()