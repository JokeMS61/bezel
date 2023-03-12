import ConfigParser

import pygame

from settings import *


class PainterL1():
    def __init__(self,configuration):

        # ----------------------------------------------------------------------- variablen initialisierung
        self.pw = None       # Breite der Anzeige
        self.ph = None       # Hoehe der Anzeige
        self.dx = None       # x - koordinate im dashboard
        self.dy = None       # y - koordinate im dashboard

        self.on = None       # filename der Anzeige "an"
        self.off = None      # filename der Anzeige "aus"
        self.width = None    # breite im dashboard
        self.height = None   # hoehe im dashboard
        self.fps = None
        self.running = False
        self.size = None
        self.state = 0
        self.value = 0
        self.imageon = None
        self.imageoff = None
        self.soundfileon = None
        self.soundfileoff = None
        self.soundon = None
        self.soundoff = None

        # Position im Dashboard
        # Pflichtfelder solten nicht None sein
        self.dx = int(configuration.getLeft())
        self.dy = int(configuration.getTop())

        # ----------------------------------------------------------------------  eigene Konfiguration lesen
        file = configuration.getConfiguration()
        self.readconfiguration(file)

        # ---------------------------------------------------------------  groessenangaben aus dem dashboard
        self.size = int(configuration.getSize())
        if self.size != None and self.size != 100:
            self.scalerescources()
        else:
            if configuration.getWidth() != None:
                self.width = int(configuration.getWidth())
            else:
                self.width = self.pw
            if configuration.getHeight() != None:
                self.height = int(configuration.getHeight())
            else:
                self.height = self.ph

        # ------------------------------------------------------ Bilder in den speicher laden und scalieren
        if self.imageon != None:
            self.on = pygame.image.load(g_pictures + self.imageon)

        if self.imageoff != None:
            self.off = pygame.image.load(g_pictures + self.imageoff)

        if self.pw != self.width or self.ph != self.height:
            self.on = pygame.transform.scale(self.on, (self.width, self.height))
            self.off = pygame.transform.scale(self.off, (self.width, self.height))

        self.mainscreen = configuration.getScreen()
        self.clock = pygame.time.Clock()
        self.time_passed = 0

        # ------------------------------------------------------------------------------ Soundfiles laden
        pygame.mixer.set_reserved(2)
        self.soundonchannel = pygame.mixer.Channel(0)
        self.soundoffchannel = pygame.mixer.Channel(1)

        if self.soundfileon != None:
            self.soundon = pygame.mixer.Sound(g_sounds + self.soundfileon)

        if self.soundfileoff != None:
            self.soundoff = pygame.mixer.Sound(g_sounds + self.soundfileoff)


    def display(self, visible):
        logger.debug("initial display called")
        if visible == True:
            self.mainscreen.blit(self.off, (self.dx, self.dy))

    def setValue(self,value):
        self.value = value

    def update(self):
        if self.value == 1:
            self.running = True
        if self.value == 0:
            self.running = False

#        print ("update painter L1")
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
                self.mainscreen.blit(self.on, (self.dx, self.dy))
            else:
                self.mainscreen.blit(self.off, (self.dx, self.dy))
        else:
            self.mainscreen.blit(self.off, (self.dx, self.dy))
            self.state = 0

    def __del__(self):
        pass

    def readconfiguration(self,file):

        configfile = g_configuration + file + ".cfg"
        cfgfile = open(configfile, 'r')
        # read content to the file
        config = ConfigParser.ConfigParser()
        config.readfp(cfgfile)

        self.pw = int(config.get('parameter', 'pwidth'))
        self.ph = int(config.get('parameter', 'pheight'))
        self.imageon = config.get('layer', 'imageon')
        self.imageoff = config.get('layer', 'imageoff')
        self.fps = int(config.get('scale', 'frequenz'))
        self.soundfileon = config.get('layer', 'soundon')
        self.soundfileoff = config.get('layer', 'soundoff')

        cfgfile.close()

    def scalerescources(self):
        logger.debug ("parameter rescources")
        self.width = int(self.pw * self.size / 100)
        self.height = int(self.ph * self.size / 100)
        logger.debug("from width=%s to width=%s", self.pw, self.width)
        logger.debug("from height=%s to height=%s", self.ph, self.height)