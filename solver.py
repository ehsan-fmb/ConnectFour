

class Solver:
    def __init__(self,draw_winner):
        self.draw=draw_winner
        self.INFINITY=1000000
        self.draw_value=0
        self.proven_win=10000
        self.proven_loss=-10000

    def turn_color(self,color):
        if color=='white':
            return 'black'
        else:
            return 'white'

    def minimaxBooleanOR(self,state):
        result = state.evaluation()
        if result != "no winning":
            if result == 'draw':
                result = self.draw
            if result == "black":
                return True
            else:
                return False
        else:
            for m in state.legal_moves():
                state.transitions(m[0], m[1], "black")
                isWin = self.minimaxBooleanAND(state)
                state.undoMove(m[0], m[1])
                if isWin:
                    return True
            return False

    def minimaxBooleanAND(self,state):
        result = state.evaluation()
        if result != "no winning":
            if result == 'draw':
                result = self.draw
            if result == "black":
                return True
            else:
                return False
        else:
            for m in state.legal_moves():
                state.transitions(m[0], m[1], "white")
                isLoss = not self.minimaxBooleanOR(state)
                state.undoMove(m[0], m[1])
                if isLoss:
                    return False
            return True

    def minimax(self,state,color):
        if color == "black":
            return self.minimaxBooleanOR(state)
        else:
            return self.minimaxBooleanAND(state)

    def negamax(self,state,color):
        result=state.evaluation()
        if result != "no winning" :
            if result=='draw':
                result=self.draw
            if result==color:
                return True
            else:
                return False
        else:
            for m in state.legal_moves():
                state.transitions(m[0],m[1],color)
                success = not self.negamax(state,self.turn_color(color))
                state.undoMove(m[0],m[1])
                if success:
                    return True
            return False

    def alphabeta(self,state, alpha, beta,color):
        result=state.evaluation()
        if result != "no winning" :
            if result=='draw':
                return self.draw_value
            if result==color:
                return self.proven_win
            else:
                return self.proven_loss
        else:
            for m in state.legal_moves():
                state.transitions(m[0],m[1],color)
                value = -self.alphabeta(state, -beta, -alpha,self.turn_color(color))
                if value > alpha:
                    alpha = value
                state.undoMove(m[0],m[1])
                if value >= beta:
                    return beta
            return alpha

    def alphabeta_tt(self,state, alpha, beta,color,tt):
        result = tt.lookup(state.code())
        if result != None:
            return result
        result=state.evaluation()
        if result != "no winning" :
            if result=='draw':
                tt.store(state.code(), self.draw_value)
                return self.draw_value
            if result==color:
                tt.store(state.code(), self.proven_win)
                return self.proven_win
            else:
                tt.store(state.code(), self.proven_loss)
                return self.proven_loss
        else:
            for m in state.legal_moves():
                state.transitions(m[0],m[1],color)
                value = -self.alphabeta_tt(state, -beta, -alpha,self.turn_color(color),tt)
                if value > alpha:
                    alpha = value
                state.undoMove(m[0],m[1])
                if value >= beta:
                    return beta
            return alpha

    def callAlphabeta(self,state,color,tt):
        if tt is None:
            return self.alphabeta(state, -self.INFINITY, self.INFINITY,color)
        else:
            return self.alphabeta_tt(state, -self.INFINITY, self.INFINITY, color,tt)