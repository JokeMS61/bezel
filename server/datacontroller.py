from settings import *
from datastorage import DataStorage
from basis import Basis

class DataController(Basis):
    def __init__(self, observer=None):
        Basis._init__(self)
        self.functions = {}
        self.dependencies = {}
        self.observers = observer
        self.readconfiguration("data")
        self.ds = DataStorage()

    def digital(self,**parms):
        identifier = parms[LBL_IDENTIFIER]
        value = int(parms[LBL_VALUE])
        logger.debug("function digital called. identifier, parameter: %s,%s", identifier, value)

        if value == 1 or value == 0:
            self.ds.saveEntry(identifier, value)
            return value
        else:
            return None

    def analog(self,**parms):
        identifier = parms[LBL_IDENTIFIER]
        value = float(parms[LBL_VALUE])
        logger.debug("function analog called. identifier, parameter: %s,%s", identifier, value)

        if value < -99999999999 or value > +99999999999:
            return None
        else:
            self.ds.saveEntry(identifier, value)
            return value

    def copy(self, **parms):
        identifier = parms[LBL_IDENTIFIER]
        valueid = parms[LBL_PARAM0]
        if identifier is not None and valueid is not None:
            values = self.ds.getLastEntries(1)
            if values is not None:
                storetime = list(values.keys())

                value = float(values[storetime[0]][valueid])
                logger.debug("new value for identifier %s: %s", identifier, value)
                self.ds.saveEntry(identifier, value, storetime[0])

    def gradient(self, **parms):

        logger.debug("function gradient called. parameter: %s",parms)

        identifier = parms[LBL_IDENTIFIER]
        xvalueid = parms[LBL_PARAM0]
        yvalueid = parms[LBL_PARAM1]
        factor = parms[LBL_PARAM2]

        if identifier is not None and xvalueid is not None and yvalueid is not None and factor is not None:
            values = self.ds.getLastEntries(2)
            if values is not None:
                storetimes = list(values.keys())
                #storetimes.sort(reverse=True)

                v1 = float(values[storetimes[0]][xvalueid])
                v2 = float(values[storetimes[1]][xvalueid])

                t1 = float(values[storetimes[0]][yvalueid])
                t2 = float(values[storetimes[1]][yvalueid])

                dv = v1 - v2
                dt = t1 - t2

                if dv is not 0:
                    value = float((dv / dt) * float(factor))
                    logger.debug("new value for identifier %s: %s", identifier, value)
                    self.ds.saveEntry(identifier, value, storetimes[0])

    def proportion (self, **parms):
        logger.debug("function proportion called. parameter: %s",parms)

        identifier = parms[LBL_IDENTIFIER]
        xvalueid = parms[LBL_PARAM0]
        yvalueid = parms[LBL_PARAM1]
        factorx = parms[LBL_PARAM2]
        factory = parms[LBL_PARAM3]
        flag = parms[LBL_PARAM4]

        logger.debug("identifier: %s", identifier)
        logger.debug("xvalueid: %s", xvalueid)
        logger.debug("yvalueid: %s", yvalueid)
        logger.debug("factorx: %s", factorx)
        logger.debug("factory: %s", factory)
        logger.debug("flag: %s", flag)

        if identifier is not None and xvalueid is not None and yvalueid is not None and flag is not None:
            values = self.ds.getLastEntries(2)
            logger.debug("values: %s", values)

            if values is not None:
                storetimes = list(values.keys())
                #storetimes.sort(reverse=True)

                v1 = float(values[storetimes[0]][xvalueid])
                v2 = float(values[storetimes[1]][xvalueid])
                vm = float(((v1+v2)/2) * float(factorx))

                t1 = float(values[storetimes[0]][yvalueid])
                t2 = float(values[storetimes[1]][yvalueid])
                dt = float(t1-t2) # microsekunden

                # zurueckgelegte distanz im Metern:
                difference = float((vm * dt) / float(factory))
                entry = self.ds.getLastEntries(1)
                value = difference

                logger.debug("v1: %s", v1)
                logger.debug("v2: %s", v2)
                logger.debug("vm: %s", vm)
                logger.debug("t1: %s", t1)
                logger.debug("t2: %s", t2)
                logger.debug("dt: %s", dt)
                logger.debug("difference: %s", difference)
                logger.debug("value: %s", value)

                if entry is not None:
                    storetime = list(entry.keys())
                    value = entry[storetime[0]][identifier] + difference
                    self.ds.saveEntry(identifier, value, storetimes[0])
                else:
                    self.ds.saveEntry(identifier, value, storetimes[0])

                logger.debug("new value for identifier %s: %s", identifier, value)

    def getStatusList(self):
        return self.ds.getStatusList()

    def getValueFromGauge(self, identifier):
        if self.observers is not None:
            if len(self.observers) > 0:
                for observer in self.observers:
                    entries = observer.getIdentifier()
                    if entries is not None:
                        if identifier in entries:
                            return observer.getValue(identifier)
                    else:
                        logger.error("entries from observer.getIdentifier is None")

    def getParameter(self,identifier, value=None):

        """
        :rtype : dict
        """
        if self.functions is not None:
            parameter = self.functions[identifier][ID_PARAMETER]

            parameterliste = {}
            parameterliste[LBL_IDENTIFIER]  = identifier
            if value is not None:
                parameterliste[LBL_VALUE]  = value

            if parameter is not None:
                anzahlparameter = len(parameter)
                if anzahlparameter > 0:
                    for x in range(0, anzahlparameter):
                        parameterliste[str(x)] = parameter[x]

            return parameterliste
        else:
            return None

    def processfactory (self, identifier, value=None, action=None):

        if action is not None:
            logger.debug("action = %s", action)
            newvalue = 0

            if action in ["on", "off"]:
                if action == "on":
                    newvalue = 1
                if action == "off":
                    newvalue = 0

            elif action in ["increase", "decrease"]:
                lastvalue = self.ds.getLastValue(identifier)
                if lastvalue is None:
                    lastvalue = self.getValueFromGauge(identifier)

                if action == "increase":
                    newvalue = int(lastvalue) + 1
                if action == "decrease":
                    newvalue = int (lastvalue) - 1

            elif action in ["update"]:
                newvalue = value


            parameterliste = self.getParameter(identifier, newvalue)
            function = self.functions[identifier][ID_FUNCTION]
            if function is not None:
                value = function(**parameterliste)

                # Nachbearbeitung, abhaengige Funktionen ausfuehren
                if identifier in self.dependencies:
                    newidentifier =  self.dependencies[identifier]
                    lst = newidentifier.split(",")

                    for x in range(0, len(lst)):
                        ident = lst[x]
                        function = self.functions[ident][ID_FUNCTION]
                        parameterliste = self.getParameter(ident)
                        value = function(**parameterliste)

    def printStorage(self):
        self.ds.printStorage()

    def registerConfiguration(self, section, label, entry):
        if section == "process":
            data = {}
            values = entry.split(",")
            parms = len(values)

            function = values[0]
            if function == ID_DIGITAL:
                data[ID_FUNCTION] = self.digital
            elif function == ID_ANALOG:
                data[ID_FUNCTION] = self.analog
            elif function == ID_GRADIENT:
                data[ID_FUNCTION] = self.gradient
            elif function == ID_PROPORTION:
                data[ID_FUNCTION] = self.proportion
            elif function == ID_COPY:
                data[ID_FUNCTION] = self.copy

            if parms > 1:
                parameter = list(values[1:parms])
            else:
                parameter = None
            data[ID_PARAMETER] = parameter

            self.functions[label] = data

        if section == "dependencies":
            self.dependencies[label] = entry

