import random

class TgerHeaders:
    def __init__(self):
        self.headPool=[{b'User-Agent': [b'Twisted WebBot'],}]

    def get(self):
        """随机获取请User-Agent"""

        head=random.choice(self.headPool)
        print('[INFO]Random choice User-Agent>',head,'\n')
        return head