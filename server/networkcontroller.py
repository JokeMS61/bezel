
from settings import *
from networkclient import NetworkClient
from networkserver import NetworkServer
from event import Event
from gaugehelper import gaugeHelper
from collections import deque
from timing import *
from processdata import *
from messagehelper import *
from tools import *

class NetworkController(object):

    def __init__(self, dash):
        self.dash = dash
        self.eventpublisher = None  # subscriber
        self.port = dash.getPort()
        self.processtime = 0
        self.starttime = 0
        self.processduration = dash.getProcessTime()

        self.slots = {}
        self.slots[1] = deque()
        self.slots[2] = deque()
        self.slots[3] = deque()
        self.slots[4] = deque()
        self.slots[5] = deque()
        self.slots[6] = deque()

        gauges = []
        boards = dash.getboards()
        for board in boards:
            gaugelist = board.getGauges()
            for gauge in gaugelist:
                gauges.append(gauge)

        self.gh = gaugeHelper(gauges)

        self.ns = NetworkServer(self.process, self.connected, self.port)
        self.ns.start()

        self.processcontroller =  ProcessDataController()
        self.processcontroller.register(self.ns)

    def register(self, publisher):
        self.eventpublisher = publisher

 
    def unregister(self, observer):
        self.eventpublisher = None

    def connected(self,message):
        self.dash.setConnected(message)

    def processQueue(self,nr):
        for i in range (0, len(self.slots[nr])):
            time =micros() - self.starttime

            if ( time > self.processduration):
                logger.debug("exit after %s microseconds. max processtime = %s", time, self.processduration )
                return None
            else:
                item = self.slots[nr].popleft()
                self.update(item)

        return True

    def clearSlot(self, nr):
        self.slots[nr].clear()

    def getSlotEntries(self,nr=None):
        if nr == None:
            cslot1 = len(self.slots[1])
            cslot2 = len(self.slots[2])
            cslot3 = len(self.slots[3])
            cslot4 = len(self.slots[4])
            cslot5 = len(self.slots[5])
            cslot6 = len(self.slots[6])
            return cslot1 + cslot2 + cslot3 + cslot4 + cslot5 + cslot6
        else:
            return len(self.slots[nr])

    def process(self, messages):

        self.starttime = micros()

        countmessages = len(messages) + self.getSlotEntries()
        logger.debug("init processing N:%s Q:%s",len(messages), self.getSlotEntries())
        abbruch = False

        # Sortieren der Nachrichten
        for message in messages:
            identifier = message[0]
            prio = self.gh.getPriority(identifier)
            queue = self.slots[prio]
            queue.append(message)

        cslot1 = self.getSlotEntries(1)
        cslot2 = self.getSlotEntries(2)
        cslot3 = self.getSlotEntries(3)
        cslot4 = self.getSlotEntries(4)
        cslot5 = self.getSlotEntries(5)
        cslot6 = self.getSlotEntries(6)

        logger.debug("start processing: cm:%s | sl1:%s sl2:%s sl3:%s sl4:%s sl5:%s sl6:%s ",countmessages,cslot1,cslot2,cslot3,cslot4,cslot5,cslot6)

        # Abarbeiten der Slots
        for i in range (1, 6):
            if self.processQueue(i) is None:
                abbruch = True

                cslot1 = self.getSlotEntries(1)
                cslot2 = self.getSlotEntries(2)
                cslot3 = self.getSlotEntries(3)
                cslot4 = self.getSlotEntries(4)
                cslot5 = self.getSlotEntries(5)
                cslot6 = self.getSlotEntries(6)


                processedmessages = countmessages - (cslot1 + cslot2 + cslot3 + cslot4 + cslot5 + cslot6)
                logger.debug("processing clear queues: %s#%s | s1:%s s2:%s s3:%s s4:%s s5:%s s6:%s ",processedmessages, countmessages ,cslot1,cslot2,cslot3,cslot4,cslot5,cslot6)
                for i in range (1, 6):
                    if i > 2: self.clearSlot(i)
                break
#            else:
#                pass

        cslot1 = self.getSlotEntries(1)
        cslot2 = self.getSlotEntries(2)
        cslot3 = self.getSlotEntries(3)
        cslot4 = self.getSlotEntries(4)
        cslot5 = self.getSlotEntries(5)
        cslot6 = self.getSlotEntries(6)

        if abbruch == True:
            logger.debug("end processing: <ABORT!> s1:%s s2:%s s3:%s s4:%s s5:%s s6:%s ",cslot1,cslot2,cslot3,cslot4,cslot5,cslot6)
        else:
            logger.debug("end processing: s1:%s s2:%s s3:%s s4:%s s5:%s s6:%s ",cslot1,cslot2,cslot3,cslot4,cslot5,cslot6)


    def update(self, *input):
        logger.debug("networkcontroller update event: " + str(input))
        if self.eventpublisher is not None:
            # event neu aufbauen:

            for item in input:

                # z.B. identifier = SPD
                #      wert = 2

                identifier = item[0]
                wert = item[1]

                if identifier is not None and wert is not None:

                    # der type ist an dieser STelle uninteressant.
                    # es handelt sich z.B. um ein fachlichen Wert (speed)
                    # egal welche Anzeigen das wie darstellen.
                    # type muss aus dem event raus.
                    # gh.getType benoetigt jetzt auch die ID
                    # nicht mehr den identifier

                    type = self.gh.getType(identifier)
                    event = Event(identifier=identifier)

                    if wert == ID_ON or wert == ID_OFF:
                        event.setType(type)
                        event.setAction(wert)
                    elif wert == ID_INCREASE or wert == ID_DECREASE:
                        event.setType(type)
                        event.setAction(wert)
                    else:
                        value = wert
                        event.setAction(LBL_UPDATE)
                        event.setValue(value)
                        event.setType(type)

                    message = event.getMessage()
                    self.eventpublisher.update(**message)

                if identifier == ID_SERVERNAME:
                    sn = self.ns.getServerName()
                    self.processcontroller.setValue(ID_SERVERNAME, sn)
                    logger.debug("set processcontroller with: %s%s", ID_SERVERNAME,sn)
                if identifier == ID_SERVERADR:
                    sa = self.ns.getServerAddress()
                    self.processcontroller.setValue(ID_SERVERADR, sa)
                    logger.debug("set processcontroller with: %s%s", ID_SERVERADR,sa)
                if identifier == ID_SERVERPORT:
                    port = self.ns.getServerPort()
                    self.processcontroller.setValue(ID_SERVERPORT, port)
                    logger.debug("set processcontroller with: %s%s", ID_SERVERPORT, port)
                if identifier == ID_CLIENTADR:
                    address = self.ns.getClientAddress()
                    self.processcontroller.setValue(ID_CLIENTADR, address)
                    logger.debug("set processcontroller with: %s%s", ID_CLIENTADR, address)
                if identifier == ID_CLIENTPORT:
                    port = self.ns.getClientPort()
                    self.processcontroller.setValue(ID_CLIENTPORT, port)
                    logger.debug("set processcontroller with: %s%s", ID_SERVERPORT, port)
#                if identifier == ID_FRAMERATE:
#                    fps = self.dash.getfps()
#                    self.processcontroller.setValue(ID_FRAMERATE, fps)
#                    logger.debug("set processcontroller with: %s%s", ID_FRAMERATE, fps)
#                if identifier == ID_LOGLEVEL:
#                    level = self.dash.getloglevel()
#                    self.processcontroller.setValue(ID_LOGLEVEL, level)
#                    logger.debug("set processcontroller with: %s%s", ID_LOGLEVEL, level)

        else:
            logger.error("register datapublisher")


    def destroy(self):
        # hier muss ein quit ueber den socket geschickt werden,
        # der der thread sich ansonsten nicht korrekt beendet.

        nsc = NetworkClient("localhost", self.port)
        nsc.connectServer()
        time.sleep(1)

        logger.debug("sending NetworkServer quit")
        nsc.send(ID_QUIT,False)
        nsc.stop()



