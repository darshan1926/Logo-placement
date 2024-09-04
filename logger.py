import logging
import inspect
from functools import wraps
from datetime import datetime

from fastapi import HTTPException
from app.config import settings
from app.utils import logUtils

class LogManager:
    def __init__(self):
        self.logLevel = settings.logLevel
        self.project_id = None
        self.functionName = ""

    def setLogger(self):
        """Configures the logger with appropriate handlers and format."""
        path = logUtils.getLogFilePath(settings.logFolderPath, "AutoLog")
        FORMAT = '%(asctime)s | %(levelname)s | %(message)s'
        logging.basicConfig(format=FORMAT, level=self.logLevel,
                            handlers=[logging.StreamHandler(), logging.FileHandler(path, 'a')])

    def logError(self, func):
        """Decorator for logging errors and execution time of a function."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            moduleName = f"{func.__module__}.py"
            self.functionName = func.__name__
            
            request_info = kwargs.get('request', None)
            self.project_id = getattr(request_info, 'projectId', "Project Id missing")
            user_id = getattr(request_info, 'userId', "User Id missing")
            workflow_id = getattr(request_info, 'workflowId', "Workflow Id missing")

            self.logStage(f"API CALL | Project: {self.project_id} | User: {user_id} | Workflow: {workflow_id}")
            self.logStage(f"FUNCTION CALL | {moduleName} | {self.functionName} function is called!")
            
            start_time = datetime.now()

            try:
                response = func(*args, **kwargs)
                elapsed_time = (datetime.now() - start_time).total_seconds()
                self.logStage(f"FUNCTION EXIT | {moduleName} | {self.functionName} function completed in {elapsed_time:.2f} seconds.")
                return response
            except Exception as e:
                logging.exception(f"Exception in {moduleName}-{func.__name__}(). Exception: {str(e)} | Project: {self.project_id}")
                self.logStage(f"FUNCTION ERROR | {moduleName} | {self.functionName} failed to execute.")
                raise HTTPException(status_code=500, detail=str(e)) from e

        return wrapper

    def logMessage(self, message: str):
        """Logs an informational message."""
        logging.info(message)

    def warning(self, message: str):
        """Logs a warning message."""
        logging.warning(message)

    def logStage(self, message: str):
        """Logs a detailed stage message."""
        logging.info(message)
        
    def debug(self, message: str):
        """Logs a debug message."""
        logging.debug(message)

    def critical(self, message: str):
        """Logs a critical message."""
        logging.critical(message)
