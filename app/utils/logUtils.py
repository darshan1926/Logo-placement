from datetime import date
from app.config import settings
import json


pathToProject = settings.LOGS_PATH

def getLogFilePath(logFolderRelativePath, fileName):
    rightNow = date.today()
    thisDay = rightNow.strftime('%Y-%m-%d-%H-%M');

    logFolderPath = pathToProject + "/" + logFolderRelativePath
    datedFileName = fileName + thisDay + '.log'
    filePath = logFolderPath + "/" + datedFileName
    
    return filePath

def getJsonFormatted(Object):
    return json.dumps(Object, indent=2, default=str)

def printObject(object, objectName):
    print (objectName + ": \n",getJsonFormatted(object))

def getDataframeFormatted(Dataframe):
    return '\t'+ Dataframe.to_string().replace('\n', '\n\t')

def getTimeTakenInSecs(elapsedTime):
    approxElapsed = round(elapsedTime, 2)
    elapsedTimeStr = str(approxElapsed)
    return elapsedTimeStr

def getTimeTakenMessage(elapsedTime, moduleName):
    logMessage = None

    elapsedTimeStr = getTimeTakenInSecs(elapsedTime)
    
    logMessage =  "{module_name} took {minutes} minutes to complete.".format(module_name = moduleName, minutes = elapsedTimeStr)

    return logMessage
