import random

class TgerHeaders:
    def __init__(self):
        self.headPool=[{b'User-Agent': [b'Twisted WebBot']},
                       {b'User-Agent':[b'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6726.400 QQBrowser/10.2.2265.400']},
                       ]

    def get(self):
        """随机获取请User-Agent"""

        head=random.choice(self.headPool)
        print('[INFO]Random choice User-Agent>',head,'\n')
        return head