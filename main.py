import sys
import time
from transposition_table import TranspositionTable
import numpy as np
from state import State
from solver import Solver

# The board size is 6*7(6 rows * 7 columns)
# The board initialized with zeros in all positions.
# black color is depicted by number -1.
# white color is depicted by number 1.
# black goes first.



if __name__ == '__main__':

    board = np.array(
        [[-1, -1, 1, 0, 0, 0, 0], [1, 1, -1, 0, 0, 0, 0], [-1, -1, 1, 1, 0, 0, 0], [1, 1, -1, -1, 0, 0, 0],
         [-1, -1, 1, 1, -1, 0, 0], [1, 1, -1, -1, 1, 0, 0]])
    #board2=np.zeros((6,7))
    s=State(None,True)
    s.board=board

    negamax_results=[]
    minimax_results=[]
    colors=['white','black']
    toplay='black'
    if np.count_nonzero(s.board == 1)<np.count_nonzero(s.board == -1):
        toplay='white'

    # negamax search
    start=time.time()
    for i in range(2):
        solver=Solver(colors[i])
        negamax_results.append(solver.negamax(s, toplay))
    end=time.time()
    negamax_time=end -start

    #minimax search
    start = time.time()
    for i in range(2):
        solver=Solver(colors[i])
        minimax_results.append(solver.minimax(s, toplay))
    end = time.time()
    minimax_time = end - start

    #alphabeta search
    start = time.time()
    # no difference in the draw winner
    solver = Solver("black")
    alphabeta_result=solver.callAlphabeta(s, toplay,None)
    end = time.time()
    alphabeta_time = end - start

    #alphabeta search with transposition table
    start = time.time()
    # no difference in the draw winner
    solver = Solver("black")
    alphabeta_result_tt = solver.callAlphabeta(s, toplay,TranspositionTable())
    end = time.time()
    alphabeta_time_tt = end - start


    #analyse negamax results
    if negamax_results[0] != negamax_results[1]:
        print("This position is a draw.")
    else:
        if negamax_results[0]:
            print("It is a win for current player("+toplay+").")
        else:
            print("It is a loss for current player("+toplay+").")
    print("negamax time: "+str(negamax_time)+" s")

    print("***************************************")

    #analyse minimax results
    if minimax_results[0] != minimax_results[1]:
        print("This position is a draw.")
    else:
        if minimax_results[0]:
            print("It is a win for first player(black).")
        else:
            print("It is a loss for first player(black).")
    print("minimax time: " + str(minimax_time) + " s")

    print("***************************************")

    #analyse alphabeta result
    if alphabeta_result==0:
        print("This position is a draw.")
    elif alphabeta_result==solver.proven_win:
        print("It is a win for current player("+toplay+").")
    else:
        print("It is a loss for current player(" + toplay + ").")
    print("alphabeta time: "+str(alphabeta_time)+" s")

    print("***************************************")

    #analyse alphabeta result with tt
    if alphabeta_result_tt==0:
        print("This position is a draw.")
    elif alphabeta_result_tt==solver.proven_win:
        print("It is a win for current player("+toplay+").")
    else:
        print("It is a loss for current player(" + toplay + ").")
    print("alphabeta time with tt: "+str(alphabeta_time_tt)+" s")

