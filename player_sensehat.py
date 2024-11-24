from player_base import PlayerBase
from display_sensehat import DisplaySenseHat
from input_sensehat import InputSenseHat
from game_state import GameState
from game_token import GameToken
from input_base import Keys
from time import sleep
from sense_hat import SenseHat

class PlayerSenseHat(PlayerBase):
    def __init__(self, player: GameToken):
        super().__init__(player)
        self._display = DisplaySenseHat()
        self._input = InputSenseHat()
        self._current_column = 3

        # Initialen Cursor zeichnen
        self._display.draw_cursor(self._current_column)
        self._display.draw_grid()

    def play_turn(self) -> int:
        while True:
            while not self._input.key_pressed():
                sleep(0.1)
            key = self._input.read_key()

            # Cursor entfernen
            self._display.draw_cursor(None)

            if key == Keys.LEFT:
                self._current_column = (self._current_column - 1) % self._display.columns
            elif key == Keys.RIGHT:
                self._current_column = (self._current_column + 1) % self._display.columns
            elif key == Keys.ENTER:
                return self._current_column

            #ACHTNG DAS MUSS DA WAHRSCHEINLICH DANN WEG?!    
            # Aktualisierten Cursor zeichnen
            self._display.draw_cursor(self._current_column)
            self._display.draw_grid()

    def draw_board(self, board: list, state: GameState):
        """
        Aktualisiert das gesamte Spielfeld basierend auf der übergebenen Datenstruktur.
        """
        for y in range(len(board)):
            for x in range(len(board[y])):
                if board[y][x] == GameToken.RED:
                    self._display.draw_token(x, y, GameToken.RED)
                elif board[y][x] == GameToken.YELLOW:
                    self._display.draw_token(x, y, GameToken.YELLOW)
                else:
                    self._display.draw_token(x, y, GameToken.EMPTY)
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
