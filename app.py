from twisted.internet import reactor
from Tagent import Tagent,startlog

reactor=reactor

#打开日志
#startlog()

t=Tagent(reactor=reactor,url='http://baidu.com')

#t.get()
#t.downpage(filename='test.html')
t.cookieRequest()
#t.redirectRequest()
#t.proxyRequest("117.141.155.242",53281)

reactor.run()