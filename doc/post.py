from Tagent import Tclient
from twisted.internet.task import react
import json

def print_result(result):
    print('print result:\n')
    print(result)

def main(reactor, *args):
    t=Tclient(method='POST',url='http://httpbin.org/post',data=json.dumps({"msg": "Twisted"}).encode('ascii'))
    d=t.post()
    d=t.execute(d)
    d.addCallback(print_result)
    return d

react(main, [])