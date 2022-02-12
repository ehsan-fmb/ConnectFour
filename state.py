import copy
import numpy as np
from scipy.signal import convolve2d

#kernels
horizontal_kernel = np.array([[ 1, 1, 1, 1]])
vertical_kernel = np.transpose(horizontal_kernel)
diag1_kernel = np.eye(4, dtype=np.uint8)
diag2_kernel = np.fliplr(diag1_kernel)
detection_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]


class State:
    def __init__(self, parent,isroot):
        if not isroot:
            self.parent=parent
            self.board=copy.deepcopy(parent.board)

    def transitions(self,x,y,color):
        if color=='white':
            self.board[x][y]=1
        else:
            self.board[x][y] = -1

    def undoMove(self,x,y):
        self.board[x][y]=0

    def code(self):
        return np.array2string(self.board)

    def evaluation(self):
        for kernel in detection_kernels:
            result_board=convolve2d(self.board, kernel, mode="valid")
            if 4 in result_board:
                return "white"
            if -4 in result_board:
                return "black"
        if len(np.where(self.board==0)[0])==0:
            return "draw"
        return "no winning"


    def legal_moves(self):
        moves=[]
        for i in range(self.board.shape[1]):
            blanks = np.where(self.board[:, i] == 0)
            if len(blanks[0]) != 0:
                moves.append([blanks[0][-1], i])
        return moves

    def plot(self):
        print(str(self.board).replace(' [', '').replace('[', '').replace(']', ''))