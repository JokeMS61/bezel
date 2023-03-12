__author__ = 'JK'

import re
import pygame
from gameobjects.vector2 import Vector2
from basis import Basis
from settings import *
from cache import Cache
from scale import *
from tools import *

class Painter(Basis):
    def __init__(self, configuration):
        Basis._init__(self)

        self.__configuration = configuration
        self.px = None                                              # x - koordinate des referenzpunktes
        self.py = None                                              # y - koordinate des referenzpunktes
        self.__left = None                                            # linke obere ecke der eigenen surface
        self.__top = None                                             # linke obere ecke der eigenen surface
        self.__right = None
        self.__bottom = None
        self.width = 0                                              # Breite der eigenen surface
        self.height = 0                                             # Hoehe der eigenen surface
        self.dx = int(self.__configuration.getLeft())               # Koordinate der Anzeige im dashboard
        self.dy = int(self.__configuration.getTop())                # Koordinate der Anzeige im dashboard
        self.size = int(self.__configuration.getSize())             # Skalierungsfaktor'
        self.gmode = self.__configuration.getGmode()
        self.lastvalue = 0                                          # vorheriger Wert
        self.debuglabel = None
        self.staticcount = 0
        self.dynamiccount = 0
        self.debugcount = 0
        self.rangecount = 0
        self.surfacecount = 0

        self.mainscreen = self.__configuration.getScreen()          # Pointer auf das Mainwindow
        self.dynamicscreen = self.__configuration.getDynamicScreen()# Pointer auf das Mainwindow (dynamic)
        self.staticscreen = self.__configuration.getStaticScreen()  # Pointer auf das Mainwindow (static)
        self.staticsurface = None                                   # Pointer auf die eigene surface (static)
        self.dynamicsurface = None                                  # Pointer auf die eigene surface (dynamic)
        self.destinationsurface = None

        self.referenceVector = None                                 # eigener Referenzvektor
        self.surfacevector = None                                   # Vector auf die eigene surface
        self.absoluteposition = None
        self.__debug_refpoint = False
        self.__frame = False
        self.__debuginfo = False

        self.surfaces = []
        self.rangesurfaces = []
        self.dynamicsurfaces = []
        self.staticsurfaces = []
        self.debugsurfaces = []
        self.text = []
        self.fonts = []
        self.colors = []
        self.ranges = []
        self.formats = {}
        self.valuelist = {}
        self.parameter = {}
        self.scales = {}

        pygame.font.init()
        self.registerConfiguration("fonts", "default", "Arial, 16, 1")
        self.registerConfiguration("colors", "default", "125, 125, 125")

        self.debugtext = pygame.font.SysFont("Arial", size=12, bold=False)
        self.cache = Cache()
        self.cacheprefix = self.__configuration.getId()

        # die Rerefenz wird schon zum Berechnen der Images benoetigt
        Painter.setreference(self, (self.dx, self.dy))

        self.readconfiguration(self.__configuration.getConfiguration())

        self.destinationsurface = self.mainscreen

        self.dumpSurfaces(self.rangesurfaces)
        self.dumpSurfaces(self.dynamicsurfaces)
        self.dumpSurfaces(self.staticsurfaces)
        self.dumpSurfaces(self.debugsurfaces)
        self.dumpSurfaces(self.surfaces)

#        if self.gmode == GMODE_DIRECT:
#            self.destinationsurface = self.mainscreen
#        else:
#           logger.error ("unsupported display mode. only <direct> supported.")


    def initialize(self):

        self.updatedimensions()

        if self.gmode == GMODE_LAYER:
            if self.staticsurface is None:
                self.staticsurface = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32)
                #self.staticsurface = self.staticsurface.convert_alpha()
            if self.dynamicsurface is None:
                self.dynamicsurface = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32)
                #self.dynamicsurface = self.dynamicsurface.convert_alpha()

        self.absoluteposition = self.getsurfacevector()

        for entry in self.staticsurfaces:
            surface = entry[1]
            visible = entry[7]
            if visible == True:
                relativeposition = entry[5]

                if self.gmode == GMODE_LAYER:
                    self.staticsurface.blit(surface, relativeposition)
                elif self.gmode == GMODE_DIRECT:
                    position = self.absoluteposition + relativeposition
                    self.staticsurface.blit(surface, relativeposition)
                    if visible == True:
                        self.mainscreen.blit(surface, position)

        self.drawScales()


    def getValueSurface(self,identifier):
        return self.valuelist[identifier]['surface']

    def getValueLayer(self,identifier):
        return self.valuelist[identifier]['layer']

    def setValue(self, identifier, value):
        self.valuelist[identifier]['value'] = value

    def getValue(self, identifier):
        value = self.valuelist[identifier]['value']
        return value

    def getType(self, identifier):
        value = self.valuelist[identifier]['type']
        return value

    def setLastValue(self,identifier, value):
        self.valuelist[identifier]['lastvalue'] = value

    def getLastValue(self,identifier):
        value = self.valuelist[identifier]['lastvalue']
        return value

    def getTop(self):
        if self.__left is not None:
            return int(self.__top)
        else:
            return None

    def getLeft(self):
        if self.__left is not None:
            return int(self.__left)
        else:
            return None

    def getWidth(self):
        if self.width is not None:
            return int(self.width)
        else:
            return None

    def getHeight(self):
        if self.height is not None:
            return int(self.height)
        else:
            return None

    def getRect(self):
        pos = self.getsurfacevector()
        rectangle = (pos.x, pos.y, self.width, self.height)
        return rectangle

    def getSize(self):
        if self.size is not None:
            return int(self.size)
        else:
            return 100

    def getValueList(self):
        return self.valuelist

    def getRanges(self):
        return self.ranges

    def getRange(self,value):
        label = None
        for j in range(0,len(self.ranges)):
            entry = self.ranges[j]
            von = entry[1]
            bis = entry[2]
            if value >= von and value < bis:
                label = entry[0]
                break
        return label

    def getMainScreen(self):
        return self.mainscreen

    def getDynamicScreen(self):
        return self.dynamicscreen

    def getStaticScreen(self):
        return self.staticscreen

    def getStaticSurface(self):
        return self.staticsurface

    def loadimage(self, image):
        #logger.debug("load image %s from %s", image, g_pictures)
        surface = pygame.image.load(g_pictures + image).convert_alpha()
        return surface

    def scalevalue(self, value):
        wert = int(value) * int(self.getSize()) / int(100)
        return int(wert)

    def scalesurface(self, surface):
        faktor = Painter.getSize(self) / 100
        new_size = Vector2(surface.get_width(),surface.get_height()) * faktor
        pygame.transform.set_smoothscale_backend('SSE')
        surface = pygame.transform.smoothscale(surface, (int(new_size.x), int(new_size.y)))
        return surface

    def getDrawingArea(self):
        rect = (int(self.surfacevector.x), int(self.surfacevector.y), self.width, self.height)
        return rect

    def delSurfaces(self,layer):
        if layer == "static":
            del self.staticsurfaces
            self.staticsurfaces = {}
            self.staticcount = 0
        elif layer == "dynamic":
            del self.dynamicsurfaces
            self.dynamiccount = 0
            self.dynamicsurfaces = {}
        elif layer == "debug":
            del self.debugsurfaces
            self.debugcount = 0
            self.debugsurfaces = {}
        elif  layer == "range":
            del self.rangesurfaces
            self.rangecount = 0
            self.rangesurfaces = {}
        else:
            del self.surfaces
            self.surfaces = {}
            self.surfacecount = 0

    def getSurfaces(self,layer):

        if layer == "static":
            surfaces = self.staticsurfaces
        elif layer == "dynamic":
            surfaces = self.dynamicsurfaces
        elif layer == "debug":
            surfaces = self.debugsurfaces
        elif self.layerisrange(layer) is True or layer == "range":
            surfaces = self.rangesurfaces
        else:
            surfaces = self.surfaces

        return surfaces


    def updatedimensions(self):
#        logger.debug("update static dimensions")
        self.staticcount = self.updatedimension("static")
#        logger.debug("update dynamic dimensions")
        self.dynamiccount = self.updatedimension("dynamic")
#        logger.debug("update debug dimensions")
        self.debugcount = self.updatedimension("debug")
#        logger.debug("update range dimensions")
        self.rangecount = self.updatedimension("range")
#        logger.debug("update other dimensions")
        self.surfacecount = self.updatedimension("other")

    def updatedimension(self, layer):

        surfaces = self.getSurfaces(layer)

        for entry in surfaces:
            pos = entry [2]
            name=entry[0]
            surface = entry[1]
            cx = pos[0]
            cy = pos[1]

            left = cx - surface.get_width() / 2
            top = cy - surface.get_height() / 2
            right = cx + surface.get_width() / 2
            bottom = cy + surface.get_height() / 2

#            logger.debug("name=%s, cx=%s, cy=%s,width=%s, height=%s",name, cx, cy, surface.get_width(),surface.get_height())
            if self.__left is not None:
                if left < self.__left:
                    self.__left = left
            else:
                self.__left = left

#            logger.debug("left=%s, self.__left=%s", left, self.__left)

            if self.__top is not None:
                if top < self.__top:
                    self.__top = top
            else:
                self.__top = top

#            logger.debug("top=%s, self.__top=%s", top, self.__top)

            if self.__right is not None:
                if right > self.__right:
                    self.__right = right
            else:
                self.__right = right

#            logger.debug("right=%s, self.__right=%s", right, self.__right)

            if self.__bottom is not None:
                if bottom > self.__bottom:
                    self.__bottom = bottom
            else:
                self.__bottom = bottom

#            logger.debug("bottom=%s, self.__bottom=%s", bottom, self.__bottom)

            self.width = self.__right - self.__left
            self.height = self.__bottom - self.__top
#            logger.debug("self.width=%s, self.height=%s", self.width, self.height)
            tempsurfacevector = Vector2(self.__left, self.__top)
            self.surfacevector = self.referenceVector + tempsurfacevector


            #tempsurfacevector = Vector2(self.__left, self.__top)
            tempImageVector = Vector2(cx - surface.get_width() / 2, cy - surface.get_height() / 2)
            imageVector = tempImageVector - tempsurfacevector

            entry[5] = (int(imageVector.x), int(imageVector.y))
            entry[6] = (surface.get_width(),surface.get_height())

#            logger.debug("layer=%s, name=%s, dimesions:(left=%s, top=%s, width=%s, height=%s)",layer,name,self.__left,self.__top,self.width,self.height)
        laenge = len(surfaces)
#        logger.debug("liefere %s Listenelemente zurueck", laenge)
        return laenge


    def updateimage(self, label, layer="dynamic", newposition=None, angle=None, visible=True):

        surfaces = self.getSurfaces(layer)
        for entry in surfaces:
            name = entry[0]

            pattern = re.compile(label)
            if pattern.match(name):
                surface = entry[1]

                if newposition is not None:
                    cx = newposition[0]
                    cy = newposition[1]
                    entry[2] = newposition
                else:
                    cx = entry[2][0]
                    cy = entry[2][1]

                tempsurfacevector = Vector2(self.__left, self.__top)
                tempImageVector = Vector2(cx - surface.get_width() / 2, cy - surface.get_height() / 2)
                imageVector = tempImageVector - tempsurfacevector

                if angle is not None:
                    entry[3] = float(angle)
                entry[5] = (imageVector.x, imageVector.y)
                entry[6] = (surface.get_width(),surface.get_height())
                entry[7] = visible

#                logger.debug("update image: %s: pos=%s,%s angle=%s ziel=%s, vector=%s,%s size=%s,%s",
#                         label ,cx, cy, angle,  entry[4], entry[5][0], entry[5][1], entry[6][0], entry[6][1])

    def updatetext(self, name, text):

        for field in self.text:
            if field[0] == name:
                font = field[1]
                color = field[2]

                for surfaceentry in self.dynamicsurfaces:
                    label = surfaceentry[0]
                    if label == name:

                        # eventuell noch formatieren.
                        if label in self.formats:
                            formatentry = self.formats[label]
                            formatstring = formatentry['formatstring']
                            factor =  formatentry['factor']
                            text = float(text) * float(factor)
                            text = formatstring.format(text)
                            text = text.strip()
                            #logger.debug("update text %s in surface %s", text, label)
                            newsurface = font.render(text, 1, color)
                            newsurface = self.scalesurface(newsurface)

                            surfaceentry[1] = newsurface
                            break
                        else:
                            logger.error("Formatangabe zum Feld %s fehlt",name)



        self.updatedimensions()

    def dumpSurfaceEntry(self, surfacelist, nr=None):
        if nr is not None:
            entry = surfacelist[nr]
            label = entry[0]
            pos = entry [2]
            angle = entry[3]
            dest = entry[4]
            vector = entry[5]
            size = entry[6]
            visible = entry[7]
            logger.debug("surface: %s: pos=%s,%s angle=%s ziel=%s, vector=%s,%s size=%s,%s visible=%s",
                         label ,pos[0], pos[1], angle,  dest, vector[0], vector[1], size[0], size[1],visible)

    def dumpSurfaces(self, surfacelist=None):

        if surfacelist == None:
            surfacelist = self.surfaces

        for entry in surfacelist:
            label = entry[0]
            pos = entry [2]
            angle = entry[3]
            dest = entry[4]
            vector = entry[5]
            size = entry[6]
            visible = entry[7]
            logger.debug("surface: %s: pos=%s,%s angle=%s ziel=%s, vector=%s,%s size=%s,%s visible=%s",
                         label ,pos[0], pos[1], angle,  dest, vector[0], vector[1], size[0], size[1], visible)

    def drawDebugInfo(self):


        if self.__debug_refpoint == True:
            debugscreen = self.mainscreen
            pos = self.getreference()
            start = (pos.x, pos.y -10)
            end = (pos.x, pos.y + 10)
            pygame.draw.line(debugscreen,(255,0,0), start, end, 1)
            start = (pos.x-10, pos.y)
            end = (pos.x+10, pos.y)
            pygame.draw.line(debugscreen,(255,0,0), start, end, 1)
            rect=pygame.Rect(pos.x-5,pos.y-5,11,11)
            pygame.draw.rect(debugscreen,(255,0,0),rect,1)

            #text = self.cacheprefix
            #self.textsurface = self.debugtext.render(text,1,(255,0,0))
            #debugscreen.blit(self.textsurface,(pos.x + 15,pos.y - 15))

        if self.__frame == True:
            debugscreen = self.mainscreen
            pos = self.getsurfacevector()
            pygame.draw.rect(debugscreen,(255,0,0),(pos.x, pos.y, self.width, self.height),1)
            #debugscreen.blit(self.textsurface,(pos.x ,pos.y - 15))

        if self.__debuginfo == True:
            text = "C: " + str(self.cache.size) + "/" + str(self.cache.maxsize)
            if self.debuglabel is not None:
                self.updatetext(self.debuglabel,text)
                debugscreen = self.mainscreen
                self.drawdebugsurface(debugscreen, self.getsurfacevector())

    def drawLine(self,surface, color,von,bis,width=1):
        color = pygame.Color(color[0], color[1], color[2], 255)
        pygame.draw.line(surface,color, von, bis, width)

#    def drawArc(self, Surface, color, Rect, start_angle, stop_angle, width=1):
#        color = pygame.Color(color[0], color[1], color[2], 255)
#        erg = pygame.draw.arc(Surface, color, Rect, start_angle, stop_angle, width)
#        logger.debug("arc")

    def getImage(self):

        self.updatedimensions()
        imagesurface = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32)
        imagesurface = imagesurface.convert_alpha()

        imagesurface.blit(self.staticsurface,(0,0))
        start = Vector2(0,0)
        self.drawDynamicSurfaces(imagesurface, start)
        return imagesurface


    def display(self, active):
        self.updatedimensions()
        self.absoluteposition = self.getsurfacevector()

#        self.drawScales()

        for entry in self.dynamicsurfaces:
            surface = entry[1]
            visible = entry[7]
            if visible == True:
                relativeposition = entry[5]

                if self.gmode == GMODE_LAYER:
                    self.dynamicsurface.blit(surface, relativeposition)
                elif self.gmode == GMODE_DIRECT:
                    position = self.absoluteposition + relativeposition
                    self.staticsurface.blit(surface, relativeposition)
                    if visible == True:
                        self.mainscreen.blit(surface, position)

        self.drawDebugInfo()

        # pygame.BLEND_ADD
        # pygame.BLEND_SUB
        # pygame.BLEND_MULT
        # pygame.BLEND_MIN
        # pygame.BLEND_MAX
        # pygame.BLEND_RGBA_ADD
        # pygame.BLEND_RGBA_SUB
        # BLEND_RGBA_MULT
        # BLEND_RGBA_MIN
        # BLEND_RGBA_MAX
        # BLEND_RGB_ADD
        # BLEND_RGB_SUB
        # BLEND_RGB_MULT
        # BLEND_RGB_MIN
        # BLEND_RGB_MAX

        if self.gmode == GMODE_LAYER and active == True:
            self.mainscreen.blit(self.staticsurface, self.absoluteposition)
            self.mainscreen.blit(self.dynamicsurface, self.absoluteposition)

        self.destinationsurface = self.mainscreen

#        self.dumpSurfaces()
#        if self.surfacecount > 0:
#            logger.warning("surfaces without correct layer !")
#            for i in range(0,self.surfacecount):
#                self.dumpSurfaceEntry(self.surfaces,i)


    def drawdebugsurface(self, destination, startvector):
        for entry in self.debugsurfaces:
            surface = entry[1]
            relativeposition = entry[5]
            # im debuginfo Feld sind Debugtexte als laufende Info (bei jedem Refresh)
            position = startvector + relativeposition
            destination.blit(surface, position)

    def drawScales(self):

        for scalebez in self.scales.keys():

            if self.getDictSection(scalebez) == True:
                radius = self.getDictEntry(scalebez,"radius")
                if radius == False: return 0
                else: radius = int(radius)

                width = self.getDictEntry(scalebez,"width")
                if width == False: return 0
                else: width = int(width)

                maincount = self.getDictEntry(scalebez,"maincount")
                if maincount == False: return 0
                else: maincount = int(maincount)

                innercount = self.getDictEntry(scalebez,"innercount")
                if innercount == False: return 0
                else: innercount = int(innercount)

                mainsize = self.getDictEntry(scalebez,"mainsize")
                if mainsize == False: return 0
                else: mainsize = int (mainsize)

                innersize = self.getDictEntry(scalebez,"innersize")
                if innersize == False: return 0
                else: innersize = int (innersize)

                textradius = self.getDictEntry(scalebez,"textradius")
                if textradius == False: return 0
                else: textradius = int (textradius)

                start = self.getDictEntry(scalebez,"start")
                if start == False: return 0
                else: start = int (start)

                step = self.getDictEntry(scalebez,"step")
                if step == False: return 0
                else: step = int (step)

                font = self.getDictEntry(scalebez,"font")
                if font == False: return 0
                else: font = str (font)

                size = self.getDictEntry(scalebez,"size")
                if size == False: return 0
                else: size = int (size)

                bold = self.getDictEntry(scalebez,"bold")
                if bold == False: return 0
                else: bold = toBoolean (bold)

                scaletype = self.getDictEntry(scalebez,"scaletype")
                if scaletype == False: return 0
                else: scaletype = int(scaletype)

                solid = self.getDictEntry(scalebez,"solid")
                if solid == False: return 0
                else: solid = toBoolean(solid)

                startangle = self.getDictEntry(scalebez,"startangle")
                if startangle == False: return 0
                else: startangle = float(startangle)

                angle = self.getDictEntry(scalebez,"angle")
                if angle == False: return 0
                else: angle = float(angle)

                colorbez = self.getDictEntry(scalebez,"color")
                if colorbez == False: return 0


                color = self.getcolor(colorbez)
                if color is None: color=(255,255,255)

                skala = Scale()

                von = float(startangle)
                von = von - 90
                arc = float(angle)
                bis = von + arc

                #display = self.getMainScreen()
                display = self.getStaticSurface()

                pos = self.getreference()-self.getsurfacevector()

                skala.drawRadialScale(display,
                                      radius,
                                      von,
                                      bis,
                                      pos,
                                      width,
                                      maincount,
                                      innercount,
                                      color,
                                      mainsize,
                                      innersize,
                                      scaletype,
                                      solid)

                skala.drawRadialText(display,
                                     textradius,
                                     von,
                                     bis,
                                     pos,
                                     maincount,
                                     start,
                                     step,
                                     font,
                                     size,
                                     bold,
                                     color)


    def drawDynamicSurfaces(self, destination, startvector):

        for entry in self.dynamicsurfaces:
            visible = entry[7]

            if visible == True:
                label = entry[0]
                position = entry[2]
                surface = entry[1]
                relativeposition = entry[5]
                angle = entry[3]

                if angle != 0:
                    rotated_sprite = self.getRotateSurface(label, surface, angle)
                    relativeposition = self.updateposition(position, rotated_sprite)
                    surface = rotated_sprite

                position = startvector + relativeposition
                destination.blit(surface, position)

    def isRangeActive(self,layer):
        for range in self.ranges:
            name=range[0]
            von=range[1]
            bis=range[2]
            identifier=range[3]

            value = self.getValue(identifier)
            if value >= von and value < bis and layer == name:
                return True

        return False

    def drawRangeSurfaces(self, destination, startvector):

        for entry in self.rangesurfaces:
            visible = entry[7]

            if visible == True:
                layer = entry[4]

                if self.isRangeActive(layer) is True:
                    label = entry[0]
                    position = entry[2]
                    surface = entry[1]
                    angle = entry[3]

                    if angle != 0:
                        rotated_sprite = self.getRotateSurface(label, surface, angle)
                        relativeposition = self.updateposition(position, rotated_sprite)
                        surface = rotated_sprite

                    relativeposition = entry[5]
                    position = startvector + relativeposition
                    destination.blit(surface, position)



    def refresh(self):

        self.mainscreen.blit(self.staticsurface, self.absoluteposition)
        self.drawDynamicSurfaces(self.destinationsurface, self.getsurfacevector())
        self.drawRangeSurfaces(self.destinationsurface, self.getsurfacevector())
        self.drawDebugInfo()


    def updateposition(self, position, surface):
        w, h = surface.get_size()
        sprite_draw_pos = Vector2(position[0]-w/2, position[1]-h/2)
        tempsurfacevector = Vector2(self.__left, self.__top)
        relativeposition = sprite_draw_pos - tempsurfacevector
        return relativeposition

    def rotateAndZoom(self,surface, angle, zoom=1.0):
        sprite = pygame.transform.rotozoom(surface, angle, zoom)
        return sprite

    def getRotateSurface(self, label, surface, angle):

        key = self.cacheprefix + ":" + label + ":" + str(angle)
        if key in self.cache:
            #logger.debug("key %s read from cache", key)
            rotated_sprite = self.cache[key]
            #logger.debug("test")
        else:
            rotated_sprite = pygame.transform.rotozoom(surface, angle, 1.0)
            self.cache.update(key,rotated_sprite)
            #logger.debug("key %s updated in cache", key)

        return rotated_sprite

    def storeimage(self, label,  surface, refposition, angle, layer, visible=True):

        entry = [label,  surface, refposition, float(angle),  layer, (0,0), (0,0), visible]

        surfaces = self.getSurfaces(layer)
        surfaces.append(entry)

    def layerisrange(self,layer=None):

        if layer is not None:
            for range in self.ranges:
                name=range[0]
                if name == layer:
                   return True
        return False

    def setreference(self, position):
        self.referenceVector = Vector2(position[0], position[1])

    def getreference(self):
        return self.referenceVector

    def getsurfacevector(self):
        return self.surfacevector

    def getfont(self, name):
        for font in self.fonts:
            label = font[0]
            value = font[1]
            if name == label:
                return value
        logger.warning ("requested font not found.")
        return None

    def getcolor(self, name):
        for color in self.colors:
            label = color[0]
            red = color[1]
            green = color[2]
            blue = color[3]

            foundcolor = (red, green, blue)
            if name == label:
                return foundcolor

        logger.warning ("requested color not found.")
        return None

    def registerConfiguration(self, type, label, entry):
        # type (Grafik oder Text)
        if type == "layer":
            self.registerimage(label, entry)
        if type == "text":
            self.registertext(label, entry)
        if type == "fonts":
            self.registerfont(label, entry)
        if type == "colors":
            self.registercolor(label, entry)
        if type == "format":
            self.registerformat(label, entry)
        if type == "values":
            self.registervalue(label, entry)
        if type == "ranges":
            self.registerrange(label, entry)
        if type == "parameter":
            self.registerparameter(label, entry)
        if type == "debug":
            self.registerdebug(label, entry)
        if type == "scales":
            self.registerscales(label, entry)

    def registerscales(self,label,value):
        scale={}
        scale["name"] = label
        self.scales[value] = scale
        logger.debug("scales: %s=%s", label,value)

    def registertext (self, label, value):
        entry = value.split(",")
        # 0 = Text, 1 = Font, 2 = color, 3,4 = position, 5 = layer
        text = entry[0]
        pos = (0, 0)
        layer = "static"
        angle = 0

        font = self.getfont("default")
        color = self.getcolor("default")

        if len(entry) > 1:
            fontname = entry[1]
            font = self.getfont(fontname)

            if len(entry) > 2:
                colorname = entry[2]
                color = self.getcolor(colorname)

                if len(entry) > 4:
                    x = entry[3]
                    y = entry[4]

                    x = self.scalevalue(x)
                    y = self.scalevalue(y)

                    pos = (int(x), int(y))

                    if len(entry) > 5:
                        angle = entry[5]

                        if len(entry) > 6:
                            layer = entry[6]
                            if layer == "debug":
                                self.debuglabel = label

        text.encode('utf-8')
        surface = font.render(text, 1, color)
        surface = self.scalesurface(surface)
        self.text.append([label, font, color])
        self.storeimage(label, surface, pos, angle, layer)
        self.updatedimensions()

    def registerfont (self, label,  value):
        entry = value.split(",")
        # 0 = Fontanme, 1 = size, 2 = bold (True/False)
        name = entry[0]
        size = int(entry[1])
        bold = entry[2]
        if bold == "True":
            font = pygame.font.SysFont(name, size, True)
        else:
            font = pygame.font.SysFont(name, size, False)
        self.fonts.append([label, font])

    def registervalue (self, label,  value):
        entry = value.split(",")
        surface = None
        min = -99999999999
        max = 99999999999
        default = 0
        layer="dynamic"
        type = TYPE_POINTER

        if len(entry) < 4:
            logger.warning("possible entries missing: %s=%s",label,value)

        if len(entry) >= 1:
            if len(entry[0]) > 0:
                surface = entry[0]
        if len(entry) >= 2:
            if len(entry[1]) > 0:
                min = float(entry[1])
        if len(entry) >= 3:
            if len(entry[2]) > 0:
                max = float(entry[2])
        if len(entry) >= 4:
            if len(entry[3]) > 0:
                layer = entry[3]
        if len(entry) >= 5:
            if len(entry[4]) > 0:
                type = entry[4]

        self.valuelist[label] = {'surface':surface,'min':min, 'max':max, 'value':default, 'lastvalue':default, 'layer':layer, 'type':type}


    def registercolor (self, label,  value):
        entry = value.split(",")
        # 0 = red, 1 = green, 2 = blue
        color = [label, int(entry[0]), int(entry[1]), int(entry[2])]
        self.colors.append(color)

    def registerformat (self, label,  value):
        entry = value.split(",")
        formatstring = entry[0]
        if len(entry) > 1:
            factor = entry[1]
        else: factor = 1
        self.formats[label] = {'formatstring':formatstring, 'factor':factor}

    def registerrange(self,label, value):

        entries = value.split(",")
        if entries is not None:
            if entries[0] is not None:

                if len(entries[0]) != "":
                    von = float(entries[0])
                else:
                    von = -9999999999

            if entries[1] is not None:
                if len(entries[1]) != "":
                    bis = float(entries[1])
                else:
                    bis = 9999999999

            if entries[2] is not None:
                identifier = entries[2]

            #logger.debug("range=%s, von=%s, bis=%s identifier=%s",label, von, bis, identifier)
            self.ranges.append([label, von, bis, identifier])

    def registerimage (self, label, entry):
        # file: Dateiname der Grafik
        # position wird relativ zum Referenzpunkt angegeben
        # layer: static oder dynamic
        value = entry.split(",")
        surface = self.loadimage(value[0])
        surface = self.scalesurface(surface)
        if len(value) >= 3:
            position = (int(self.scalevalue(value[1])), int(self.scalevalue(value[2])))
        else:
            position = (0,0)

        if len(value) >= 4:
            angle = value[3]
        else:
            angle = 0

        if len(value) >= 5:
            layer = value[4]
        else:
            layer="static"

        self.storeimage(label, surface, position, angle, layer)
        self.updatedimensions()

    def registerparameter(self, label, entry):
        self.parameter[label] = entry

        if label == 'pcenterx':
            self.px =   int(entry)
        if label == 'pcentery':
            self.py = int(entry)

    def registerdebug(self, label, value):
        if label == "refpoint":
            if value == "True":
                self.__debug_refpoint = True
            else:
                self.__debug_refpoint = False

        if label == "frame":
            if value == "True":
                self.__frame = True
            else:
                self.__frame = False

        if label == "info":
            if value == "True":
                self.__debuginfo = True
            else:
                self.__debuginfo = False





