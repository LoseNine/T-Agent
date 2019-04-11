from Tagent import Tclient,Execute
import _utils

class own_execute(Execute):
    """
        自定义execute
    """
    def __init__(self,agent,reactor):
        self.reactor=reactor
        super(own_execute, self).__init__(agent,reactor)

    def result(self,res):
        print(res)
        self.reactor.stop()

    def add_execute(self,d):
        super(own_execute, self).add_execute(d)
        d.addBoth(self.result)

def app_execute(t,d):
    exe=own_execute(t.agent,t.reactor)
    exe.execute(d)

if __name__ == '__main__':
    t=Tclient(url="https://github.com")
    d=t.get()
    #html=t.execute(d)
    html=app_execute(t,d)
    t.run()
