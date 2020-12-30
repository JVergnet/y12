#!/usr/bin/env python3

import random
import tkinter as tk
from tkinter import messagebox, Frame, ttk, Grid
from tkinter.ttk import Button


LARGE_FONT = ("Verdana", 12)


def get_total_value(cards):
    total_value = 0
    for card in cards:
        total_value += card.get_value()
    return total_value


class Deck():
    """
    all functions to make a realist deck
    """

    def __init__(self, n_decks=1):
        """
        with n identical decks
        nb : spanish 21 rules plays with 6 decks
        """
        self.initial_deck = []
        self.remaining_deck = []
        for _ in range(n_decks):
            self.initial_deck += self.create_one_deck()
        print(self.initial_deck)

        self.reset_deck()

    def create_one_deck(self):
        "decks of 52 cards = 4 families of 13 cards"
        family = [n+1 for n in range(10)]  # numbers
        family += ["J", "Q", "K"]  # royal figures
        decklist = family+family+family+family
        return decklist

    def reset_deck(self):
        "all cards back to deck and shuffle"
        # do a "sacrificial copy"
        # to be modified while the original stay intact
        self.remaining_deck = self.initial_deck.copy()
        random.shuffle(self.remaining_deck)

    def draw_card(self):
        "remain card from current (shuffled) deck"
        return self.remaining_deck.pop()


class Card():
    def __init__(self, parent_frame, symbol, visible=True):
        self.visible = visible
        self.symbol = symbol

        # if card is invisible (dealer hand) display a "?"
        card_text = "{}".format(self.symbol) if self.visible else "?"
        card_color = '#856ff8' if visible else "#6ff8ad"
        # create the visual object (Frame) for the card
        self.label = tk.Label(parent_frame,
                              bg=card_color,
                              text=card_text,
                              font=("Verdana", 24),
                              highlightbackground=card_color,
                              highlightthickness=1)
        # say where the object if placed (here side by side)
        self.label.pack(fill=tk.BOTH,
                        expand=True,
                        side=tk.LEFT,
                        padx=10,
                        pady=10)

    def make_visible(self):
        """
        when card is make visible (after check)
        the "?" is replaced by the actual number
        """
        self.label.config(text=str(self.symbol))

    def get_value(self):
        if type(self.symbol) is int:
            return self.symbol
        else:
            return 11

    def delete_card(self):
        "delete the visual contained for the card (Frame)"
        self.label.pack_forget()
        self.label.destroy()


class ReadRun_app(tk.Tk):

    def __init__(self, *args, **kwargs):

        # Initialize global FRAME =============
        tk.Tk.__init__(self, *args, **kwargs)
        self.initializing_window()

        # INITIALIZING THE GAME LOGIC !
        self.dealer_cards = []
        self.dealer_hand_value = 0
        self.cards = []
        self.user_hand_value = 0

        self.deck = Deck()  # instantiation of Deck
        self.new_game()

    def initializing_window(self):
        # tk.Tk.iconbitmap(self, default = "CDF.ico")
        tk.Tk.wm_title(self, "BlackJack app")
        self.minsize(500, 500)

        # top left : dealer hand value, seperated in 2
        self.dealer_label = tk.Label(self,
                                     text="DEALER HAND",
                                     font=LARGE_FONT)
        self.dealer_label.grid(row=0, column=0,
                               sticky="SWE")

        self.dealer_hand_frame = tk.Frame(self)
        self.dealer_hand_frame.grid(row=1, column=0,
                                    sticky="NSWE")

        # right : user hand value ====================
        self.win_label = tk.Label(self, text="",
                                  font=LARGE_FONT)
        self.win_label.grid(row=0, rowspan=2, column=1, sticky="NSWE")

        # mid frame  =  container for user cards =========
        self.user_label = tk.Label(self,
                                   text="USER HAND",
                                   font=LARGE_FONT)
        self.user_label.grid(row=2, column=1,
                             sticky="WSE")
        self.user_hand = tk.Frame(self)
        self.user_hand.grid(row=3,
                            column=0, columnspan=2,  sticky="NSWE")

        # bottom frame  =  container for buttons ========
        self.button_container = tk.Frame(self)
        self.button_container.grid(
            row=4, column=0, columnspan=2,  sticky="NSWE")
        self.buttons = {}
        for button_name, function in [
                ("NEW CARD", self.get_new_card),
                ("CHECK", self.check),
                ("NEW GAME", self.new_game)]:
            self.buttons[button_name] = ttk.Button(
                self.button_container,
                text=button_name,
                command=function)
            self.buttons[button_name].pack(fill=tk.BOTH,
                                           expand=True, side=tk.LEFT,
                                           padx=10, pady=10)

        # give a weight to the grid elements, allowing resizing
        for row, weight in zip(range(5), [0, 2, 0, 2, 2]):
            Grid.rowconfigure(self, row, weight=weight)
        for y in range(self.grid_size()[0]):
            Grid.columnconfigure(self, y, weight=1)

    def enable_buttons(self, enabled):
        "Enable or disble new card and check buttons"
        for button_name in ["NEW CARD", "CHECK"]:
            state = "normal" if enabled else "disabled"
            self.buttons[button_name]["state"] = state

    def display_winner(self, winner, busted=False):
        "change label accordingly"

        if winner == "user":
            fg = "green"
            if busted:
                text = "dealer got \n BUSTED !"
            else:
                text = "YOU WIN !"
        else:
            fg = "red"
            if busted:
                text = "YOU got \n BUSTED !"
            else:
                text = "YOU LOSE !"
        self.win_label.config(text=text, fg=fg)
        self.enable_buttons(False)

    def get_new_card(self):
        "get new card to player, update the display"
        # if self.user_hand_value <= 21:
        self.cards.append(
            Card(self.user_hand, self.deck.draw_card()))
        self.user_hand_value = get_total_value(self.cards)
        self.user_label.config(
            text="USER HAND : {}".format(self.user_hand_value))
        if self.user_hand_value > 21:
            self.display_winner("dealer", busted=True)

    def check(self):
        """
        compare dealer and user hands
        """
        self.get_dealer_hand()

        # check if dealer has lost
        user = self.user_hand_value
        dealer = self.dealer_hand_value

        if dealer > 21:
            self.display_winner("user", busted=True)
        elif dealer < user:
            # check if you have won
            self.display_winner("user")
        elif dealer > user:
            # check if you have won
            self.display_winner("dealer")
        elif dealer == user:
            # TODO : implement figure comparison
            self.display_winner("user")

    def get_dealer_hand(self):
        "simple 'stay below 17' strategy"
        self.dealer_hand_value = get_total_value(
            self.dealer_cards)
        while self.dealer_hand_value <= 17:
            self.dealer_cards.append(
                Card(self.dealer_hand_frame,
                     self.deck.draw_card(),
                     visible=False))
            self.dealer_hand_value = get_total_value(
                self.dealer_cards)

        for card in self.dealer_cards:
            card.make_visible()
        self.dealer_label.config(
            text="DEALER HAND : {}".format(self.dealer_hand_value))

    def get_dealer_initial_hand(self):
        "initial dealer hand : on face up and one face down"
        for _ in range(2):
            self.dealer_cards.append(
                Card(self.dealer_hand_frame,
                     self.deck.draw_card(),
                     visible=False))
        self.dealer_cards[0].make_visible()
        self.dealer_label.config(
            text="DEALER HAND")

    def initialize_game(self, parameter_list):
        """
        docstring
        """
        pass

    def new_game(self):
        "remove existing game and start new game"
        # visual element reset
        for card in self.cards + self.dealer_cards:
            card.delete_card()
        self.win_label.config(text="")
        self.enable_buttons(True)

        # game logic reset
        self.deck.reset_deck()

        self.cards = []
        self.user_hand_value = 0
        self.get_new_card()
        self.get_new_card()

        self.dealer_cards = []
        self.dealer_hand_value = 0
        self.get_dealer_initial_hand()

# MENU CREATION WITH ASSOCIATED FUNCTIONS ======


def create_menu():
    "self-explanatory tile..."

    # main widget
    menubar = tk.Menu()

    # 1st object : create a cascade under the word "file"
    menu_file = tk.Menu(menubar, tearoff=0)
    menu_file.add_command(label="Quit", command=app.quit)
    menubar.add_cascade(label="File", menu=menu_file)

    # 2nd object : create a cascade under the word "Help"
    menu_help = tk.Menu(menubar, tearoff=0)
    menu_help.add_command(label="Help !", command=Help)
    menu_file.add_separator()
    menu_help.add_command(label="Rules", command=rules)
    menubar.add_cascade(label="Help", menu=menu_help)

    return menubar


def Help():
    "Call for help"
    tk.messagebox.showinfo(
        'Looking for help ?',
        "Ask God \nor  Mr. Preston, \nthey'll know")


def rules():
    "prints the rules"
    tk.messagebox.showinfo(
        'here ar the rules',
        """

The dealer shuffles the cards and draws two cards, laying one face up and the second face down on the table. Next, the dealer draws two cards for each player and lays both face up.

After all of the players have received their cards, the game proceeds clockwise from the dealer's left. Each player may request an additional card from the dealer. This is known as a "hit." There is no limit to the number of hits that a player may request, so long as the total does not exceed 21. Players may also "stand," or decline additional cards. An exact total of 21 is considered an automatic victory.

Once all of the players have either stood or exceeded a total of 21, known as going "bust," the dealer reveals the card that he or she laid face down at the beginning of the game.The dealer must hit until his total is at least 17, and may go bust. Players who did not bust win the hand if their total is higher than the dealer's or if the dealer goes bust. It is considered a draw if the dealer and player have the same score.

""")


# the ACTUAL bit of code that is executed
if __name__ == "__main__":

    # create the page with all the widgets
    app = ReadRun_app()
    # add the menu
    app.config(menu=create_menu())

    # infinite loop waiting for the user to interact
    # until he/she quits the app
    app.mainloop()
