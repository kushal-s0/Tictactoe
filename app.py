from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Tic Tac Toe board
board = [" " for _ in range(9)]

# Winning combinations
winning_combos = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

def check_winner(board, player):
    for combo in winning_combos:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] == player:
            return True
    return False

def check_draw(board):
    return " " not in board

@app.route('/')
def index():
    global board
    return render_template('index.html', board=board)

@app.route('/move', methods=['POST'])
def make_move():
    data = request.get_json()
    position = int(data['position'])
    player = data['player']

    if board[position] == " ":
        board[position] = player
        if check_winner(board, player):
            return jsonify({'status': 'win', 'board': board})
        elif check_draw(board):
            return jsonify({'status': 'draw', 'board': board})
        else:
            return jsonify({'status': 'next', 'board': board})
    return jsonify({'status': 'invalid', 'board': board})

@app.route('/reset', methods=['POST'])
def reset_board():
    global board
    board = [" " for _ in range(9)]
    return jsonify({'status': 'reset', 'board': board})

if __name__ == '__main__':
    app.run(debug=True)
