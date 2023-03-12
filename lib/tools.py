__author__ = 'JK'

#import settings

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