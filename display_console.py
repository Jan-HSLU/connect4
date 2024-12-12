from ansi import Ansi
from game_token import GameToken
from display_base import DisplayBase


class DisplayConsole(DisplayBase):
    def __init__(self):
        """
        Initialisiert das DisplayConsole-Objekt mit einer
        vorgegebenen Anzahl von Zeilen und Spalten und erzeugt ein leeres Spielfeld.
        """
        super().__init__()
        self.rows = 6
        self.columns = 7
        self.grid = [[' ' for _ in range(self.columns)] for _ in range(self.rows)]

    def draw_grid(self) -> None:
        """
        Zeichnet das aktuelle Spielfeldgitter mit Unicode-Rahmen und den darauf platzierten Spielsteinen.
        """
        print("\u250c" + ("\u252c".join(["\u2500" * 3 for _ in range(self.columns)])) + "\u2510")
        for row in range(self.rows):
            print("\u2502" + ("\u2502".join([f" {self.grid[row][col]} " for col in range(self.columns)])) + "\u2502")
            if row < self.rows - 1:
                print("\u251c" + ("\u253c".join(["\u2500" * 3 for _ in range(self.columns)])) + "\u2524")
        
        print("\u2514" + ("\u2534".join(["\u2500" * 3 for _ in range(self.columns)])) + "\u2518")
        print("\u2514"+" 0 " + "\u2534" + " 1 " + "\u2534" + " 2 " + "\u2534" + " 3 " + "\u2534" + " 4 " + "\u2534" + " 5 " + "\u2534" + " 6 " + "\u2518")

    def draw_token(self, x: int, y: int, token: GameToken) -> None:
        """
        Platziert einen Spielstein an der angegebenen Position (x, y) im Spielfeldgitter mit Farbanzeige.
        """
        if 0 <= y < self.rows and 0 <= x < self.columns:
            if token == GameToken.RED:
                self.grid[y][x] = f"\033[31m●\033[0m"  # Roter Spielstein
            elif token == GameToken.YELLOW:
                self.grid[y][x] = f"\033[33m●\033[0m"  # Gelber Spielstein
            else:
                self.grid[y][x] = ' '



if __name__ == '__main__':
    Ansi.clear_screen()
    Ansi.reset()
    fc = DisplayConsole()
    fc.draw_grid()
    fc.draw_token(0, 0, GameToken.RED)
    fc.draw_token(6, 2, GameToken.YELLOW)
    fc.draw_grid()
    Ansi.gotoXY(1, 20)



