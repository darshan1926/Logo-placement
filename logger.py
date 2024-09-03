import logging
import inspect
from app.config import settings
from app.utils import logUtils
from functools import wraps

class LogManager:
    def __init__(self):
        self.logLevel = settings.logLevel 
        self.started = "Started"
        self.completed = "Completed"
        self.project_id = None
        self.screen = None
        self.functionName = ""
        
    def setLogger(self):
        path = logUtils.getLogFilePath(settings.logFolderPath, "AutoLog")
        FORMAT = '%(asctime)s | %(levelname)s | %(message)s' 
        logging.basicConfig( format=FORMAT, level=settings.logLevel, handlers=[logging.StreamHandler(), logging.FileHandler( path, 'a')])
    
    def logMessage(self, message):
        logging.info(f"{message}")

    def warning(self, message):
        """Logs a warning message."""
        logging.warning(message)

    def logStage(self, message):
        logging.info({"message" :message})
        
    def debug(self, message):
        """Logs a debug message."""
        logging.debug(message)

    def badCondtion(self, message):
        """Logs a critical message."""
        logging.critical(message)