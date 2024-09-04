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
    DATABASE_URL : str = "mysql+mysqlconnector://root:Darshan%401926@localhost:3306/userdata"

    STABLE_DIFFUSION_MODEL : str = "runwayml/stable-diffusion-inpainting"

    # Logs
    logLevel : str = "INFO"
    logFolderPath: str = "Logs"
    
settings = Settings()
