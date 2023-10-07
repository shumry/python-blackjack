def getNumberValueFromCard(display_card):
    split_val = display_card.split("_")
    if (split_val[0] in ["j", "q", "k"]):
        return 10
    else:
        return int(split_val[0])