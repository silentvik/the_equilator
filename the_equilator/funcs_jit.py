import numpy as np
from numba import float32, njit, uint16, vectorize


@njit(cache=True)
def calculate_w_of_array(array, default_slot=2):
    """
        Available for nJIT.
        Calculates total weight of player's range. Returns it.
    """
    w = 0
    for h in range(len(array)):
        w += array[h][default_slot]
    return w


@njit(cache=True)
def from_string_to_numbers(string):
    """
        Available for nJIT.
        If will see a point in the text = returns float, else = int.
    """

    number = 0.0
    before_point_count = 0
    after_point_count = 0
    was_point = False
    for char in string:
        if char == ".":
            was_point = True
        elif (
            char == "0"
            or char == "1"
            or char == "2"
            or char == "3"
            or char == "4"
            or char == "5"
            or char == "6"
            or char == "7"
            or char == "8"
            or char == "9"
        ):
            if was_point is False:
                before_point_count += 1
            else:
                after_point_count += 1
    if before_point_count > 0:
        was_point = False
    if before_point_count + after_point_count == 0:
        print(
            "[from_string_to_numbers]\n     zero numbers detected in text. returned 0"
        )
        return 0

    after_point_counter = 1
    for char in string:
        if char == "." or before_point_count == 0:
            was_point = True
        if was_point is False:
            # if char=='0':
            #     continue
            if char == "1":
                number += 1 * 10 ** (before_point_count - 1)
                before_point_count -= 1
            elif char == "2":
                number += 2 * 10 ** (before_point_count - 1)
                before_point_count -= 1
            elif char == "3":
                number += 3 * 10 ** (before_point_count - 1)
                before_point_count -= 1
            elif char == "4":
                number += 4 * 10 ** (before_point_count - 1)
                before_point_count -= 1
            elif char == "5":
                number += 5 * 10 ** (before_point_count - 1)
                before_point_count -= 1
            elif char == "6":
                number += 6 * 10 ** (before_point_count - 1)
                before_point_count -= 1
            elif char == "7":
                number += 7 * 10 ** (before_point_count - 1)
                before_point_count -= 1
            elif char == "8":
                number += 8 * 10 ** (before_point_count - 1)
                before_point_count -= 1
            elif char == "9":
                number += 9 * 10 ** (before_point_count - 1)
                before_point_count -= 1
        if was_point is True:
            # if char=='0':
            #     continue
            if char == "1":
                number += 1 / (10 ** (after_point_counter))
                after_point_counter += 1
            elif char == "2":
                number += 2 / (10 ** (after_point_counter))
                after_point_counter += 1
            elif char == "3":
                number += 3 / (10 ** (after_point_counter))
                after_point_counter += 1
            elif char == "4":
                number += 4 / (10 ** (after_point_counter))
                after_point_counter += 1
            elif char == "5":
                number += 5 / (10 ** (after_point_counter))
                after_point_counter += 1
            elif char == "6":
                number += 6 / (10 ** (after_point_counter))
                after_point_counter += 1
            elif char == "7":
                number += 7 / (10 ** (after_point_counter))
                after_point_counter += 1
            elif char == "8":
                number += 8 / (10 ** (after_point_counter))
                after_point_counter += 1
            elif char == "9":
                number += 9 / (10 ** (after_point_counter))
                after_point_counter += 1
    if after_point_count == 0:
        number = int(number)

    return number


@njit(cache=True)
def card_strength(card):
    """
        Available for nJIT.
        Returns a certain sequential number of the card, based on a custom hierarchy
    """

    # переводит карты А, К и подобные в ЧИСЛА (int от 2 до 14)
    if card == "A":
        return 14
    elif card == "K":
        return 13
    elif card == "Q":
        return 12
    elif card == "J":
        return 11
    elif card == "T":
        return 10
    elif card == "9":
        return 9
    elif card == "8":
        return 8
    elif card == "7":
        return 7
    elif card == "6":
        return 6
    elif card == "5":
        return 5
    elif card == "4":
        return 4
    elif card == "3":
        return 3
    elif card == "2":
        return 2
    elif card == "h":
        return 4
    elif card == "d":
        return 3
    elif card == "c":
        return 2
    elif card == "s":
        return 1
    elif card == 14:
        return 14
    elif card == 13:
        return 13
    elif card == 12:
        return 12
    elif card == 11:
        return 11
    elif card == 10:
        return 10
    elif card == 9:
        return 9
    elif card == 8:
        return 8
    elif card == 7:
        return 7
    elif card == 6:
        return 6
    elif card == 5:
        return 5
    elif card == 4:
        return 4
    elif card == 3:
        return 3
    elif card == 2:
        return 2


@njit(cache=True)
def strength_to_card(strength):
    """
        Available for nJIT.
        From custom hierarchy to -> directly text view
    """

    if strength > 100:
        rank = strength // 10
        suit = strength % 10
        if rank == 24:
            rank = "A"
        elif rank == 23:
            rank = "K"
        elif rank == 22:
            rank = "Q"
        elif rank == 21:
            rank = "J"
        elif rank == 20:
            rank = "T"
        elif rank == 19:
            rank = "9"
        elif rank == 18:
            rank = "8"
        elif rank == 17:
            rank = "7"
        elif rank == 16:
            rank = "6"
        elif rank == 15:
            rank = "5"
        elif rank == 14:
            rank = "4"
        elif rank == 13:
            rank = "3"
        elif rank == 12:
            rank = "2"
        else:
            rank = "2"
        if suit == 4:
            suit = "h"
        elif suit == 3:
            suit = "d"
        elif suit == 2:
            suit = "c"
        else:
            suit = "s"
        return rank + suit
    else:
        if strength == 14:
            return "A"
        elif strength == 13:
            return "K"
        elif strength == 12:
            return "Q"
        elif strength == 11:
            return "J"
        elif strength == 10:
            return "T"
        elif strength == 9:
            return "9"
        elif strength == 8:
            return "8"
        elif strength == 7:
            return "7"
        elif strength == 6:
            return "6"
        elif strength == 5:
            return "5"
        elif strength == 4:
            return "4"
        elif strength == 3:
            return "3"
        elif strength == 2:
            return "2"


@njit(cache=True)
def jcard_strength(card):
    """
        Available for nJIT.
        Returns a certain sequential number of the card, based on a custom hierarchy.
        Works with a pair of cards.
    """

    rank = card[0]
    suit = card[1]
    r = 0
    s = 0
    if rank == "A":
        r = 240
    if rank == "K":
        r = 230
    if rank == "Q":
        r = 220
    if rank == "J":
        r = 210
    if rank == "T":
        r = 200
    if rank == "9":
        r = 190
    if rank == "8":
        r = 180
    if rank == "7":
        r = 170
    if rank == "6":
        r = 160
    if rank == "5":
        r = 150
    if rank == "4":
        r = 140
    if rank == "3":
        r = 130
    if rank == "2":
        r = 120
    if suit == "h":
        s = 4
    if suit == "d":
        s = 3
    if suit == "c":
        s = 2
    if suit == "s":
        s = 1
    return r + s


@njit(cache=True)
def convert_range_from_text_to_weighted_array(weighted_range_text):
    """
        Returns an array of numeric hands with weights from input
    """

    player_range_array = np.zeros((1326, 3), dtype=float32)
    text_temp = ""
    hand_number = 0
    for char in weighted_range_text:
        if char == "[" or char == "]" or char == "," or char == " ":
            continue
        elif char == "(":
            card1, card2 = text_temp[:2], text_temp[2:]
            card1, card2 = jcard_strength(card1), jcard_strength(card2)
            player_range_array[hand_number][0], player_range_array[hand_number][1] = (
                card1,
                card2,
            )
            text_temp = ""
        elif char == ")":
            w = from_string_to_numbers(text_temp)
            player_range_array[hand_number][2] = w
            text_temp = ""
            hand_number += 1
        else:
            text_temp += char

    weighted_hands_count = 0
    for h in range(len(player_range_array)):
        if player_range_array[h][2] > 0:
            weighted_hands_count += 1
    real_player_range_array = np.zeros((weighted_hands_count, 3), dtype=float32)
    current_hand_number = 0
    for h in range(len(player_range_array)):
        if player_range_array[h][2] != 0:
            real_player_range_array[current_hand_number] = player_range_array[h]
            current_hand_number += 1
    return real_player_range_array


@njit(cache=True)
def make_all_board_possible_cards_array():
    """
        creates 52-cards array and set default weigth, returns it
    """

    all_cards_array_with_weigth = np.ones((52, 4), dtype=uint16)
    for i in range(13):
        for j in range(4):
            all_cards_array_with_weigth[i * 4 + j][0] = i * 10 + 120 + j + 1
    return all_cards_array_with_weigth


@njit(cache=True)
def any_pair(r):
    """
        Returns the strength of a combination in which a pair may be present
    """
    r1, r2, r3, r4, r5, r6, r7 = r[0], r[1], r[2], r[3], r[4], r[5], r[6]
    if r1 != r2 and r2 != r3 and r3 != r4 and r4 != r5 and r5 != r6 and r6 != r7:
        return r1 * 28561 + r2 * 2197 + r3 * 169 + r4 * 13 + r5

    if r1 == r4:
        return 3150000 + r1 * 13 + r5

    elif r2 == r5 or r3 == r6 or r4 == r7:
        return 3150000 + r4 * 13 + r1

    else:
        if r1 == r3:
            if r4 == r5:
                return 2700000 + r1 * 13 + r4

            if r5 == r6 or r6 == r7:
                return 2700000 + r1 * 13 + r6

            return 1350000 + r1 * 169 + r4 * 13 + r5
        elif r2 == r4:
            if r5 == r6 or r6 == r7:
                return 2700000 + r2 * 13 + r6

            return 1350000 + r2 * 169 + r1 * 13 + r5

        elif r3 == r5:
            if r1 == r2:
                return 2700000 + r3 * 13 + r1

            if r6 == r7:
                return 2700000 + r3 * 13 + r6

            return 1350000 + r5 * 169 + r1 * 13 + r2
        elif r4 == r6:
            if r1 == r2 or r2 == r3:
                return 2700000 + r4 * 13 + r2

            return 1350000 + r5 * 169 + r1 * 13 + r2

        elif r5 == r7:
            if r1 == r2:
                return 2700000 + r5 * 13 + r1

            if r2 == r3 or r3 == r4:
                return 2700000 + r5 * 13 + r3

            return 1350000 + r5 * 169 + r1 * 13 + r2

        else:
            if r1 == r2:
                if r3 == r4:
                    return 900000 + r1 * 169 + r3 * 13 + r5

                if r4 == r5:
                    return 900000 + r1 * 169 + r4 * 13 + r3

                if r5 == r6 or r6 == r7:
                    return 900000 + r1 * 169 + r6 * 13 + r3

                return 450000 + r1 * 2197 + r3 * 169 + r4 * 13 + r5

            elif r2 == r3:
                if r4 == r5:
                    return 900000 + r2 * 169 + r4 * 13 + r1

                if r5 == r6 or r6 == r7:
                    return 900000 + r2 * 169 + r6 * 13 + r1

                return 450000 + r2 * 2197 + r1 * 169 + r4 * 13 + r5

            elif r3 == r4:
                if r5 == r6 or r6 == r7:
                    return 900000 + r3 * 169 + r6 * 13 + r1

                return 450000 + r3 * 2197 + r1 * 169 + r2 * 13 + r5

            elif r4 == r5:
                if r6 == r7:
                    return 900000 + r4 * 169 + r6 * 13 + r1

                return 450000 + r4 * 2197 + r1 * 169 + r2 * 13 + r3

            elif r5 == r6 or r6 == r7:
                return 450000 + r6 * 2197 + r1 * 169 + r2 * 13 + r3

            return r1 * 28561 + r2 * 2197 + r3 * 169 + r4 * 13 + r5


@njit(cache=True)
def current_strength_of_this_hand(zeros):
    """
        Counts and returns the final strength of the combination.
        Input - a special prepared data array with shape (5,7).
        This func contains a lot of repetitions, but it works faster with them than if you take them out separately.
    """
    # 0=cards(empty),1=r(empty),2=s(empty),3=ss(empty),4=full board

    board1 = zeros[4]
    (
        zeros[0][0],
        zeros[0][1],
        zeros[0][2],
        zeros[0][3],
        zeros[0][4],
        zeros[0][5],
        zeros[0][6],
    ) = (board1[0], board1[1], board1[2], board1[3], board1[4], board1[5], board1[6])
    cards = zeros[0]
    for i in range(7):
        for j in range(i + 1, 7):
            if cards[i] > cards[j]:
                cards[i], cards[j] = cards[j], cards[i]
    cards = np.flip(cards)
    r = zeros[1]
    r[0], r[1], r[2], r[3], r[4], r[5], r[6] = (
        int(cards[0] / 10 - 10),
        int(cards[1] / 10 - 10),
        int(cards[2] / 10 - 10),
        int(cards[3] / 10 - 10),
        int(cards[4] / 10 - 10),
        int(cards[5] / 10 - 10),
        int(cards[6] / 10 - 10),
    )
    s = zeros[2]

    s[0], s[1], s[2], s[3], s[4], s[5], s[6] = (
        cards[0] - r[0] * 10,
        cards[1] - r[1] * 10,
        cards[2] - r[2] * 10,
        cards[3] - r[3] * 10,
        cards[4] - r[4] * 10,
        cards[5] - r[5] * 10,
        cards[6] - r[6] * 10,
    )

    ss = zeros[3]  # можно и по-раньше это сделать
    if s[4] > 0:
        ss[0], ss[1], ss[2], ss[3], ss[4], ss[5], ss[6] = (
            s[0],
            s[1],
            s[2],
            s[3],
            s[4],
            s[5],
            s[6],
        )
        for i in range(7):
            for j in range(i + 1, 7):
                if ss[i] > ss[j]:
                    ss[i], ss[j] = ss[j], ss[i]

    # оценка силы

    pair_str1 = any_pair(r)

    # print('pair_str1 = ',pair_str1)
    if s[4] > 0:
        str1 = 0
        if ss[0] == ss[4] or ss[1] == ss[5] or ss[2] == ss[6]:
            suit = ss[2]
            count = 0
            for i in range(7):
                if s[i] == suit:
                    ss[count] = r[i]
                    count += 1

            x1, x2, x3, x4, x5 = ss[0], ss[1], ss[2], ss[3], ss[4]
            if x4 - x5 != 1:
                str1 = 2250000 + x1 * 28561 + x2 * 2197 + x3 * 169 + x4 * 13 + x5
            elif count == 5:
                if x1 - x2 == x2 - x3 == x3 - x4 == x4 - x5 == 1:
                    return 3600000 + x1
                else:
                    if x1 == 14 and x2 - x3 == x3 - x4 == x4 - x5 == x5 - 1 == 1:
                        return 3600000 + x2
                    else:
                        str1 = (
                            2250000 + x1 * 28561 + x2 * 2197 + x3 * 169 + x4 * 13 + x5
                        )
            elif count == 6:
                x6 = ss[5]
                if x1 - x2 == x2 - x3 == x3 - x4 == x4 - x5 == 1:
                    return 3600000 + x1
                if x5 - x6 == x2 - x3 == x3 - x4 == x4 - x5 == 1:
                    return 3600000 + x2
                else:
                    if x1 == 14 and x3 - x4 == x4 - x5 == x5 - x6 == x6 - 1 == 1:
                        return 3600000 + x3
                    else:
                        str1 = (
                            2250000 + x1 * 28561 + x2 * 2197 + x3 * 169 + x4 * 13 + x5
                        )
            elif count == 7:
                x6 = ss[5]
                x7 = ss[6]
                if x1 - x2 == x2 - x3 == x3 - x4 == x4 - x5 == 1:
                    return 3600000 + x1
                if x5 - x6 == x2 - x3 == x3 - x4 == x4 - x5 == 1:
                    return 3600000 + x2
                if x5 - x6 == x6 - x7 == x3 - x4 == x4 - x5 == 1:
                    return 3600000 + x3
                else:
                    if x1 == 14 and x4 - x5 == x5 - x6 == x6 - x7 == x7 - 1 == 1:
                        return 3600000 + x4
                    else:
                        str1 = (
                            2250000 + x1 * 28561 + x2 * 2197 + x3 * 169 + x4 * 13 + x5
                        )
            else:
                str1 = 2250000 + x1 * 28561 + x2 * 2197 + x3 * 169 + x4 * 13 + x5

            # str1=j_is_strtfl_or_fl(r,s,ss)
        if str1 > pair_str1:
            return str1

    if pair_str1 > 2250000:
        return pair_str1

    # раз флаша нету и фулла тоже - то проверяем на стрит
    count = 0
    ss[0] = r[0]
    for i in range(6):
        if r[i] != r[i + 1]:
            ss[count] = r[i]
            count += 1
    ss[count] = r[6]
    r1, r2, r3, r4, r5, r6, r7 = ss[0], ss[1], ss[2], ss[3], ss[4], ss[5], ss[6]
    if r1 != 14 and r3 != r4 and r3 - r4 != 1:
        return pair_str1
    elif r1 - r2 == r2 - r3 == r3 - r4 == r4 - r5 == 1:
        return 1800000 + r1
    elif r2 - r3 == r3 - r4 == r4 - r5 == r5 - r6 == 1:
        return 1800000 + r2
    elif r3 - r4 == r4 - r5 == r5 - r6 == r6 - r7 == 1:
        return 1800000 + r3
    elif r1 == 14:
        if r2 - r3 == r3 - r4 == r4 - r5 == r5 - 1 == 1:
            return 1800000 + r2
        elif r3 - r4 == r4 - r5 == r5 - r6 == r6 - 1 == 1:
            return 1800000 + r3
        elif r4 - r5 == r5 - r6 == r6 - r7 == r7 - 1 == 1:
            return 1800000 + r4
        else:
            return pair_str1
    else:
        return pair_str1


@njit(cache=True)
def find_each_equity_turn(
    hero_range_array,
    opps_range_array,
    hero_rivers_strength,
    opps_rivers_strength,
    basic_turns_paired_matrix,
):
    """
        Calculates an equity on every turn and writes it.
        Returns None
    """

    turns_count = len(basic_turns_paired_matrix)
    range_len_hr = range(len(hero_range_array))
    range_len_or = range(len(opps_range_array))
    range_48 = range(48)
    for k in range(turns_count):
        for i in range_len_hr:
            for j in range_len_or:
                if basic_turns_paired_matrix[k][i][j] < 0:
                    continue
                eq = 0
                games = 44
                for k2 in range_48:
                    str1 = hero_rivers_strength[k][k2][i]
                    str2 = opps_rivers_strength[k][k2][j]
                    if str1 == 0 or str2 == 0:
                        continue
                    if str1 > str2:
                        eq += 1
                    elif str1 == str2:
                        eq += 0.5
                basic_turns_paired_matrix[k][i][j] = eq / games

    return


@njit(cache=True)
def translate_abstractions_flop(
    basic_flop_paired_matrix, basic_turns_paired_matrix, turns
):
    turns_count = len(basic_turns_paired_matrix)
    r_turns_count = range(turns_count)

    for i in r_turns_count:
        basic_flop_paired_matrix = vectorized_summ_matrix(
            basic_flop_paired_matrix, basic_turns_paired_matrix[i]
        )
    played_turns = turns_count - 4
    for h1 in range(len(basic_flop_paired_matrix)):
        for h2 in range(len(basic_flop_paired_matrix[0])):
            if basic_flop_paired_matrix[h1][h2] < 0:
                continue
            basic_flop_paired_matrix[h1][h2] = (
                basic_flop_paired_matrix[h1][h2] / played_turns
            )

    return basic_flop_paired_matrix


@njit(cache=True)
def convert_range_from_array_with_weigths(range_array):
    text = "["
    for i in range(len(range_array)):
        hand_string = ""
        if i > 0:
            hand_string += ","
        hand = range_array[i]
        card1, card2, w = int(hand[0]), int(hand[1]), int(hand[2])

        hand_string += strength_to_card(card1) + strength_to_card(card2)
        hand_string += "(" + str(w) + ")"
        text += hand_string
    text += "]"
    return text


@vectorize(cache=True)
def vectorized_summ_matrix(a, b):
    """
        A very specialized sum of matrices
    """
    if b < 0:
        return a
    elif a < 0:
        return a
    return a + b


@njit(cache=True)
def convert_char_to_float_array(char_array):
    """
        Converts array full of hand names to numeric array with default weight = 1.
        Returns a new array
    """

    float_array = np.empty((len(char_array), 3), dtype=float32)
    for i in range(len(char_array)):
        card1, card2 = (
            char_array[i][0] + char_array[i][1],
            char_array[i][2] + char_array[i][3],
        )
        jcard1, jcard2 = jcard_strength(card1), jcard_strength(card2)
        float_array[i][0], float_array[i][1] = jcard1, jcard2
        float_array[i][2] = 1
    return float_array
