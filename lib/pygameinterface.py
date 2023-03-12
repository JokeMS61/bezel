__author__ = 'JK'
import pygame
from types import *
from pygame import gfxdraw

class PygameInterface():
    def __init__(self):
        pygame.init()
        pygame.display.init()
        pygame.font.init()
        pygame.display.set_caption("test")
        pygame.mixer.pre_init(22050, -16, 2, 1024)
        self.display = None

    class Surface():
        def __init__(self, *args):
            #args -- tuple of anonymous arguments
            #kwargs -- dictionary of named arguments):
            self.surface = None
            if len(args) > 1:
                if type(args[0]) == IntType and type(args[1]) == IntType:
                    self.surface = pygame.Surface ((args[0], args[1]), pygame.SRCALPHA, 32)
            if len(args) == 1:
                if type(args[0]) == StringType:
                    file = str(args[0])
                    self.surface = pygame.image.load(file).convert_alpha()

        def getReference(self):
            return self.surface

        def copy(self, surface, x,y):
            copy_surface = surface.getReference()
            self_surface = self.getReference()
            self_surface.blit(copy_surface, (x,y))

        def render(self, text, x, y, font="Arial", size=12, bold=True, color=(101,255,253)):
            fonttext = pygame.font.SysFont(font, size, bold)
            textsurface = fonttext.render(text,True,color)
            surface = self.getReference()
            surface.blit(textsurface,(x,y))

        def line(self, x0, y0, x1, y1, color=(255,255,255)):
            surface = self.getReference()
            pygame.draw.aaline(surface, color, (x0,y0), (x1,y1), True)

        def lines(self, points, color):
            surface = self.getReference()
            pygame.draw.aalines(surface, color, False, points, 1)

        def polygon(self, points, color):
            surface = self.getReference()
            pygame.gfxdraw.aapolygon(surface,points,color)
            pygame.gfxdraw.filled_polygon(surface,points,color)

        def text(self, x,y, text, font, color, size=10, bold=True):
            surface = self.getReference()
            fonttext = pygame.font.SysFont(font, size, bold)
            textsurface = fonttext.render(text, 1, color)
            xpos = x - (textsurface.get_width() / 2)
            ypos = y - (textsurface.get_height() / 2)
            surface.blit(textsurface,(xpos,ypos))

        def clear(self):
            self_surface = self.getReference()
            self_surface.fill((0,0,0))

    class Display(Surface):
        def __init__(self, width, height, *args):
            PygameInterface.Surface.__init__(self)
            self.display = pygame.display.set_mode((width, height), 0)

        def show(self):
            pygame.display.flip()

        def getReference(self):
            return self.display


    def surface(self, width, height):
        surface = PygameInterface.Surface(width, height)
        return surface

    def initialize(self, width, height):
        self.display = PygameInterface.Display(width, height)
        return self.display

    def loadimage(self,file):
        surface = PygameInterface.Surface(file)
        return surface


