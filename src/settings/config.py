from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # Github Actions / Docker Hub
    dockerhub_username: str = Field(..., env="DOCKERHUB_USERNAME")
    dockerhub_token: str = Field(..., env="DOCKERHUB_TOKEN")

    # AWS
    aws_access_key_id: str = Field(..., env="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str = Field(..., env="AWS_SECRET_ACCESS_KEY")
    aws_region: str = Field("us-east-1", env="AWS_REGION")

    # Database
    database_url: str = Field(..., env="DATABASE_URL")

    # Exchange APIs
    binance_api_key: str = Field(..., env="BINANCE_API_KEY")
    binance_api_secret: str = Field(..., env="BINANCE_API_SECRET")
    alpha_vantage_key: str = Field(..., env="ALPHA_VANTAGE_KEY")

    # OpenAI
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")

    # newsapi
    newsapi_key: str = Field(..., env="NEWSAPI_KEY")

    # Telegram
    tg_token: str = Field(..., env="TG_TOKEN")
    tg_chat_id: str = Field(..., env="TG_CHAT_ID")

    # knowledge base
    knowledge_base_path: str = Field("knowledge_base", env="KNOWLEDGE_BASE_PATH")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"

settings = Settings()