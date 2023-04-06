__author__ = 'JK'

import configparser
import pygame
from settings import *
from board import Board
from boardconfiguration import boardConfiguration
from timing import *
from processdata import *

# following task are to do:
# 1. better position of debug-messages
# ...

class dashmain():
    def __init__(self):
        #logger.debug('dashmain constructor')
        self._boards = []
        self.fps = 0
        self.fpsarray = []
        self.fpscount = 150
        self.fpsmin = 0
        self.fpsmax = 0
        self.firstfpscall = True
        self.configuration = None
        self.connected = "not connected"
        self.pingfile = None
        self.pingclock = None
        self.pingtime = 0
        self.pingcounter = 0
        self.soundon = None
        self.pingtext = "o"
        self.soundonchannel = None
        self.pingsymbol = False
        self.identifier = []
        # im default 25 Millisekunden maximale Ausfuehrungszeit
        self.process = MAX_PROCESSTIME
        self.screen = None

        pygame.init()
        pygame.display.init()
        pygame.font.init()
        pygame.display.set_caption("i-sig 1.0 server")
        self.fonttext = pygame.font.SysFont("Arial", size=12, bold=True)
        pygame.mixer.pre_init(22050, -16, 2, 1024)

        logger.info("Pygame version: %s", pygame.version.ver)


        self.processcontroller = ProcessDataController()

        configfile_name = g_configuration + "main.cfg"
        configuration = self.readconfig(configfile_name)
        if configuration:
            width = configuration.getWidth()
            height = configuration.getHeight()
            flag = 0
#            flag = flag | pygame.FULLSCREEN    #create a fullscreen display
#            flag = flag | pygame.DOUBLEBUF     #recommended for HWSURFACE or OPENGL
#            flag = flag | pygame.HWSURFACE     #hardware accelerated, only in FULLSCREEN
            self.screen = pygame.display.set_mode ([width, height],flag)

            loglevel = configuration.getLoglevel()
            self.setloglevel(loglevel)
            self.port = int(configuration.getSocket())
            self.pingfile = configuration.getPingfile()
            self.identifier = configuration.getIdentifier()
            logger.info("display initialized. size: %s, %s", width, height)

            self.createboards(configfile_name)
            self.printGaugeList()

        else:
            logger.error("missing configuration in dashmain")
    def printGaugeList(self):

            logger.debug("--------------------------- Gauge List --------------------------------")
            logger.debug("Board\t\t\t\t\t\tGauge\t\t\tType\tVisible\t")
            for board in self._boards:
                bi = board.getIdentifier()
                bd = board.getId()
                bs = board.getState()
                for gauge in board.getGauges():
                    gi = gauge.getIdentifier()
                    gt = gauge.getType()
                    gv = gauge.getVisible()
                    gd = gauge.getId()

                    logger.debug("%s\t%s\t%s\t%s\t%s\t%s\t%s",bi,bd,bs,gi,gd,gt,gv)

    def getPort(self):
        return self.port

    def getloglevel(self):
        ret = logger.level
        if ret is not None:
            if ret == 0:
                return "None"
            if ret == 10:
                return "debug"
            elif ret == 20:
                return "info"
            elif ret == 30:
                return "warning"
            elif ret == 40:
                return "error"
            elif ret == 50:
                return "critical"
            else:
                return "?"


    def setloglevel (self,loglevel):
        if loglevel == LOGLEVEL_NOTSET:
            logger.setLevel(logging.NOTSET)
        if loglevel == LOGLEVEL_DEBUG:
            logger.setLevel(logging.DEBUG)
        if loglevel == LOGLEVEL_INFO:
            logger.setLevel(logging.INFO)
        if loglevel == LOGLEVEL_WARNING:
            logger.setLevel(logging.WARNING)
        if loglevel == LOGLEVEL_ERROR:
            logger.setLevel(logging.ERROR)
        if loglevel == LOGLEVEL_CRITICAL:
            logger.setLevel(logging.CRITICAL)

        self.processcontroller.setValue(ID_LOGLEVEL,loglevel)


    def getsectionmap(self,config,section):
        dict = {}
        options = config.options(section)
        for option in options:
            try:
                dict[option] = config.get(section, option)
                if dict[option] == -1:
                    logger.debug ("skip: %s" % option)
            except:
                logger.warning("exception on %s!" % option)
                dict[option] = None
        return dict

    def getIdentifier(self):
        return self.identifier

    def setConnected(self, message):
        self.connected = str(message)

    def paintdebuginfo(self):
        text = "fps: " + self.getfps() + " / llv: " + self.getloglevel() + " / " + self.connected
        textsurface = self.fonttext.render(text,1,(101,255,253))
        self.screen.blit(textsurface,(5,5))

#        self.paintfps()
#        self.paintloglevel()
#        self.paintPing()
#        self.paintClient()

    def paintloglevel(self):
        text = "llv: " + self.getloglevel()
        textsurface = self.fonttext.render(text,1,(101,255,253))
        self.screen.blit(textsurface,(20,35))

    def paintfps(self):
        #Texte zeichnen
        text = "fps: " + self.getfps()
        textsurface = self.fonttext.render(text,1,(101,255,253))
        self.screen.blit(textsurface,(20,20))

    def paintPing(self):

        if self.pingsymbol == True:
            time = micros()
            timediff = time - self.pingtime
            #logger.debug("time=%s, timediff=%s", time, timediff)
            if (timediff) >= 500000:
                self.pingtime = time
                # 1 sekunde verstrichen
                self.pingcounter = self.pingcounter + 1
                #logger.debug("pingcounter=%s", self.pingcounter)
                self.pingtext = "o"
                for i in range(0,self.pingcounter):
                    self.pingtext = self.pingtext + " )"

                if self.pingcounter > 6:
                    self.pingcounter = 0
                    self.pingsymbol = False
                    self.pingtext = ""
                    #self.soundonchannel.stop()
                #logger.debug("pingtext=%s", self.pingtext)

        textsurface = self.fonttext.render(self.pingtext,1,(101,255,253))
        self.screen.blit(textsurface,(20,50))

    def paintClient(self):
        message = self.connected
        textsurface = self.fonttext.render(message,1,(101,255,253))
        self.screen.blit(textsurface,(20,65))

    def setPing(self):
        #pygame.mixer.set_reserved(1)
        self.soundonchannel = pygame.mixer.Channel(0)
        if self.pingfile != None:
            self.pingtime = micros()
            self.soundon = pygame.mixer.Sound(g_sounds + self.pingfile)
            self.soundonchannel.play(self.soundon,loops=0)
            self.pingsymbol = True

    def setfps(self,fps):
        self.fpsarray.append(fps)

        if len(self.fpsarray) == self.fpscount:
            sum =  0
            for entry in self.fpsarray:
                sum += entry

            self.fps = int(sum / self.fpscount)
#            self.fpsarray.sort()
#            self.fpsmin = self.fpsarray[0]
#            self.fpsmax = self.fpsarray[self.fpscount-1]
            self.fpsarray = []
            self.processcontroller.setValue(ID_FRAMERATE,fps)


    def getfps(self):
        return str(int(self.fps))

    def getProcessTime(self):
        return self.process

    def getfpsmin(self):
        return str(int(self.fpsmin))

    def getfpsmax(self):
        return str(int(self.fpsmax))

    def update(self, **event):

        if event is not None:
            identifier = event.get('identifier')
            if identifier is not None:
                logger.debug("event: %s", event)
                type = event.get('type')
                if type == 'app':
                    if identifier == ID_LOGLEVEL:
                        self.setloglevel(event.get('value'))
                    if identifier == ID_PING:
                        self.setPing()
                if type == 'group':
                    if identifier == ID_DASH:
                        # boardwechsel wird hier gemacht:
                        identifier = event.get('value')
                        self.setBoard(identifier)
                        self.printGaugeList()

        for board in self._boards:
            if board.getState() is True:
                board.update()

        self.paintdebuginfo()

    def setBoard(self, value):
        logger.debug("set board with identifier %s", value)
        board = self.getVisibleBoard()
        if board is not None:
            idlist = board.getIdentifier()

            if value not in idlist:
                board.setState(False)
                if self.setVisibleBoard(value) is False:
                    board.setState(True)
                    logger.error ("can not change board. Identifier korrekt in keyboard.cfg ?")

    def getVisibleBoard(self):
        for board in self._boards:
            if board.getState() is True:
                return board
        logger.error("no board vsible")
        return None

    def setVisibleBoard(self,value):
        for board in self._boards:
            boardidentifier = board.getIdentifier()
            if value in boardidentifier:
                logger.debug("new visible board: %s", board.getId())
                board.setState(True)
                self.screen.fill((0,0,0))
                board.clear()
                board.display()
                pygame.display.flip()

                title = "Board " + str(value)
                pygame.display.set_caption(title)
                return True
        logger.error("set visible command not completed")
        return False

    def getDrawArea(self):
        board = self.getVisibleBoard()
        if board is not None:
            return board.getDrawArea()


    def display(self):
        for board in self._boards:
            if board.getState() is True:
                board.display()

    def getboards(self):
        return self._boards


    def readconfig(self,file):
        if os.path.exists(file):
            # configurationsfile existiert
            cfgfile = open(file, 'r')
            # read content to the file
            config = configparser.ConfigParser()
            config.readfp(cfgfile)

            configuration = boardConfiguration()

            width = int(config.get('globals', 'width'))
            height = int(config.get('globals', 'height'))
            loglevel = config.get('globals', 'loglevel')
            identifier = config.get('globals','identifier')
            self.process = int(config.get('globals','process'))
            pingfile = config.get('sound','ping')
            port = config.get('network','socket')

            configuration.setPingfile(pingfile)
            configuration.setWidth(width)
            configuration.setHeight(height)
            configuration.setLoglevel(loglevel)
            configuration.setIdentifier(identifier)
            configuration.setSocket(port)

            cfgfile.close()
            return configuration
        else:
            return False

    def createboards(self,file):
        if os.path.exists(file):
            cfgfile = open(file, 'r')
            # read content to the file
            config = configparser.ConfigParser()
            config.read_file(cfgfile)
            # alle dashboards unter boards instanziieren
            for board, state in config.items("boards"):
                logger.debug('board  %s = %s initialized' % (board, state))
                sectionmap = self.getsectionmap(config, board)

                configuration = boardConfiguration()
                configuration.setState(state)
                configuration.setScreen(self.screen)
                for option in sectionmap:
                    if option == "id":
                        value = sectionmap["id"]
                        configuration.setId(value)      # Anzeigentyp
                    if option == "identifier":
                        value = sectionmap["identifier"]
                        configuration.setIdentifier(value)      # Liste von Bezeichnern, auf die das board reagiert
                        if value not in idlist:
                            idlist[value]=LBL_BOARD
                    if option == "group":
                        value = sectionmap["group"]
                        configuration.setGroup(value)      # Liste von Bezeichnern, auf die das board reagiert
                    if option == "position":
                        value = int(sectionmap["position"])
                        configuration.setPosition(value)      # Liste von Bezeichnern, auf die das board reagiert

                dashboard = Board(configuration)
                painter = dashboard.getpainter()
                gauges = dashboard.getGauges()
                for item in gauges:
                    painter.addPainter(item.getPainter())

                self._boards.append(dashboard)
            return True
        else:
            logger.error ("missing configurationfile for dashmain")
            return False
