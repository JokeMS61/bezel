from settings import *
from painter import Painter


class PainterC1(Painter):
    def __init__(self, configuration):
        Painter.__init__(self, configuration)

    def update(self):
        for identifier in self.valuelist:
            value = float(self.getValue(identifier))
            layer = self.getValueLayer(identifier)
            lastvalue = float(self.getLastValue(identifier))
            if value != lastvalue:

                logger.debug("new value in painterC1 : %s", value)

                angle = (value * 25 / 16.5) * -1
                if angle >= 0: angle = 0
                if angle <= -270: angle = -270

                # formatierung, damit weniger platz im cache verbraucht wird.
                angle = "%.1f" % float(angle)

                logger.debug("update image pointer with angle=%s", angle)
                surface = self.getValueSurface(identifier)
                self.updateimage(surface, layer, None, angle)
                self.setLastValue (identifier, value)

        self.refresh()
