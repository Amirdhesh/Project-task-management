from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv
load_dotenv()




class Settings(BaseSettings):
    JWT_secret = "your_secret_key_here"
    db_URL = os.getenv('MYSQL')






settings = Settings()