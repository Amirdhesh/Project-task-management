from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv
load_dotenv()




class Settings(BaseSettings):
    JWT_secret:str = "your_secret_key_here"
    db_URL:str = os.getenv('MYSQL')






settings = Settings()