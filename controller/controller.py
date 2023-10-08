from views.view import View
from models.gameState import GameState
import common.constants as const


class Controller:
    def __init__(self):
        self.model = GameState()
        self.view = View(self)

    def main(self):
        self.view.main()

    def handlePlayerAction(self, input_string):
        if input_string == const.HIT:
            self.model.addCardToPlayer()
            self.view.rebuildPlayerHand(self.model.getPlayerHand())
            self.view.rebuildControlsPanel(self.model.getActions())

        elif input_string == const.STAND:
            self.model.playerStands()
            self.model.executeDealerTurn(self.rebuildDealerFrame)
            self.view.rebuildControlsPanel(self.model.getActions())

        elif input_string == const.START_OVER:
            self.restartGame()
            self.view.updateScore(self.model.game_score, "Starting a new game...")

        elif input_string == const.DEAL_NEXT_HAND:
            self.dealNextHand()

        elif input_string == const.CONTINUE:
            self.model.executeDealerTurn(self.rebuildDealerFrame)
            self.view.rebuildControlsPanel(self.model.getActions())

        did_round_end = self.model.didRoundEnd()

        if (did_round_end):
            self.view.updateScore(self.model.game_score, self.model.latest_results)
        return

    def rebuildDealerFrame(self):
        self.view.rebuildDealerHand(self.model.dealer)

    def dealNextHand(self):
        self.model.resetRound()
        self.view.rebuildPlayerHand(self.model.getPlayerHand())
        self.view.rebuildDealerHand(self.model.getDealerHand())

        self.model.addCardToPlayer()
        self.view.rebuildPlayerHand(self.model.getPlayerHand())

        self.model.addCardToDealer()
        self.view.rebuildDealerHand(self.model.getDealerHand())

        self.model.addCardToPlayer()
        self.view.rebuildPlayerHand(self.model.getPlayerHand())
        self.view.rebuildControlsPanel(self.model.getActions())
        return

    def restartGame(self):
        self.model = GameState()
        self.dealNextHand()
        return
