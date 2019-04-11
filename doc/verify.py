from Tagent import Tclient
from twisted.internet.task import react

def print_result(result):
    print('print result:\n')
    print(result)

def main(reactor, *args):
    t=Tclient(method='GET',url='https://github.com',verify=False)
    d=t.get()
    d=t.execute(d)
    d.addCallback(print_result)
    return d

react(main, [])