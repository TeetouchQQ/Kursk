class Player(object):
    def __init__(self,name):
        self.name = name
        self.exp = 0
    def level_up(self):
        pass
    def add_exp(self,amount):
        self.exp += amount
    def save_score(self):
        pass