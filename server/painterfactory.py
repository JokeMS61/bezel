from settings import *
from painterL2 import PainterL2
from painterL3 import PainterL3
from painterB1 import PainterB1
from painterC1 import PainterC1
from PainterC2 import PainterC2
from painterD1 import PainterD1
from painterS1 import PainterS1
from painterS2 import PainterS2
from painterS3 import PainterS3
from painterM1 import PainterM1

class Paint(object):

    def factory(configuration):
        type = configuration.getPainter()
        logger.debug("create Painter with type %s", type)
        if type == "L2":
            return PainterL2(configuration)
        if type == "L3":
            return PainterL3(configuration)
        if type == "B1":
            return PainterB1(configuration)
        if type == "C1":
            return PainterC1(configuration)
        if type == "C2":
            return PainterC2(configuration)
        if type == "D1":
            return PainterD1(configuration)
        if type == "S1":
            return PainterS1(configuration)
        if type == "S2":
            return PainterS2(configuration)
        if type == "S3":
            return PainterS3(configuration)
        if type == "M1":
            return PainterM1(configuration)
        assert 0, "Bad painter creation: " + type

    factory = staticmethod(factory)

