from pydantic import BaseSettings

class Settings(BaseSettings):
    consumer_key: str
    consumer_secret: str
    access_token: str
    access_token_secret: str
    bearer_token: str

    class Config:
        env_file = ".env"

settings = Settings()