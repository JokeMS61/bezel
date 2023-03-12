
class boardConfiguration():
    def __init__(self):

        # --------------------------------------------------------------------------- variablen initialisierung
        self.cfgfile = None             # Konfigurationsfile des Boards
        self.left = None                # horizontaler Abstand in Pixeln von links oben
        self.top = None                 # vertikaler Abstand in Pixeln von links oben
        self.width = None               # Breite der Anzeige im dashboard (Alternativ zu size)
        self.height = None              # Hoehe der Anzeige im dashboard (Alternativ zu size)
        self.description = None         # Beschreibung
        self.screen = None              # Pointer auf die Window Oberflaeche
        self.staticscreen = None        # Pointer auf den Hintergrund (statische Oberfaeche)
        self.dynamicscreen = None       # Pointer auf den Vordergrund (wird zyklisch ueberschrieben)
        self.id = None                  # ID der Anzeige (Identifier)
        self.type = None                # Type der Anzeige. Ueber den Typ der wird der korrekte Painter zugeordnet
        self.value = None               # Bezeichnung der Einheit auf die die Anzeige reagiert
        self.size = None                # Skalierungsfaktor (0-100). Alternativ zu width / height
        self.background = None          # Hintergrundfarbe der Anzeige
        self.hostname = None            # Hostname des Servers
        self.socket = None              # TCP socket auf dem der Server Nachrichten empfaengt
        self.state = None               # Status des dashboards (Visible / non visible)
        self.min = None                 # unterer Wert der Anzeige
        self.max = None                 # oberer wert der Anzeige
        self.group = None               # Gruppe zu der die Anzeige gehoert
        self.position = None            # Position der Anzeige in der Gruppe
        self.configuration = None       # Konfigurationsdatei der Anzeige
        self.visible = None             # Sichtbarkeit der Anzeige
        self.gmode = None               # Grafikmodus direct oder layer
        self.loglevel = None            # Loglevel (DEBUG,INFO,WARNING,ERROR)
        self.groupStep = None           # Geschwindigkeit beim Gruppenwechsel
        self.identifier = None          # Liste von Bezeichnern auf die eine Anzeige oder board reagiert
        self.painter = None             # Type der Anzeige. Ueber den Typ der wird der korrekte Painter zugeordnet
        self.pingfile = None            # Soundfile zur Verbindungskontrolle
        self.priority = None            # Prioritaet mit der das Signal verarbeitet werden soll

    # ---------------------------------------------------------------------------------------------------- Getter
    def getId(self):
        return self.id
    def getLeft(self):
        return self.left
    def getTop(self):
        return self.top
    def getDescription(self):
        return self.description
    def getScreen(self):
        return self.screen
    def getType(self):
        return self.type
    def getValue(self):
        return self.value
    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height
    def getSize(self):
        return self.size
    def getBackground(self):
        return self.background
    def getHostname(self):
        return self.hostname
    def getSocket(self):
        return self.socket
    def getStaticScreen(self):
        return self.staticscreen
    def getDynamicScreen(self):
        return self.dynamicscreen
    def getState(self):
        return self.state
    def getMin(self):
        return self.min
    def getMax(self):
        return self.max
    def getGroup(self):
        return self.group
    def getPosition(self):
        return self.position
    def getConfiguration(self):
        return self.configuration
    def getVisible(self):
        return self.visible
    def getGmode(self):
        return self.gmode
    def getLoglevel(self):
        return self.loglevel
    def getGroupStep(self):
        return self.groupStep
    def getIdentifier(self):
        return self.identifier
    def getPainter(self):
        return self.painter
    def getPingfile(self):
        return self.pingfile
    def getPriority(self):
        return self.priority
    def getCfgFile(self):
        return self.cfgfile
    # -------------------------------------------------------------------------------------------------- Setter
    def setPriority(self, priority):
        self.priority = priority
    def setPingfile(self, file):
        self.pingfile = file
    def setPainter(self, painter):
        self.painter = painter
    def setIdentifier(self, identifier):
        self.identifier = identifier
    def setGroupStep(self, step):
        self.groupStep = step
    def setLoglevel(self,loglevel):
        self.loglevel=loglevel
    def setGmode(self,gmode):
        self.gmode=gmode
    def setVisible(self,visible):
        self.visible=visible
    def setConfiguration(self,configuration):
        self.configuration=configuration
    def setPosition(self,position):
        self.position=position
    def setGroup(self,group):
        self.group=group
    def setMin(self,min):
        self.min=min
    def setMax(self,max):
        self.max=max
    def setState(self,state):
        self.state=state
    def setStaticScreen(self,screen):
        self.staticscreen=screen
    def setDynamicScreen(self,screen):
        self.dynamicscreen=screen
    def setHostname(self,name):
        self.hostname=name
    def setSocket(self,socket):
        self.socket=socket
    def setBackground(self,color):
        self.background=color
    def setId(self,id):
        self.id = id
    def setLeft(self,left):
        self.left = left
    def setTop(self,top):
        self.top = top
    def setDescription(self,description):
        self.description = description
    def setScreen(self,screen):
        self.screen = screen
    def setType(self,type):
        self.type = type
    def setValue(self,value):
        self.value = value
    def setWidth(self,width):
        self.width = width
    def setHeight(self,height):
        self.height=height
    def setSize(self,size):
        self.size=size
    def setCfgFile(self,file):
        self.cfgfile=file