__author__ = 'JK'

from settings import *
import configparser
import codecs


class Basis(object):
    def _init__(self):
        self.configurationdict = {}

    def registerConfiguration(self, section, label, value):
        pass

    def getConfigurationDict(self):
        return self.configurationdict

    def loadConfiguration(self,file):
        configfile = g_configuration + file + ".cfg"
        logger.debug("load configuration %s", configfile)

        cfgfile = codecs.open(configfile, "rU", encoding='utf-8')
        # read content to the file
        config = configparser.ConfigParser()

        # folgende Option ist wichtig, sonst werden die keys nur
        # als kleinbuchstaben eingelesen. siehe auch:
        # https://stackoverflow.com/questions/1611799/preserve-case-in-configparser
        config.optionxform = str

        config.read_file(cfgfile)
        cfgfile.close()
        return config

    def getDictSection(self,key):
        if key in self.configurationdict:
            return True
        else:
            return False

    def getDictEntry(self,section,key):
        if section in self.configurationdict:
            if key in self.configurationdict[section]:
                return self.configurationdict[section][key]
            else:
                return False
        else:
            return False

    def readconfiguration(self,file):
        config = self.loadConfiguration(file)
        sections = config.sections()
        for x in range(0,len(sections)):
            sectionname = sections[x]
            sectionvalues = config.items(sectionname)
            entries = {}
            for label, value in sectionvalues:
                self.registerConfiguration(sectionname, label,value)
                entries[label] = value
            self.configurationdict[sectionname] = entries
