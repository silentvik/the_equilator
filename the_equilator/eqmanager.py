import numpy as np

from equilator import Equilator
from exceptions import EquilatorError
from funcs_jit import (convert_char_to_float_array,
                       convert_range_from_text_to_weighted_array,
                       jcard_strength)
from funcs_py import range_converter


class PlayersRange:
    """
        goal: to turn the entered string into a range for calculations
    """
    input_value = None
    _range_list = None
    _transformed_range = None
    _adapted_range_list = None
    _adapted_range = None

    def __init__(self, input_value):
        self.input_value = input_value
        if input_value:
            if type(input_value) != str:
                raise ValueError("Player's range input must be a string")
            if '(' in input_value or '[' in input_value:  # weighted input
                self._range_list = input_value[1:-1].split(',')
                for i, hand in enumerate(self._range_list):
                    hand_wo_w = ''
                    for symbol in hand:
                        if symbol == '(':
                            break
                        hand_wo_w += symbol
                    self._range_list[i] = hand_wo_w
                self._transformed_range = convert_range_from_text_to_weighted_array(input_value)
            else:
                final_char_list = []
                for combo in range_converter(input_value):
                    if combo in Equilator.all_paired_combos:
                        final_char_list.append(combo)
                        continue
                    print(
                        f'PlayersRange WARNING! Input is not fully correct!\n     combo {combo}'
                        f' is not in standart list, list = {Equilator.all_paired_combos}'
                    )
                self._range_list = final_char_list
                self._transformed_range = convert_char_to_float_array(np.array(self._range_list))
        else:
            self._range_list = None
            self._transformed_range = None

    def adapt_for_preflop(self):
        self._adapted_range_list = Equilator.convert_to_range_list(self._transformed_range)
        self._adapted_range = self._transformed_range

    def adapt_for_postflop(self, board_array):
        self._adapted_range = Equilator.recalculate_range(self._transformed_range, board_array)

    def __str__(self):
        len_list = 0
        if type(self._range_list) == list:
            len_list = len(self._range_list)
            if len(self._range_list) > 4:
                range_list_str = f'{str(self._range_list[:2])[:-1]}...{str(self._range_list[-2:])[1:]}'
            else:
                range_list_str = str(self._range_list)
        else:
            range_list_str = 'None'

        len_array = 0
        if type(self._transformed_range) == np.ndarray:
            len_array = len(self._transformed_range)
            if len(self._transformed_range) > 2:
                transformed_range_str = (
                    f'{str(self._transformed_range[:1])[:-1]}...{str(self._transformed_range[-1:])[1:]}'
                )
            else:
                transformed_range_str = str(self._transformed_range)
        else:
            transformed_range_str = 'None'

        text = (
            f'       class {self.__class__.__name__}'
            f'\n        input = "{self.input_value}"'
            f'\n        range(list) = {range_list_str},  len = {len_list}'
            f'\n        transformed = {transformed_range_str},  len = {len_array}'
        )
        return text


class Board:
    """
        goal: to turn the entered string into a valid board for calculations
    """
    input_value = None
    board = []
    _stage = 0
    _transformed_board = None

    def __init__(self, input_value):
        self.input_value = input_value
        if type(input_value) == str:
            input_value = input_value.split(',')

        if type(input_value) == list:
            if len(input_value) == 0:
                self._stage = 0
                self.board = []
                return

            board_list = []
            for comb in input_value:
                if comb in Equilator.all_cards and comb not in board_list:
                    board_list.append(comb)
            if len(board_list) < 3 or len(board_list) > 5:
                self._stage = 0
                self.board = []
                self._transformed_board = None
                return

            board_array = np.zeros((5), dtype='float32')
            for i in range(len(board_list)):
                board_array[i] = jcard_strength(board_list[i])

            if len(board_list) == 3:
                self._stage = 1
            elif len(board_list) == 4:
                self._stage = 2
            else:
                self._stage = 3
            self.board = board_list
            self._transformed_board = board_array
        else:
            self._stage = 0
            self.board = []
            self._transformed_board = None

    def __str__(self):
        text = (
            f'       class {self.__class__.__name__}'
            f'\n        input = "{self.input_value}"'
            f'\n        board(list) = {self.board}'
        )
        return text


class EqManager:
    ''' EqManager DOC
        Equity - the chance of victory by first range against second.
        By using this class you can calculate equity or get playability/equity-arrays for the future solving.

        Input data via self.player1_range (str), self.player2_range (str), self.board (list) or string.
        Write hands as "AsKd, 8d5c". Available suits = [h,d,c,s], ranks = [A,K,Q,J,T,9...2]
        Input board as list like ["Qd", "Jc", "5s"] or like string as "Qd, Jc, 5s" or w/o spaces "Qd,Jc,5s"
        Method self.get_equity - to evaluate ranges. Returns an equity.

        Features:
                input "22+" - means all possible pockets from 22 to AA.
                77-22 - all possible pockets from 22 to 77, include both 22 and 77
                22-77 - its WRONG. you will get an error
                A2s+ or A8s-A3s - the same as pockets
                A2o+ or A8o-A3o - the same as pockets and suited cards
                82s+ - will give you all combos of 82s, 83s .. to 87s.
                87s+ - will NOT give you all higher connectors. You will get 4 combos of 87s.

                "any two" or "any2" - input all combos
                "suit" - input only all suited combos
                "offsuit" - input only all offsuited combos
                "pockets" or "any pair" - input only all pockets

        Additional info:
            1. EqManager.prepare_ranges() will return False if:
                Equilator cant work and no combos available for players (when board blocks them)
                example range1 = "AhAd", range2 = "KK", board = ["Ah","Kd","2c"]

            2. EqManager allways tryes to set values, even if input is incorrect.
                recommendation: check current values after input via self.board, etc.
                for exapmle, if your code:
                    eqmanager_instance = EqManager()
                    eqmanager_instance.board = ["Ah", "Qd", "7c", "%&%^&??"]  # (wrong 4th card input)
                is stage == turn? - No!;
                print(eqmanager_instance.board)
                ["Ah", "Qd", "7c"]  -> stage = flop
                combination with name "%&%^&??" was ignored

            3.  You can ALSO use weighted input:
                self.range1 = "[2h2d(8734),4h4c(69556),5h5c(34132),6d6s(3740),7d7c(28040)]"
                here you cant use format "22+" or "suit"
                every combination MUST have a full name like "2h2d" and weight, without spaces.

            4. If the weight was not set, the weight is set to 1.

            5. If enter a weight for a hand => all hands in a range must be entered with weights

        Example of usage class EqManager:
                eqmanager_instance = EqManager()
                eqmanager_instance.player1_range = "22+, AhKd, 76s, J8s-J2s"
                eqmanager_instance.player2_range = "TT-55, 22, AdKc, 8s7s, 7d6d, 7h6h, 7s6s, 4d3d, 4h3h"
                eqmanager_instance.board = ['Qd', '7c', '4s']

                eq = eq_instance.get_equity()
                print(eq)
            or:
                prepared = eqmanager_instance.prepare_ranges()
                if not prepared:
                    eqmanager_instance.print_current_values()
                else:
                    m1,m2 = eqmanager_instance.get_paired_matrix()
    '''

    prints_enabled = False
    _player1_range = None
    _player2_range = None
    _board = None
    _equity = None
    _main_paired_matrix = None
    _side_paired_matrix = None

    _prepared = False

    def __init__(self, player1_range=None, player2_range=None, board=None):
        self.player1_range = player1_range
        self.player2_range = player2_range
        self.board = board
        self._prepared = False

    def printer(self, *args):
        '''
            Adds prefix to any text.
            If self.prints_enabled -> any prints will work
        '''

        if self.prints_enabled:
            text = ''
            for arg in args:
                text += str(arg)
            print('[EqManager] ', text)

    def print_current_values(self):
        print('\n[EqManager][print_current_values]')

        print('     range1:\n', self.player1_range,)

        print('     range2:\n', self.player2_range)
        print('     board:\n', self.board, '\n')

    def refresh_properties(self):
        """
            Set properties to their defaults. Now we need preparation.
        """
        self._equity = None
        self._prepared = False
        self._main_paired_matrix = None
        self._side_paired_matrix = None

    @property
    def player1_range(self):
        return self._player1_range

    @player1_range.setter
    def player1_range(self, input):
        self._player1_range = PlayersRange(input)
        self.refresh_properties()

    @property
    def player2_range(self):
        return self._player2_range

    @player2_range.setter
    def player2_range(self, input):
        self._player2_range = PlayersRange(input)
        self.refresh_properties()

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, input):
        self._board = Board(input)
        self.refresh_properties()

    def get_ranges(self):
        return self._player1_range, self._player2_range

    def prepare_ranges(self):
        """
            Prepare ranges for solving.
            Create playability matrix.
            Returns True if the preparation was successful, False otherwise.
        """
        self._prepared = False
        stage = self.board._stage
        player_1_range_array = self.player1_range._transformed_range
        player_2_range_array = self.player2_range._transformed_range
        board_array = self.board._transformed_board

        if type(player_1_range_array) != np.ndarray:
            self.printer('[Equilator][prepare_ranges] ERROR: values are incorrect. Can not prepare player 1 range')
            self.print_current_values()
            return False
        if type(player_2_range_array) != np.ndarray:
            self.printer('[Equilator][prepare_ranges] ERROR: values are incorrect. Can not prepare player 2 range')
            self.print_current_values()
            return False
        if stage > 0 and type(board_array) != np.ndarray:
            self.printer('[Equilator][prepare_ranges] ERROR: values are incorrect. Can not prepare the board')
            self.print_current_values()
            return False

        if stage > 0:
            self.player1_range.adapt_for_postflop(board_array)
            self.player2_range.adapt_for_postflop(board_array)
        else:
            self.player1_range.adapt_for_preflop()
            self.player2_range.adapt_for_preflop()

        playable, self._playability_matrix = Equilator.check_playability(
            self.player1_range._adapted_range,
            self.player2_range._adapted_range
        )

        self.printer('playable = ', playable)
        if not playable:
            self.printer('[prepare_ranges] ERROR: values are correct, but ranges are not playable.')
            self.print_current_values()
            self._prepared = False
            return False
        self.printer('[prepare_ranges] Ready to equilate!')
        self._prepared = True
        return True

    def equilate_and_make(self):
        '''
            Make main_paired martix w all vs all hands equity,
            if stage is flop or turn -> side_paired_matrix can be added,
            then calculates equity. No return.
        '''
        stage = self.board._stage
        board = self.board._transformed_board
        OOP_range_array = self.player1_range._adapted_range
        IP_range_array = self.player2_range._adapted_range

        if stage == 0:
            index_array_1 = Equilator.make_index_array(self.player1_range._range_list, Equilator.all_paired_combos)
            index_array_2 = Equilator.make_index_array(self.player2_range._range_list, Equilator.all_paired_combos)
            recalculated_preflop_matrix = Equilator.recalculate_preflop_matrix(
                Equilator.full_preflop_matrix,
                index_array_1,
                index_array_2
            )
            self._equity = Equilator.calculate_eq(recalculated_preflop_matrix, OOP_range_array, IP_range_array)
            self._main_paired_matrix = recalculated_preflop_matrix
            self._side_paired_matrix = None

        else:
            main_paired_matrix, side_paired_matrix = Equilator.make_equity_arrays(
                stage,
                OOP_range_array,
                IP_range_array,
                board
            )
            self._equity = Equilator.calculate_eq(main_paired_matrix, OOP_range_array, IP_range_array)
            self._main_paired_matrix = main_paired_matrix
            self._side_paired_matrix = side_paired_matrix

    def run_maker(self):
        """
            Prepare ranges, then make equity matrices.
        """
        if not self.prepare_ranges():
            raise EquilatorError('Cant equilate. Ranges are not prepared!')
        self.equilate_and_make()

    def get_equity(self):
        self.run_maker()
        return self._equity

    def get_playability_matrix(self):
        """
            Returns playability matrix if ranges were prepared. Otherwise tryes to prepare and return.
        """
        if not self._prepared:
            if not self.prepare_ranges():
                raise EquilatorError('Cant equilate. Ranges are not prepared!')
        return self._playability_matrix

    def get_paired_matrix(self):
        """
            Creates and returns equity matrices.
        """
        if self._main_paired_matrix is None or self._side_paired_matrix is None:
            self.run_maker()
        return (self._main_paired_matrix, self._side_paired_matrix)
