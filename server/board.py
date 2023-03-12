import configparser
import os

from settings import *
from tools import *
from observer import Observer
from boardconfiguration import boardConfiguration
from gauge import Gauge
from boardpainter import boardPainter
from gaugehelper import gaugeHelper
import pygame



class Board(Observer):
    def __init__(self, config):

        self.gauges = []
        self.boardpainter = None
        self.configuration = None
        self.groups = []
        self.identifier = []
        self.refreshtype = None
        self.rectangles = []
        self.frame = False
        self.debuginfo = False
        self.cfgfile = None

        self.state = toBoolean(config.getState())

        self.id = config.getId()
        entry = config.getIdentifier()
        if entry is None:
            logger.error("missing identifier for board %s", self.id)
        self.setIdentifier(entry)
        logger.info("initializing dashboard id=%s", self.id)
        self.screen = config.getScreen()
        file = g_configuration + self.id + ".cfg"
        self.cfgfile=file
        if os.path.exists(file):
            # configurationsfile existiert
            self.createconfiguration(file, config)
        else:
            logger.error("configurationfile missing")

        self.gaugehelper = gaugeHelper(self.gauges)
        self.initGroupChange = False
        self.gaugeref = None
        #self.display()

    def clear(self):
        self.boardpainter.clear()

    def display(self):
        self.boardpainter.display()

        for gauge in self.gauges:
            gauge.display()

        #self.boardpainter.blitStatic()
        #self.boardpainter.blitDynamic()

    def update(self, **event):

        action = event.get("action")
        if action is not None:
            type = event.get("type")
            logger.debug("type=%s, action=%s",type, action)

            if type == "group" and self.initGroupChange == False:
                # waehrend ein groupchange lauft ... nichts machen.
                identifier = event.get("identifier")
                group = self.gaugehelper.getGroup(identifier)
                if group:
                    logger.debug("found identfier %s in group list.", identifier)
                    if action == "increase":
                        item =  self.gaugehelper.getNextVisibleGauge(group,1)
                    if action == "decrease":
                        item = self.gaugehelper.getNextVisibleGauge(group, -1)

                    if item is not None:
                        oldgauge = item["old"]
                        newgauge = item["new"]
                        logger.debug("groupchange called. %s -> %s", oldgauge, newgauge)

                        oldgaugeref = self.gaugehelper.getGaugeReference(oldgauge)
                        self.newgaugeref = self.gaugehelper.getGaugeReference(newgauge)

                        painter1 = oldgaugeref.getPainter()
                        painter2 = self.newgaugeref.getPainter()

                        self.initGroupChange = True

                        logger.debug("create groupimage. start groupchange. set gauge %s unvisible", oldgaugeref.getId())
                        self.boardpainter.creategroupimage(painter1, painter2)
                        oldgaugeref.setVisible(False)
                        self.newgaugeref.setVisible(False)
                        self.boardpainter.setgroupstate(True, self.newgaugeref)
                else:
                    logger.warning("board update called but identifier %s not in group list", identifier)

            else:
                logger.warning("unknown event: %s", event)

        # hier fehlt die Abfrage ob dashboard == True bzw. visible
        self.boardpainter.update()

        for gauge in self.gauges:
            gauge.update()

        self.boardpainter.refresh()

        if self.initGroupChange == True:
            #logger.debug ("groupchange running")
            if self.boardpainter.getChangeState() == False:
        #        logger.debug ("groupchange stopped")
        #        logger.debug("set gauge %s visible", self.newgaugeref.getId())
        #        self.newgaugeref.setVisible(True)
                self.initGroupChange = False

        if self.debuginfo == True:
            self.drawDebugInfo()

    def drawDebugInfo(self):
        if self.frame == True:
            if self.rectangles is not None:
                for rect in self.rectangles:
                    prect = pygame.Rect(rect[0],rect[1],rect[2],rect[3])
                    pygame.draw.rect(self.screen,(0,0,255),prect,1)

    def getDrawArea(self):
        if self.rectangles is None:
            # alles updaten
            return None
        else:
            # option wurde gefunden, es sind aber
            # keine gueltigen rectangles definiert
            if len(self.rectangles) == 0:
                for gauge in self.getGauges():
                    self.rectangles.append(gauge.getDrawingArea())

            return self.rectangles

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state

        for gauge in self.gauges:
            group = gauge.getGroup()
            if group is None:
                gauge.setVisible(state)



    def getId(self):
        return self.id

    def getIdentifier(self):
        return self.identifier

    def setIdentifier(self,identifier):
        self.identifier = identifier.split(",")

    def getpainter(self):
        return self.boardpainter

    def getConfiguration(self):
        return self.configuration

    def createconfiguration(self, filename, config):

        logger.debug("enter configuration. initializing dashboardpainter")
        self.boardpainter = boardPainter(config)
        self.staticscreen = self.boardpainter.getStaticScreen()
        self.dynamicScreen = self.boardpainter.getDynamicScreen()

        cfgfile = open(filename, 'r')
        # read content to the file
        config = configparser.ConfigParser()
        config.read_file(cfgfile)

        if config.has_option("globals","refresh") is True:
            self.refreshtype = config.get("globals","refresh")
            if self.refreshtype is not None:
                sectionmap = self.getsectionmap(config, self.refreshtype)
                for option in sectionmap:
                    value = sectionmap[option]
                    values = value.split(",")
                    if values is not None:
                        if len(values) == 4:
                            # left, top, width, height
                            rect = (int(values[0]),int(values[1]),int(values[2]),int(values[3]))
                            self.rectangles.append(rect)
            else:
                self.rectangles = None
        else:
            self.rectangles = None

        if config.has_option("globals", "groupstep"):
            step = int(config.get("globals", "groupstep"))
            if step > 0:
                self.boardpainter.setGroupStep(step)
        else:
            # do nothing ?
            self.boardpainter.setGroupStep(None)

        # alle gauges unter types instanziieren
        for gaugeid, description in config.items("types"):
            type = None
            logger.info ('gauge %s = %s' % (gaugeid, description))

            self.configuration = boardConfiguration()
            self.configuration.setBackground(config.get("globals", "background"))
            self.configuration.setGmode (config.get("globals", "gmode"))

            # debuginfo's
            if config.has_section("debug"):
                self.debuginfo = True
                if config.has_option("debug","frame"):
                    self.frame = toBoolean(config.get("debug","frame"))

            sectionmap = self.getsectionmap(config, gaugeid)

            for option in sectionmap:
                if option == "type":
                    type = sectionmap["type"]
                    if type in gaugetypes:
                        self.configuration.setType(type)  # Anzeigentyp
                    else:
                        logger.error("type %s invalid in file %s", type, filename)
                if option == "painter":
                    self.configuration.setPainter(sectionmap["painter"])  # Anzeigentyp
                if option == "identifier":
                    identifier = sectionmap["identifier"]
                    self.configuration.setIdentifier(identifier)  # Messgroessen auf die die Anzeige reagiert

                if option == "top":
                    self.configuration.setTop(sectionmap["top"])  # y-Position im dashboardscreen
                if option == "left":
                    self.configuration.setLeft(sectionmap["left"])  # x-Position im dashboardscreen
                if option == "width":
                    self.configuration.setWidth(sectionmap["width"])
                if option == "height":
                    self.configuration.setHeight(sectionmap["height"])
                if option == "size":
                    self.configuration.setSize(sectionmap["size"])
                if option == "min":
                    self.configuration.setMin(sectionmap["min"])
                if option == "max":
                    self.configuration.setMax(sectionmap["max"])
                if option == "priority":
                    self.configuration.setPriority(sectionmap["priority"])
                if option == "cfg":
                    self.configuration.setConfiguration(sectionmap["cfg"])
                if option == "group":
                    group = sectionmap["group"]
                    self.configuration.setGroup(group)
                if option == "position":
                    self.configuration.setPosition(sectionmap["position"])
                if option == "visible":
                    value = sectionmap["visible"]
                    if value == "True":
                        self.configuration.setVisible(True)
                    else:
                        self.configuration.setVisible(False)

            if identifier not in idlist:
                idlist[identifier] = type

            self.configuration.setScreen(self.screen)
            self.configuration.setStaticScreen(self.staticscreen)
            self.configuration.setDynamicScreen(self.dynamicScreen)
            self.configuration.setCfgFile(self.cfgfile)
            self.configuration.setDescription(description)
            self.configuration.setId(gaugeid)

            # die einzelnen Anzeigen instanziieren
            gauge = Gauge(self.configuration)
            self.gauges.append(gauge)


        logger.debug("idlist: %s", idlist)
        cfgfile.close()

    def getGauges(self):
        return self.gauges

    def getsectionmap(self, config, section):
        dict = {}
        options = config.options(section)
        for option in options:
            try:
                dict[option] = config.get(section, option)
                if dict[option] == -1:
                    logger.debug("skip: %s" % option)
            except:
                logger.warning("exception on %s!" % option)
                dict[option] = None
        return dict