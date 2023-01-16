import chess
import chess.engine

#This doesnt work - presumably since this is compiled for windows
engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")

board = chess.Board()
while not board.is_game_over():
    result = engine.play(board, chess.engine.Limit(time=0.1))
    board.push(result.move)
    print(result.move)

engine.quit()
