import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """
    Convention : Use Snake Cased Capital letters for all constants
    """
    ORIGINS: list = ["*"]
    PROJECT_PATH: str = os.path.dirname(os.path.realpath(__file__))
    LOGS_PATH: str = os.getcwd()
    
    # Define the MySQL database URL
    DATABASE_URL = "mysql+mysqlconnector://username:password@localhost/dbname"

    SAM_MODEL=""
    STABLE_DIFFUSION_MODEL=""

    
settings = Settings()
