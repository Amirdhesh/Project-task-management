from pydantic_settings import BaseSettings





class Settings(BaseSettings):
    JWT_secret = "your_secret_key_here"






settings = Settings()