import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    host: str
    port: int

    model_config = {
        "env_file": os.path.join(os.path.dirname(__file__), "..", ".env"),
        "env_file_encoding": "utf-8",
    }


settings = Settings()
