__author__ = 'JK'

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from  pygameinterface import *



# Client
class Dashgraphics:
    concreteLib = None

    def __init__(self, concreteLib):
        self.concreteLib = concreteLib

    class Surface():
        def __init__(self, *args):
            Dashgraphics.concreteLib.Surface.__init__(*args)

        def getReference(self):
            reference = Dashgraphics.concreteLib.Surface.getReference()
            return reference

        def copy(self, surface, x,y):
            Dashgraphics.concreteLib.Surface.copy(surface, x,y)

        def render(self,text,x,y,*args):
            Dashgraphics.concreteLib.Surface.render(text, x, y, *args)

        def clear(self):
            Dashgraphics.concreteLib.Surface.clear()

        def line(self, x1, y1, x2, y2, color):
            Dashgraphics.concreteLib.Surface.line(x1, y1, x2, y2, color)

        def polygon(self, points, color):
            Dashgraphics.concreteLib.Surface.polygon(points, color)

        def lines(self, points, color):
            Dashgraphics.concreteLib.Surface.lines(points, color)

        def text(self, x,y, text, font, color, size):
            Dashgraphics.concreteLib.Surface.text(x,y, text, font, color, size)

    class Display(Surface):
        def __init__(self, width, height):
            Dashgraphics.concreteLib.Surface.__init__(self,width, height)

        def show(self):
            Dashgraphics.concreteLib.Display.show()

        def getReference(self):
            reference = Dashgraphics.concreteLib.Display.getReference()
            return reference

    def surface(self, width, height):
        return self.concreteLib.surface(width, height)

    def initialize(self, width, height):
        return self.concreteLib.initialize(width, height)

    def loadimage(self,file):
        return self.concreteLib.loadimage(file)

def main():

    picturepath = "../pic/"
    bgpath = "../../../Bilder/Gauges/"
    pgi  = PygameInterface()
    dt  = Dashgraphics(pgi)

    display = dt.initialize(1192,670)

    pic = dt.loadimage(bgpath + "dashtest.png")

    display.copy(pic,0,0)
    display.show()

    clock = pygame.time.Clock()

    print("start...")

    done = False

    while not done:
        #display.clear()
        #exit when esc is pressed
        for event in pygame.event.get():
           if event.type == pygame.QUIT:
               done = True
           elif event.type == pygame.KEYDOWN:
               if event.key == pygame.K_ESCAPE:
                done = True

        clock.tick()
        fps = int(clock.get_fps())
        display.copy(pic,0,0)
        display.render(str(fps),0,0)
        display.show()

    print("exit")
    pygame.quit()


if __name__ == "__main__":
    main()
