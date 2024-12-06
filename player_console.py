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
        #super().__init__(player)
        self._display = DisplayConsole()
        self._input = InputConsole()

    def play_turn(self, state: GameState) -> int:
        """
        Führt den Spielzug des Spielers in der Konsole aus.
        
        Zeigt den aktuellen Fokus auf der Spaltenauswahl an und ermöglicht die Navigation mit den Pfeiltasten.
        Bestätigen (ENTER) gibt die gewählte Spalte zurück. ESC bricht den Zug ab (Rückgabe -1).
        
        :param state: Der aktuelle Spielzustand.
        :return: Die ausgewählte Spaltennummer, oder -1 bei Abbruch.
        """
        columns = 7
        current_column = 3

        Ansi.gotoXY(2, 1)
        for i in range(columns):
            if i == current_column:
                print(f"[{i}]", end=" ")
            else:
                print(f" {i} ", end=" ")
        print()

        while True:
            key = self._input.read_key()
            
            Ansi.gotoXY(2, 1)
            for i in range(columns):
                if i == current_column:
                    print(f" {i} ", end=" ")
                else:
                    print(f" {i} ", end=" ")
            print()

            if key == Keys.LEFT:
                if current_column > 0:
                    current_column -= 1
            elif key == Keys.RIGHT:
                if current_column < columns - 1:
                    current_column += 1
            elif key == Keys.ENTER:
                return current_column
            elif key == Keys.ESC:
                #Ansi.clear_screen()
                return -1

            Ansi.gotoXY(2, 1)
            for i in range(columns):
                if i == current_column:
                    print(f"[{i}]", end=" ")
                else:
                    print(f" {i} ", end=" ")
            print()
            sleep(20 / 1000)

    def draw_board(self, board: list, state: GameState) -> None:
        """
        Zeichnet das übergebene Spielfeld in der Konsole, 
        einschließlich aller vorhandenen Spielsteine und leert zunächst den Bildschirm.
        
        :param board: Eine 2D-Liste mit dem aktuellen Zustand des Spielfelds.
        :param state: Der aktuelle Spielzustand.
        """
        # TODO: draw grid with tokens
        Ansi.clear_screen()
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
