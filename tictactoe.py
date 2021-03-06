
from client import play, connect



class TicTacToe(object):

    memo = {}

    def __init__(self, board=None):
        if board is None:
            board = ' ' * 9
        self.board = board


    def current_player(self):
        # Player 1 or player 2.

        unplayed = self.board.count(' ')
        if unplayed %2 == 1:
            return 1
        else:
            return 2

    def get_symbol(self, player):
        return {
            1: 'x',
            2: 'o',
            }[player]


    def get_player(self, symbol):
        return {
            'x': 1,
            'o': 2,
            }[symbol]


    def draw_board(self):
        print(self.board[:3])
        print(self.board[3:6])
        print(self.board[6:9])
        print("===")

    def opponent(self, player):
        if self.current_player() == 1:
            return 2
        else:
            return 1


    def winner(self):
        WINCOMBOS = [[0,1,2], [3,4,5], [6,7,8],
                     [0,3,6], [1,4,7], [2,5,8],
                     [0,4,8], [2,4,6]]
        
        for line in WINCOMBOS:
            s = set([self.board[e] for e in line])
            if len(s) == 1 and ' ' not in s:
                winner = s.pop()
                return self.get_player(winner)
        return None


    def is_tie(self):
        return self.board.count(' ') == 0

    def is_over(self):
        return self.winner() or self.is_tie()

    def utility(self):  
        # utility is from player #1's perspective (+1 if #1 wins, -1 if #1 loses)
        winner = self.winner()
        if winner == 1:
            return 1
        elif winner == 2:
            return -1
        else:
            return 0

        
    def minimax_score(self):
        """
        Get the minimax score of the current position.
        Minimax is a decision rule that finds the best 
        strategy in a game with an adversary who acts ideally.
        It operates by minimizing the worst case scenario.
        """

        # Retrieve a memoized minimax score.
        if self.board in self.memo:
            return self.memo[self.board]

        # If the game is over, return the board's utility from
        # the perspective of player 1.
        if self.is_over():
            utility = self.utility()

        # Otherwise, compute the value of the row below you.
        else:
            moves = self.legal_moves() # Generate the next layer of the decision tree.
            states = [self.transition(move) for move in moves] # Create the nodes for this tree.
            values = [e.minimax_score() for e in states] # Calculate minimax values for each of the states.

            if self.current_player() == 1:
                utility = max(values)
            else:
                utility = min(values)

        # Memoize and return the discovered result.
        self.memo[self.board] = utility
        return utility


    def minimax_move(self):
        moves = self.legal_moves() # Generate the next layer of the decision tree.
        states = [self.transition(move) for move in moves] # Create the nodes for this tree.
        values = [e.minimax_score() for e in states] # Calculate minimax values for each of the states.

        if self.current_player() == 1:
            v = max(values)
        else:
            v = min(values)

        i = values.index(v)
        return moves[i]


    def legal_moves(self):
        return [index for index, value in enumerate(self.board) if value == ' ']

    def transition(self, index):
        symbol = self.get_symbol(self.current_player())
        l = list(self.board)
        if l[index] == ' ':
            l[index] = symbol
            return TicTacToe(''.join(l))
        else:
            raise
        
        


def play_tictactoe(host, port):
    sock = connect(host, port, 'tictactoe')
    return play(sock, get_move)

def get_move(state):
    board = state['board']
    t = TicTacToe(board)
    move = t.minimax_move()
    return move
    

if __name__ == "__main__":
    play_tictactoe('', 12345)

    #print(TicTacToe('xxx      ').board_score(1))
    #print(TicTacToe('ooo      ').board_score(1))
    
    #print c.get_legal_moves()
    #print c.minimax_score('x')

    #c = TicTacToe('xx oo ox ')
    #c = TicTacToe('xox      ')
    #c.draw_board()

    #while not c.over():
    #    move = c.minimax_move(c.current_player())
    #    c = c.transition(move)
    #    c.draw_board()        


