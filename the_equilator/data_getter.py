import os
import pickle

from funcs_py import range_converter


class DataGetter:
    ranks = 'AKQJT98765432'
    suits = 'hdcs'

    @staticmethod
    def get_all_cards_list():
        all_cards_list = []
        for i in DataGetter.ranks:
            for j in DataGetter.suits:
                all_cards_list.append(i+j)
        return all_cards_list

    @staticmethod
    def get_all_paired_combos():
        all_paired_combos = range_converter('any2')
        return all_paired_combos

    @staticmethod
    def load_preflop_matrix():
        dir_path = os.path.dirname(os.path.realpath(__file__))
        some_file = open(dir_path+'/datafiles/preflop_matrix.pkl', 'rb')
        preflop_full_matrix = pickle.load(some_file)
        return preflop_full_matrix


asdf = DataGetter.load_preflop_matrix()
