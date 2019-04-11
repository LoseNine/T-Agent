from twisted.internet.protocol import Protocol

class ResourcePrinter(Protocol):
    def __init__(self, finished):
        self.finished = finished
        self.data=None

    def connectionMade(self):
        print('[INFO]connect made\n')

    def dataReceived(self, data):
        print('[INFO]html decode:\n')
        #print(data.decode('utf-8'))
        self.data=data.decode('utf-8')

    def connectionLost(self, reason):
        print('Finished receiving body:', reason.getErrorMessage())

        self.finished.callback(self.data)