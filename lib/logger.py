__author__ = 'JK'

import logging
from processdata import *

LOGLEVEL_DEBUG = 'DEBUG'
LOGLEVEL_INFO = 'INFO'
LOGLEVEL_WARNING = 'WARNING'
LOGLEVEL_ERROR = 'ERROR'
LOGLEVEL_CRITICAL = 'CRITICAL'
LOGLEVEL_NOTSET = 'NOTSET'

class Logger():
    __metaclass__ = Singleton

    def __init__(self):
        self.processcontroller = ProcessDataController()

        #global logger
        self.loglevel = LOGLEVEL_DEBUG
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s (%(module)s,%(funcName)s) : %(message)s')
        fh = logging.FileHandler('../log/log.txt')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def debug(self,message,*args,**kwargs):
        self.logger.debug(message,*args,**kwargs)
        if self.loglevel == LOGLEVEL_DEBUG:
            sendtext = message % args
            self.processcontroller.setValue(ID_LOGENTRY,sendtext)

    def info(self,message,*args,**kwargs):
        self.logger.debug(message,*args,**kwargs)
        if self.loglevel == LOGLEVEL_INFO:
            sendtext = message % args
            self.processcontroller.setValue(ID_LOGENTRY,sendtext)

    def warning(self,message,*args,**kwargs):
        self.logger.debug(message,*args,**kwargs)
        if self.loglevel == LOGLEVEL_WARNING:
            sendtext = message % args
            self.processcontroller.setValue(ID_LOGENTRY,sendtext)

    def error(self,message,*args,**kwargs):
        self.logger.debug(message,*args,**kwargs)
        if self.loglevel == LOGLEVEL_ERROR:
            sendtext = message % args
            self.processcontroller.setValue(ID_LOGENTRY,sendtext)

    def critical(self,message,*args,**kwargs):
        self.logger.debug(message,*args,**kwargs)
        if self.loglevel == LOGLEVEL_CRITICAL:
            sendtext = message % args
            if self.processcontroller is True:
                self.processcontroller.setValue(ID_LOGENTRY,sendtext)

    def setLevel(self,level):

        if (level == LOGLEVEL_DEBUG):
            self.logger.setLevel(logging.DEBUG)
            self.loglevel = level
        elif (level == LOGLEVEL_INFO):
            self.logger.setLevel(logging.INFO)
            self.loglevel = level
        elif (level == LOGLEVEL_WARNING):
            self.logger.setLevel(logging.WARNING)
            self.loglevel = level
        elif (level == LOGLEVEL_ERROR):
            self.logger.setLevel(logging.ERROR)
            self.loglevel = level
        elif (level == LOGLEVEL_CRITICAL):
            self.logger.setLevel(logging.CRITICAL)
            self.loglevel = level
        else:
            self.error("unknown loglevel !")

    def getLevel(self):
        # intern int, extern String
        return self.loglevel

