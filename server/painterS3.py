__author__ = 'JK'
from settings import *
from painter import Painter
from gameobjects.vector2 import Vector2
from math import *

class PainterS3(Painter):
    def __init__(self, configuration):
        Painter.__init__(self, configuration)
        logger.debug("Painter S3 init")

        # ----------------------------------------------------------------------  eigene Konfiguration lesen
        configurationdict = self.getConfigurationDict()
        self.radius = int(configurationdict['parameter']['radius'])
        self.orientation = configurationdict['parameter']['orientation']
        self.scalestart = configurationdict['parameter']['scalestart']
        self.scalewidth = configurationdict['parameter']['scalewidth']
        self.factor = configurationdict['parameter']['spacing']
        # --------------------------------------------------------------------------------------- vorbelegungen
        self.elementcount = 0

        self.min = int(configuration.getMin())
        self.max = int(configuration.getMax())
        self.valuerange = self.max - self.min
        self.scalewidth = Painter.scalevalue(self, self.scalewidth)
        self.start_pos = Vector2(-self.scalewidth / 2, 0)

        logger.debug("initialwerte: start_pos=%s,%s", self.start_pos.x, self.start_pos.y)

    def initialize(self):

        logger.debug("Painter S3 initialized")
        Painter.initialize(self)


    def update(self):
        for identifier in self.valuelist:
            value = float(self.getValue(identifier))
            layer = self.getValueLayer(identifier)
            lastvalue = float(self.getLastValue(identifier))
            if value != lastvalue:

                logger.debug("new value in painterS3 : %s", value)

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