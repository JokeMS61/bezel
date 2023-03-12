from gameobjects.vector2 import *
from settings import *
from painter import Painter

class PainterB1(Painter):

    def __init__(self, configuration):
        Painter.__init__(self, configuration)
        # --------------------------------------------------------------------------- variablen initialisierung
        self.scalewidth = None              #
        self.__scalestart = None              #
        # --------------------------------------------------------------------------------------- vorbelegungen
        self.min = int(configuration.getMin())
        self.max = int(configuration.getMax())
        self.valuerange = self.max - self.min

        file = configuration.getConfiguration()
        config = self.loadConfiguration(file)

        self.scalewidth = int(config.get('parameter', 'scalewidth'))
        self.scalewidth = Painter.scalevalue(self, self.scalewidth)

        self.start_pos = Vector2(-self.scalewidth / 2, 0)
        logger.debug("initialwerte: start_pos=%s,%s", self.start_pos.x, self.start_pos.y)

    def update(self):
        for identifier in self.valuelist:
            typ = self.getType(identifier)
            if typ == TYPE_POINTER:
                value =self.getValue(identifier)
                lastvalue = self.getLastValue(identifier)
                if lastvalue != value:
                    logger.debug("new (graphic) value in painterB1 : %s=%s", identifier,value)
                    surface = self.getValueSurface(identifier)
                    layer = self.getValueLayer(identifier)
                    difference = value * self.scalewidth / self.valuerange
                    valueVector = Vector2(difference,0)
                    newPosition = self.start_pos + valueVector
                    self.updateimage(surface , layer, newPosition)
                    self.setLastValue(identifier, value)
            elif typ == TYPE_TEXT:
                value =self.getValue(identifier)
                lastvalue = self.getLastValue(identifier)
                if lastvalue != value:
                    logger.debug("new (text) value in painterB1 : %s=%s", identifier,value)
                    surface = self.getValueSurface(identifier)
                    self.updatetext(surface,value)
                    self.setLastValue(identifier,value)

        self.refresh()





