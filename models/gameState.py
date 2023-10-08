from common.calculator import Calculator
from common.dealerState import DealerHand
from common.deck import Deck
from common.playerState import PlayerHand
import config.gameConfig as config
import common.constants as const
from time import sleep

class GameState:
    def __init__(self):
        self.game_score = 0
        self.player = PlayerHand()
        self.dealer = DealerHand()
        self.actions = []
        self.deck = Deck(config.NUM_DECKS)
        self.round_ended = False
        self.latest_results = ""
        self.calculator = Calculator()
        return

    def resetRound(self):
        self.player = PlayerHand()
        self.dealer = DealerHand()
        self.round_ended = False

        if self.deck.getNumCardsRemaining() <= config.RESHUFFLE_THRESHOLD:
            self.deck.reshuffleDeck()

    def addCardToPlayer(self):
        drawn_card = self.deck.drawCard()
        new_player_state = self.player.addCard(drawn_card)
        self.updateGameScore(new_player_state)

    def updateGameScore(self, new_state):
        if new_state == const.BLACKJACK:
            self.game_score += config.BLACKJACK_SCORE_MULTIPLIER * config.BASE_SCORE
            self.latest_results = "Player got a BlackJack and won!"
        elif new_state == const.BUSTED:
            self.game_score -= config.BASE_SCORE
            self.latest_results = "Player busted and lost"

    def addCardToDealer(self):
        drawn_card = self.deck.drawCard()
        self.dealer.addCard(drawn_card)

    def executeDealerTurn(self, callback_fn):
        if (self.dealer.state == const.PENDING):
            drawn_card = self.deck.drawCard()
            self.dealer.addCard(drawn_card)

            if (self.dealer.state != const.PENDING):
                self.updateGameScoreFromDealerHand()
            callback_fn()
        return

    def updateGameScoreFromDealerHand(self):
        if (self.dealer.state == const.BUSTED):
            self.game_score += config.BASE_SCORE
            self.latest_results = "The dealer busted and the player won!"

        elif (self.dealer.state == const.BLACKJACK):
            self.game_score -= config.BASE_SCORE
            self.latest_results = "The dealer got a Blackjack and the player lost!"

        else:
            if self.player.max_score > self.dealer.score:
                self.game_score += config.BASE_SCORE
                self.latest_results = "The player got a higher score and won!"
            elif self.player.max_score < self.dealer.score:
                self.game_score -= config.BASE_SCORE
                self.latest_results = "The player got a lower score and lost!"
            else:
                self.latest_results = "It was a tie!"
                
    def playerStands(self):
        self.player.updateState(const.STAND)
        return

    def getPlayerHand(self):
        return self.player

    def getDealerHand(self):
        return self.dealer

    def didRoundEnd(self):
        player_state = self.player.state
        dealer_state = self.dealer.state

        if (player_state == const.PENDING):
            self.round_ended = False
        elif (player_state == const.STAND and dealer_state == const.PENDING):
            self.round_ended = False
        else:
            return True

        return self.round_ended

    def getActions(self):
        player_state = self.player.state
        dealer_state = self.dealer.state

        if (player_state == const.PENDING):
            return [const.HIT, const.STAND]

        if (player_state == const.STAND and dealer_state == const.PENDING):
            return [const.CONTINUE]

        # if neither, show continue next hand
        return [const.DEAL_NEXT_HAND]

    def getBestMove(self):
        return self.calculator.evaluate(self.player, self.dealer, self.deck.math_deck)