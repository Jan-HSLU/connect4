from game_token import GameToken
from display_base import DisplayBase
try:
    from sense_hat import SenseHat
except ImportError:
    from sense_emu import SenseHat
from game_state import GameState
from time import sleep

TOKEN_COLORS = {
    GameToken.EMPTY: [0, 0, 255],
    GameToken.RED: [255, 0, 0],
    GameToken.YELLOW: [255, 255, 0],
    "CURSOR": [255, 255, 255],
    "OFF": [0, 0, 0],
}

class DisplaySenseHat(DisplayBase):
    def __init__(self):
        """
        Initialisiert ein DisplaySenseHat-Objekt, stellt die Verbindung zum SenseHat her 
        und erzeugt ein leeres Spielfeld (board) mit vordefinierten Reihen (rows) und Spalten (columns).
        """
        self.sense = SenseHat()
        self.rows = 6
        self.columns = 7
        self.board = [[GameToken.EMPTY for _ in range(self.columns)] for _ in range(self.rows)]
        self.cursor_x = None  # Aktuelle Cursorposition

    def clear_board(self):
        """
        Löscht das Spielfeld, indem es alle Zellen auf EMPTY setzt, setzt den Cursor zurück 
        und zeichnet das Feld neu, um den leeren Zustand anzuzeigen.
        """
        # Setze alle Zellen auf EMPTY und zeichne anschließend neu
        self.board = [[GameToken.EMPTY for _ in range(self.columns)] for _ in range(self.rows)]
        self.cursor_x = None
        self.draw_grid()

    def draw_grid(self):
        """
        Zeichnet das aktuelle Spielfeld auf dem SenseHat-Display neu, 
        einschließlich der Spielsteine und des Cursors (falls vorhanden).
        """
        pixels = []
        for y in range(8):
            for x in range(8):
                if y == 0 and x == self.cursor_x:
                    # Cursor in der obersten Zeile anzeigen
                    pixels.append(TOKEN_COLORS["CURSOR"])
                elif 1 <= y <= self.rows and x < self.columns:
                    token = self.board[y - 1][x]
                    pixels.append(TOKEN_COLORS[token])
                else:
                    pixels.append(TOKEN_COLORS["OFF"])
        self.sense.set_pixels(pixels)

    def draw_cursor(self, x):
        """
        Setzt die aktuelle Cursorposition (cursor_x) auf den angegebenen Wert x, 
        ohne das gesamte Spielfeld neu zu zeichnen.
        
        :param x: Die neue x-Position des Cursors.
        """
        self.cursor_x = x

    def draw_token(self, x, y, token):
        """
        Platziert einen Spielstein (token) an der angegebenen Position (x, y) im Spielfeld, 
        sofern die Position gültig ist. Spielstein wird als Token-Wert in das board geschrieben.
        
        :param x: Spaltenindex der Position.
        :param y: Zeilenindex der Position.
        :param token: Der zu platzierende Spielstein (GameToken).
        """
        if 0 <= y < self.rows and 0 <= x < self.columns:
            if isinstance(token, GameToken):
                self.board[y][x] = token.value
            else:
                pass


if __name__ == '__main__':
    display = DisplaySenseHat()

    display.draw_token(0, 5, GameToken.RED)
    display.draw_token(6, 3, GameToken.YELLOW)

    display.draw_cursor(3)
    display.draw_grid()
    sleep(5)
    display.sense.clear()