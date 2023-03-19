__author__ = 'JK'

import logging

#global logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s (%(module)s,%(funcName)s) : %(message)s')

fh = logging.FileHandler('../log/log.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

g_pictures = "../pic/"
g_configuration = "../cfg/"
g_sounds = "../snd/"
g_log = "../log/"
g_data = "../data/"
g_sim = "../sim/"

GMODE_DIRECT = 'direct'
GMODE_LAYER = 'layer'

LOGLEVEL_DEBUG = 'DEBUG'
LOGLEVEL_INFO = 'INFO'
LOGLEVEL_WARNING = 'WARNING'
LOGLEVEL_ERROR = 'ERROR'
LOGLEVEL_CRITICAL = 'CRITICAL'
LOGLEVEL_NOTSET = 'NOTSET'

LBL_PARAM0 = "0"
LBL_PARAM1 = "1"
LBL_PARAM2 = "2"
LBL_PARAM3 = "3"
LBL_PARAM4 = "4"
LBL_IDENTIFIER = 'identifier'
LBL_TYPE = 'type'
LBL_ACTION = 'action'
LBL_PRIO = 'prio'
LBL_VALUE = 'value'
LBL_UPDATE = 'update'
LBL_GAUGE = 'gauge'
LBL_SIGNAL = 'signal'
LBL_CHART = 'chart'
LBL_GROUP = 'group'
LBL_BOARD = 'board'
LBL_APP = 'app'

# identifier
'''
ID_LOGLEVEL = 'loglevel'
ID_INNERDASH = 'innerdash'
ID_QUIT = 'quit'
ID_STORAGE = 'general'
ID_SPEED = 'speed'
ID_ACCE = 'acceleration'
ID_TEMPW = 'tempw'
ID_TEMPO = 'tempo'
ID_DRIVE = 'rpm'
ID_BLINKR = 'blinkright'
ID_BLINKL = 'blinkleft'
ID_GAS = 'gas'
ID_MILEAGE = 'mileage'
ID_HIGHBEAM = 'highbeam'
ID_LOWBEAM = 'lowbeam'
ID_PREHEAT = 'preheat'
ID_CRUISECONTROL = 'cruisec'
ID_STARTSTOP = 'startstop'
ID_FOGLIGHT = 'foglight'
ID_TEMPSIG = 'tempsig'
ID_BATTERY = 'battery'
ID_ENGINE = 'engine'
ID_OILPRESSURE = 'oilpressure'
ID_BRAKE = 'brake'
ID_DPF = 'dpf'
ID_WATER='water'
ID_MAINTANCE = 'maintance'
ID_ABS = 'abs'
ID_ESP = 'esp'
ID_STEERING = 'steering'
ID_REST = 'rest'
ID_PARKLIGHT = 'parklight'
ID_SEATBELT = 'seatbelt'
ID_DOOR = 'door'
ID_AIRBAG = 'airbag'
ID_WIPER = 'wiper'
ID_TIRES = 'tires'
'''

ID_STORAGE = 'general'

# value ids
ID_AIRBAG       = 'ABG'
ID_ABS          = 'ABS'
ID_ACCE         = 'ACC'
ID_BATTERY      = 'BAT'
ID_BLINKL       = 'BLL'
ID_BLINKR       = 'BLR'
ID_BRAKE        = 'BRK'
ID_CLIENTADR    = 'CAD'
ID_CRUISECONTROL= 'CCT'
ID_CLIENTPORT   = 'CPT'
ID_CLIENTNAME   = 'CNM'
ID_DOOR         = 'DOR'
ID_DPF          = 'DPF'
ID_DASH         = 'DSH'
ID_ENGINE       = 'ENG'
ID_ESP          = 'ESP'
ID_FOGLIGHT     = 'FLT'
ID_FRAMERATE    = 'FRT'
ID_GAS          = 'GAS'
ID_HIGHBEAM     = 'HBM'
ID_INNERDASH    = 'IDS'
ID_KILLME       = 'KME'
ID_LOWBEAM      = 'LBM'
ID_LOGENTRY     = 'LEY'
ID_LOGLEVEL     = 'LLL'
ID_MILEAGE      = 'MIL'
ID_MAINTANCE    = 'MTC'
ID_OILPRESSURE  = 'OPR'
ID_PREHEAT      = 'PHT'
ID_PARKLIGHT    = 'PLT'
ID_PING         = 'PNG'
ID_QUIT         = 'QUT'
ID_DRIVE        = 'RPM'
ID_REST         = 'RST'
ID_SERVERADR    = 'SAD'
ID_SEATBELT     = 'SBT'
ID_SERVERNAME   = 'SNA'
ID_SPEED        = 'SPD'
ID_SERVERPORT   = 'SPT'
ID_STARTSTOP    = 'SSP'
ID_STEERING     = 'STE'
ID_TEMPO        = 'TPO'
ID_TEMPSIG      = 'TPS'
ID_TEMPW        = 'TPW'
ID_TIRES        = 'TRS'
ID_WIPER        = 'WPR'
ID_WATER        = 'WTR'

ID_NONE = 'none'
ID_ON = 'on'
ID_OFF = 'off'
ID_TRUE = 'True'
ID_FALSE = 'False'
ID_INCREASE = 'increase'
ID_DECREASE = 'decrease'

ID_INITIAL = 'initial'
ID_POSITION = 'position'
ID_VALUEFORMAT = 'valueformat'
ID_TITLEFORMAT = 'titleformat'
ID_TITLE = 'title'
ID_STORAGETIME = "storagetime"
ID_LASTENTRIES = "lastentries"
ID_STORAGESIZE = "storagesize"
ID_GENERAL = "general"
ID_LASTVALUE = "lastvalue"
ID_TODELIVER = "todeliver"
ID_DIGITAL = "digital"
ID_ANALOG = "analog"
ID_GRADIENT = "gradient"
ID_PROPORTION = "proportion"
ID_COPY = "copy"
ID_FUNCTION = "function"
ID_PARAMETER = "parameter"

gaugetypes = [LBL_GAUGE, LBL_SIGNAL, LBL_CHART]

processids = [
    ID_FRAMERATE,
    ID_LOGLEVEL,
    ID_SERVERADR,
    ID_LOGENTRY
]

idlist = {
          ID_QUIT:LBL_APP,
          ID_LOGLEVEL:LBL_APP,
          ID_PING:LBL_APP,
          ID_DASH:LBL_APP,
          ID_SERVERADR:LBL_APP,
          ID_SERVERNAME:LBL_APP,
          ID_SERVERPORT:LBL_APP,
          ID_FRAMERATE:LBL_APP,
          ID_KILLME:LBL_APP,
          ID_LOGLEVEL:LBL_APP
         }

valuelist = [ID_FALSE,
             ID_TRUE,
             ID_ON,
             ID_OFF,
             ID_INCREASE,
             ID_DECREASE,
             LOGLEVEL_CRITICAL,
             LOGLEVEL_DEBUG,
             LOGLEVEL_ERROR,
             LOGLEVEL_INFO,
             LOGLEVEL_WARNING,
             LOGLEVEL_NOTSET]

TYPE_POINTER = 'P'
TYPE_TEXT = 'T'

Message_Prefix = "@"
Message_Postfix = "#"
Message_Length = 13
Message_FillChar = "_"
Message_ValueLength = 20
Message_IDLength = 3
MAX_PROCESSTIME = 25000