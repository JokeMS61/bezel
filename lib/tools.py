__author__ = 'JK'
from settings import *

# 1. make these parameter configure
# Message_Prefix = "@"
# Message_Postfix = "#"
# Message_Length = 13
# Message_FillChar = "_"
# Message_ValueLength = 20
# Message_IDLength = 3
# MAX_PROCESSTIME = 25000

def toBoolean( val ):
    """
    Get the boolean value of the provided input.

        If the value is a boolean return the value.
        Otherwise check to see if the value is in
        ["false", "f", "no", "n", "none", "0", "[]", "{}", "" ]
        and returns True if value is not in the list
    """

    if val is True or val is False:
        return val

    falseItems = ["false", "f", "no", "n", "none", "0", "[]", "{}", "" ]

    return not str( val ).strip().lower() in falseItems

def formatMessageContent(id, value):
    val = str(value)

    if val != None:
        if len(val) > Message_ValueLength:
            logger.error("Value in Message too long: %s", val)
            return None
        else:
            val.rjust(Message_ValueLength,Message_FillChar)

        if len(id) > Message_IDLength:
            logger.error("ID in Message too long: %s", id)
            return None
        else:
            id.rjust(Message_IDLength,Message_FillChar)
        rc = Message_Prefix + id + val + Message_Postfix
        return rc.encode("UTF-8")
    else:
        logger.error("vo valid value (id = %s)", id)

def getTimeKey( diff ):
    # die funktion macht aus einem Wert "microsekunden"
    # einen timestamp, um diesen dann spaeter im dump
    # ausgeben zu koennen.
    # diff in seconds:
    microseconds = int(diff)
    milliseconds = int(microseconds / 1000)
    seconds = int(milliseconds / 1000)

    diffhours = 0
    diffminutes = 0
    diffseconds = 0
    diffmilliseconds = 0
    diffmicroseconds = 0

    if microseconds > 0:
        diffmicroseconds = microseconds
    if milliseconds > 0:
        diffmicroseconds = microseconds - (milliseconds * 1000)
        diffmilliseconds = milliseconds
        if seconds > 0:
            diffmilliseconds = milliseconds - (seconds * 1000)
            diffminutes = int(seconds / 60)
            if diffminutes > 0:
                diffseconds = seconds - (diffminutes * 60)
                if diffminutes > 60:
                    diffhours = int(diffminutes / 60)
                    diffminutes = diffminutes - (diffhours * 60)
            else:
                diffseconds = seconds

    key = "{:03d}:{:02d}:{:02d}:{:03d}.{:03d}".format(diffhours,diffminutes,diffseconds,diffmilliseconds,diffmicroseconds)
    return key