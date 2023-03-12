__author__ = 'JK'
from settings import *
from painter import Painter
from gameobjects.vector2 import Vector2
from math import *

class PainterS2(Painter):
    def __init__(self, configuration):
        Painter.__init__(self, configuration)
        logger.debug("Painter S1 init")

        # ----------------------------------------------------------------------  eigene Konfiguration lesen

        configurationdict = self.getConfigurationDict()
        self.radius = int(configurationdict['parameter']['radius'])
        self.orientation = configurationdict['parameter']['orientation']
        self.scalestart = configurationdict['parameter']['scalestart']
        self.scalewidth = configurationdict['parameter']['scalewidth']
        self.factor = configurationdict['parameter']['spacing']
        self.imagewidth = configurationdict['parameter']['imagewidth']

        # ------------------------------------------------------------------------------ Soundfiles laden
        self.elementcount = 0

    def initialize(self):

        logger.debug("Painter S1 initialized")
        self.initializeImages("static")
        self.initializeLabels("static")
#        self.dumpSurfaces(self.getSurfaces("static"))

        self.initializeImages("dynamic")
#        self.dumpSurfaces(self.getSurfaces("dynamic"))

        self.delSurfaces("range")

    def initializeImages(self, type=None):
        values = self.getValueList()
        visible = False

        for key in values:
            # es darf fuer diese Anzeige nur 1 key definiet werden.
            # ansonsten ist nur der letzte gueltig
            entry = values[key]

            identifier = key
            min = entry["min"]
            max = entry["max"]

            alpha = float(self.scalestart)
            teilumfang = float(self.scalewidth)

            # images werden hier dynamisch erzeugt. die images aus der
            # basiskonfiguration werden nicht mehr gebraucht. Diese dienen
            # ausschliesslich als vorlage

            # startpunkt ist immer 0 Grad (Vector zeigt vom Mittelpunkt nach oben)
            startvector = Vector2(0, -self.radius)
            laenge = startvector.length
            size = float(self.imagewidth)

            if size is not None:
                factor = float(self.factor)
                abstand = float(size * factor)

                # Berechnung des winkels mit dem Kosinusatz
                # cos (winkel) = (2 * (radius zum quadrat) - (abstand zum  quadrat)) / (2 * (radius zum quadrat))
                t1 = (self.radius * self.radius)
                t2 = (abstand * abstand)
                t3 = 2 * t1

                cos_beta = ((2 * t1) - t2) / t3
                beta = acos(cos_beta)
                beta = degrees(beta)
                anzahl_elemente = teilumfang / beta

                # abstand soweit verringern, das die Anzahl auf die naechste ganzahlige
                # kleinere anzahl verkleinert wird. also z.B. wird aus 20,5 -> 20 und der
                # Winkel muss daraufhin ebenfalls angepasst werden.

                anzahl = int(anzahl_elemente)
                self.elementcount = anzahl
                winkel = teilumfang / anzahl

                for i in range(0,anzahl):

                    newangle = (i * winkel)

                    image = None
                    label = "image-" + str(i)

                    if type == "dynamic":
                        # jede gradzahl entspricht einem value
                        newvalue = newangle * (max-min) / teilumfang
                        layer = self.getRange(newvalue)
                        image = self.getImageFilenameFromValue(layer)
                        label = "id-" + str(i)
                        visible = False
                    if type == "static":
                        image = self.getImageFilenameFromValue(type)
                        label = "is-" + str(i)
                        visible = True

                    if image is not None:
                        surface = self.loadimage(image)
                        angle = radians(alpha+newangle)
                        x = round((laenge * sin(angle)),2)
                        y = -1 * round((laenge * cos(angle)),2)

                        position = (x,y)

                        sprite = self.rotateAndZoom(surface, alpha - newangle, 1.0)
                        surface = self.scalesurface(sprite)
                        self.storeimage(label, surface, position, 0 , type, visible)
                    else:
                        logger.error ("no image defined for type=%s",type)

                self.updatedimensions()
            else:
                logger.warning("surface without size")


    def getImageFilenameFromValue(self,range=None):
        # diese Funktion liest den Dateinamen aus der Konfiguration
        # und disabled diesen sofern nicht schon geschehen, da ja neue
        # images angelegt werden auf Basis dieses Files
        image = None

        configurationdict = self.getConfigurationDict()
        layer = configurationdict['layer']
        surfaces = self.getSurfaces(range)

        for key in layer:
            if range is not None:
                values = layer[key]
                value = values.split(",")
                if value[4] == range:
                    image = value[0]
                    # Datei in self.surfaces auf "False" setzen
                    # fals diese noch auf "True" steht
                    for entry in surfaces:
                        label = entry[0]
                        if label == key:
                            visible = entry[7]
                            if visible == True:
                                entry[7] = False
                            return image

        return image

    def drawLabel(self, layer):
        values = self.getValueList()

        for key in values:
            # es darf fuer diese Anzeige nur 1 key definiet werden.
            # ansonsten ist nur der letzte gueltig
            entry = values[key]
            step = int(1000)
            min = int(entry["min"]/step)
            max = int(entry["max"]/step)

            alpha = float(self.scalestart)
            teilumfang = float(self.scalewidth)

            # startpunkt ist immer 0 Grad (Vector zeigt vom Mittelpunkt nach oben)
            startvector = Vector2(0, -self.radius)
            laenge = startvector.length

            font = self.getfont("default")
            color = self.getcolor("default")
            laenge = laenge * 0.9


            for j in range(min, max + 1, 1):

                value = j
                newangle = value * teilumfang/(max-min)
                angle = radians(alpha+newangle)
                x = round((laenge * sin(angle)),2)
                y = -1 * round((laenge * cos(angle)),2)

                position = (x,y)

                text = str(int(value))
                surface = font.render(text, 1, color)
                label = "st-" + text
                self.storeimage(label, surface, refposition=position, angle=0 , layer=layer, visible=True)
            else:
                logger.error ("no image defined for type=%s",type)

    def drawScales(self):
        values = self.getValueList()

        for key in values:
            # es darf fuer diese Anzeige nur 1 key definiet werden.
            # ansonsten ist nur der letzte gueltig
            entry = values[key]

            step = int(1000)
            min = int(entry["min"]/step)
            max = int(entry["max"]/step)

            alpha = float(self.scalestart)
            teilumfang = float(self.scalewidth)
            radius = -self.radius * 0.9

            startvector = Vector2(int(self.width/2), int(self.height/2))
            laenge = abs(radius)
            lastposition = None
            color = self.getcolor("default")
            rectangle = self.getRect()
            surface = self.getStaticSurface()
#            self.drawArc(surface, color, (0,0,self.width, self.height), 0, 90, 1)

            # Anzahl segmente
            for j in range(min, max + 1, 1):
                # Unterteilung in den segmenten

                i = 0
                while i < 1:

                    value = j + i
                    newangle = value * teilumfang/(max-min)
                    angle = radians(alpha+newangle)
                    x = round((laenge * sin(angle)),2)
                    y = -1 * round((laenge * cos(angle)),2)


                    position = startvector - Vector2(x, y)

                    if lastposition is not None:
                        self.drawLine(surface, color, (lastposition.x, lastposition.y), (position.x, position.y),1)
                    lastposition = position
                    i = i + 0.01

    def initializeLabels(self, layer):
        self.drawLabel(layer)

    def update(self):
        values = self.getValueList()

        for key in values:
            # es darf fuer diese Anzeige nur 1 key definiet werden.
            # ansonsten ist nur der letzte gueltig
            entry = values[key]

            identifier = key
            min = entry["min"]
            max = entry["max"]

            value = self.getValue(identifier)
            lastvalue = float(self.getLastValue(identifier))

            if value != lastvalue:

                anzahl = self.elementcount

                # anzahl entspricht (max - min)
                # step   entspricht value

                step = int(anzahl * value / (max-min))
                for i in range(1, anzahl+1):
                    entry = self.dynamicsurfaces[i-1]

                    if i > step:
                        entry[7] = False
                    else:
                        entry[7] = True

                self.setLastValue (identifier, value)

        self.refresh()