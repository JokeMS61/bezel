from settings import *
from observer import Observer
from painterfactory import Paint


class Gauge(Observer):
    def __init__(self,configuration):

        self.group = None
        self.visible = None
        self.position = None
        self.painter = Paint.factory(configuration)
        self.identifier = []
        self.id = configuration.getId()
        self.group = configuration.getGroup()
        self.visible = configuration.getVisible()
        self.position = configuration.getPosition()
        self.type = configuration.getType()
        self.prio = configuration.getPriority()

        if configuration.getMin() != None:
            self.min = float(configuration.getMin())
        else: self.min = 0
        if configuration.getMax() != None:
            self.max = float(configuration.getMax())
        else: self.max = 0
        entry = configuration.getIdentifier()

        if entry is None:
            logger.error("missing identifier for gauge %s", self.id)

        self.setIdentifier(entry)
        self.painter.initialize()

    def getId(self):
        return self.id

    def getPrio(self):
        return self.prio

    def getType(self):
        return self.type

    def getPainter(self):
        return self.painter

    def getGroup(self):
        return self.group

    def getVisible(self):
        return self.visible

    def setVisible(self, visible):
        self.visible = visible

    def getPosition(self):
        return self.position

    def getDrawingArea(self):
        return self.painter.getDrawingArea()

    def getValue(self,identifier):
        value = self.painter.getValue(identifier)
        return value

    def setValue(self,identifier, value):
        logger.debug("value=%s", value)
        if value < self.min:
            logger.debug("gauge %s: set Value to Minimum %s", self.identifier, self.min)
            value = self.min
        if value > self.max:
            logger.debug("gauge %s: set Value to Maximum %s", self.identifier, self.max)
            value = self.max

        self.painter.setValue(identifier, value)

    def getIdentifier(self):
        return self.identifier

    def setIdentifier(self,identifier):
        list = identifier.split(",")
        self.identifier = list

    def update(self, **kwargs):
        if self.getVisible() == True:
            #logger.debug("call painter update from gauge %s", self.getId())
            self.painter.update()
            pass

    def display (self):
        visible = self.getVisible()
        logger.debug("initial gauge display called. gauge=%s, visible=%s", self.getId(),visible)
        logger.debug("initial painter called. gauge=%s", self.getId())
        self.painter.display(visible)


