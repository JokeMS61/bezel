import pickle
from timing import *
from settings import *
from basis import Basis
import atexit
import tools

class DataStorage(Basis):
    def __init__(self):
        Basis._init__(self)
        self.storage = {}
        self.status = {}
        self.defaults = {}
        self.unitformat = {}
        self.printformat = {}
        self.title = {}
        self.lastEntries = {}
        self.entries = {}
        self.EntryCount = 0
        self.lastkeys = []
        self.startingTime = None

        self.readconfiguration("data")

        conf = self.getConfigurationDict()
        if ID_GENERAL in conf:
            if ID_STORAGESIZE in conf[ID_GENERAL]:
                self.MAX_STORAGE_SIZE = conf[ID_GENERAL][ID_STORAGESIZE]
            else:
                self.MAX_STORAGE_SIZE = 50000
            if ID_LASTENTRIES in conf[ID_GENERAL]:
                self.LAST_ENTRIES_COUNT = conf[ID_GENERAL][ID_LASTENTRIES]
            else:
                self.LAST_ENTRIES_COUNT = 2

        self.initStorage()
        atexit.register(self.cleanup)
        #self.printStorage()

    def cleanup(self):
        logger.debug("cleanup called")
        self.saveStorage()
        #self.printStorage()

    def getStatusList(self):
        return self.status

    def saveStorage(self):
        filename = g_data + self.storageFilename + ".bin"
        outfile = open(filename, "wb")
        pickle.dump(self.storage, outfile)
        outfile.close()

        if logger.getEffectiveLevel() == logging.DEBUG:
            self.printStorage(file=self.storageFilename, storage=self.storage)

    def readLastStorage(self):
        # letzten File lesen
        verzeichnis = os.listdir(g_data)
        verzeichnis.sort(reverse=True)
        if len(verzeichnis) > 0:
            file = verzeichnis[0]
            infile = open(g_data + file,"rb")
            storage = pickle.load(infile)
            logger.debug("read storage %s", file)
#            if storage is not None:
#                self.printStorage(storage)
            return storage
        else:
            logger.info("no storagefile in directory %s", g_data)
            return None


    def getCountIdentifier(self):
        erg = 0
        for key in self.defaults:
            erg = erg + 1
        return erg

    def getSortedIdentifier(self):
        actualposition = 0
        nextIdentifier = ID_STORAGETIME
        differenz = 1
        count = 0
        value = 0
        positions = []
        positions.append(ID_STORAGETIME)
        runden = self.getCountIdentifier()

        for x in range(1,runden):
            for key in self.defaults:
                value = self.defaults[key][ID_POSITION]
                if value > actualposition:
                    count = count + 1
                    newdifferenz = value - actualposition
                    if count == 1:
                        differenz = newdifferenz
                        nextIdentifier = key
                    else:
                        if newdifferenz < (differenz):
                            differenz = newdifferenz
                            nextIdentifier = key
                        else:
                            # do nothing
                            pass
            count = 0
            actualposition = differenz + actualposition
            positions.append(nextIdentifier)

        return positions

    def printStorage(self,storage = None, file = None):
        titles = []

        if storage is None and self.storage is not None:
            pstorage = self.storage
        else:
            pstorage = storage

        if pstorage is not None:
            if len(pstorage) > 0:

                outfile = None
                if file is not None:
                    filename = g_log + self.storageFilename + ".log"
                    outfile = open(filename, "w")

                #for key in self.defaults:
                #    value = self.defaults[key][ID_POSITION]
                #    print "unsorted position %s: %s", value, key

                # positionen sortieren
                positions = self.getSortedIdentifier()
                #for x in range(0,len(positions)):
                #    print "position %s: ", x, positions[x]

                # Ueberschrift
                formatstring = "{p[0]" + self.defaults[positions[0]][ID_TITLEFORMAT] + "}"
                titles.append(self.defaults[positions[0]][ID_TITLE])
                for x in range(1,len(positions)):
                    formatstring = formatstring + " | " + "{p[" + str(int(x)) + "]" + self.defaults[positions[x]][ID_TITLEFORMAT] + "}"
                    titles.append(self.defaults[positions[x]][ID_TITLE])

                outstring = formatstring.format(p=titles)

                if outfile is not None:
                    outfile.write(outstring+"\n")
                else:
                    print (outstring)

                storekeys = list(pstorage.keys())
                storekeys.sort()

                for x in range(0,len(storekeys)):
                    key = storekeys[x]
                    values = pstorage[key]
                    timekey = tools.getTimeKey(key)

                    entries = []
                    entries.append(timekey)
                    for x in range(1,len(positions)):
                        unitformat = "{" + self.defaults[positions[x]][ID_VALUEFORMAT] + "}"
                        storevalue = values[positions[x]]
                        value = unitformat.format(storevalue)
                        entries.append(str(value))

                    outstring = formatstring.format(p=entries)
                    if outfile is not None:
                        outfile.write(outstring+"\n")
                    else:
                        print (outstring)

                if outfile is not None:
                    outfile.close()


            else:
                logger.warning("no entries in storage")
        else:
            logger.warning("no storage to print !")

    def getStorage(self):
        return self.storage


    def getEntryCount(self):
        return int(self.EntryCount)

    def getLastValue(self,key):
        if key in self.lastEntries:
            return self.lastEntries[key]

    def getLastEntries(self, count):

        anzahlkeys = len(self.lastkeys)
        if anzahlkeys >= count:
            liste = {}
            i = 1
            while i <= count:
                timekey = self.lastkeys[anzahlkeys - i]
                self.storage[timekey][ID_STORAGETIME] = timekey
                liste[timekey] = dict(self.storage[timekey])
                i = i + 1
            return liste
        else:
            return None

    def reinitializeStorage(self):
        start = micros()
        self.saveStorage()
        end = micros()
        logger.debug("storetime=", (end-start), " (microseconds) for " ,  self.getEntryCount() , " entries")
        self.initStorage()

    def insertLastEntries(self, identifier, value):

        #notwendige datenstruktur fuer storageinitialisierung
        self.lastEntries[identifier] = value

    def saveValue (self, param, value, microseconds=None):


        if microseconds is None:
            microseconds = micros() - self.startingTime
            self.EntryCount = self.EntryCount + 1
            self.lastkeys.append(microseconds)
            if len(self.lastkeys) > int(self.LAST_ENTRIES_COUNT):
                self.lastkeys.pop(0)

        # immer die letzten Werte speichern
        self.insertLastEntries(param, value)


        entry = dict(self.lastEntries)
        self.storage[microseconds] = entry

    def setStatus(self, identifier=None, deliver=False, value = None):
        if identifier is not None:
            if identifier in self.status:
                list = self.status[identifier]
                list['todeliver'] = deliver
                list['lastvalue'] = value
            else:
                list = {}
                list['todeliver'] = deliver
                list['lastvalue']  = value
                self.status[identifier] = list

            logger.debug("Statuslist: %s", self.status)

    def saveEntry(self, param, value, time=None):

        entries = self.getEntryCount()
        maxentries = int(self.MAX_STORAGE_SIZE)
        logger.debug("param: %s, value: %s, time: %s, entries: %s, maxentries: %s", param, value, time, entries, maxentries)

        if  entries  > maxentries:
            self.reinitializeStorage()

        self.saveValue(param, value, time)
        self.setStatus(identifier=param, deliver=True, value=value)


    def initStorage(self):
        self.storage = {}
        self.EntryCount = 0
        starttime = getLocalTime()
        self.storageFilename = getTimeStamp(starttime)
        self.startingTime = micros()

        # storage werte vorbelegen
        for key in self.defaults:
            value = self.defaults[key][ID_INITIAL]
            if value == "storage":
                # ist der wert noch im speicher ?
                if key in self.status:
                    if "lastvalue" in self.status[key]:
                        self.defaults[key][ID_INITIAL] = self.status[key]['lastvalue']
                        logger.info("initialize %s to %s from memory", key, self.status[key]['lastvalue'])
                else:
                    # vom letzten Storage auf Platte lesen
                    # den inhalt der lokalen variable storage zuweisen
                    storage = self.readLastStorage()
                    if storage is not None:
                        # den letzte gespeicherten Wert auslesen
                        timestamps = list(storage.keys())
                        timestamps.sort()
                        timestamps.reverse()

                        for timestamp in timestamps:
                            entry = storage[timestamp]
                            if key in entry:
                                # einen wert gefunden
                                self.defaults[key][ID_INITIAL] = entry[key]
                                logger.info("initalize %s with %s", key, entry[key])
                                break
                    else:
                        # wenn jetzt der wert immer noch storage heisst,
                        # dann wurde dieser bisher nie gespeichert. auf 0 setzen.
                        if self.defaults[key][ID_INITIAL] == "storage":
                            logger.info("no values for %s in last storage", key)
                            logger.info("initialize %s to zero", key)
                            self.defaults[key][ID_INITIAL] = 0
            else:
                # nur als Zahl formatieren, da in defaults ja
                # dann bereits die gueltige werte drinstehen
                self.defaults[key][ID_INITIAL] = float (self.defaults[key][ID_INITIAL])

        for key in self.defaults:
            entry = dict(self.defaults[key])
            value = None

            if ID_INITIAL in entry:
                value = entry[ID_INITIAL]
            if value is not None:
                self.lastEntries[key] = value
            else:
                self.lastEntries[key] = 0

            if key in self.status:
                entry = self.status[key]
            else:
                entry = {}

            entry[ID_LASTVALUE] = value
            entry[ID_TODELIVER] = True
            self.status[key] = entry


        logger.debug("initial lastEntries: %s", self.lastEntries)

        firstentry = micros() - self.startingTime
        entries = {}
        for key in self.lastEntries:
            entries[key] = self.lastEntries[key]

        self.storage[firstentry] = entries
        self.EntryCount = 1

        logger.debug("initial storage: %s", self.storage)

    def registerConfiguration(self, section, label, value):
        # TODO
        # type (Grafik oder Text)
        if section == "init":

            # 1. Initialwert (value / storage)
            # 2. Position bei der Ausgabe
            # 3. Formatierung als Value
            # 4. Formatierung der Ueberschrift
            # 5. Ueberschrift

            entry = value.split(",")
            daten = {}

            daten[ID_INITIAL] = entry[0]
            daten[ID_POSITION] = int(entry[1])
            daten[ID_VALUEFORMAT] = entry[2]
            daten[ID_TITLEFORMAT] = entry[3]
            daten[ID_TITLE] = entry[4]

            self.defaults[label] = daten

        if section == "general":
            if label == ID_STORAGETIME:
                entry = value.split(",")
                daten = {}

                daten[ID_INITIAL] = entry[0]
                daten[ID_POSITION] = int(entry[1])
                daten[ID_VALUEFORMAT] = entry[2]
                daten[ID_TITLEFORMAT] = entry[3]
                daten[ID_TITLE] = entry[4]

                self.defaults[label] = daten


