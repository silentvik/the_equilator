from funcs_jit import card_strength, strength_to_card


def range_converter(humanrange):
    # my very first function :) right after hello world.
    # it started my programming journey.
    # I'm saving it for history close to its original form
    #   (not counting uncharitable refactoring from black (very sad),
    #   adding JIT to funcs 'card_strength', 'strength_to_card',
    #   some refactoring in the first week of training)
    # Oh, and the effort was spent on it at that moment...
    """
        converts basic range (string, no weigths) to range-list.
        the input should be primarily after copying the text-range from 'pokerstrategy equilab'
    """

    def make_suits_for_pocket(pocket):
        # print('pocket = ', pocket)
        pockets_list = []
        suits1 = ["h", "d", "c", "s"]
        suits2 = ["h", "d", "c", "s"]
        for suit1 in suits1:
            suits2.remove(suit1)
            for suit2 in suits2:
                pockets_list.append(str(pocket) + suit1 + str(pocket) + suit2)
        return pockets_list

    def make_suits_for_XYo(x, y):
        cards_list = []
        suits1 = ["h", "d", "c", "s"]
        suits2 = ["h", "d", "c", "s"]
        z = 0
        for suit1 in suits1:
            suits2.remove(suit1)
            for suit2 in suits2:
                cards_list.append(str(x) + suit1 + str(y) + suit2)
            suits2.insert(z, suit1)
            z += 1
        return cards_list

    def make_suits_for_XYs(x, y):
        tempolist = []
        for suit in ["h", "d", "c", "s"]:
            tempolist.append(x + suit + y + suit)
        return tempolist

    possible_ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]

    if humanrange in ["any two", "anytwo", "случайный", "any2"]:
        humanrange = (
            "22+,A2s+,K2s+,Q2s+,J2s+,T2s+,92s+,82s+,72s+,62s+,52s+,"
            "42s+,32s+,A2o+,K2o+,Q2o+,J2o+,T2o+,92o+,82o+,72o+,62o+,52o+,42o+,32o+"
        )
    elif humanrange == "ofsuit":
        humanrange = "A2o+,K2o+,Q2o+,J2o+,T2o+,92o+,82o+,72o+,62o+,52o+,42o+,32o+"
    elif humanrange == "suit":
        humanrange = "A2s+,K2s+,Q2s+,J2s+,T2s+,92s+,82s+,72s+,62s+,52s+,42s+,32s+"
    elif humanrange == "pockets":
        humanrange = "22+"

    # удаление пробелов:
    text = ""
    for symbol in humanrange:
        if symbol in [
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "T",
            "J",
            "Q",
            "K",
            "A",
            "h",
            "d",
            "c",
            "s",
            "+",
            "-",
            ",",
            "o",
        ]:
            text += symbol
    humanrange = text

    if "," not in humanrange and len(humanrange) == 6:
        flop1 = str(list(humanrange)[0]) + str(list(humanrange)[1])
        flop2 = str(list(humanrange)[2]) + str(list(humanrange)[3])
        flop3 = str(list(humanrange)[4]) + str(list(humanrange)[5])
        return [flop1, flop2, flop3]
    elif "," not in humanrange and len(humanrange) == 8:
        flop1 = str(list(humanrange)[0]) + str(list(humanrange)[1])
        flop2 = str(list(humanrange)[2]) + str(list(humanrange)[3])
        flop3 = str(list(humanrange)[4]) + str(list(humanrange)[5])
        turn = str(list(humanrange)[6]) + str(list(humanrange)[7])
        return [flop1, flop2, flop3, turn]
    elif "," not in humanrange and len(humanrange) == 10:
        flop1 = str(list(humanrange)[0]) + str(list(humanrange)[1])
        flop2 = str(list(humanrange)[2]) + str(list(humanrange)[3])
        flop3 = str(list(humanrange)[4]) + str(list(humanrange)[5])
        turn = str(list(humanrange)[6]) + str(list(humanrange)[7])
        rvr = str(list(humanrange)[8]) + str(list(humanrange)[9])
        return [flop1, flop2, flop3, turn, rvr]

    new_list1 = humanrange.split(",")
    new_list2 = []
    for element in new_list1:
        try:
            if len(element) == 2:

                if list(element)[0] == list(element)[1]:
                    new_list2.extend(make_suits_for_pocket(list(element)[0]))
                else:
                    None
            elif len(element) == 3:

                if (
                    list(element)[2] == "+"
                    and list(element)[0] == list(element)[1]
                    and list(element)[0] in possible_ranks
                ):
                    lowest_pocket = card_strength(list(element)[0])
                    for every_pocket in range(
                        card_strength(lowest_pocket),
                        15
                    ):
                        new_list2.extend(
                            make_suits_for_pocket(
                                strength_to_card(every_pocket)
                            )
                        )
                elif list(element)[2] == "s":
                    new_list2.extend(
                        make_suits_for_XYs(list(element)[0], list(element)[1])
                    )
                elif list(element)[2] == "o":
                    new_list2.extend(
                        make_suits_for_XYo(list(element)[0], list(element)[1])
                    )

                else:
                    None
            elif len(element) == 4:
                if list(element)[3] == "+" and list(element)[2] == "o":
                    card_strength1 = card_strength(list(element)[0])
                    card_strength2 = card_strength(list(element)[1])
                    for kicker_int in range(card_strength2, card_strength1):
                        new_list2.extend(
                            make_suits_for_XYo(
                                list(element)[0], strength_to_card(kicker_int)
                            )
                        )
                elif list(element)[3] == "+" and list(element)[2] == "s":
                    card_strength1 = card_strength(list(element)[0])
                    card_strength2 = card_strength(list(element)[1])
                    for kicker_int in range(card_strength2, card_strength1):
                        new_list2.extend(
                            make_suits_for_XYs(
                                list(element)[0], strength_to_card(kicker_int)
                            )
                        )
                else:
                    str1 = card_strength(element[0])
                    str2 = card_strength(element[2])
                    if str1 > str2:
                        new_list2.append(element)
                    elif str1 < str2:
                        element = element[2:] + element[:2]
                        new_list2.append(element)
                    else:
                        suit1 = element[1]
                        suit2 = element[3]
                        x1, x2 = 0, 0
                        if suit1 == "h":
                            x1 = 4
                        elif suit1 == "d":
                            x1 = 3
                        elif suit1 == "c":
                            x1 = 2
                        else:
                            x1 = 1
                        if suit2 == "h":
                            x2 = 4
                        elif suit2 == "d":
                            x2 = 3
                        elif suit2 == "c":
                            x2 = 2
                        else:
                            x2 = 1

                        if x1 < x2:
                            element = element[2:] + element[:2]
                        new_list2.append(element)

            elif len(element) == 5 and list(element)[2] == "-":
                lowest_pocket = card_strength(list(element)[3])
                highest_pocket = card_strength(list(element)[0])
                for every_pocket in range(lowest_pocket, highest_pocket + 1):
                    new_list2.extend(
                        make_suits_for_pocket(strength_to_card(every_pocket))
                    )
            elif len(element) == 7 and list(element)[3] == "-":
                if list(element)[2] == "o":
                    kicker_strength1 = card_strength(list(element)[1])
                    kicker_strength2 = card_strength(list(element)[5])
                    for kicker_int in range(
                        kicker_strength2,
                        kicker_strength1 + 1
                    ):
                        new_list2.extend(
                            make_suits_for_XYo(
                                list(element)[0], strength_to_card(kicker_int)
                            )
                        )
                elif list(element)[2] == "s":
                    kicker_strength1 = card_strength(list(element)[1])
                    kicker_strength2 = card_strength(list(element)[5])
                    for kicker_int in range(
                        kicker_strength2,
                        kicker_strength1 + 1
                    ):
                        new_list2.extend(
                            make_suits_for_XYs(
                                list(element)[0], strength_to_card(kicker_int)
                            )
                        )
            else:
                None
        except Exception:
            pass

    new_list_3 = []
    for _, hand in enumerate(new_list2):
        if new_list_3.count(hand) == 0:
            new_list_3.append(hand)

    return new_list_3
