__author__ = 'JK'

from settings import *

class gaugeHelper():
    def __init__(self, gauges):
        self.gauges = gauges
        self.groups = []
        self.gaugedata = {}

        for gauge in self.gauges:
            # allgemeine gauge Daten
            id = gauge.getId()
            entry = {}
            entry ["type"] = gauge.getType()
            entry ["prio"] = gauge.getPrio()
            entry ["identifier"] = gauge.getIdentifier()
            self.gaugedata[id] = entry

            # groupdata zusammenstellen
            group = gauge.getGroup()
            if not group in self.getGroups():
                logger.debug("append group %s",group)
                self.groups.append(group)

        logger.debug("Gaugehelper init ---------------------------------------")
        for gauge in self.gauges:
            # allgemeine gauge Daten
            id = gauge.getId()
            identifier = gauge.getIdentifier()
            type = gauge.getType()

            logger.debug("id: %s \t identifier: %s \t type: %s \t", id, identifier, type)


    def getGroup(self,key):
        for group in self.groups:
            if group == key:
                return group
        return None

    def getGroups(self):
        return self.groups

    def getPriority(self, id):
        if id in self.gaugedata:
            prio = int(self.gaugedata[id]["prio"])
        else:
            prio = 2
        return prio

    def getType(self, id):

#        logger.debug("get type from identifier %s ",identifier)
        group = self.getGroup(id)
        if group is not None:
#            logger.debug("identifier in group found.return type=group")
            return LBL_GROUP
        else:
            if id in self.gaugedata:
                type = self.gaugedata[id]["type"]
                return type

#            for gauge in self.gauges:
#                ident = gauge.getIdentifier()
#                if identifier in ident:
#                    type = gauge.getType()
#                    logger.debug("identifier in gauge found. return type=gauge")
#                    return type

        if id in idlist:
            return idlist[id]

        logger.error("can't get type from identifier %s", id)
        return None

    def getIdentifierType(self, identifier):
        return

    def getGauge(self, group, index):
        for gauge in self.gauges:
            gaugegroup = gauge.getGroup()
            if gaugegroup == group:
                position = gauge.getPosition()
                if position == index:
                    gaugeId = gauge.getId()
                    return gaugeId
        return None

    def getGaugeReference(self, id):
        for gauge in self.gauges:
            gaugeId = gauge.getId()
            if gaugeId == id:
                return gauge
        return None

    def getNextGaugePosition(self, group, index):

        def getkey(item):
            return item[0]

        logger.debug("function called with group=%s, index=%s", group, index)
        gauges = []
        # 1.Pruefung: sind groups vorhanden ?
        count = len(self.groups)
        logger.debug("count entries in groups = %s", count)
        if count > 0:
            # 2. Pruefung: gibt es die uebergebene group ?
            for item in self.groups:
                if item == group:
                    logger.debug("group %s found", group)
                    startposition = index
                    countGauges = 0
                    # 3. Pruefung: wieviel Anzeigen gibt es in der gruppe ?
                    for gauge in self.gauges:
                        gaugeGroup = gauge.getGroup()
                        if gaugeGroup == group:
                            countGauges += 1
                            position = gauge.getPosition()
                            gaugeId = gauge.getId()

                            gauges.append((position, gaugeId))
                            logger.debug("gauge %s in group %s on position %s", gaugeId, group, position)

                    logger.debug("complete %s gauges in group %s", countGauges, group)
                    if len(gauges) == 1:
                        pos, id = gauges[0]
                        logger.debug("1 gauge %s on pos %s in group %s", id, pos, group)
                        return pos
                    elif len(gauges) > 1:
                        sorted(gauges, key=getkey)
                        logger.debug("gauge field sorted")
                        pos = 1
                        for gauge in gauges:
                            logger.debug("gauge %s: pos=%s, id=%s", pos, gauge[0], gauge[1])
                            if gauge[0] == index:
                                logger.debug("gauge found with actual index. pos=%s, id=%s", gauge[0], gauge[1])
                                if pos >= 1 and pos < len(gauges):
                                    ret = gauges[pos]
                                    logger.debug("return next gauge at position %s, id=%s", ret[0], ret[1])
                                    return ret[0]
                                else:
                                    # den ersten Eintrag zurueckliefern
                                    ret = gauges[0]
                                    logger.debug("return first gauge. pos=%s, id=%s", ret[0], ret[1] )
                                    return ret[0]
                            pos += 1
                    logger.warning("no gauge in requested group. request useless")
                    return None
            logger.warning("requested group not found. request useless")
            return None
        else:
            logger.Warning("no groups defined. request useless")
            return None


    def getVisibleGauge(self,group):
        for gauge in self.gauges:
            gaugeGroup = gauge.getGroup()
            gaugeVisible = gauge.getVisible()
            gaugePosition = gauge.getPosition()
            logger.debug("search in gauges for group %s, (group=%s, position=%s, visible=%s)", group,gaugeGroup,gaugePosition,gaugeVisible )
            if gaugeVisible and gaugeGroup == group:
                return gaugePosition
        return None

    def displayGauge(self, group, oldIndex, newIndex):
        logger.debug("change gauge. group=%s, oldindex=%s, newindex=%s", group, oldIndex, newIndex)
        if newIndex != oldIndex:
            gaugeold = self.getGauge(group, oldIndex)
            gaugenew = self.getGauge(group, newIndex)
            return {"group": group, "old" : gaugeold, "new" : gaugenew}

    def getNextVisibleGauge(self, group, direction):
        # welche Anzeige ist zur Zeit sichtbar ?
        logger.debug("function called. group=%s, direction=%s", group, direction)
        actualIndex = self.getVisibleGauge(group)
        logger.debug("actual index in group: %s",actualIndex)
        if actualIndex:
            newIndex = self.getNextGaugePosition(group, actualIndex)
            logger.debug("newindex:%s",newIndex)
            if newIndex:
                # sichtbare gauge in der group gefunden
                ret = self.displayGauge (group, actualIndex, newIndex)
                return ret
            else:
                return None
