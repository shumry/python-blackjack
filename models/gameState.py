import random

class GameState:
    def __init__(self):
        self.player = []
        self.deck = ["7_h", "j_s", "1_s", "10_h"]
        return
    
    def addCardToPlayer(self):
        random.shuffle(self.deck)
        self.player.append(self.deck[0])
        return
    
    def getPlayerHand(self):
        return self.player