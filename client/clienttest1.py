
from networkclient import NetworkClient
from tools import *
import time


class TestClient():
    def __init__(self, parent=None):
        self.nc = NetworkClient("localhost",32000)

    def connect(self):
        self.nc.connectServer()

    def send(self,id, value):
        receive = ""
        message = formatMessageContent(id,value)

        if message != None:
            self.nc.send(message, receive)
            print("receive: %s", receive)

    def stop(self):
        self.nc.stop()

def main():
    tc = TestClient()
    tc.connect()
    tc.send("SPD","10")
    time.sleep(0.5)
    tc.send("SPD","12")
    time.sleep(0.5)
    tc.send("SPD","14")
    tc.stop()

if __name__ == '__main__':
    main()