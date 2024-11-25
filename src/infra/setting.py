from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str
    LLM_URL: str
    LLM_MODEL: str
    JWT_SECRET_KEY: str
    ALGORITHM: str
    GLOBAL_EXPIRATION: int
