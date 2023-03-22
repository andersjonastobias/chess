
from chess import Board, Move, STARTING_FEN, Piece, PieceType, Color, SQUARES
import chess
import random
import numpy as np
import time

version = "0.1"
DEPTH = 2


def generate_move():
    # board = Board(fen)
    _, move = minimax(board, True, DEPTH)
    return move


def sort_moves(moves, maximizing_player):
    return moves


piece_score = {
    Piece.from_symbol("P").piece_type: 100,
    Piece.from_symbol("N").piece_type: 320,
    Piece.from_symbol("B").piece_type: 330,
    Piece.from_symbol("R").piece_type: 500,
    Piece.from_symbol("Q").piece_type: 900,
    Piece.from_symbol("K").piece_type: 20000
}


pawnEvalWhite = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, -20, -20, 10, 10,  5,
    5, -5, -10,  0,  0, -10, -5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5,  5, 10, 25, 25, 10,  5,  5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0
]
pawnEvalBlack = list(reversed(pawnEvalWhite))

knightEval = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
]

bishopEvalWhite = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]
bishopEvalBlack = list(reversed(bishopEvalWhite))

rookEvalWhite = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0
]
rookEvalBlack = list(reversed(rookEvalWhite))

queenEval = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -5, 0, 5, 5, 5, 5, 0, -5,
    0, 0, 5, 5, 5, 5, 0, -5,
    -10, 5, 5, 5, 5, 5, 0, -10,
    -10, 0, 5, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20
]

kingEvalWhite = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30
]
kingEvalBlack = list(reversed(kingEvalWhite))

kingEvalEndGameWhite = [
    50, -30, -30, -30, -30, -30, -30, -50,
    -30, -30,  0,  0,  0,  0, -30, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -20, -10,  0,  0, -10, -20, -30,
    -50, -40, -30, -20, -20, -30, -40, -50
]
kingEvalEndGameBlack = list(reversed(kingEvalEndGameWhite))


def evaluate_piece(piece: Piece, square: chess.Square) -> int:
    piece_type = piece.piece_type
    mapping = []
    if piece_type == chess.PAWN:
        mapping = pawnEvalWhite if piece.color == chess.WHITE else pawnEvalBlack
    if piece_type == chess.KNIGHT:
        mapping = knightEval
    if piece_type == chess.BISHOP:
        mapping = bishopEvalWhite if piece.color == chess.WHITE else bishopEvalBlack
    if piece_type == chess.ROOK:
        mapping = rookEvalWhite if piece.color == chess.WHITE else rookEvalBlack
    if piece_type == chess.QUEEN:
        mapping = queenEval
    if piece_type == chess.KING:
        # use end game piece-square tables if neither side has a queen
        # if end_game:
        #     mapping = (
        #         kingEvalEndGameWhite
        #         if piece.color == chess.WHITE
        #         else kingEvalEndGameBlack
        #     )
        # else:
            mapping = kingEvalWhite if piece.color == chess.WHITE else kingEvalBlack

    return mapping[square]


def score_piece(type, color):
    return piece_score[type]*(-1)**color


def score_board(board):
    # board.piece_map() will given dictionary form position (1..64) to pieces. A piece
    # has a type (int 1...6 where int corresponds to strength of piece) and a color (bool indicating
    # whether it is white or not).
    # Now using list(board.pieces(board.piece_map()[8].piece_type, board.piece_map()[8].color)) will return
    # list of int (0..64) where a pice of given type is located
    value = 0
    for square in SQUARES:
        piece = board.piece_at(square)
        if (piece):
            value += score_piece(piece.piece_type, piece.color)+evaluate_piece(piece, square)
    return value


def minimax(board, maximizing_player, depth, path=f"logs/log"):
    #if (depth == 0 or board.is_game_over()): We need the opponent to actually take the queen for minimax to 
    # see how bad it is.
    moves = sort_moves(board.legal_moves, maximizing_player)
    if (depth == 0 or len(list(moves))==0):# if no legal moves stop and score board
        return score_board(board), None
    if (maximizing_player):
        value = -np.Inf
        if(len(list(moves))<3):#Bonus if we are looking at a forcing line
            depth+=1
            print_to_log(path,"boosting due to forcing line")
            print_to_log(path,str(moves))
            print_to_log(path,str(depth))
        for move in moves:
            board.push(move)
            mval, _ = minimax(board, not maximizing_player, depth-1)
            if (mval > value):55
                value = mval
                bestmove = move
                print_to_log(path,value, bestmove,  maximizing_player, depth)
            board.pop()
    else:
        value = np.Inf
        for move in moves:
            board.push(move)
            mval, _ = minimax(board, not maximizing_player, depth-1)
            if (mval < value):
                value = mval
                bestmove = move
                print_to_log(path,value, bestmove, maximizing_player)
            board.pop()
    return value, bestmove



log_moves=False
def print_to_log(path,*args):
    if(log_moves):
        strline=""
        for arg in args:
            strline+=" "+str(arg)
        with open(path, "a") as f:
            f.write(str(time.asctime()) + "\t" + strline + "\n")


hist = []
board = Board(STARTING_FEN)
while (True):
    inp = input()
    args = inp.split()
    with open("log", "a") as f:
        f.write(inp + "\n")
    if (args[0] == "uci"):
        print(f"id name {version}")
        print("id author Anders Kølvraa")
        print("uciok")
    elif (args[0] == "isready"):
        print("readyok")
    elif (args[0] == "quit"):
        break
    elif (args[0] == "ucinewgame"):
        board = Board(STARTING_FEN)
        continue
    elif (args[0] == "position"):
        if (args[1] == "startpos"):
            board.reset()
            move_start = 2
        elif (args[1] == "fen"):
            fen = " ".join(args[2:8])
            board.set_fen(fen)
            move_start = 8
        else:
            raise Exception("Not implemented yet")
        for move in args[move_start+1:]:
            board.push_uci(move)
    elif (args[0] == "go"):
        print(f"bestmove {generate_move()}")
        print_to_log(f"bestmove {str(generate_move())}")
        print_to_log("  ")
        print_to_log(str(board))
        print_to_log(" ")
    else:
        break
