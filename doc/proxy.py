from Tagent import Tclient
from twisted.internet.task import react

def print_result(result):
    print('print result:\n')
    print(result)

def main(reactor, *args):
    t=Tclient(method='GET',url='http://baidu.com',verify=False,proxy={'http://111.79.198.127':'9999'})
    d=t.get()
    d.addCallback(print_result)
    return d

react(main, [])