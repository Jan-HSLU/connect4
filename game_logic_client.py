from game_logic import GameLogicBase
from game_state import GameState
from drop_state import DropState
from game_token import GameToken
import requests

class GameLogicClient(GameLogicBase):

    def __init__(self, host: str) -> None:
        """
        Initialisiert den GameLogicClient mit der angegebenen Host-Adresse.

        :param host: Die Host-Adresse des Servers
        """
        super().__init__()
        print(f"GameLogicClient initialized with host {host}")
        self._url = f'http://{host}:5000/api'

    def get_board(self) -> list:
        """
        Ruft das aktuelle Spielfeld vom Server ab.

        :return: Das Spielfeld als Liste von Listen (Reihen und Spalten)
        """
        response = requests.get(f"{self._url}/board")
        return response.json().get("board")

    def get_state(self) -> GameState:
        """
        Ruft den aktuellen Spielstatus vom Server ab.

        :return: Der aktuelle Spielstatus als GameState-Enum
        """
        response = requests.get(f"{self._url}/state")
        game_state = response.json().get("state")

        if game_state == 0:
            return GameState.TURN_RED
        elif game_state == 1:
            return GameState.TURN_YELLOW
        elif game_state == 2:
            return GameState.WON_RED
        elif game_state == 3:
            return GameState.WON_YELLOW
        elif game_state == 4:
            return GameState.DRAW
        else:
            print("ERROR GAMESTATE API")

    def drop_token(self, player: GameToken, column: int) -> DropState:
        """
        Lässt einen Spielstein in die angegebene Spalte fallen.

        :param player: Der Spieler (GameToken.RED oder GameToken.YELLOW)
        :param column: Die Spalte, in die der Spielstein fallen soll
        :return: Der Status des Drops als DropState-Enum
        """
        if player == GameToken.RED:
            player_id = "X"
        else:
            player_id = "O"

        payload = {
            "column": column,
            "player_id": player_id
        }

        response = requests.post(f"{self._url}/drop", json=payload)
        drop_state = response.json().get("drop_state")

        if drop_state == 0:
            return DropState.DROP_OK
        elif drop_state == 1:
            return DropState.COLUMN_INVALID
        elif drop_state == 2:
            return DropState.COLUMN_FULL
        elif drop_state == 3:
            return DropState.WRONG_PLAYER
        else:
            print("ERROR DROPSTATE API")


if __name__ == '__main__':
    """
    Test programm to manually check if GameLogicClient is working.
    Limitations:
    - Implements both players at once--no distributed gameplay possible
    - Does not handle errors
    - Does not handle end of game gracefully
    """
    # local function
    def draw_board( board: list, state: GameState) -> None:
        print("0|1|2|3|4|5|6")
        for row in board:
            print('|'.join(row))
        print( f"GameState: {state}" )

    client = GameLogicClient("127.0.0.1")
    while( True ):
        game_state = client.get_state()
        board = client.get_board()
        print(board)

        draw_board( board, game_state )

        if game_state == GameState.TURN_RED or  game_state == GameState.TURN_YELLOW:
            player = GameToken.RED if game_state == GameState.TURN_RED else GameToken.YELLOW  
            column = int(input("Which colum to drop? "))    
            drop_state = client.drop_token( player, column )
            print( "drop_state:", drop_state )
        else: break # bail out if its neither RED's nor YELLOW's turn, i.e. WON or DRAW
    
    print("Game Over")
