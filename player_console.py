from player_base import PlayerBase
from display_console import DisplayConsole
from input_console import InputConsole
from game_state import GameState
from game_token import GameToken
from ansi import Ansi
from input_base import Keys
from time import sleep



class PlayerConsole(PlayerBase):
    def __init__(self, player: GameToken):  # Red or Yellow player
        """
        Initialisiert den Konsolenspieler mit einem zugehörigen Spielstein (Red oder Yellow).
        Stellt Display- und Eingabeobjekte bereit.
        
        :param player: Der Spielstein (GameToken), der diesem Spieler zugeordnet ist.
        """
        super().__init__(player)
        self._display = DisplayConsole()
        self._input = InputConsole()

    def play_turn(self, state: GameState) -> int:
        """
        Führt den Spielzug des Spielers in der Konsole aus und zeigt den aktuellen Fokus
        als farbigen Spielstein oberhalb des Spielfelds an.
        """
        columns = 7
        current_column = 3
        player_token = GameToken.RED if state == GameState.TURN_RED else GameToken.YELLOW

        while True:
            Ansi.gotoXY(1, 1)
            for col in range(columns):
                if col == current_column:
                    if player_token == GameToken.RED:
                        token = f"\033[31m●\033[0m"  # Roter Token
                    elif player_token == GameToken.YELLOW:
                        token = f"\033[33m●\033[0m"  # Gelber Token
                    else:
                        token = " "
                else:
                    token = " "

                # Abstand: 2 Leerzeichen vor und 1 nach dem Token
                print(f"  {token} ", end="")
            print()

            key = self._input.read_key()

            if key == Keys.LEFT and current_column > 0:
                current_column -= 1
            elif key == Keys.RIGHT and current_column < columns - 1:
                current_column += 1
            elif key == Keys.ENTER:
                return current_column
            elif key == Keys.ESC:
                return -1

    def draw_board(self, board: list, state: GameState) -> None:
        """
        Zeichnet das übergebene Spielfeld in der Konsole, 
        einschließlich aller vorhandenen Spielsteine und leert zunächst den Bildschirm.
        
        :param board: Eine 2D-Liste mit dem aktuellen Zustand des Spielfelds.
        :param state: Der aktuelle Spielzustand.
        """
        Ansi.clear_screen()
        Ansi.gotoXY(1, 2)
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

    board = [[' ' for _ in range(7)] for _ in range(6)]
    board[5][0] = GameToken.RED  # [Y][X]
    p = PlayerConsole(GameToken.YELLOW)

    Ansi.clear_screen()
    Ansi.reset()
    p.draw_board(board, GameState.TURN_YELLOW)
    pos = p.play_turn()
    Ansi.reset()
    Ansi.gotoXY(1, 20)
    print(f"Position: {pos}")
