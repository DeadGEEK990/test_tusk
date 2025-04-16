from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test.db"
    TRON_NETWORK: str = "nile"

    class Config:
        env_file = ".env"


settings = Settings()