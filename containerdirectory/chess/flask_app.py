from flask import Flask
from flask import render_template
from flask import request
import chess
import chess.engine

#engine = chess.engine.SimpleEngine.popen_uci('/usr/games/stockfish', debug=True)
#engine = chess.engine.SimpleEngine.popen_uci(["python","./engine/randomchessbot.py"], debug=True)
#engine = chess.engine.SimpleEngine.popen_uci(["python3.10","/home/codic/chess/containerdirectory/chess/engine/minimaxbot.py"], debug=True)

app = Flask(__name__)

@app.route('/')
def root():
	print("Check")
	return render_template('chess.html') # Apparently flask is looking in tempatefolder by default

@app.route('/make_move', methods=['POST']) # by default only get-methods are used.
def make_move():
	print('request form', request.form)
	fen = request.form.get('fen')
	print('fen', fen)
	board = chess.Board(fen)
	print(board)
	#Unclear why it was necessary to move engine here to make engine work
	engine = chess.engine.SimpleEngine.popen_uci(["python","./engine/minimaxbot.py"], debug=True)
	result = engine.play(board, chess.engine.Limit(time=0.1))
	engine.quit()
	print("result",result)
	board.push(result.move)
	print(board)
	fen=board.fen()
	return {'fen': fen}

#print(__name__)
#if(__name__=='__main__'):
#	app.run(debug=True, threaded=True, port = 80, host='0.0.0.0')
# We apparently need to supply the host='0.0.0.0' to make sure it is running on all hosts if we want it exposed
#outside the container.


