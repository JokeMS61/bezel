__author__ = 'JK'

from settings import *
from singleton import *

class ProcessDataController():
    __metaclass__ = Singleton
    def __init__(self):
        self.observers = []  # subscriber
        self.data = {}
        self.ids = processids

    def register(self, observer):
        logger.debug("register called")
        self.observers.append(observer)

    def unregister(self,observer):
        logger.debug("unregister called")
        if observer in self.observers:
            self.observers.remove(observer)

    def initids(self):
        for id in self.ids:
            self.data[id] = ''

    def setValue(self,id,value):
        self.data[id] = value
        for observer in self.observers:
            observer.update(id,value)
