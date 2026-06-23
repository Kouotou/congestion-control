from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI-Driven Traffic Control"
    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/congestiondb"
    model_dir: str = "./backend/app/ml/models"

    class Config:
        env_file = ".env"


settings = Settings()
