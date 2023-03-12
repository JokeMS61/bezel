__author__ = 'JK'

import threading
import traceback
import socket
import sys
from messagehelper import *
from settings import *
from timing import delay


class NetworkServer(threading.Thread):

    def __init__(self, callback, callbackConnected, port):
        threading.Thread.__init__(self)
        self.running = True
        self.connectclient = True
        self.listener = callback
        self.clientstring = callbackConnected
        self.sock = None
        self.port = port
        self.establishserver(port)
        self.connection = None
        self.clientconnected = False
        self.mh = MessageHelper()
        self.clientport = ""
        self.clientaddress = ""

    def stop(self):
        logger.debug("attempt so stop the thread")
        self.running = False
        self.connectclient = False

    def establishserver(self,port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ("localhost", port)
        logger.info('starting up on %s port %s' % server_address)
        self.sock.bind(server_address)
        self.servername = socket.gethostname()
        logger.info("servername: %s", self.servername)
        self.serveraddress = socket.gethostbyname(self.servername)
        logger.info("serveraddress: %s", self.serveraddress)
        self.sock.listen(5)

    def run(self):

        message=""
        while self.running:
            waitinfo = 'waiting for connection'
            logger.info(waitinfo)
            logger.info(waitinfo)
            (self.connection, client_address) = self.sock.accept()
            self.clientaddress = str(client_address[0])
            self.clientport = str(client_address[1])
            connectinfo = "ca:" + self.clientaddress + ":" + self.clientport
            logger.info(connectinfo)
            self.clientstring(connectinfo)
            logger.info('client connected: %s', client_address)
            self.clientconnected = True

            try:
                while self.running and self.connectclient:
                    rawdata = self.connection.recv(1024)
                    data = rawdata.decode("utf-8")
                    if len(data) > 0:
                        message = data
                        logger.debug("new data : %s", message)
                        messages = self.mh.getallMessages(message)
                        if messages is not None:
                            if self.messageContainsQuit(messages) == True:
                                self.running = False
                                self.connectclient = False
                            self.sendmessages(messages)
                    else:
                        self.running = False
                        self.connectclient = False

                logger.debug("innerwhile verlassen")
            except IOError as errno:
                self.clientconnected = False
                logger.error("I/O error %s",errno)
            except ValueError:
                logger.warning("No valid value in message.")
            except Exception:
                print( 'print_exception():')
                exc_type, exc_value, exc_tb = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_tb)
                logger.error("message: %s", message)
            finally:
                logger.info("connection.close()")
                self.connection.close()
                self.clientstring(waitinfo)

        self.sock.close()

    def messageContainsQuit(self, messages):
        for x in range(0,len(messages)):
            if messages[x][0] == ID_QUIT:
                logger.debug("server ueber networkclient beenden")
                return True
        return False

    def validate(self,message):
        value = message.split('=')
        if value[0] is not None and value[1] is not None:
            if value[0] in idlist:
                if value[1] in valuelist or float(value[1]) is not None:
                    return 1
            else:
                return -2
        else:
            return -1
    def getServerPort(self):
        return str(self.port)

    def getClientPort(self):
        return self.clientport

    def getClientAddress(self):
        return self.clientaddress

    def getServerAddress(self):
        return str(self.serveraddress)

    def getServerName(self):
        return str(self.servername)

    def sendmessages(self,messages):
#        logger.debug("send message to publisher callback")
        self.listener(messages)

    def update(self, id, value):
        if id == ID_QUIT:
            self.running = False
            self.connectclient = False
            logger.debug("server ueber processdata.setValue() beenden.")
            # gut gedacht. Der Server bleibt aber in socket.recv,
            # wenn keine weiteren Meldungen eintreffen.
            # deswegen beenden weiter ueber den Netwerkcontroller
            # und dessen destroy methode
        else:
            message = '@' + id + str(value) + '#'
            if self.clientconnected is True:
                try:
                    rc = self.connection.sendall(message.encode("utf-8"))
                    logger.debug("message: %s rc: %s",message, rc )
                except:
                    logger.debug("socket error")
                finally:
                    return 0