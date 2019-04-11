from __future__ import print_function

from twisted.web import client
from twisted.internet import reactor
from twisted.web.http_headers import Headers
from twisted.internet.defer import Deferred
from twisted.web.client import ProxyAgent
from twisted.internet.endpoints import TCP4ClientEndpoint
from Theaders import TgerHeaders
from twisted.python import log,compat
from twisted.python import failure


from IBody import StringProducer
from Resource import ResourcePrinter


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
    def __init__(self,reactor,url=None,method='GET',data=None,headers=None,timeout=None,ip=None,port=None):

        self.reactor=reactor
        self.url=url.encode('utf_?')
        self.headers=headers
        self.method=method.encode('utf_?')
        self.timeout=timeout
        self.ip=ip
        self.port=port

        if self.headers ==None:
            headers=TgerHeaders().get()
            self.headers=Headers(headers)
            
            self.headers.setRawHeaders(b'accept',[b'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'])

        if data!=None:
            self.body = StringProducer(data)
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


    def displayCookies(self,response, cookieJar):
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
        e=texe.execute(d)
        return e

    def get(self):
        return self._request()

    def post(self):
        return self._request()

    def downpage(self,filename):
        client.downloadPage(url=self.url,file=filename)
        self.run()
    
    def _request(self):
        cookieJar = compat.cookielib.CookieJar()
        agent = TredirectLimitAgent(TcookieAgent(self.agent,cookieJar))
        if self.ip and self.port:
            endpoint = TCP4ClientEndpoint(reactor, self.ip, self.port)
            p = ProxyAgent(endpoint)
            agent = TredirectLimitAgent(TcookieAgent(p, cookieJar))
        d=agent.request(method=self.method,uri=self.url, headers=self.headers,bodyProducer=self.body)

        d.addCallback(self.displayCookies, cookieJar)

        # if self.timeout:
        #     TimeoutCall = self.reactor.callLater(self.timeout, d.cancel)
        #     def gotResult(result):
        #         if TimeoutCall.active():
        #             TimeoutCall.cancel()
        #         return result
        # d.addBoth(gotResult)
        return self.execute(d)
        

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

    def execute(self, d):
        e=d.addCallbacks(self.printResource, self.printError)
        return e

class Tclient:
    def __init__(self,reactor=reactor,url=None,method='GET',data=None,headers=None,verify=True,timeout=None,**kwargs):
        ip = None
        port = None

        if not verify:
            import _utils
        print(kwargs)
        if 'proxy' in kwargs:

            for k,v in kwargs['proxy'].items():
                ip=k
                port=v

        self.reactor=reactor
        self.agent=Tagent(self.reactor,url=url,data=data,method=method,
                          headers=headers,timeout=timeout,ip=ip,port=port)

    def run(self):
        self.reactor.run()

    def stop(self):
        self.reactor.stop()

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


def startlog(filename=None):
    if not filename:
        filename='T-Crawl.log'
    log.startLogging(open(filename, 'w'))