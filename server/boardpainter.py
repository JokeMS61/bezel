import configparser
import os
import threading
from gameobjects.vector2 import Vector2
import pygame

from settings import *


class boardPainter():
    def __init__(self,config):

        self.screen = None
        self.fps = None
        self.gmode = None
        self.background = []
        self.painters = []


        self.screen = config.getScreen()
        name = config.getId()
        self.stepsize = None

        self.staticScreen = None
        self.dynamicScreen = None
        self.surfacearray = None
        self.surface = None
        self.picturesurface = None

        file = g_configuration + name + ".cfg"
        logger.debug ("read dashboardpainter configuration. file=%s", file)
        self.create(file)

        self.changegroup = False
        self.groupposition = 0
        self.groupwidth = 0
        self.groupheight = 0
        self.picturesurfacepos = (0,0)

    def changepicturepos(self,direction):

        if (self.groupposition > (0 + self.stepsize)) and (direction == -1) or \
           (self.groupposition < (int(self.groupwidth / 2) - self.stepsize)) and (direction == 1):
            self.groupposition += (direction * self.stepsize)

            #logger.debug("position: %s", self.groupposition)

            return True
        else:
            return False

    def getChangeState(self):
        return self.changegroup

    def setGroupStep(self,step):
        self.stepsize = step

    def refresh(self):

        if self.changegroup == True:
            x1 = self.groupposition
            y1 = 0
            x2 = int(self.groupwidth / 2) + self.groupposition
            y2 = int(self.groupheight)
            area = ((x1, y1), (x2 , y2))
            #logger.debug ("area = (%s,%s) (%s,%s)", x1,y1,x2,y2)
            pygame.surfarray.blit_array(self.changesurface, self.changesurfacearray)
            self.changesurface.blit(self.picturesurface, (0,0), area=area)
            self.screen.blit(self.changesurface, self.picturesurfacepos )
            self.changegroup = self.changepicturepos(1)
            if self.changegroup == False:
                self.newgaugeref.setVisible(True)


    def blitStatic(self):
        self.screen.blit(self.staticScreen, (0,0))

    def blitDynamic(self):
        self.screen.blit(self.dynamicScreen, (0,0))

    def display(self):
        self.screen.blit(self.surface, (0,0))
        if self.surfacearray is None:
            self.surfacearray = pygame.surfarray.array2d(self.surface)

    def creategroupimage(self, painter1, painter2):


        self.groupposition = 0
        surface1 = painter1.getImage()
        surface2 = painter2.getImage()

        if surface1 is not None and surface2 is not None:

            vector1 = painter1.getsurfacevector()
            vector2 = painter2.getsurfacevector()

            # Breite ermitteln
            width1 = surface1.get_width()
            width2 = surface2.get_width()
            # Hoehe ermitteln
            height1 = surface1.get_height()
            height2 = surface2.get_height()

            if vector1.x <= vector2.x:
                posx = int(vector1.x)
            else:
                posx = int(vector2.x)

            if vector1.y <= vector2.y:
                posy = int(vector1.y)
            else:
                posy = int(vector2.y)

            if int(vector1.x + width1) >= int(vector2.x + width2):
                pwidth = int(vector1.x + width1 - posx)
            else:
                pwidth = int(vector2.x + width2 - posx)

            if int(vector1.y + height1) >= int(vector2.y + height2):
                pheight = int(vector1.y + height1 - posy)
            else:
                pheight = int(vector2.y + height2 - posy)

            self.groupwidth = int(pwidth * 2)
            self.groupheight = int(pheight)

            self.picturesurface = pygame.Surface((self.groupwidth, self.groupheight) , pygame.SRCALPHA, 32)
            self.picturesurface = self.picturesurface.convert_alpha()

            self.picturesurfacepos = Vector2(posx,posy)
            pos1 = vector1 - Vector2(posx,posy)
            pos2 = vector2 - Vector2(posx,posy) + Vector2(pwidth,0)

            logger.debug("vector1=%s vector2=%s",vector1, vector2)
            logger.debug("width1=%s width2=%s",width1, width2)
            logger.debug("height=%s height2=%s",height1, height2)
            logger.debug("posx=%s posy=%s",posx, posy)
            logger.debug("pwidth=%s pheight=%s",pwidth, pheight)
            logger.debug("groupwidth=%s groupheight=%s",self.groupwidth, self.groupheight)
            logger.debug("pos1=%s, pos2=%s", pos1, pos2)


            #posy1 = int((pheight/2)-(height1/2))

            #posx2 = int(pwidth + (pwidth/2)-(width2/2))
            #posy2 = int((pheight/2)-(height2/2))

            self.picturesurface.blit(surface1,pos1)
            self.picturesurface.blit(surface2,pos2)

            #referenz = painter1.getreference()
            #drawpos =  referenz + Vector2(-int(pwidth/2), -int(pheight/2))

            #self.picturesurfacepos = drawpos
            self.changesurface = pygame.Surface((pwidth, pheight), pygame.SRCALPHA, 32)
            self.changesurface = self.changesurface.convert_alpha()
            self.changesurfacearray = pygame.surfarray.array2d(self.changesurface)

        else:
            logger.error("groupimages could not be created.")

    def setgroupstate(self, state, newgaugeref=None):
        if state == False:
            self.groupposition = 0

        if newgaugeref is not None:
            self.newgaugeref = newgaugeref

        self.changegroup = state

    def cleardynamicScreen(self):
        pass

    def update(self):
        pygame.surfarray.blit_array(self.screen, self.surfacearray)

    def addPainter(self,painter):
        self.painters.append(painter)

    def getScreen(self):
        return self.screen

    def setScreen(self,screen):
        self.screen = screen

    def getStaticScreen(self):
        return self.staticScreen

    def getDynamicScreen(self):
        return self.dynamicScreen

    def create(self,configfile):
        if os.path.exists(configfile) == True and self.getScreen() != None:
            # configurationsfile existiert
            file = open(configfile, 'r')
            # read content to the file
            Config = configparser.ConfigParser()
            Config.read_file(file)

            width = int(Config.get('globals','width'))
            height = int(Config.get('globals','height'))
            logger.debug("width: %s",width)
            logger.debug("height: %s",height)

            caption = Config.get('globals','caption')
            color = Config.get('globals','background')
            self.background = color.split(',')
            self.fps = Config.get('globals','speed')
            self.gmode = Config.get('globals','gmode')

            self.staticScreen = pygame.Surface([width,height], pygame.SRCALPHA, 32)
            #self.staticScreen = self.staticScreen.convert_alpha()
            self.dynamicScreen = pygame.Surface([width,height], pygame.SRCALPHA, 32)
            #self.dynamicScreen = self.dynamicScreen.convert_alpha()

            self.surface = pygame.Surface([width,height], pygame.SRCALPHA, 32)
            #self.surface = self.staticScreen.convert_alpha()

            self.clear()

            image = self.getoption(Config,'globals','image')
            if image != None:
                self.surface = pygame.image.load(g_pictures + image)
                if self.surface.get_width() != width:
                    self.surface = pygame.transform.smoothscale(self.surface, (width,height))



            return True
        else:
            logger.error("missing configuration file %s",configfile)
            return False

    def clear(self):
#        self.staticScreen.fill((int(self.background[0]),int(self.background[1]),int(self.background[2])))
#        self.dynamicScreen.fill((int(self.background[0]),int(self.background[1]),int(self.background[2])))
#        self.surface.fill((int(self.background[0]),int(self.background[1]),int(self.background[2])))
#        self.screen.fill((int(self.background[0]),int(self.background[1]),int(self.background[2])))
        pass

    def getoption(self,config,section,option):
        try:
            config.get(section,option)
        except:
            return None
        else:
            return config.get(section,option)


    def __del__(self):
        pass

