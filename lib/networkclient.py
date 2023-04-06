__author__ = 'JK'
import socket
from settings import *

# following task are to do:
# 1. connection must be more reliable
# 2. use selectors
# 3. implement multi-connections
# look here: https://realpython.com/python-sockets/

class NetworkClient():
    def __init__(self,hostname="localhost", adress=10000):
        self.port = adress

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

    def setBlocking(self,flag=False):
        self.sock.setblocking(flag)

    def stop(self):
        self.sock.close()

    def receive(self):
        try:
            data = self.sock.recv(1024)
            print ('received "%s"' % data)
        except ConnectionResetError:
            return None
        finally:
            pass

        return data

    def send(self, message, receive):
        try:
            self.sock.sendall(message)
            if receive:
                data = self.sock.recv(1024, "utf-8")
                #print ('received "%s"' % data)
                return data
        except:
            return None

        finally:
            return 0

