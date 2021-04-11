from chess import uci #need to find the version number for python chess used,
# this code uses and old version

class StockfishPlayer(object):
    def __init__(self):
        self._engine = uci.popen_engine('/usr/games/stockfish')
        self._engine.uci()

    def select_move(self, board):
        self._engine.position(board)
        result = self._engine.go(movetime=1000)
        return result.bestmove
