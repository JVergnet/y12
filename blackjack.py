import random


def get_card():
    return random.randint(1, 11)


def player_turn():
    print("")
    cards = [get_card(), get_card()]

    print("cards", cards, "total value", get_total_value(cards))
    get_new_card(cards)
    return cards


def get_new_card(cards):
    while get_total_value(cards) <= 21:
        try:
            if input("draw_card ? [y]")[0] == "y":
                cards.append(get_card())
                print("cards", cards, "total value", get_total_value(cards))
            else:
                break
        except Exception:
            break
    return cards


def dealer_turn():
    cards = [get_card(), get_card()]

    while get_total_value(cards) <= 17:
        cards.append(get_card())
    print("dealer :", get_total_value(cards))
    return cards


if __name__ == "__main__":

    while True:
        player_cards = player_turn()
        if get_total_value(player_cards) > 21:
            print("lose")
        dealer_cards = dealer_turn()
        if get_total_value(dealer_cards) > 21:
            print("win")
        if get_total_value(player_cards) > get_total_value(dealer_cards):
            print("win")
        else:
            print("lose")

        try:
            if input("keep playing ? [y]")[0] != "y":
                break
        except Exception:
            break
