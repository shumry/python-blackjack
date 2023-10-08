from views.view import View
from models.gameState import GameState
import common.constants as const
import config.gameConfig as game_config

class Controller:
    def __init__(self):
        self.model = GameState()
        self.view = View(self)

    def main(self):
        self.view.main()

    def handlePlayerAction(self, input_string):
        if input_string == const.HIT:
            self.view.updateScore(self.model.game_score, "Player hits")
            self.model.addCardToPlayer()
            self.view.rebuildPlayerHand(self.model.getPlayerHand())
            self.view.rebuildControlsPanel(self.model.getActions())

        elif input_string == const.STAND:
            self.view.updateScore(self.model.game_score, "Player stands")
            self.model.playerStands()
            self.model.executeDealerTurn(self.rebuildDealerFrame)
            self.view.rebuildControlsPanel(self.model.getActions())

        elif input_string == const.DEAL_NEXT_HAND:
            self.view.updateScore(self.model.game_score, "Dealing next hand...")
            self.dealNextHand()

        elif input_string == const.CONTINUE:
            self.model.executeDealerTurn(self.rebuildDealerFrame)
            self.view.rebuildControlsPanel(self.model.getActions())

        elif input_string == const.START_OVER:
            self.restartGame()
            self.view.updateScore(self.model.game_score,
                                  "Starting a new game...")
            return

        elif input_string == const.GET_MATH:
            _, _, results = self.model.getBestMove()
            self.view.updateScore(self.model.game_score,
                                  f"The math says...")

            for move, ev in results.items():
                self.view.updateScore(self.model.game_score, f"{move}: {ev * game_config.BASE_SCORE}")

            return

        did_round_end=self.model.didRoundEnd()

        if (did_round_end):
            self.view.updateScore(self.model.game_score,
                                  self.model.latest_results)
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
        self.model=GameState()
        self.dealNextHand()
        return
