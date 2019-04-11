from __future__ import print_function

from twisted.web import client
from twisted.web.client import ContentDecoderAgent,GzipDecoder
from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.internet.protocol import Protocol
from twisted.web.http_headers import Headers
from twisted.internet.defer import Deferred, succeed

from twisted.python.log import err
from twisted.web.client import ProxyAgent
from twisted.internet.endpoints import TCP4ClientEndpoint

from twisted.web.iweb import IBodyProducer  #用于POST传输数据data
from zope.interface import implementer      #python3

from Theaders import TgerHeaders
from twisted.python import log,compat

# import OpenSSL
# from twisted.internet.ssl import SSL


@implementer(IBodyProducer)
class StringProducer(object):
    """
        To provide the IBodyProducer interface, which is enforced by Twisted’s use
        of zope.interface.implements, a class must implement the following
        methods, as well as a length attribute tracking the length of the data the
        producer will eventually produce:

        1.startProducing

        2.stopProducing

        3.pauseProducing

        4.resumeProducing
    """

    def __init__(self, body):
        self.body = body
        self.length = len(body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass

class TredirectLimitAgent(client.RedirectAgent):
    """
        防止陷阱，限制最多30x重定向
    """
    def __init__(self,agent,limit=10):
        super(TredirectLimitAgent, self).__init__(agent,limit)

class TcookieAgent(client.CookieAgent):
    """
        Send a Cookie header if a cookie for uri is stored in CookieAgent.cookieJar.
        Cookies are automatically extracted and stored from requests.

        If a 'cookie' header appears in headers
        it will override the automatic cookie header
        obtained from the cookie jar.
    """
    def __init__(self,agent,cookieJar=None):
        super(TcookieAgent, self).__init__(agent,cookieJar)


class Tagent:
    def __init__(self,reactor,url=None,method='GET',data=None,headers=None):

        self.reactor=reactor
        self.url=url.encode('utf_?')
        self.headers=headers
        self.method=method.encode('utf_?')

        if self.headers ==None:
            headers=TgerHeaders().get()
            self.headers=Headers(headers)
            
            self.headers.setRawHeaders(b'accept',[b'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'])

        if data!=None:
            self.body = StringProducer(data.encode('utf_?'))
        else:
            self.body=None

        self.agent=client.Agent(reactor)

    def printHeaders(self,response):
        print('HTTP version:', response.version)
        print('Status code:', response.code)
        print('Status phrase:', response.phrase)
        print('Response headers:')

        for header, value in response.headers.getAllRawHeaders():
            print(header, value)

    # def printResource(self,response):
    #     print('[INFO]printResource:',response)
    #     print("[INFO]code:",response.code)
    #     print('[INFO]phrase:',response.phrase)
    #     print("[INFO]headers:",response.headers)
    #     print('[INFO]transport:', response._transport)
    #     finished = Deferred()
    #     response.deliverBody(ResourcePrinter(finished)) #所有response交给ResourcePrinter处理
    #     return finished
    #
    # def printError(self,failure):
    #     print("error:\n")
    #     print(failure)
    #     print(failure.value.reasons[0].printTraceback())

    def displayCookies(self,response, cookieJar):
        #print('Received response')
        #print(response)
        print('[INFO]Cookies:', len(cookieJar))
        for cookie in cookieJar:
            print(cookie)
        return response

    def display(self,response):
        print("Received response")
        print(response.code)
        print(response.headers)
        return response

    def stop(self,result):
        print(result)
        reactor.stop()

    def execute(self,d):
        # d.addCallbacks(self.printResource, self.printError)
        # d.addBoth(self.stop)

        texe=Execute(self.agent,self.reactor)

        texe.execute(d)

    def get(self):
        agent=TredirectLimitAgent(self.agent)
        d = agent.request(method=b'GET', uri=self.url, headers=self.headers, bodyProducer=self.body)
        return d

    def post(self):
        d=self.agent.request(method=b'POST',uri=self.url, headers=self.headers,bodyProducer=self.body)
        return d

    def downpage(self,filename):
        client.downloadPage(url=self.url,file=filename)
        self.run()

    def contentDecodeRequest(self):
        agent = ContentDecoderAgent(TredirectLimitAgent(self.agent),['gzip',GzipDecoder])
        d=agent.request(method=self.method,uri=self.url, headers=self.headers,bodyProducer=self.body)
        d.addCallback(self.display)
        return d

    def cookieRequest(self):
        cookieJar = compat.cookielib.CookieJar()
        #agent=TredirectLimitAgent(TcookieAgent(self.agent,cookieJar))
        agent = TredirectLimitAgent(TcookieAgent(self.agent,cookieJar))
        d=agent.request(method=self.method,uri=self.url, headers=self.headers,bodyProducer=self.body)

        d.addCallback(self.displayCookies, cookieJar)
        return d

    def redirectRequest(self):
        agent=TredirectLimitAgent(self.agent)
        d=agent.request(method=self.method,uri=self.url, headers=self.headers,bodyProducer=self.body)
        return d

    def proxyRequest(self,ip,port):
        endpoint = TCP4ClientEndpoint(reactor, ip, port)
        agent = ProxyAgent(endpoint)
        d = agent.request(method=self.method,uri=self.url, headers=self.headers,bodyProducer=self.body)
        d.addCallbacks(self.display)
        return d

class ResourcePrinter(Protocol):
    def __init__(self, finished):
        self.finished = finished
        self.data=None

    def connectionMade(self):
        print('[INFO]connect made\n')

    def dataReceived(self, data):
        print('[INFO]html decode:\n')
        print(data.decode('utf-8'))
        self.data=data.decode('utf-8')

    def connectionLost(self, reason):
        print('Finished receiving body:', reason.getErrorMessage())

        self.finished.callback(self.data)

class Execute:

    def __init__(self,agent,reactor):
        self.agent=agent
        self.reactor=reactor

    def printResource(self,response):
        """
            等待response被ResourcePrinter接收完毕后返回
            在connectionLost里callback启动，赋予finished初始值
            结果被stop打印出来

            :param response: IResponse
            :return: Deferred()
        """

        print('[INFO]printResource:',response)
        print("[INFO]code:",response.code)
        print('[INFO]phrase:',response.phrase)
        print("[INFO]headers:",response.headers)
        print('[INFO]transport:', response._transport)

        finished = Deferred()   #创建Deferred()

        response.deliverBody(ResourcePrinter(finished)) #所有response交给ResourcePrinter处理

        return finished

    def printError(self,failure):
        print("error:\n")
        print(failure)
        print(failure.value.reasons[0].printTraceback())


    def stop(self, result):
        print(result)
        self.reactor.stop()

    def add_execute(self,d):
        d.addCallbacks(self.printResource, self.printError)

    def execute(self, d):
        d.addCallbacks(self.printResource, self.printError)
        d.addBoth(self.stop)

class Tclient:
    def __init__(self,url):
        self.reactor=reactor
        self.agent=Tagent(self.reactor,url=url)

    def run(self):
        self.reactor.run()

    def execute(self,d):
        self.agent.execute(d)

    def startlog(self,filename=None):
        startlog(filename)

    def get(self):
        return self.agent.get()

    def post(self):
        return self.agent.post()

    def download(self,to):
        self.agent.downpage(to)

    def getpage(self):
        return client.getPage(url=self.agent.url)

    def cookieRequest(self):
        return self.agent.cookieRequest()

    def redirectRequest(self):
        return self.agent.redirectRequest()

    def proxyRequest(self,address,port):
        return self.agent.proxyRequest(address,port)

def startlog(filename=None):
    if not filename:
        filename='T-Crawl.log'
    log.startLogging(open(filename, 'w'))