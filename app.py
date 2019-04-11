from twisted.internet import reactor
from Tagent import Tagent,startlog

class Tclient:
    def __init__(self,url):
        self.reactor=reactor
        self.agent=Tagent(self.reactor,url=url)

    def run(self):
        self.reactor.run()

    def startlog(self):
        startlog()

    def get(self):
        self.agent.get()

    def download(self,to):
        self.agent.downpage(to)

    def cookieRequest(self):
        self.agent.cookieRequest()

    def redirectRequest(self):
        self.agent.redirectRequest()

    def proxyRequest(self,address,port):
        self.agent.proxyRequest(address,port)

if __name__ == '__main__':
    t=Tclient("http://baidu.com")
    t.get()
    t.run()