import chess
from chess import uci
b = chess.Board()
engine = uci.popen_engine("stockfish")
engine.uci()

print(engine.name)
print(engine.author)

engine.position(b)

result = engine.go(movetime=1000)
print result.bestmove

move1 = "g2g3"
move1_uci = chess.Move.from_uci(move1)

print(move1_uci in b.legal_moves)
