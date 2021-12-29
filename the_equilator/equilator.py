import numpy as np
from numba import float32, njit, uint8, uint16, uint32

from data_getter import DataGetter
from exceptions import EquilatorError
from funcs_jit import (current_strength_of_this_hand, find_each_equity_turn,
                       make_all_board_possible_cards_array, strength_to_card,
                       translate_abstractions_flop)


class Equilator:
    """
        Contains functions for equity calculations.
    """

    # Note2: This is my first created class in my life with very few refactoring.
    # I apologize for many architectural and other mistakes. This is an example of bad but working code.
    # Now it's impossible to watch without tears, but it's also a pity to delete.

    all_cards = DataGetter.get_all_cards_list()
    all_paired_combos = DataGetter.get_all_paired_combos()
    full_preflop_matrix = DataGetter.load_preflop_matrix()

    @staticmethod
    @njit(cache=True)
    def make_equity_arrays(stage, OOP_range_array, IP_range_array, board):
        """
            Here we make arrays of equity / fill them up.
            Postflop only.
            Each stage needs its own approach.
            Contains alot of repetions,
            but splitting the function into smaller ones leads to faster compilation and slower execution
        """

        range_len_OOP = range(len(OOP_range_array))
        range_len_IP = range(len(IP_range_array))

        # flop
        if stage == 1:
            # 1. INITIALIZATION
            turns = np.ones((49, 2), dtype=uint8)
            flops = np.empty((3), dtype=uint8)
            all_cards_array_with_weigth = make_all_board_possible_cards_array()
            board_card1, board_card2, board_card3 = (
                int(board[0]),
                int(board[1]),
                int(board[2]),
            )
            flops[0], flops[1], flops[2] = board_card1, board_card2, board_card3
            suit1, suit2, suit3 = (
                board_card1 - int(board_card1 / 10) * 10,
                board_card2 - int(board_card2 / 10) * 10,
                board_card3 - int(board_card3 / 10) * 10,
            )

            index = 0
            for i in range(52):
                new_card = all_cards_array_with_weigth[i][0]
                if (
                    new_card == board_card1
                    or new_card == board_card2
                    or new_card == board_card3
                ):
                    continue
                turns[index][0] = new_card
                index += 1

            turns_count = len(turns)
            OOP_rivers_strength = np.zeros(
                (turns_count, 48, len(OOP_range_array)), dtype=uint32
            )
            IP_rivers_strength = np.zeros(
                (turns_count, 48, len(IP_range_array)), dtype=uint32
            )
            basic_flop_paired_matrix = np.zeros(
                (len(OOP_range_array), len(IP_range_array)), dtype=float32
            )  # include playability player vs player
            basic_turns_paired_matrix = np.zeros(
                (turns_count, len(OOP_range_array), len(IP_range_array)), dtype=float32
            )
            for i in range(len(OOP_range_array)):
                OOP_card1, OOP_card2 = OOP_range_array[i][0], OOP_range_array[i][1]
                for j in range(len(IP_range_array)):
                    IP_card1, IP_card2 = IP_range_array[j][0], IP_range_array[j][1]
                    if (
                        OOP_card1 == IP_card1
                        or OOP_card2 == IP_card1
                        or OOP_card1 == IP_card2
                        or OOP_card2 == IP_card2
                    ):
                        basic_flop_paired_matrix[i][j] = -1
                        for k in range(turns_count):
                            basic_turns_paired_matrix[k][i][j] = -1
                        continue

            rivers = np.zeros((turns_count, 48, 2), dtype=uint8)
            for i in range(turns_count):
                turn_card = turns[i][0]
                rvr_index = 0
                for j in range(52):
                    new_card = all_cards_array_with_weigth[j][0]
                    if (
                        new_card == board_card1
                        or new_card == board_card2
                        or new_card == board_card3
                        or new_card == turn_card
                    ):
                        continue
                    rivers[i][rvr_index][0] = new_card
                    rvr_index += 1

            data_massive_small = np.zeros((6, 7), dtype=uint8)
            (
                data_massive_small[5][0],
                data_massive_small[5][1],
                data_massive_small[5][2],
            ) = (suit1, suit2, suit3)
            (
                data_massive_small[4][0],
                data_massive_small[4][1],
                data_massive_small[4][2],
            ) = (board_card1, board_card2, board_card3)

            # 2. calculate strength of each hand

            for k2 in range(2):
                # k2 number is a numeric player position equivalent.
                # Used to define a player 0 or player 1
                len_r_a = len(OOP_range_array)
                len_ops_r_a = len(IP_range_array)
                range_array = OOP_range_array
                rivers_strength = OOP_rivers_strength
                if k2 == 1:
                    len_r_a, len_ops_r_a = len_ops_r_a, len_r_a
                    rivers_strength = IP_rivers_strength
                    range_array = IP_range_array
                for i in range(len_r_a):
                    h_card1, h_card2 = range_array[i][0], range_array[i][1]
                    data_massive_small[4][5], data_massive_small[4][6] = (
                        h_card1,
                        h_card2,
                    )
                    hc_suit1, hc_suit2 = (
                        h_card1 - int(h_card1 / 10) * 10,
                        h_card2 - int(h_card2 / 10) * 10,
                    )
                    data_massive_small[5][3], data_massive_small[5][4] = (
                        hc_suit1,
                        hc_suit2,
                    )
                    for j in range(turns_count):
                        b_card4 = turns[j][0]
                        if h_card1 == b_card4 or h_card2 == b_card4:
                            if k2 == 0:
                                for k in range(len_ops_r_a):
                                    basic_turns_paired_matrix[j][i][k] = -1
                            else:
                                for k in range(len_ops_r_a):
                                    basic_turns_paired_matrix[j][k][i] = -1
                            continue
                        data_massive_small[4][3] = b_card4

                        fd = 0
                        suit4 = b_card4 - int(b_card4 / 10) * 10
                        data_massive_small[5][5] = suit4
                        fd_suit = 0
                        fd_cards_count = 0
                        for k1 in range(1, 5):
                            count = 0
                            for k in range(6):
                                if data_massive_small[5][k] == k1:
                                    count += 1
                            if count > 3:
                                fd_suit = k1
                                fd = 1
                                fd_cards_count = count
                                break

                        if fd == 0:
                            old_river_rank = 0
                            str1 = 0
                            for k in range(48):
                                river_card = rivers[j][k][0]
                                if river_card == h_card1 or river_card == h_card2:
                                    rivers_strength[j][k][i] = 0
                                    continue
                                river_rank = int(river_card / 10) * 10
                                if river_rank == old_river_rank:
                                    rivers_strength[j][k][i] = str1
                                    continue
                                data_massive_small[4][4] = river_rank
                                old_river_rank = river_rank
                                str1 = current_strength_of_this_hand(data_massive_small)
                                rivers_strength[j][k][i] = str1

                        else:
                            old_river_rank = 0
                            str1 = 0
                            for k in range(48):
                                river_card = rivers[j][k][0]
                                if river_card == h_card1 or river_card == h_card2:
                                    rivers_strength[j][k][i] = 0
                                    continue
                                river_suit = river_card - int(river_card / 10) * 10
                                if river_suit == fd_suit or fd_cards_count > 4:
                                    data_massive_small[4][4] = river_card
                                    str2 = current_strength_of_this_hand(
                                        data_massive_small
                                    )
                                    rivers_strength[j][k][i] = str2
                                    continue

                                river_rank = int(river_card / 10) * 10
                                if river_rank == old_river_rank:
                                    rivers_strength[j][k][i] = str1
                                    continue
                                data_massive_small[4][4] = river_rank
                                old_river_rank = river_rank
                                str1 = current_strength_of_this_hand(data_massive_small)
                                rivers_strength[j][k][i] = str1

            # 3. CALC EQUITY

            find_each_equity_turn(
                OOP_range_array,
                IP_range_array,
                OOP_rivers_strength,
                IP_rivers_strength,
                basic_turns_paired_matrix,
                turns,
                basic_flop_paired_matrix,
            )
            basic_flop_paired_matrix = translate_abstractions_flop(
                basic_flop_paired_matrix, basic_turns_paired_matrix, turns
            )

            return basic_flop_paired_matrix, basic_turns_paired_matrix

        # turn
        elif stage == 2:
            # 1. INITIALIZATION
            board_card1, board_card2, board_card3 = (
                int(board[0]),
                int(board[1]),
                int(board[2]),
            )
            suit1, suit2, suit3 = (
                board_card1 - int(board_card1 / 10) * 10,
                board_card2 - int(board_card2 / 10) * 10,
                board_card3 - int(board_card3 / 10) * 10,
            )
            turns = np.ones((1, 2), dtype=uint8)
            turns[0] = int(board[3])
            turns_count = 1  # we are on the turn
            all_cards_array_with_weigth = make_all_board_possible_cards_array()
            OOP_rivers_strength = np.zeros(
                (turns_count, 48, len(OOP_range_array)), dtype=uint32
            )
            IP_rivers_strength = np.zeros(
                (turns_count, 48, len(IP_range_array)), dtype=uint32
            )
            main_paired_matrix = np.zeros(
                (len(OOP_range_array), len(IP_range_array)), dtype=float32
            )  # include playability player vs player
            side_paired_matrix = np.zeros(
                (48, len(OOP_range_array), len(IP_range_array)), dtype=float32
            )
            rivers = np.zeros((turns_count, 48, 2), dtype=uint8)
            for i in range(turns_count):
                turn_card = turns[i][0]
                rvr_index = 0
                for j in range(52):
                    new_card = all_cards_array_with_weigth[j][0]
                    if (
                        new_card == board_card1
                        or new_card == board_card2
                        or new_card == board_card3
                        or new_card == turn_card
                    ):
                        continue
                    rivers[i][rvr_index][0] = new_card
                    rvr_index += 1
            data_massive_small = np.zeros((6, 7), dtype=uint8)
            (
                data_massive_small[5][0],
                data_massive_small[5][1],
                data_massive_small[5][2],
            ) = (suit1, suit2, suit3)
            (
                data_massive_small[4][0],
                data_massive_small[4][1],
                data_massive_small[4][2],
            ) = (board_card1, board_card2, board_card3)

            # 2. calculate strength of each hand
            for k2 in range(2):
                # k2 number is a numeric player position equivalent.
                # Used to define a player 0 or player 1
                len_r_a = len(OOP_range_array)
                len_ops_r_a = len(IP_range_array)
                range_array = OOP_range_array
                rivers_strength = OOP_rivers_strength
                if k2 == 1:
                    len_r_a, len_ops_r_a = len_ops_r_a, len_r_a
                    rivers_strength = IP_rivers_strength
                    range_array = IP_range_array
                for i in range(len_r_a):
                    h_card1, h_card2 = range_array[i][0], range_array[i][1]
                    data_massive_small[4][5], data_massive_small[4][6] = (
                        h_card1,
                        h_card2,
                    )
                    hc_suit1, hc_suit2 = (
                        h_card1 - int(h_card1 / 10) * 10,
                        h_card2 - int(h_card2 / 10) * 10,
                    )
                    data_massive_small[5][3], data_massive_small[5][4] = (
                        hc_suit1,
                        hc_suit2,
                    )
                    for j in range(turns_count):
                        b_card4 = turns[j][0]
                        data_massive_small[4][3] = b_card4
                        fd = 0
                        suit4 = b_card4 - int(b_card4 / 10) * 10
                        data_massive_small[5][5] = suit4
                        fd_suit = 0
                        fd_cards_count = 0
                        for k1 in range(1, 5):
                            count = 0
                            for k in range(6):
                                if data_massive_small[5][k] == k1:
                                    count += 1
                            if count > 3:
                                fd_suit = k1
                                fd = 1
                                fd_cards_count = count
                                break

                        if fd == 0:
                            old_river_rank = 0
                            str1 = 0
                            for k in range(48):
                                river_card = rivers[j][k][0]
                                if river_card == h_card1 or river_card == h_card2:
                                    rivers_strength[j][k][i] = 0
                                    continue
                                river_rank = int(river_card / 10) * 10
                                if river_rank == old_river_rank:
                                    rivers_strength[j][k][i] = str1
                                    continue

                                data_massive_small[4][4] = river_rank
                                old_river_rank = river_rank
                                str1 = current_strength_of_this_hand(data_massive_small)
                                rivers_strength[j][k][i] = str1

                        else:
                            old_river_rank = 0
                            str1 = 0
                            for k in range(48):
                                river_card = rivers[j][k][0]
                                if river_card == h_card1 or river_card == h_card2:
                                    rivers_strength[j][k][i] = 0
                                    continue
                                river_suit = river_card - int(river_card / 10) * 10
                                if river_suit == fd_suit or fd_cards_count > 4:
                                    data_massive_small[4][4] = river_card
                                    str2 = current_strength_of_this_hand(
                                        data_massive_small
                                    )
                                    rivers_strength[j][k][i] = str2
                                    continue

                                river_rank = int(river_card / 10) * 10
                                if river_rank == old_river_rank:
                                    rivers_strength[j][k][i] = str1
                                    continue

                                data_massive_small[4][4] = river_rank
                                old_river_rank = river_rank
                                str1 = current_strength_of_this_hand(data_massive_small)
                                rivers_strength[j][k][i] = str1

            # 3. CALC EQUITY
            range_eq = 0
            range_games = 0
            range_48 = range(48)
            for i in range_len_OOP:
                hero_card1, hero_card2 = OOP_range_array[i][0], OOP_range_array[i][1]
                w1 = OOP_range_array[i][2]
                for j in range_len_IP:
                    opps_card1, opps_card2 = IP_range_array[j][0], IP_range_array[j][1]
                    if (
                        hero_card1 == opps_card1
                        or hero_card2 == opps_card1
                        or hero_card1 == opps_card2
                        or hero_card2 == opps_card2
                    ):
                        main_paired_matrix[i][j] = -1
                        for k2 in range_48:
                            side_paired_matrix[k2][i][j] = -1
                        continue
                    eq = 0
                    games = 44  # allways =44
                    for k2 in range_48:
                        str1 = OOP_rivers_strength[0][k2][i]
                        str2 = IP_rivers_strength[0][k2][j]
                        if str1 == 0 or str2 == 0:
                            side_paired_matrix[k2][i][j] = -1
                            continue
                        if str1 > str2:
                            side_paired_matrix[k2][i][j] = 1
                            eq += 1
                        elif str1 == str2:
                            eq += 0.5
                            side_paired_matrix[k2][i][j] = 0.5
                    main_paired_matrix[i][j] = eq / games
                    w2 = IP_range_array[j][2]
                    range_eq += main_paired_matrix[i][j] * w1 * w2
                    range_games += w1 * w2
            if range_games > 0:
                range_eq /= range_games
            return main_paired_matrix, side_paired_matrix

        # river
        else:
            # 1. INITIALIZATION
            board_card1, board_card2, board_card3, board_card4, board_card5 = (
                int(board[0]),
                int(board[1]),
                int(board[2]),
                int(board[3]),
                int(board[4]),
            )
            turns = np.ones((1, 2), dtype=uint8)
            OOP_rivers_strength = np.zeros((1, 1, len(OOP_range_array)), dtype=uint32)
            IP_rivers_strength = np.zeros((1, 1, len(IP_range_array)), dtype=uint32)
            main_paired_matrix = np.zeros(
                (len(OOP_range_array), len(IP_range_array)), dtype=float32
            )  # include playability player vs player
            side_paired_matrix = np.zeros((1, 1, 1), dtype=float32)
            rivers = np.zeros((1, 1, 2), dtype=uint8)
            rivers[0][0][0] = board_card5
            data_massive_small = np.zeros((6, 7), dtype=uint8)
            (
                data_massive_small[4][0],
                data_massive_small[4][1],
                data_massive_small[4][2],
                data_massive_small[4][3],
                data_massive_small[4][4],
            ) = (board_card1, board_card2, board_card3, board_card4, board_card5)

            # 2. calculate strength of each hand
            for k2 in range(2):
                # k2 number is a numeric player position equivalent.
                # Used to define a player 0 or player 1
                len_r_a = len(OOP_range_array)
                len_ops_r_a = len(IP_range_array)
                range_array = OOP_range_array
                rivers_strength = OOP_rivers_strength
                if k2 == 1:
                    len_r_a, len_ops_r_a = len_ops_r_a, len_r_a
                    rivers_strength = IP_rivers_strength
                    range_array = IP_range_array
                for i in range(len_r_a):
                    h_card1, h_card2 = range_array[i][0], range_array[i][1]
                    data_massive_small[4][5], data_massive_small[4][6] = (
                        h_card1,
                        h_card2,
                    )
                    current_strength = current_strength_of_this_hand(data_massive_small)
                    rivers_strength[0][0][i] = current_strength

            # 3. CALC EQUITY
            range_eq = 0
            range_games = 0
            for i in range_len_OOP:
                hero_card1, hero_card2 = OOP_range_array[i][0], OOP_range_array[i][1]
                str1 = OOP_rivers_strength[0][0][i]
                hand_eq = 0
                hand_games = 0
                for j in range_len_IP:
                    opps_card1, opps_card2 = IP_range_array[j][0], IP_range_array[j][1]
                    if (
                        hero_card1 == opps_card1
                        or hero_card2 == opps_card1
                        or hero_card1 == opps_card2
                        or hero_card2 == opps_card2
                    ):
                        main_paired_matrix[i][j] = -1
                        continue
                    str2 = IP_rivers_strength[0][0][j]
                    if str1 == 0 or str2 == 0:
                        main_paired_matrix[i][j] = -1
                        continue
                    range_games += 1
                    hand_games += 1
                    if str1 > str2:
                        main_paired_matrix[i][j] = 1
                        hand_eq += 1
                        range_eq += 1
                    elif str1 == str2:
                        main_paired_matrix[i][j] = 0.5
                        hand_eq += 0.5
                        range_eq += 0.5
                if hand_games > 0:
                    hand_eq /= hand_games

            if range_games > 0:
                range_eq /= range_games

            return main_paired_matrix, side_paired_matrix

    @staticmethod
    @njit(cache=True)
    def calculate_eq(matrix, transformed_range1, transformed_range2):
        total_eq = 0
        total_games = 0
        for i in range(len(matrix)):
            w1 = transformed_range1[i][2]
            for j in range(len(matrix[0])):
                eq = matrix[i][j]
                if eq < 0:
                    continue
                w2 = transformed_range2[j][2]
                ww = w1 * w2
                total_eq += ww * eq
                total_games += ww
        if total_games > 0:
            total_eq /= total_games
        return round(total_eq, 6)

    @staticmethod
    @njit(cache=True)
    def get_playability_matrix(player_1_range_array, player_2_range_array):
        playability_matrix = np.empty(
            (len(player_1_range_array), len(player_2_range_array)), dtype=float32
        )
        total_games = 0
        playable = False
        for i in range(len(player_1_range_array)):
            jcard1, jcard2 = int(player_1_range_array[i][0]), int(
                player_1_range_array[i][1]
            )
            w1 = player_1_range_array[i][2]
            for j in range(len(player_2_range_array)):
                jcard3, jcard4 = int(player_2_range_array[j][0]), int(
                    player_2_range_array[j][1]
                )
                if (
                    jcard1 == jcard3
                    or jcard1 == jcard4
                    or jcard2 == jcard3
                    or jcard2 == jcard4
                ):
                    playability_matrix[i][j] = 0
                    continue
                w2 = player_2_range_array[j][2]
                posibility_value = w1 * w2
                playability_matrix[i][j] = posibility_value
                total_games += posibility_value
        if total_games > 0:
            playable = True
            for i in range(len(player_1_range_array)):
                for j in range(len(player_2_range_array)):
                    playability_matrix[i][j] = playability_matrix[i][j] / total_games

        return playable, playability_matrix

    @staticmethod
    def make_index_array(target_range, range_to_find_index):
        index_array = np.empty((len(target_range)), dtype="uint32")
        for i in range(len(target_range)):
            try:
                index_array[i] = range_to_find_index.index(target_range[i])
            except Exception:
                raise EquilatorError(f"Can't make index array! {target_range[i]} is not in = {range_to_find_index}")
        return index_array

    @staticmethod
    @njit(cache=True)
    def recalculate_preflop_matrix(full_preflop_matrix, index_array_1, index_array_2):
        recalculated_preflop_matrix = np.empty(
            (len(index_array_1), len(index_array_2)), dtype=float32
        )
        for i in range(len(index_array_1)):
            idx1 = index_array_1[i]
            for j in range(len(index_array_2)):
                idx2 = index_array_2[j]
                eq = full_preflop_matrix[idx1][idx2]
                recalculated_preflop_matrix[i][j] = eq
        return recalculated_preflop_matrix

    @staticmethod
    @njit(cache=True)
    def recalculate_range(player_range_array, board_array):
        indexed_player_range_array = np.empty((len(player_range_array)), dtype=uint16)
        new_len = 0
        for h in range(len(player_range_array)):
            jcard1, jcard2 = int(player_range_array[h][0]), int(
                player_range_array[h][1]
            )
            blocked = False
            for i in range(len(board_array)):
                jboard_card = int(board_array[i])
                if jcard1 == jboard_card or jcard2 == jboard_card:
                    blocked = True
                    break
            if not blocked:
                indexed_player_range_array[new_len] = h
                new_len += 1
        if new_len == 0:
            return None
        new_player_range_array = np.empty((new_len, 3), dtype=float32)
        for h in range(new_len):
            new_player_range_array[h] = player_range_array[
                indexed_player_range_array[h]
            ]

        return new_player_range_array

    @staticmethod
    def convert_to_range_list(range_array):
        range_list = []
        for i in range(len(range_array)):
            range_list.append(
                strength_to_card(range_array[i][0])
                + strength_to_card(range_array[i][1])
            )
        return range_list

    @staticmethod
    @njit(cache=True)
    def check_playability(player_1_range_array, player_2_range_array):
        playability_matrix = np.empty(
            (len(player_1_range_array), len(player_2_range_array)), dtype=float32
        )
        total_games = 0
        playable = False
        for i in range(len(player_1_range_array)):
            jcard1, jcard2 = int(player_1_range_array[i][0]), int(
                player_1_range_array[i][1]
            )
            w1 = player_1_range_array[i][2]
            for j in range(len(player_2_range_array)):
                jcard3, jcard4 = int(player_2_range_array[j][0]), int(
                    player_2_range_array[j][1]
                )
                if (
                    jcard1 == jcard3
                    or jcard1 == jcard4
                    or jcard2 == jcard3
                    or jcard2 == jcard4
                ):
                    playability_matrix[i][j] = 0
                    continue
                w2 = player_2_range_array[j][2]
                posibility_value = w1 * w2
                playability_matrix[i][j] = posibility_value
                total_games += posibility_value
        if total_games > 0:
            playable = True
            for i in range(len(player_1_range_array)):
                for j in range(len(player_2_range_array)):
                    playability_matrix[i][j] = playability_matrix[i][j] / total_games

        return playable, playability_matrix
