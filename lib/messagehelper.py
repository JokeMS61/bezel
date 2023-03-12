__author__ = 'JK'

from settings import *
import re

class MessageHelper():
    def __init__(self):
        pass

    def getallMessages(self,message):
        logger.debug("incomming raw data: %s", message)
        values = re.findall(r"@([A-Z]{3})([0-9A-Za-z.,-_]{0,})#", message)
        logger.debug("extracting values: %s", values)
        if values:
            return values
        return None

    def getmessages(self,message):
        values = re.findall(r"@(\w+=\w+)#", message)
        if values:
            return values
        return None

    def getfirstmessage(self,message):
        ret = ""
        # findet nur die erste Nachricht und verarbeitet keine weiteren mehr
        values = re.search(r"^@(.*?=.*?)#", message)
        if values:
            ret = values.group(1)
        logger.debug("ergebnis: " + ret)
        return ret

    def getvalues(self,message):
        values = message.split('=')
        return values


    def containsPing(self,messages):
        messages = messages.upper()
        values = re.findall(r"@(PING=0)#", messages)
        if len(values) > 0:
            return True
        else:
            return False

    def containsQuit(self,messages):
        messages = messages.upper()
        values = re.findall(r"@(QUIT=TRUE)#", messages)
        if len(values) > 0:
            return True
        else:
            return False