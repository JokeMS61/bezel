
from painter import Painter

class PainterL3(Painter):
    def __init__(self,configuration):
        Painter.__init__(self, configuration)

    def initialize(self):
        Painter.initialize(self)

    def display(self,visible):
        Painter.display(self,visible)

    def update(self):
        Painter.refresh(self)
