import tkinter as tk
from tkinter import ttk
import config.viewConfig as config

class View(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.c = controller
        self.cards = {}
        self.initCards()
        self.initData()
        self._make_background()
        self._make_dealer_frame()
        self._make_player_frame(self.player_hand)
        self._make_info_box()
        self._make_controls_panel()

    def main(self):
        self.mainloop()

    def initData(self):
        self.player_hand = []
        self.dealer_hand = []
    
    def _make_background(self):
        self.geometry(config.WINDOW_DIMENSIONS)
        self.title(config.WINDOW_TITLE)
        self.configure(bg=config.BACKGROUND_COLOR)
        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        return
    
    def _make_dealer_frame(self):
        self.dealer_frame = ttk.Frame(self)
        self.dealer_frame.grid(row=0, column=0, sticky="nsew")

        headerText = ttk.Label(self.dealer_frame, text="Dealer's Hand: ")
        headerText.pack()
        card_frame = ttk.Frame(self.dealer_frame)

        for i in range(2):
            image_label = tk.Label(card_frame, image=self.cards["8_h"])
            image_label.pack(side = "left", anchor="center")

        card_frame.pack()

        scoreText = ttk.Label(self.dealer_frame, text=f"Current Score: {str(12)}")
        scoreText.pack()
        return

    def _make_player_frame(self, player_hand):
        self.player_frame = ttk.Frame(self)

        self.player_frame.grid(row=1, column=0, sticky="nsew")

        text = ttk.Label(self.player_frame, text="Player's Hand: ")
        text.pack()
        
        card_frame = ttk.Frame(self.player_frame)

        for display_card in player_hand:
            image_label = tk.Label(card_frame, image=self.cards[display_card])
            image_label.pack(side = "left")
        card_frame.pack()

        scoreText = ttk.Label(self.player_frame, text=f"Current Score: {str(12)}")
        scoreText.pack()
        return

    def _make_info_box(self):
        self.info_box_frame = ttk.Frame(self)
        self.info_box_frame.grid(row=0, column=1, sticky="nsew")
        return

    def _make_controls_panel(self):
        self.controls_panel_frame = ttk.Frame(self)
        self.controls_panel_frame.grid(row=1, column=1, sticky="nsew")

        text = ttk.Label(self.controls_panel_frame, text="Actions:")
        text.pack(pady=(10,0))
        
        buttons_frame = ttk.Frame(self.controls_panel_frame)

        player_actions = ["Hit", "Cheat", "Cry"]

        for action in player_actions:
            def func_to_run(x = action):
                return self.c.handlePlayerAction(x)

            button_dict = ttk.Button(self.controls_panel_frame, text = action, command = func_to_run)
            button_dict.pack() 
        
        buttons_frame.pack()
        return

    def _make_card(self, parent_frame, card_text="7_h"):
        return

    def initCards(self):
        for elem in config.CARD_LIST:
            image = tk.PhotoImage(file=f'assets/playingCardImages/{elem}.png').subsample(4,4)
            self.cards[elem] = image
        # card_drawing = tk.Canvas(parent_frame, width=60, height=90, bg="white")
        # card_drawing.pack(padx=10, pady=10)
        # card_drawing.create_rectangle(0, 0, 60, 90, fill="white", outline="black", width=2)
        # card_drawing.create_text(50, 75, text=card_text, font=("Arial", 24), fill="black")
        return
    
    def rebuildPlayerHand(self, new_player_data):
        self.player = new_player_data
        print(new_player_data)
        self._make_player_frame(new_player_data)
