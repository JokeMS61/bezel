__author__ = 'JK'
import socket
from settings import *

class NetworkClient():
    def __init__(self,hostname="localhost", adress=10000, broadcast=False):

        self.broadcast = broadcast
        self.port = adress

        if self.broadcast:
            # open UDP Socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
            self.sock.settimeout(5)
        else:
            # Create a TCP/IP socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_address = (hostname,adress)


    def connectSocket(self):
        return self.sock.connect_ex(self.server_address)

    def connectServer(self):
        logger.info('attempt connecting to %s port %s' % self.server_address)
        rc = 1
        while rc != 0:
            rc = self.sock.connect_ex(self.server_address)
        logger.debug("connected at: %s",self.sock.getsockname())
        return rc

    def reconnectServer(self):
        logger.info('attempt reconnecting to %s port %s' % self.server_address)
        rc = 1
        while rc != 0:
            rc = self.sock.connect_ex(self.server_address)
            logger.debug("reconnect rc=%s",rc)
            #pygame.time.wait(1000)
        logger.info("reconnected")


    def stop(self):
        self.sock.close()

    def receive(self):
        data = self.sock.recv(512)
        print ('received "%s"' % data)
        return data

    def send(self, message, receive):
        if self.broadcast:
            try:
                self.sock.sendto("PING=0", ("<broadcast>", self.port))
                try:
                    print("Response: %s" % self.sock.recv(1024))
                except socket.timeout:
                    print( "No server found")
            except:
                return 1
            finally:
                return 0
        else:
            try:
                message = "@" + message + "#"
                logger.debug('sending "%s"' % message)

                #self.sock.sendall(bytes(message + "\n", "utf-8"))
                self.sock.sendall(message.encode("utf-8"))
                if receive:
                    data = self.sock.recv(1024, "utf-8")
                    print ('received "%s"' % data)
                    return data
            except:
                return 1

            finally:
                return 0

