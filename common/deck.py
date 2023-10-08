import random

SINGLE_DISPLAY_DECK =["1_c", "1_s", "1_d", "1_h", "2_c", "2_s", "2_d", "2_h", "3_c", "3_s", "3_d", "3_h", "4_c", "4_s", "4_d", "4_h", "5_c", "5_s", "5_d", "5_h", "6_c", "6_s", "6_d", "6_h", "7_c", "7_s", "7_d", "7_h", "8_c", "8_s", "8_d", "8_h", "9_c", "9_s", "9_d", "9_h", "10_c", "10_s", "10_d", "10_h", "j_c", "j_s", "j_d", "j_h", "q_c", "q_s", "q_d", "q_h", "k_c", "k_s", "k_d", "k_h"]
SINGLE_MATH_DECK = [4, 4, 4, 4, 4, 4, 4, 4, 4, 16]

class Deck:
    def __init__(self, num_decks):
        self.num_decks = num_decks
        self.display_deck = []
        self.math_deck = []
        self.setNewDeck()
        self.shuffleDeck()
    
    def getDeck(self):
        return self.display_deck
    
    def getNumCardsRemaining(self):
        return len(self.display_deck)
    
    def drawCard(self):
        if len(self.display_deck) == 0:
            raise Exception("Deck is empty")
        return self.display_deck.pop()
        
    def setNewDeck(self):
        self.display_deck = SINGLE_DISPLAY_DECK * self.num_decks
        self.math_deck = [x * self.num_decks for x in SINGLE_MATH_DECK]
        return

    def shuffleDeck(self):
        random.shuffle(self.display_deck)
        return
    
    def reshuffleDeck(self, cards_in_play = []):
        self.setNewDeck()
        
        if len(cards_in_play) != 0:
            for card in cards_in_play:
                self.display_deck.remove(card)
        
        self.shuffleDeck()
        return