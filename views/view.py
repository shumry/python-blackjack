import tkinter as tk
from tkinter import ttk
from common.dealerState import DealerHand
import config.viewConfig as config
from common.playerState import PlayerHand
import common.constants as const


class View(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.c = controller
        self.cards = {}
        self.initCards()
        self._make_background()
        self._make_dealer_frame(DealerHand())
        self._make_player_frame(PlayerHand())
        self._make_info_box()
        self._make_controls_panel()

    def main(self):
        self.mainloop()

    def _make_background(self):
        self.geometry(config.WINDOW_DIMENSIONS)
        self.title(config.WINDOW_TITLE)
        self.configure(bg=config.BACKGROUND_COLOR)
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        return

    def _make_dealer_frame(self, dealer_data):
        self.dealer_frame = ttk.Frame(self)
        self.dealer_frame.grid(row=0, column=0, sticky="nsew")

        headerText = ttk.Label(self.dealer_frame, text="Dealer's Hand: ")
        headerText.pack()
        card_frame = ttk.Frame(self.dealer_frame)

        if (len(dealer_data.display_hand) < 2):
            for i in range(2-len(dealer_data.display_hand)):
                image_label = tk.Label(card_frame, image=self.cards["back"])
                image_label.pack(side="left", anchor="center")

        for display_card in dealer_data.display_hand:
            image_label = tk.Label(
                card_frame, image=self.cards[display_card])
            image_label.pack(side="left")

        card_frame.pack()

        scoreText = ttk.Label(
            self.dealer_frame, text=f"Dealer Score: {self._get_text_for_dealer_hand(dealer_data)}")
        scoreText.pack()
        return

    def _make_player_frame(self, player_hand):
        self.player_frame = ttk.Frame(self)

        self.player_frame.grid(row=1, column=0, sticky="nsew")

        text = ttk.Label(self.player_frame, text="Player's Hand: ")
        text.pack()

        card_frame = ttk.Frame(self.player_frame)

        for display_card in player_hand.display_hand:
            image_label = tk.Label(
                card_frame, image=self.cards[display_card])
            image_label.pack(side="left")

        card_frame.pack()

        scoreText = ttk.Label(
            self.player_frame, text=f"Current Score: {self._get_text_for_player_hand(player_hand)}")
        scoreText.pack()
        return

    def _get_text_for_dealer_hand(self, dealer_data):

        if (dealer_data.state == const.BLACKJACK):
            return "21 with BLACK_JACK!!"

        if (dealer_data.state == const.BUSTED):
            return f"{dealer_data.score}, oh no... BUSTED"

        return dealer_data.score
    
    def _get_text_for_player_hand(self, player_hand):

        if (player_hand.state == const.BLACKJACK):
            return "21 with BLACK_JACK!!"

        if (player_hand.state == const.BUSTED):
            return f"{player_hand.max_score}, oh no... BUSTED"

        return player_hand.max_score

    def _make_info_box(self, score=0):
        self.info_box_frame = ttk.Frame(self)
        self.info_box_frame.grid(row=0, column=1, sticky="nsew")

        score_frame = ttk.Frame(self.info_box_frame)
        text = ttk.Label(score_frame, text=f"Score: {score}")
        text.pack()
        score_frame.pack()
        return

    def _make_controls_panel(self, player_actions=[]):
        self.controls_panel_frame = ttk.Frame(self)
        self.controls_panel_frame.grid(row=1, column=1, sticky="nsew")

        self.controls_panel_frame.grid_rowconfigure(0, weight=1)
        self.controls_panel_frame.grid_rowconfigure(1, weight=1)

        player_actions_frame = ttk.Frame(self.controls_panel_frame)
        player_actions_frame.grid(row=0, sticky='nsew')
        text = ttk.Label(player_actions_frame, text="Actions:")
        text.pack(pady=(10, 0))

        player_buttons_frame = ttk.Frame(player_actions_frame)

        for action in player_actions:
            def func_to_run(x=action):
                return self.c.handlePlayerAction(x)

            button = ttk.Button(player_actions_frame,
                                text=action, command=func_to_run)
            button.pack()

        player_buttons_frame.pack()

        game_actions_frame = ttk.Frame(self.controls_panel_frame)
        game_actions_frame.grid(row=1, sticky='nsew')

        game_buttons_frame = ttk.Frame(game_actions_frame)
        game_actions = [const.START_OVER]

        for action in game_actions:
            def func_to_run(x=action):
                return self.c.handlePlayerAction(x)

            button = ttk.Button(game_buttons_frame,
                                text=action, command=func_to_run)
            button.pack()
        game_buttons_frame.pack()
        return

    def initCards(self):
        for elem in config.CARD_LIST:
            image = tk.PhotoImage(
                file=f'assets/playingCardImages/{elem}.png').subsample(4, 4)
            self.cards[elem] = image
        return

    def rebuildPlayerHand(self, new_player_data):
        self._make_player_frame(new_player_data)
        self._make_controls_panel(new_player_data.getValidActions())

    def updateScore(self, score):
        self._make_info_box(score)

    def rebuildDealerHand(self, new_dealer_data):
        self._make_dealer_frame(new_dealer_data)
        return
