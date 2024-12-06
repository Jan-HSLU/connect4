from player_base import PlayerBase
from display_sensehat import DisplaySenseHat
from input_sensehat import InputSenseHat
from game_state import GameState
from game_token import GameToken
from input_base import Keys
from time import sleep

class PlayerSenseHat(PlayerBase):
    def __init__(self, player: GameToken):
        """
        Initialisiert einen PlayerSenseHat-Spieler mit dem übergebenen Spielstein.
        Richtet die Anzeige (DisplaySenseHat) und die Eingabe (InputSenseHat) ein.
        
        :param player: Der Spielstein (GameToken) dieses Spielers.
        """
        super().__init__(player)
        self._display = DisplaySenseHat()
        self._input = InputSenseHat()
        self._current_column = 3

        # Beim Start das Board komplett leeren
        self._display.clear_board()

    def play_turn(self, state: GameState) -> int:
        """
        Führt einen Spielzug auf dem SenseHat-Display durch, indem die aktuelle Spalte 
        mittels Joystick links/rechts ausgewählt und mit ENTER bestätigt wird.
        Wenn bestätigt, wird die aktuelle Spalte zurückgegeben.
        
        :param state: Der aktuelle Spielzustand.
        :return: Die aktuell ausgewählte Spalte als int.
        """
        while True:
            while not self._input.key_pressed():
                sleep(0.1)
            key = self._input.read_key()

            if key == Keys.LEFT:
                self._current_column = (self._current_column - 1) % self._display.columns
            elif key == Keys.RIGHT:
                self._current_column = (self._current_column + 1) % self._display.columns
            elif key == Keys.ENTER:
                # Zug zurückgeben und zuvor Cursor ausblenden
                self._display.draw_cursor(None)
                self._display.draw_grid()
                return self._current_column

            self.draw_board(self._display.board, state)

    def draw_board(self, board: list, state: GameState):
        """
        Zeichnet das übergebene Spielfeld (board) auf dem SenseHat-Display.
        Platziert die vorhandenen Spielsteine und zeigt den Cursor nur an, 
        wenn dieser Spieler am Zug ist.
        
        :param board: Eine 2D-Liste, die den aktuellen Zustand des Spielfeldes darstellt.
        :param state: Der aktuelle Spielzustand.
        """
        for y in range(len(board)):
            for x in range(len(board[y])):
                if board[y][x] == GameToken.RED:
                    self._display.draw_token(x, y, GameToken.RED)
                elif board[y][x] == GameToken.YELLOW:
                    self._display.draw_token(x, y, GameToken.YELLOW)
                else:
                    self._display.draw_token(x, y, GameToken.EMPTY)

        # Cursor nur anzeigen, wenn dieser Spieler am Zug ist
        if (self._player == GameToken.YELLOW and state == GameState.TURN_YELLOW) or \
           (self._player == GameToken.RED and state == GameState.TURN_RED):
            self._display.draw_cursor(self._current_column)
        else:
            self._display.draw_cursor(None)

        self._display.draw_grid()

if __name__ == '__main__':
    from sense_hat import SenseHat

    sense = SenseHat()
    board = [[GameToken.EMPTY for _ in range(7)] for _ in range(6)]
    board[5][0] = GameToken.RED  # [Y][X]
    p = PlayerSenseHat(GameToken.YELLOW)
    sense.clear()
    p.draw_board(board, GameState.TURN_YELLOW)
    pos = p.play_turn()
    print(f"Position: {pos}")
