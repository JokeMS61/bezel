from gameobjects.vector2 import *
from settings import *
from painter import Painter


# --------------------------------
# Chart Painter                  -
# --------------------------------

class PainterC2(Painter):

    def __init__(self, configuration):
        Painter.__init__(self, configuration)

        logger.debug(configuration)



    def update(self):
        self.refresh()





