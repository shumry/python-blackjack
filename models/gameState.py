from models.deck import Deck
import config.gameConfig as config

class GameState:
    def __init__(self):
        self.player = []
        self.deck = Deck(config.NUM_DECKS)
        return
    
    def addCardToPlayer(self):
        drawn_card = self.deck.drawCard()
        self.player.append(drawn_card)
        return
    
    def getPlayerHand(self):
        return self.player