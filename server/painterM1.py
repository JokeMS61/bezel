
#import numpy as np
#import urllib
from painter import Painter

class PainterM1(Painter):
    def __init__(self,configuration):
        Painter.__init__(self, configuration)

    def initialize(self):
        Painter.initialize(self)

#        stream = urllib.request.urlopen('http://localhost:8080/frame.mjpg')
#        bytes = bytes()
#        while True:
#            bytes += stream.read(1024)
#            a = bytes.find(b'\xff\xd8')
#            b = bytes.find(b'\xff\xd9')
#            if a != -1 and b != -1:
#                jpg = bytes[a:b+2]
#                bytes = bytes[b+2:]
#                i = np.fromstring(jpg, dtype=np.uint8)

    def display(self,visible):
        Painter.display(self,visible)

    def update(self):
        Painter.refresh(self)
