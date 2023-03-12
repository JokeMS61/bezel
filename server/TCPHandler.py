import socketserver
import settings

class TCPHandler(socketserver.BaseRequestHandler):



    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)

        if len(self.data) > 0:
            message = self.data
            logger.debug("new data : %s", message)
            messages = self.mh.getallMessages(message)
            if messages is not None:
                if self.messageContainsQuit(messages) == True:
                    pass

                self.process(messages)

    def update(self, id, value):
        message = '@' + id + str(value) + '#'
        self.request.sendall(message)
