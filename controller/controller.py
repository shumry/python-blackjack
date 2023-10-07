from views.view import View
from models.gameState import GameState
import common.constants as const
from time import sleep

class Controller:
    def __init__(self):
        self.model = GameState()
        self.view = View(self)

    def main(self):
        self.view.main()

    def handlePlayerAction(self, input_string):
        print(input_string)

        if input_string == const.HIT:
            new_state = self.model.addCardToPlayer()            
            self.view.rebuildPlayerHand(self.model.getPlayerHand())
        
        elif input_string == const.STAND:
            self.model.executeDealerTurn()
            self.view.rebuildDealerHand(self.model.dealer)
            
        elif input_string == const.START_OVER:
            self.restartGame()
        
        elif input_string == const.DEAL_NEXT_HAND:
            self.dealNextHand()
        
        self.view.updateScore(self.model.player_score)
        return

    def dealNextHand(self):
        self.model.resetRound()
        self.view.rebuildPlayerHand(self.model.player)
        self.view.rebuildDealerHand(self.model.dealer)
        
        sleep(1)
        
        self.model.addCardToPlayer()
        self.view.rebuildPlayerHand(self.model.getPlayerHand())
        sleep(1)
        print("added one card")
        self.model.addCardToDealer()
        self.view.rebuildDealerHand(self.model.getDealerHand())
        # sleep(1)
        self.model.addCardToPlayer()
        self.view.rebuildPlayerHand(self.model.getPlayerHand())
        return
    
    def restartGame(self):
        print("in restartGame")
        self.model = GameState()
        self.dealNextHand()
       

        return
