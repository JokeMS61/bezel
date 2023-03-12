__author__ = 'JK'
from settings import *
from datacontroller import DataController

class EventPublisher():
    def __init__(self):
        self.observers = []  # subscriber
        self.data = {}
        self.dc = DataController(self.observers)

    def register(self, dash):

        logger.debug("DataPublisher register called")
        self.observers.append(dash)
        boards = dash.getboards()
        for board in boards:
            self.observers.append(board)
            gauges = board.getGauges()
            for observer in gauges:
                if not observer in self.observers:
                    logger.debug("append observer. Gauge %s", observer.getId())
                    self.observers.append(observer)

    def unregister(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def unregister_all(self):
        if self.observers:
            del self.observers[:]

    def setNewValue(self,identifier, value):
        if identifier in self.data:
            entry = self.data[identifier]
            entry["value"] = value

    def getOldValue(self, identifier):

        if identifier in self.data:
            entry = self.data[identifier]
            oldvalue = entry["value"]
            #logger.debug("identifier in memory")
        else:
            # neuen Eintrag anlegen mit einem Defaultwert
            entry = {}
            oldvalue = 0
            entry["value"] = oldvalue
            self.data[identifier] = entry
            #logger.debug("identifier not in memory. ")
        return oldvalue

    def deliverEvent(self, identifier, event):
        logger.debug("event for board.")
        for observer in self.observers:
            entries = observer.getIdentifier()
            if entries is not None:
                if identifier in entries:
                    observer.update(**event)
            else:
                logger.error("entries from observer.getIdentifier is None")


    def deliverValue(self,identifier, value):
        logger.debug("set new value = %s for identifier = %s", value, identifier)

        for observer in self.observers:
            entries = observer.getIdentifier()
            if entries is not None:
                if identifier in entries:
                    logger.debug("call oberver (%s,%s) with id=%s and value=%s", observer.getId(), observer.getIdentifier(), identifier, value)
                    observer.setValue(identifier, value)
            else:
                logger.error("entries from observer.getIdentifier is None")

    def deliverValues(self):
        list = self.dc.getStatusList()

        for key in list:
            if list[key][ID_TODELIVER] == True:
                value = list[key][ID_LASTVALUE]
                self.deliverValue(key,value)
                list[key][ID_TODELIVER] = False

    def update(self, **event):

        # -------------------------------------------------------------------
        # event kan aus folgenden elementen bestehen:
        # identifier    (muss). entspricht den in settings definierten ID's
        # type          (muss). "signal" , "gauge" oder "board"
        # action        (muss). "on", "off", "increase", "decrease", "update"
        # value         (kann). wert. wird bei action=update uebernommen
        # -------------------------------------------------------------------

        logger.debug("event: %s", event)
        if event is not None:

            identifier = event[LBL_IDENTIFIER]
            type = event[LBL_TYPE]
            action = event[LBL_ACTION]
            newvalue = event[LBL_VALUE]

            if identifier is not None:
                logger.debug("event for identifier %s", identifier)

                if type in gaugetypes:
                    # self.dc.process_old(identifier, newvalue, action)
                    self.dc.processfactory(identifier, newvalue, action)
                    self.deliverValues()

                else:
                    self.deliverEvent(identifier, event)
