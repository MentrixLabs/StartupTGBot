from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    API_BASE_URL: str = "https://mlstartupbackend-mentrixlabs.amvera.io"  # можно переопределить через .env
    MODE: str = "DEV"  # опционально, для логов

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()