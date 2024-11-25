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
        #super().__init__(player)
        self._display = DisplayConsole()
        self._input = InputConsole()

    def play_turn(self, state: GameState) -> int:
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
                Ansi.clear_screen()
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
        # TODO: draw grid with tokens
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
