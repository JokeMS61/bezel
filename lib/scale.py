__author__ = 'JK'

from gameobjects.vector2 import Vector2
import math
from dashgraphics import *
from settings import *

class ScaleConfiguration():
    def __init__(self):
        pass

    def setType(self,type):
        pass

    def getType(self):
        pass


class Scale():
    def __init__(self):
        pass

    def getArcVectors(self, radius, startangle, endangle, segments):

        #  Berechnung der Radiusvektoren fuer
        # einen Kreis vom Durchmesser r
        # y = r * cos alpha
        # x = r * son alpha
        # Aufloesung : 1 Grad (zunaechst)

        # logger.debug("radius:%s, startangle=%s, endangle=%s, segments=%s",radius, startangle, endangle, segments )
        bvectors = []


        if endangle < startangle:
            print ("Fehler! Endwinkel muss groesser Startwinkel sein")
        else:
            angle = float(startangle)
            arc = float(endangle) - startangle
            diffangle = arc / segments
            #diffangle = 10

            while angle < endangle:

                radangle = math.radians(angle)
                x = radius * math.cos(radangle)
                y = radius * math.sin(radangle)

                vector = Vector2(x,y)
                bvectors.append(vector)
                # print ("angle:%s, x:%s, y:%s ", angle,x,y)
                angle = angle + diffangle

            # Endvector
            radangle = math.radians(endangle)
            x = radius * math.cos(radangle)
            y = radius * math.sin(radangle)
            vector = Vector2(x,y)
            bvectors.append(vector)

            return bvectors
        return None

    def createAbsArc(self, radius, start, end, avector, diffangle):
        # Zielvectoren fuer den Radius erzeugen
        # Zielvector (C) = vector zum Mittelpunkt des Radius (A) + Vector vom Mittelpunkt (B)
        #

        # logger.debug("radius:%s, start=%s, end=%s, avector=%s, diffangle=%s",radius, start, end, avector, diffangle)
        cvectors = []
        bvectors = self.getArcVectors(radius, start, end, diffangle)

        if bvectors is not None:
            for bvector in bvectors:
                cvector = avector + bvector
                cvectors.append(cvector)
            return cvectors
        else:
            return None



    def linearScale(self):
        pass

    def radialSolidArc(self,radius, start, end, startvector, width):

        # logger.debug("radius=%s, start=%s, end=%s, startvector=%s, width=%s", radius, start, end, startvector, width)

        radiusaussen = float(radius + width / 2)
        radiusinnen = float(radius - width / 2)

        radius = radiusinnen
        lines = []
        # pro grad ein Liniensegment
        diffangle = (end - start)

 #       radius = radiusaussen

        while radius <= radiusaussen:
            vectors = self.createAbsArc(radius, start, end, startvector, diffangle)
            if vectors is not None:
                count = len(vectors)
                i=0
                while i <= count-2:
                    x1 = vectors[i].x
                    y1 = vectors[i].y

                    x2 = vectors[i+1].x
                    y2 = vectors[i+1].y
                    line = (x1, y1, x2,y2)

                    lines.append(line)
                    i=i+1

            radius = radius + 0.15

        return lines

    def radialFrameArc(self,radius, start, end, startvector, width):

        # logger.debug("radius=%s, start=%s, end=%s, startvector=%s, width=%s", radius, start, end, startvector, width)
        #
        #                        1 -> 2 -> 3 -> 4 -> 5
        #            Aussenlinie |----|----|----|----|
        #  insert new line ->    |                   | <- insert new line
        #            Innenlinie  |----|----|----|----|
        #                        1 -> 2 -> 3 -> 4 -> 5
        #
        radiusaussen = float(radius + width / 2)
        radiusinnen = float(radius - width / 2)
        # pro grad ein Liniensegment
        diffangle = (end - start)

        #                        1 -> 2 -> 3 -> 4 -> 5
        #            Aussenlinie |----|----|----|----|
        vectorsaussen = self.createAbsArc(radiusaussen, start, end, startvector,diffangle)

        #            Innenlinie  |----|----|----|----|
        #                        1 -> 2 -> 3 -> 4 -> 5
        vectorsinnen =  self.createAbsArc(radiusinnen, start, end, startvector,diffangle)

        linesa = []
        linesi = []
        lines = []


        if vectorsaussen is not None:
            count = len(vectorsaussen)
            i=0
            while i <= count-2:
                x1 = vectorsaussen[i].x
                y1 = vectorsaussen[i].y
                x2 = vectorsaussen[i+1].x
                y2 = vectorsaussen[i+1].y
                line = (x1, y1, x2, y2)

                # print ("lx1=%s, ly1=%s, lx2=%s ly2=%s", x1,y1,x2,y2)
                linesa.append(line)
                i=i+1

        if vectorsinnen is not None:
            count = len(vectorsinnen)
            i=0
            while i <= count-2:
                x1 = vectorsinnen[i].x
                y1 = vectorsinnen[i].y
                x2 = vectorsinnen[i+1].x
                y2 = vectorsinnen[i+1].y
                line = (x2, y2, x1, y1)
                #  Innenlinie  |----|----|----|----|
                #              1 <- 2 <- 3 <- 4 <- 5
                #  Richtung der einzelnen Teilstuecke umkehren

                # print ("lx1=%s, ly1=%s, lx2=%s ly2=%s", x2,y2,x1,y1)

                linesi.append(line)
                i=i+1

        # Aussenlienie der Gesamtliste hinzufuegen
        lines = linesa

        #  Innenlinie  |----|----|----|----|
        #              5 <- 4 <- 3 <- 2 <- 1
        #  Innenliste neu ordnen
        linesi.reverse()

        # neue Linienstuecke einfuegen s.o.
        length = len(lines)
        linie = (lines[length-1][2],lines[length-1][3],linesi[0][0],linesi[0][1])
        lines.append(linie)
        lines.extend(linesi)
        length = len(linesi)
        linie = (linesi[length-1][2],linesi[length-1][3],lines[0][0],lines[0][1])
        lines.append(linie)

        return lines

    def drawRadialScale(self,
                        surface,
                        radius,
                        start,
                        end,
                        startvector,
                        width,
                        maincount,
                        innercount,
                        color,
                        mainwidth=10,
                        innerwidth = 5,
                        scaletype=1,
                        solid=False):

        if solid == False:
            lines = self.radialFrameArc(radius,start,end,startvector, width)
        else:
            lines = self.radialSolidArc(radius,start,end,startvector, width)

        #rect = pygame.draw.aaline(surface, color, (150,25), (20,155), 1)

        #res1 = surface.get_alpha()
        #res2 = surface.get_colorkey()

        #surface.set_alpha(255)
        #surface.set_colorkey((255,255,255))

        if lines is not None:
            for line in lines:
                if type(surface) == pygame.Surface:

                    #logger.debug("line[0]=%s, line[1]=%s, line[2]=%s, line[3]=%s",line[0], line[1], line[2], line[3])
                    #x1=int(round(line[0],0))
                    #y1=int(round(line[1],0))
                    #x2=int(round(line[2],0))
                    #y2=int(round(line[3],0))
                    #logger.debug("line: x1=%s, y1=%s, x2=%s, y2=%s",x1, y1, x2, y2)
                    x1=line[0]
                    y1=line[1]
                    x2=line[2]
                    y2=line[3]

                    #pygame.draw.line(surface, color, (x1, y1), (x2, y2), 1)


                    pygame.draw.aaline(surface, color, (x1, y1), (x2, y2), 1)
                else:
                    surface.line(line[0], line[1], line[2], line[3], color)
        else:
            surface.render("Fehler",10,10)

#        # Beginn der Lines ist links aussen
#        xa = lines[0][0]
#        ya = lines[0][1]

        radiusaussen = float(radius + width / 2)
        radiusinnen = float(radius - width / 2)

        if scaletype < 1 or scaletype > 4: scaletype = 1
        if scaletype ==1 or scaletype == 2: radius = radiusinnen
        if scaletype == 3 or scaletype == 4: radius = radiusaussen

        # scale an der innenseite ausserhalb des frames
        # mainscale
        if maincount >= 1:
            bvectors = self.getArcVectors(radius,start,end,maincount)

            lines = []
            if bvectors is not None:
                for i in range (0, len(bvectors), 1):
                    laenge = bvectors[i].get_magnitude()
                    if scaletype == 1 or scaletype == 3:
                        scalefactor = 1 - (mainwidth / laenge)
                    else:
                        scalefactor = 1 + (mainwidth / laenge)

                    cvector1 = startvector + bvectors[i]
                    cvector2 = startvector + bvectors[i] * scalefactor

                    lines.append((cvector1.x,cvector1.y,cvector2.x,cvector2.y))

            if lines is not None:
                for line in lines:
                    if type(surface) == pygame.Surface:
                        pygame.draw.line(surface, color, (line[0], line[1]), (line[2], line[3]),2)
#                        pygame.draw.aaline(surface, color, (line[0], line[1]), (line[2], line[3]), False)
                    else:
                        surface.line(line[0], line[1], line[2], line[3], color)

        #innerscale
        if innercount >= 1:
            diffangle = (float(end) - float(start)) / maincount

            for i in range(0,maincount ,1):
                end = start+diffangle
                bvectors = self.getArcVectors(radius,start, end ,innercount)

                lines = []
                if bvectors is not None:
                    if len(bvectors) >= 3:
                        for i in range (1, len(bvectors)-1, 1):
                            laenge = bvectors[i].get_magnitude()
                            if scaletype == 1 or scaletype == 3:
                                scalefactor = 1 - (innerwidth / laenge)
                            else:
                                scalefactor = 1 + (innerwidth / laenge)

                            cvector1 = startvector + bvectors[i]
                            cvector2 = startvector + bvectors[i] * scalefactor

                            lines.append((cvector1.x,cvector1.y,cvector2.x,cvector2.y))

                if lines is not None:
                    for line in lines:
                        if type(surface) == pygame.Surface:
                            pygame.draw.aaline(surface, color, (line[0], line[1]), (line[2], line[3]), True)
                        else:
                            surface.line(line[0], line[1], line[2], line[3], color)

                start = end

    def drawRadialText(self,
                       surface,
                       radius,
                       start,
                       end,
                       startvector,
                       segments,
                       startvalue,
                       step,
                       font,
                       size,
                       bold,
                       color
                       ):

        # scale an der innenseite ausserhalb des frames
        # mainscale
        bvectors = self.getArcVectors(radius,start,end,segments)

        vectors = []
        if bvectors is not None:
            for i in range (0, len(bvectors), 1):
                cvector = startvector + bvectors[i]
                vectors.append(cvector)

        value = startvalue
        for vector in vectors:
            text = str(int(value))
            xpos = vector.x
            ypos = vector.y
            value = value + step
            if type(surface) == pygame.Surface:
                fonttext = pygame.font.SysFont(font, size, bold)
                textsurface = fonttext.render(text, 1, color)
                xpos = xpos - (textsurface.get_width() / 2)
                ypos = ypos - (textsurface.get_height() / 2)
                surface.blit(textsurface,(xpos,ypos))
            else:
                surface.text(xpos, ypos, text, font,color, size)

def main():

    pgi  = PygameInterface()
    dt  = Dashgraphics(pgi)

    print (pygame.vernum)
    display = dt.initialize(1192, 670)

    scale = Scale()
    startvector = Vector2(600,340)
    color = (101,255,253)

    scale.drawRadialScale(display,200,91,269,startvector,1,12,10,color,12,6,1)
    scale.drawRadialScale(display,200,-90,90,startvector,1,12,10,color,12,6,2)

    scale.drawRadialScale(display,250,91,269,startvector,20,12,10,color,12,6,3)
    scale.drawRadialScale(display,250,-90,90,startvector,20,12,10,color,12,6,4)

    scale.drawRadialScale(display,300,91,269,startvector,3,12,10,color,12,6,1,True)
    scale.drawRadialScale(display,300,-90,90,startvector,3,12,10,color,12,6,2,True)

    scale.drawRadialScale(display,350,-110,-70,Vector2(1020,400),3,10,5,color,12,6,1,True)

    scale.drawRadialText(display,330,-110,-70,Vector2(1020,400),10,1,1,"Arial",10,True)

    display.show()

    print("start...")

    done = False
    while not done:
        for event in pygame.event.get():
           if event.type == pygame.QUIT:
               done = True
           elif event.type == pygame.KEYDOWN:
               if event.key == pygame.K_ESCAPE:
                done = True

    print("exit")
    pygame.quit()


if __name__ == "__main__":
    main()
