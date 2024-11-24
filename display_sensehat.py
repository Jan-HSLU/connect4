from game_token import GameToken
from display_base import DisplayBase
from sense_hat import SenseHat
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
        self.sense = SenseHat()
        self.rows = 6
        self.columns = 7
        self.board = [[GameToken.EMPTY for _ in range(self.columns)] for _ in range(self.rows)]
        self.cursor_x = None  # Aktuelle Cursorposition

    def draw_grid(self):
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
        self.cursor_x = x

    def draw_token(self, x, y, token):
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