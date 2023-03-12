
from networkclient import NetworkClient
import time
import settings

class TestClient():
    def __init__(self, parent=None):
        self.nc = NetworkClient("localhost",32000)

    def connect(self):
        self.nc.connectServer()

    def send(self,message):
        receive = ""
        self.nc.send(message, receive)
        print("receive: %s", receive)

    def stop(self):
        self.nc.stop()

def main():
    tc = TestClient()
    tc.connect()
    tc.send("SPD10")
    time.sleep(0.5)
    tc.send("SPD12")
    time.sleep(0.5)
    tc.send("SPD14")
    tc.stop()

if __name__ == '__main__':
    main()