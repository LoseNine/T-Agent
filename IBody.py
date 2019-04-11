from twisted.web.iweb import IBodyProducer  
from twisted.internet.defer import  succeed

from zope.interface import implementer      #python3


@implementer(IBodyProducer)
class StringProducer(object):
    """
        To provide the IBodyProducer interface, which is enforced by Twisted’s use
        of zope.interface.implements, a class must implement the following
        methods, as well as a length attribute tracking the length of the data the
        producer will eventually produce:

        1.startProducing
        它应该返回一个Deferred当所有数据都生成时会触发。
        应该只触发Deferred归还startProducing .
        2.stopProducing

        3.pauseProducing

        4.resumeProducing


    """

    def __init__(self, body):
        self.body = body
        self.length = len(body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        #Return a L{Deferred} that has already had C{.callback(result)} called.
        """    
            d = Deferred()
            d.callback(result)
            return d
        """
        return succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass