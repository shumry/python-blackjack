from common.functions import getNumberValueFromCard
import common.constants as const

class PlayerHand:
    def __init__(self):
        self.display_hand = []
        self.state = const.PENDING
        # A representation of the score and number of aces (int, int)
        self.hand = (0, 0)
        self.max_score = 0
        # Didn't have time to implement feature allowing player to double
        # self.canDouble = self.checkAndSetCanDouble()

    def getDisplayHand(self):
        return self.display_hand

    def addCard(self, newCard):
        if (self.state != const.PENDING):
            print(self.state)
            print("Error, trying to add card in invalid state")
            return
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
            self.max_score = raw_score
            self.state = const.BUSTED
            return

        if (num_aces < 1):
            self.max_score = raw_score
            return

        if (len(self.display_hand) == 2 and raw_score == 11 and num_aces == 1):
            self.max_score = 21
            self.state = const.BLACKJACK
            return

        self.max_score = raw_score if raw_score + 10 > 21 else raw_score + 10
        return

    def checkAndSetCanDouble(self):
        if (len(self.display_hand) == 2):
            self.canDouble = True
            return True
        return False

    def updateState(self, new_state):
        self.state = new_state
        return

    # for testing
    def __repr__(self) -> str:
        return "Cards: " + str(self.display_hand) + " hand " + str(self.hand) + "canDouble:  " + str(self.canDouble)
