from common.dealerState import DealerHand
from models.deck import Deck
from common.playerState import PlayerHand
import config.gameConfig as config
import common.constants as const


class GameState:
    def __init__(self):
        self.player_score = 0
        self.player = PlayerHand()
        self.dealer = DealerHand()
        self.deck = Deck(config.NUM_DECKS)
        return

    def resetRound(self):
        self.player = PlayerHand()
        # self.dealer = DealerHand()
        if self.deck.getNumCardsRemaining() <= 15:
            self.deck = self.deck.reshuffleDeck()
            print(self.deck.getDeck())

    def addCardToPlayer(self):
        drawn_card = self.deck.drawCard()
        new_player_state = self.player.addCard(drawn_card)
        self.updateScore(new_player_state)

    def updateScore(self, new_state):
        if new_state == const.BLACKJACK:
            self.player_score += 15
        elif new_state == const.BUSTED:
            self.player_score -= 10

    def addCardToDealer(self):
        drawn_card = self.deck.drawCard()
        self.dealer.addCard(drawn_card)
        
    def executeDealerTurn(self):
        while(self.dealer.state == const.PENDING):
            drawn_card = self.deck.drawCard()
            self.dealer.addCard(drawn_card)
        self.updateScoreFromDealerHand()
        return
    
    def updateScoreFromDealerHand(self):
        if (self.dealer.state == const.BUSTED):
            self.player_score += 10
        
        elif (self.dealer.state == const.BLACKJACK):
            self.player_score -= 10
        
        else:
            if self.player.max_score > self.dealer.score:
                self.player_score += 10
            elif self.player.max_score < self.dealer.score:
                self.player_score -= 10
            
    def getPlayerHand(self):
        return self.player
    
    def getDealerHand(self):
        return self.dealer