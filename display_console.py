from ansi import Ansi
from game_token import GameToken
from display_base import DisplayBase


class DisplayConsole(DisplayBase):
    """
    ┌
    ┐
    └
    ┘
    ├
    ┤
    ┼
    ─
    │
    ┬
    ┴
    █ 

    https://de.wikipedia.org/wiki/Unicodeblock_Rahmenzeichnung
    """
    def __init__(self):
        #super().__init__(player)
        self.rows = 6
        self.columns = 7
        self.grid = [[' ' for _ in range(self.columns)] for _ in range(self.rows)]

    def draw_grid(self):
        #print("\u250c"+" 0 " + "\u252c" + " 1 " + "\u252c" + " 2 " + "\u252c" + " 3 " + "\u252c" + " 4 " + "\u252c" + " 5 " + "\u252c" + " 6 " + "\u2510")
        print("\u250c" + ("\u252c".join(["\u2500" * 3 for _ in range(self.columns)])) + "\u2510")
        for row in range(self.rows):
            print("\u2502" + ("\u2502".join([f" {self.grid[row][col]} " for col in range(self.columns)])) + "\u2502")
            if row < self.rows - 1:
                print("\u251c" + ("\u253c".join(["\u2500" * 3 for _ in range(self.columns)])) + "\u2524")
        
        print("\u2514" + ("\u2534".join(["\u2500" * 3 for _ in range(self.columns)])) + "\u2518")
        print("\u2514"+" 0 " + "\u2534" + " 1 " + "\u2534" + " 2 " + "\u2534" + " 3 " + "\u2534" + " 4 " + "\u2534" + " 5 " + "\u2534" + " 6 " + "\u2518")

    def draw_token(self, x: int, y: int, token) -> None:
        
        if 0 <= y < self.rows and 0 <= x < self.columns:
            self.grid[y][x] = token.value
        Ansi.clear_screen()


if __name__ == '__main__':
    Ansi.clear_screen()
    Ansi.reset()
    fc = DisplayConsole()
    fc.draw_grid()
    fc.draw_token(0, 0, GameToken.RED)
    fc.draw_token(6, 2, GameToken.YELLOW)
    Ansi.gotoXY(1, 20)
    print(type(GameToken.RED))
    print(GameToken.RED)



