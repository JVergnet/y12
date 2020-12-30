#!/usr/bin/env python3

import random
import tkinter as tk
from tkinter import messagebox, Frame, ttk
from tkinter.ttk import Button


LARGE_FONT = ("Verdana", 12)


def get_total_value(cards):
    total_value = 0
    for card in cards:
        total_value += card.value
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
        "decks of 54 cards"
        decklist = [n+1 for n in range(10)]  # number
        decklist += [11 for _ in range(4)]  # royal figures
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
    def __init__(self, parent_frame, number, visible=True):
        self.visible = visible
        self.value = number

        # if card is invisible (dealer hand) display a "?"
        card_text = "{}".format(self.value) if self.visible else "?"

        # create the visual object (Frame) for the card
        self.label = tk.Label(parent_frame,
                              text=card_text,
                              font=LARGE_FONT,
                              highlightbackground="black",
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
        self.label.config(text=str(self.value))

    def delete_card(self):
        "delete the visual contained for the card (Frame)"
        self.label.pack_forget()
        self.label.destroy()


def Help():
    "Call for help"
    tk.messagebox.showinfo(
        'Looking for help ?',
        "Ask God \nor  Mr. Preston, \nthey'll know")


class ReadRun_app(tk.Tk):

    def __init__(self, *args, **kwargs):

        # Initialize global FRAME =============
        tk.Tk.__init__(self, *args, **kwargs)
        # tk.Tk.iconbitmap(self, default = "CDF.ico")
        tk.Tk.wm_title(self, "BlackJack app")
        self.minsize(500, 500)

        app_page = Frame(self)
        app_page.pack(side="top", fill="both", expand=True,
                      padx=10,
                      pady=10)

        self.dealer_cards = []
        self.dealer_hand_value = 0

        self.cards = []
        self.user_hand_value = 0

        # top frame : hand values ====================
        self.top_frame = tk.Frame(app_page)
        self.top_frame.pack(fill=tk.BOTH, expand=True,
                            padx=10,
                            pady=10)

        # top frame left : dealer hand value ====================
        self.dealer_frame = tk.Frame(self.top_frame)
        self.dealer_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        self.dealer_label = tk.Label(
            self.dealer_frame,
            text="DEALER HAND",
            font=LARGE_FONT)
        self.dealer_label.pack(fill=tk.BOTH, expand=True)  # print "North"

        self.dealer_hand_frame = tk.Frame(self.dealer_frame)
        self.dealer_hand_frame.pack(fill=tk.BOTH, expand=True)

        # top frame right : user hand value ====================
        self.user_label = tk.Label(
            self.top_frame,
            text="",
            font=LARGE_FONT)
        self.user_label.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # mid frame  =  user cards ==============================
        self.mid_frame = tk.Frame(app_page)
        self.mid_frame.pack(fill=tk.BOTH, expand=True)

        # bottom frame  =  SELECTION buttons ========
        self.bottom_frame = tk.Frame(app_page)
        self.bottom_frame.pack(fill=tk.BOTH, expand=True)
        self.buttons = {}
        for button_name, function in [
                ("NEW CARD", self.get_new_card),
                ("CHECK", self.check),
                ("NEW GAME", self.new_game)]:
            self.buttons[button_name] = ttk.Button(
                self.bottom_frame,
                text=button_name,
                command=function)
            self.buttons[button_name].pack(
                fill=tk.BOTH,
                expand=True,
                side=tk.LEFT,
                padx=10,
                pady=10)

        self.deck = Deck()
        self.new_game()

    def enable_buttons(self, enabled):
        "Enable or disble new card and check buttons"
        for button_name in ["NEW CARD", "CHECK"]:
            state = "normal" if enabled else "disabled"
            self.buttons[button_name]["state"] = state

    def update_user_hand(self):
        "Check the value of the player's hand and trigger loss if >21"
        if self.user_hand_value <= 21:
            self.user_label.config(
                text="user hand \n {}".format(self.user_hand_value))
        else:
            self.do_you_win(False)

    def do_you_win(self, win):
        "change label accordingly"
        text = "YOU WIN !" if win else "YOU LOSE !"
        self.user_label.config(text=text)
        self.enable_buttons(False)

    def get_new_card(self):
        "get new card to player, update the display"
        # if self.user_hand_value <= 21:
        self.cards.append(Card(self.mid_frame, self.deck.draw_card()))
        self.user_hand_value = get_total_value(self.cards)
        self.update_user_hand()

    def check(self):
        """
        compare dealer and user cards values 
        """
        # make dealer cards visible
        for card in self.dealer_cards:
            card.make_visible()

        # check if dealer has lost
        if self.user_hand_value > 21:
            self.do_you_win(False)
        elif self.dealer_hand_value > 21:
            self.do_you_win(True)
        else:
            # check if you have won
            self.do_you_win(self.dealer_hand_value < self.user_hand_value)

    def get_dealer_hand(self):
        "simple 'stay below 17' strategy"
        while self.dealer_hand_value <= 17:
            self.dealer_cards.append(
                Card(self.dealer_hand_frame,
                     self.deck.draw_card(),
                     visible=False))
            self.dealer_hand_value = get_total_value(
                self.dealer_cards)

    def new_game(self):
        for card in self.cards + self.dealer_cards:
            card.delete_card()

        self.deck.reset_deck()

        self.dealer_cards = []
        self.dealer_hand_value = 0
        self.get_dealer_hand()

        self.cards = []
        self.user_hand_value = 0
        self.get_new_card()
        self.get_new_card()

        self.enable_buttons(True)


def create_menu():
    menubar = tk.Menu(app)

    menu_file = tk.Menu(menubar, tearoff=0)
    menu_file.add_command(label="Help", command=Help)
    menu_file.add_separator()
    menu_file.add_command(label="Quit", command=app.quit)
    menubar.add_cascade(label="File", menu=menu_file)

    menu_help = tk.Menu(menubar, tearoff=0)
    menu_help.add_command(label="Help !", command=Help)
    menubar.add_cascade(label="Help", menu=menu_help)
    return menubar


if __name__ == "__main__":

    app = ReadRun_app()

    app.config(menu=create_menu())

    app.mainloop()
