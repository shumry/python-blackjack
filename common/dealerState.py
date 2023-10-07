from common.functions import getNumberValueFromCard
import common.constants as const

class DealerHand:
    def __init__(self):
        self.display_hand = []
        self.score = 0
        self.state = const.PENDING
        # A representation of the score and number of aces (int, int)
        self.hand = (0, 0)

    def getDisplayHand(self):
        return self.display_hand
    
    def addCard(self, newCard):
        val, numAces = self.hand

        newCardVal = getNumberValueFromCard(newCard)

        if (newCardVal == 1):
            numAces += 1

        self.display_hand.append(newCard)
        self.hand = val + newCardVal, numAces
        
        self.updateScoreAndState()
        return self.state
    
    def updateScoreAndState(self):
        raw_score, num_aces = self.hand

        if (raw_score > 21):
            self.score = raw_score
            self.state = const.BUSTED
            return
        
        if (len(self.display_hand) == 2 and raw_score == 11 and num_aces == 1):
            self.score = 21
            self.state = const.BLACKJACK
            return

        if (num_aces < 1):
            self.score = raw_score
        else:
            self.score = raw_score if raw_score + 10 > 21 else raw_score + 10
        
        if self.score >= 17:
            self.state = const.STAND
        return
