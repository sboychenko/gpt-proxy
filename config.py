from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # API Keys
    OPENAI_API_KEY: str
    GROK_API_KEY: str
    DEEPSEEK_API_KEY: str
    
    # Redis settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None
    REDIS_SSL: bool = False
    REDIS_RETRY_ON_TIMEOUT: bool = True
    REDIS_SOCKET_TIMEOUT: int = 5
    REDIS_SOCKET_CONNECT_TIMEOUT: int = 5
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # API endpoints
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    GROK_BASE_URL: str = "https://api.grok.ai/v1"
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com/v1"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings() 