from time import time

from the_equilator.eqmanager import EqManager

if __name__ == '__main__':

    # setting player ranges
    # more information in EqManager.__doc__

    range_1 = (
        "22+,AKs"
    )
    range_2 = (
        'KK, 99, 66, K6s-K4s, Q7s'
    )

    # create manager instance
    # it is possible to enter a board here

    eqmanager_inst = EqManager(
        player1_range=range_1,
        player2_range=range_2,
        board=None  # the board can be set later
    )

    # or set values after init eqmanager_inst
    if False:
        eqmanager_inst.player2_range = 'KK,99'  # range can be set here
        eqmanager_inst.board = '2h,3d,4c'  # board can be set here

    eqmanager_inst.print_current_values()

    start_timer = time()
    eq = eqmanager_inst.get_equity()

    # evaluation will be very fast, but only after first run (after compilation)
    print(f'time = {time() - start_timer} s')

    print(f'\nEQ RESULT = {eq}\n')

    # get matrices
    if False:
        # in reality (when you want to create a poker solver/engine)
        # you no need an average equity of ranges. All you need is:

        # how often player can play hand vs another player
        playability_matrix = eqmanager_inst.get_playability_matrix()

        # equity of each hand against each from a different range
        pm1, pm2 = eqmanager_inst.get_paired_matrix()

        # enjoy!
