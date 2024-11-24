from game_token import GameToken
from display_base import DisplayBase
from sense_hat import SenseHat

TOKEN_COLORS = {
    GameToken.EMPTY: [0, 0, 255],
    GameToken.RED: [255, 0, 0],
    GameToken.YELLOW: [255, 255, 0],
    "CURSOR": [255, 255, 255],
    "OFF": [0, 0, 0],
}

class DisplaySenseHat(DisplayBase):
    def __init__(self):
        #super().__init__(player)
        self.sense = SenseHat()
        self.rows = 6
        self.columns = 7
        self.board = [[GameToken.EMPTY for _ in range(self.columns)] for _ in range(self.rows)]

    def draw_grid(self):
        pixels = []
        for y in range(8):
            for x in range(8):
                if 1 <= y <= self.rows and x < self.columns:
                    token = self.board[y - 1][x]
                    pixels.append(TOKEN_COLORS[token])
                else:
                    pixels.append(TOKEN_COLORS["OFF"])
        self.sense.set_pixels(pixels)
    
    def draw_token(self, x, y, token):
        if 0 <= y < self.rows and 0 <= x < self.columns:
            self.board[y][x] = token.value
            #löschen wenn es funktioniert
            self.draw_grid()

    

if __name__ == '__main__':
    fc = DisplaySenseHat()
    fc.draw_grid()
    fc.draw_token(0, 0, GameToken.RED)
    fc.draw_token(6, 2, GameToken.YELLOW)
    print(type(GameToken.RED))
    print(GameToken.RED)