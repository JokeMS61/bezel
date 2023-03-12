__author__ = 'JK'

from settings import *

class Event():
    def __init__(self,identifier=ID_NONE, action=ID_NONE, value=0, type=ID_NONE, priority=4):
        self.event = {}
        self.event[LBL_IDENTIFIER] = identifier
        self.event[LBL_ACTION] = action
        self.event[LBL_TYPE] = type
        self.event[LBL_VALUE] = float(value)
        self.event[LBL_PRIO] = priority

    def getMessage(self):
        return self.event

    def setIdentifier(self, identifier):
        self.event[LBL_IDENTIFIER] = identifier

    def setAction(self,action):
        self.event[LBL_ACTION] = action

    def setPriority(self,prio):
        self.event[LBL_PRIO] = prio

    def setType(self, type):
        self.event[LBL_TYPE] = type

    def setValue(self, value):
        self.event[LBL_VALUE] = value

    def getIdentifier(self):
        return self.event[LBL_IDENTIFIER]

    def getAction(self):
        return self.event[LBL_ACTION]

    def getType(self):
        return self.event[LBL_TYPE]

    def getValue(self):
        return self.event[LBL_VALUE]

class main():
    event = Event(identifier=ID_SPEED)
    message = event.getMessage()
    print(message)

if __name__ == "__main__":
    main()