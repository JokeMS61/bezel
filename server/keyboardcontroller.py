__author__ = 'Jo'

import pygame
from event import Event
from settings import *
from basis import Basis
from keyhelper import Keyhelper
from operator import itemgetter


class keyboardController(Basis):
    def __init__(self):
        Basis._init__(self)
        self.eventpublisher = None  # subscriber
        self.keys = {}
        self.modtaste =""
        self.readconfiguration("keyboard")
        kh = Keyhelper()
        kh.printKeyInfo()
        logger.debug("self.keys: %s", self.keys)

    def registerConfiguration(self, section, label, value):
        #values = section.split(",")
        #t1 = (values)

        logger.debug("value: %s", value)
        #logger.debug("t1: %s", t1)

        #t2 = tuple(i for i in values)
        if section in self.keys:
            entry = self.keys[section]
        else:
            entry = {}

        entry[label] = value
        self.keys[section] = entry


    def register(self, publisher):
        logger.debug("keyboardPublisher register called")
        self.eventpublisher = publisher

    def unregister(self, gaugeObj):
        self.eventpublisher = None

    def notify(self, event):
        logger.debug("event: " + str(event))
        if self.eventpublisher is not None:
            self.eventpublisher.update(**event)
        else:
            logger.error("register datapublisher")

    def getpressedKeys(self, keys):
        key_indexes = []
        index = 0

        for value in keys:
            if value:
                key_indexes.append(index)
            index += 1

        if len(key_indexes) > 0:
            if len(key_indexes) > 1:
                value = tuple(sorted(key_indexes,reverse=True))
                return value
            return tuple(key_indexes)
        else:
            return None

    def getEntry(self, tasten):
        logger.debug("tastenvergleich mit %s",tasten)

        i=1
        for entry in self.keys:
            logger.debug("Eintrag in self.keys Nummer %s",i)
            logger.debug("key: %s, Eintrag: %s",entry, self.keys[entry])
            i = i+1


        if tasten in self.keys:
            # Tastenkombination ist ein predefined shortcut
            entry = self.keys[tasten]
            # alle entries zu dem shortcut laden
            # und event anlegen
            event = Event()
            for label in entry.keys():
                # event aufbauen
                if label in ["identifier"]:
                    value = entry["identifier"]
                    event.setIdentifier(value)
                if label in ["on", "off", "increase", "decrease"]:
                    event.setAction(label)
                if label in ["type"]:
                    value = entry["type"]
                    event.setType(value)
                if label in ["value"]:
                    value = entry["value"]
                    event.setValue(value)
            #logger.debug("Eintrag gefunden. entry=%s", entry)
            return event.getMessage()
        #logger.debug("key don't match any entry")
        return None

    def switch(self,mod):

        if mod != pygame.KMOD_NONE:
            if mod & pygame.KMOD_LSHIFT:
                return  "left shift"
            elif mod & pygame.KMOD_RSHIFT:
                return "right shift"
            elif mod & pygame.KMOD_LCTRL:
                return "left ctrl"
            elif mod & pygame.KMOD_RCTRL:
                return "right ctrl"
            elif mod & pygame.KMOD_LALT:
                return "left alt"
            elif mod & pygame.KMOD_RALT:
                return "right alt"
        else:
            return None

    def validatevalue(self, event=None):

        #mod = event.mod
        mod = pygame.key.get_mods()
        taste = event.key

        modtaste = self.switch(mod)
        # hier liegen die scancodes der tasten bereits vor.
        logger.debug ("modtaste: %s, tastename: %s",modtaste, pygame.key.name(taste))

        if taste != None:
            if  modtaste != None:
                keys = modtaste + pygame.key.name(taste)
            else:
                keys = pygame.key.name(taste)

        action = self.getEntry(keys)
        logger.debug("action: %s", action)
        if action:
            self.notify(action)

