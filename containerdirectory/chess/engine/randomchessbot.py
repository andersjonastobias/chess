from chess import Board, Move, STARTING_FEN
import random

version="0.1"

def generate_random():
    #board = Board(fen)
    legal_moves = list(board.legal_moves)
    if(len(legal_moves)==0):
        return ""
    return random.choice(legal_moves)

hist=[]
board=Board(STARTING_FEN)
while(True):
    inp=input()
    args=inp.split()
    with open("log","a") as f:
        f.write(inp + "\n")
    if(args[0] == "uci"):
        print(f"id name {version}")
        print("id author Anders Kølvraa")
        print("uciok")
    elif(args[0]=="isready"):
        print("readyok")
    elif(args[0] =="quit"):
        break
    elif(args[0]=="ucinewgame"):
        board = Board(STARTING_FEN)
        continue
    elif(args[0]== "position"):
        if(args[1]=="startpos"):
            board.reset()
            move_start=2
        elif(args[1]=="fen"):
            fen = " ".join(args[2:8])
            board.set_fen(fen)
            move_start=8
        else:
            raise Exception("Not implemented yet")
        for move in args[move_start+1:]:
            board.push_uci(move)
    elif(args[0]=="go"):
        print(f"bestmove {generate_random()}")
        with open("log","a") as f:
            f.write(str(generate_random()))
    else: 
        break

        

