from views.view import View
from models.gameState import GameState

class Controller:
    def __init__(self):
        self.model = GameState()
        self.view = View(self)

    def main(self):
        self.view.main()

    def handlePlayerAction(self, input_string):
        print(input_string)

        if input_string == "Hit":
            self.model.addCardToPlayer()
            self.view.rebuildPlayerHand(self.model.getPlayerHand())
        return
