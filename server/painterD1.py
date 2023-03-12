from settings import *
from painter import Painter


class PainterD1(Painter):

    def __init__(self, configuration):
        Painter.__init__(self, configuration)

        #file = configuration.getConfiguration()
        #config = self.loadConfiguration(file)

        logger.debug("Painter D1 init")

    def update(self):
        for identifier in self.valuelist:
            value =self.getValue(identifier)
            lastvalue = self.getLastValue(identifier)
            if lastvalue != value:
                logger.debug("new value in painterD1 : %s", value)
                surface = self.getValueSurface(identifier)
                self.updatetext(surface,value)
                self.setLastValue(identifier,value)

        self.refresh()





