from flask import Flask, jsonify, request
from game_logic import GameLogic
from game_token import GameToken
from drop_state import DropState
from game_state import GameState

app = Flask(__name__)

# Initialisiere GameLogic
game = GameLogic()


@app.route('/board', methods=['GET'])
def get_board():
    """
    Gibt das aktuelle Spielfeld zurück.
    """
    return jsonify({"board": game.get_board()})


@app.route('/state', methods=['GET'])
def get_state():
    """
    Gibt den aktuellen Spielzustand zurück.
    """
    return jsonify({"state": game.get_state().name})


@app.route('/drop', methods=['POST'])
def drop_token():
    """
    Setzt einen Token in die angegebene Spalte.
    Erwartet JSON-Eingabe: {"player": "RED", "column": <int>}
    """
    data = request.json
    player = GameToken.RED if data['player'] == 'RED' else GameToken.YELLOW
    column = data['column']

    drop_result = game.drop_token(player, column)

    return jsonify({"drop_state": drop_result.name, "board": game.get_board()})


if __name__ == '__main__':
    app.run(debug=True)
