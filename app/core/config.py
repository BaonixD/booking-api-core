from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "BOOKING API CORE"
    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    REFRESH_SECRET_KEY: str  # ← Отдельный ключ!
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7  # 7 дней

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
