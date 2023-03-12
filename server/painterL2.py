import configparser
import pygame
from settings import *
from painter import Painter

class PainterL2(Painter):
    def __init__(self,configuration):
        Painter.__init__(self, configuration)
        # ----------------------------------------------------------------------- variablen initialisierung
        self.on = None                  # filename der Anzeige "an"
        self.off = None                 # filename der Anzeige "aus"
        self.fps = None
        self.running = False
        self.state = 0
        self.soundfileon = None
        self.soundfileoff = None
        self.soundon = None
        self.soundoff = None

        self.clock = pygame.time.Clock()
        self.time_passed = 0

        # ----------------------------------------------------------------------  eigene Konfiguration lesen

        configurationdict = self.getConfigurationDict()
        self.fps = int(configurationdict['parameter']['frequenz'])
        self.soundfileon = configurationdict['sound']['soundon']
        self.soundfileoff = configurationdict['sound']['soundoff']

        # ------------------------------------------------------------------------------ Soundfiles laden
        pygame.mixer.set_reserved(2)
        self.soundonchannel = pygame.mixer.Channel(0)
        self.soundoffchannel = pygame.mixer.Channel(1)

        if self.soundfileon != None:
            self.soundon = pygame.mixer.Sound(g_sounds + self.soundfileon)

        if self.soundfileoff != None:
            self.soundoff = pygame.mixer.Sound(g_sounds + self.soundfileoff)

    def update(self):

        for identifier in self.valuelist:
            value = self.getValue(identifier)
            if value == 1:
                self.running = True
            if value == 0:
                self.running = False

            if self.running == True:
                self.time_passed += self.clock.tick()

                if (self.fps * self.time_passed) > 1000:
                    if self.state == 0:
                        self.state = 1
                        if self.soundon != None:
                            self.soundoffchannel.stop()
                            self.soundonchannel.play(self.soundon,loops=0)
                    elif self.state == 1:
                        self.state = 0
                        if self.soundoff != None:
                            self.soundonchannel.stop()
                            self.soundoffchannel.play(self.soundoff,loops=0)

                    self.time_passed = 0

                if self.state == 1:
                    for identifier in self.valuelist:
                        surface =self.getValueSurface(identifier)
                        layer = self.getValueLayer(identifier)
                        self.updateimage(surface + "-" + ID_ON,layer,visible=True)
                        self.updateimage(surface + "-" + ID_OFF,layer,visible=False)
                else:
                    for identifier in self.valuelist:
                        surface =self.getValueSurface(identifier)
                        layer = self.getValueLayer(identifier)
                        self.updateimage(surface + "-" + ID_ON,layer, visible=False)
                        self.updateimage(surface + "-" + ID_OFF,layer, visible=True)

            elif self.state == 1:
                for identifier in self.valuelist:
                    surface =self.getValueSurface(identifier)
                    layer = self.getValueLayer(identifier)
                    self.updateimage(surface + "-" + ID_ON,layer, visible=False)
                    self.updateimage(surface + "-" + ID_OFF,layer, visible=True)
                self.state = 0

        self.refresh()


